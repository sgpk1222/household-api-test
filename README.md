# 户籍管理系统 接口测试

![接口自动化测试](https://github.com/sgpk1222/household-api-test/actions/workflows/tests.yml/badge.svg)

这是我做的一个接口测试练习。被测系统是一个户籍管理系统，我把它部署在本地 Tomcat 上，拿它来练测试流程。

## 被测系统

- 技术：Spring + SpringMVC + MyBatis
- 数据库：MySQL 8.0，库名 household_db
- 容器：Tomcat 9
- 地址：http://localhost:8080/HouseholdSystem
- 管理员账号：admin / 123456
- 居民账号：用身份证号登录，密码 123456

一共 16 个接口，列表在 docs/接口清单.md。

## 我做了什么

先测的是「新增居民」和「用户登录」两个模块。选它们的理由：

- 新增居民字段最多，有 8 个，边界情况也最多
- 登录涉及会话和权限，容易出安全问题

用例设计用了三种方法：等价类划分、边界值分析、错误推测法。一共写了 32 条，覆盖正常值、边界值、异常值、业务规则四类。

用例和执行结果在 docs/测试用例-新增居民.xlsx（身份证号那一列我设成了文本格式，不然 Excel 会把它变成科学计数法）。

**接口测试**：用 Postman 建了 10 个请求，覆盖登录、查询、搜索、新增（含文件上传）、删除，通过 Cookie 保持处理登录态。其中 4 个是专门验证「不该成功的时候有没有成功」的反向用例。Collection 和环境变量都在 postman/ 目录，导入就能跑。

**数据核对**：写了一组 SQL 到数据库里核对接口的结果。接口返回 200 只代表请求被处理了，不代表数据写对了——字段错位、日期格式变了这些，在页面上看不出来。见 docs/数据验证SQL.md。

## 发现的问题

32 条用例里 18 条不符合预期。后来用 Postman 做反向用例时又发现一个，一共 6 个缺陷：

| 编号 | 问题 | 严重程度 |
|---|---|---|
| BUG-006 | 未登录可以直接访问和删除管理端接口 | 严重 |
| BUG-001 | 姓名能存进脚本，列表页会执行弹窗 | 严重 |
| BUG-002 | 身份证号完全不校验格式 | 严重 |
| BUG-003 | 姓名首尾的空格被原样存进数据库 | 一般 |
| BUG-004 | 姓名只填一个空格也能保存 | 一般 |
| BUG-005 | 出错时把数据库报错原文显示给用户 | 一般 |

详细记录在 docs/缺陷记录.md。其中 4 条可以在 Postman 里直接复现，见 postman/ 目录里带「【反向】」前缀的那几个请求。

## 目录

```
household-api-test/
├── README.md
├── requirements.txt            依赖清单
├── pytest.ini                  pytest 配置
├── .github/workflows/          GitHub Actions 配置
├── db/
│   └── household_db.sql        数据库初始化脚本
├── docs/
│   ├── 接口清单.md
│   ├── 测试用例-新增居民.xlsx
│   ├── 缺陷记录.md
│   └── 数据验证SQL.md
├── postman/                    Postman Collection 和环境变量
├── sut/
│   └── household-system.war    被测系统的可部署包（CI 用它把系统跑起来）
├── tests/                      pytest 接口自动化测试
└── tools/                      日志分析脚本
```

## 自动化测试

用 pytest + requests 写的接口自动化测试，跑起来是：

```
pytest tests/ -v --html=report.html --self-contained-html
```

当前的执行结果：**10 条通过，5 条标记为 xfail**（对应 5 个已知缺陷，见 `docs/缺陷记录.md`）。

`xfail` 的含义是「我断言系统应该拒绝，但系统目前没有拒绝」。**哪天开发把缺陷修了，
这些用例会变成 xpass**，那就提醒你该更新缺陷记录了。

## 持续集成

每次 push 到 main 分支，GitHub Actions 会自动跑一遍：启动 MySQL、导入数据库脚本、
下载 Tomcat、部署被测系统、执行全部测试，并把 HTML 报告作为附件上传。

配置在 `.github/workflows/tests.yml`，分两个作业：

| 作业 | 内容 | 需要外部依赖吗 |
|---|---|---|
| 单元测试 | 日志分析脚本的单元测试 | 不需要 |
| 接口测试 | 全量接口测试 + HTML 报告 | 需要 MySQL 和被测系统 |

## 后面可以做的

- [ ] 补充居民端（注册、登录、个人档案）的测试用例
- [ ] 补充搜索、统计分析等其他模块的用例
- [ ] 被测系统修复缺陷后，去掉对应的 xfail 标记

## 怎么复现

这个仓库里没有被测系统的源码，但带了一份可以部署的包：`sut/household-system.war`。

**本地跑测试：**

1. 启动 MySQL，导入数据库：`mysql -uroot -p < db/household_db.sql`
2. 把 `sut/household-system.war` 部署到 Tomcat 9，访问路径是 `/HouseholdSystem`
3. 确认 `http://localhost:8080/HouseholdSystem/toLogin` 能打开
4. `pip install -r requirements.txt`，然后 `pytest tests/ -v`

**只看接口测试的 Postman 版本**：把 `postman/` 下那两个 JSON 导入 Postman，
选中 `HouseholdSystem-Local` 环境，就能直接跑。
