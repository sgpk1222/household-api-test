import requests

BASE = "http://localhost:8080/HouseholdSystem"

# ---- 1. 不用 Session，直接访问受保护的接口 ----
print("=== 1. 不用 Session 访问 /user/profile ===")
r = requests.get(f"{BASE}/user/profile", allow_redirects=False)
print("  状态码:", r.status_code)
print("  Location:", r.headers.get("Location"))

# ---- 2. 用 Session 登录居民账号 ----
print()
print("=== 2. 用 Session 登录居民账号 ===")
s = requests.Session()
r = s.post(f"{BASE}/user/login",
           data={"username": "33010619850310123X", "password": "123456"},
           allow_redirects=False)
print("  状态码:", r.status_code)
print("  Location:", r.headers.get("Location"))
print("  Session 存下的 Cookie:", s.cookies.get_dict())

# ---- 3. 用同一个 Session 再访问 ----
print()
print("=== 3. 用同一个 Session 再访问 /user/profile ===")
r = s.get(f"{BASE}/user/profile")
print("  状态码:", r.status_code)
print("  页面里有王伟吗:", "王伟" in r.text)
print("  这次实际带上去的 Cookie:", r.request.headers.get("Cookie"))