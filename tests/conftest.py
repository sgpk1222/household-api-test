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