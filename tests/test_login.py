import requests


def test_管理员登录成功会跳转到主页(base_url):
    s = requests.Session()
    r = s.post(f"{base_url}/login",
               data={"username": "admin", "password": "123456"},
               allow_redirects=False)
    assert r.status_code == 302
    assert "/toMain" in r.headers.get("Location", "")
    assert "JSESSIONID" in s.cookies.get_dict()


def test_密码错误会回到登录页并提示(base_url):
    r = requests.post(f"{base_url}/login",
                      data={"username": "admin", "password": "wrong-password"},
                      allow_redirects=False)
    assert r.status_code == 200
    assert "用户名或密码错误" in r.text