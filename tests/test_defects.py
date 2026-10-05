"""反向用例：验证系统在「不该成功的时候」确实没成功。

这里每一条断言的都是「系统应该怎样」，而不是「系统实际怎样」。
当前系统有这个缺陷，所以这些用例会失败——用 xfail 标记之后，pytest
不把它们算作失败，而是标成 xfail。

哪天开发把缺陷修好了，对应的用例会变成 xpass（意外通过），
那就是提醒你：缺陷已修复，可以更新缺陷记录、去掉 xfail 标记了。
"""

import pytest


def add_resident(session, base_url, **fields):
    """新增居民的公共部分：补齐必填字段，并带上一个假图片。"""
    data = {
        "name": "自动化测试",
        "idCard": "000000000000000000",
        "gender": "男",
        "birthday": "2000-01-01",
        "phone": "13000000000",
        "address": "自动化测试地址",
        "hType": "城市家庭户口",
    }
    data.update(fields)
    return session.post(
        f"{base_url}/resident/add",
        data=data,
        files={"file": ("test.jpg", b"fake-image", "image/jpeg")},
        allow_redirects=False,
    )


@pytest.mark.xfail(reason="已知缺陷 BUG-004：姓名只填空格也能保存")
def test_姓名只填空格应该被拒绝(admin_session, base_url, temp_resident):
    add_resident(admin_session, base_url, name=" ", idCard=temp_resident)

    r = admin_session.get(f"{base_url}/resident/list",
                          params={"searchIdCard": temp_resident})
    assert "暂无相关数据" in r.text, "系统应该拒绝保存，但这条记录还是进库了"


@pytest.mark.xfail(reason="已知缺陷 BUG-002：身份证号没有任何格式校验")
def test_身份证号只有17位应该被拒绝(admin_session, base_url, temp_resident):
    add_resident(admin_session, base_url, name="身份证测试", idCard=temp_resident[:17])

    r = admin_session.get(f"{base_url}/resident/list",
                          params={"searchIdCard": temp_resident[:17]})
    assert "暂无相关数据" in r.text, "系统应该拒绝 17 位身份证号，但这条记录进库了"


@pytest.mark.xfail(reason="已知缺陷 BUG-001：列表页直接输出姓名，存在存储型 XSS")
def test_姓名里的脚本标签应该被转义(admin_session, base_url, temp_resident):
    add_resident(admin_session, base_url,
                 name="<script>alert(1)</script>", idCard=temp_resident)

    r = admin_session.get(f"{base_url}/resident/list",
                          params={"searchIdCard": temp_resident})
    assert "<script>alert(1)</script>" not in r.text, \
        "列表页应该把标签转义成 &lt;script&gt;，但实际原样输出了"


@pytest.mark.xfail(reason="已知缺陷 BUG-005：出错时把数据库报错原文返回给用户")
def test_姓名超长时不应该暴露数据库信息(admin_session, base_url, temp_resident):
    r = add_resident(admin_session, base_url, name="张" * 51, idCard=temp_resident)

    assert "Data too long" not in r.text, "不应该把数据库的原始报错返回给用户"
    assert "INSERT INTO" not in r.text, "不应该把 SQL 语句暴露出来"
