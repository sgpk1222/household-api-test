import pytest
import requests
import re

def test_删除不存在的记录不会崩溃(admin_session, base_url):
    r = admin_session.get(f"{base_url}/resident/delete",
                       params={"rId": 999999},
                       allow_redirects=False)

    # 期望：正常处理完跳回列表页，而不是抛 500 服务器错误
    assert r.status_code == 302, f"删除不存在的记录时出错了，实际状态码 {r.status_code}"



def test_管理员能看到居民列表(admin_session, base_url):
    r = admin_session.get(f"{base_url}/resident/list")
    assert r.status_code == 200
    assert "王伟" in r.text


@pytest.mark.parametrize("keyword, expected, unexpected", [
    ("王",        ["王伟", "王芳"], ["李强", "张鹏"]),
    ("李",        ["李强", "李娜"], ["王伟", "张鹏"]),
    ("张",        ["张鹏"],         ["王伟", "李强"]),
    ("不存在的人", [],              ["王伟", "李强", "张鹏"]),
], ids=["搜王", "搜李", "搜张", "搜不存在的名字"])
def test_按姓名搜索只会返回匹配的记录(admin_session, base_url, keyword, expected, unexpected):
    r = admin_session.get(f"{base_url}/resident/list", params={"searchName": keyword})
    assert r.status_code == 200

    for n in expected:
        assert n in r.text, f"搜「{keyword}」应该能搜到 {n}"
    for n in unexpected:
        assert n not in r.text, f"搜「{keyword}」不该出现 {n}"


@pytest.mark.xfail(reason="已知缺陷 BUG-006：管理端接口未做登录校验，未登录也能拿到数据")
def test_未登录访问居民列表应该被拒绝(base_url):
    r = requests.get(f"{base_url}/resident/list", allow_redirects=False)
    assert r.status_code == 302


def test_新增居民后能查到并删除(admin_session, base_url):
    """完整走一遍：新增 → 查询确认 → 删除 → 再确认已删除"""
    name = "自动化测试用户"
    id_card = "339988770000000099"
    rid = None

    try:
        # 1) 新增（带上一个假的图片，验证 multipart 上传这条路径）
        r = admin_session.post(
            f"{base_url}/resident/add",
            data={
                "name": name,
                "idCard": id_card,
                "gender": "男",
                "birthday": "2000-01-01",
                "phone": "13000000000",
                "address": "自动化测试地址",
                "hType": "城市家庭户口",
            },
            files={"file": ("test.jpg", b"fake-image-bytes", "image/jpeg")},
            allow_redirects=False,
        )
        assert r.status_code == 302, "新增成功应该返回 302 跳转到列表页"

        # 2) 查询确认真的写进库了
        r = admin_session.get(f"{base_url}/resident/list", params={"searchName": name})
        assert r.status_code == 200
        assert "暂无相关数据" not in r.text, "新增之后应该能搜到这条记录"

        # 3) 从页面 HTML 里把 rId 抠出来，删除要用
        m = re.search(r"rId=(\d+)", r.text)
        assert m, "列表页里应该能找到这条记录的 rId"
        rid = m.group(1)

        # 4) 删除
        r = admin_session.get(f"{base_url}/resident/delete", params={"rId": rid},
                              allow_redirects=False)
        assert r.status_code == 302
        rid = None      # 删成功了，不用善后

        # 5) 再确认删掉了
        r = admin_session.get(f"{base_url}/resident/list", params={"searchName": name})
        assert "暂无相关数据" in r.text, "删除之后应该查不到了"

    finally:
        # 不管上面哪一步失败，都尽量把测试数据清掉，不给下次运行留垃圾
        if rid:
            admin_session.get(f"{base_url}/resident/delete", params={"rId": rid})