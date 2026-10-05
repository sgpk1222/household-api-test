import random
import re
import string

import pytest
import requests

BASE_URL = "http://localhost:8080/HouseholdSystem"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def admin_session(base_url):
    """用管理员账号登录，返回一个已经带着登录态的 Session。

    整个测试会话只登录一次，所有用例共用这一个 Session。
    """
    s = requests.Session()
    r = s.post(f"{base_url}/login",
               data={"username": "admin", "password": "123456"},
               allow_redirects=False)
    assert r.status_code == 302, f"管理员登录失败，状态码 {r.status_code}"
    assert "/toMain" in r.headers.get("Location", ""), "登录后没有跳转到主页"
    return s


@pytest.fixture
def temp_resident(admin_session, base_url):
    """提供一个本次测试专用的身份证号，测试结束后自动把这条记录删掉。

    yield 之前是"准备"，yield 之后是"善后"。善后代码不管测试通过还是失败
    都会执行——这样测试就算中途失败，也不会在库里留下垃圾数据，
    更不会因为身份证号重复把下一次运行卡住。
    """
    id_card = "33998877" + "".join(random.choices(string.digits, k=10))
    yield id_card

    # 用前 17 位搜：这样无论记录里存的是 18 位还是 17 位，都能匹配到
    r = admin_session.get(f"{base_url}/resident/list",
                          params={"searchIdCard": id_card[:17]})
    for rid in set(re.findall(r"rId=(\d+)", r.text)):
        admin_session.get(f"{base_url}/resident/delete",
                          params={"rId": rid}, allow_redirects=False)
