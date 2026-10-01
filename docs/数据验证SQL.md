# 数据验证 SQL

接口测试跑完之后，用它去数据库里核对数据。

**为什么要这一步**：接口返回 200 只说明请求被处理了，不代表数据写对了。字段错位、日期格式变了、某个字段悄悄丢了，这些在页面上都看不出来，只有直接查库才能发现。

---

## 一、熟悉数据

```sql
-- 全部男性居民
SELECT r_id, name, gender FROM resident WHERE gender = '男';

-- 姓名里带「李」的居民
SELECT r_id, name FROM resident WHERE name LIKE '%李%';

-- 按出生日期从早到晚排列
SELECT r_id, name, birthday FROM resident ORDER BY birthday;
```

---

## 二、统计类（对应系统里的统计报表）

```sql
-- 居民总数
SELECT COUNT(*) AS 居民总数 FROM resident;

-- 1985 年出生的居民
SELECT r_id, name, birthday FROM resident WHERE YEAR(birthday) = 1985;

-- 每种户口类型的人数，从多到少排
SELECT h_type, COUNT(*) AS 人数 FROM resident GROUP BY h_type ORDER BY 人数 DESC;

-- 人数在 6 人及以上的户口类型
SELECT h_type, COUNT(*) AS 人数 FROM resident GROUP BY h_type HAVING 人数 >= 6;
```

---

## 三、数据完整性检查

```sql
-- 没有上传照片的居民
-- 列表页对这类记录显示「无图」占位符，不会出现裂图
SELECT r_id, photo FROM resident WHERE photo IS NULL;

-- 居民档案和登录账号的关联情况
SELECT r.name AS 姓名, u.username AS 账号
FROM resident r
JOIN resident_user u ON r.account_id = u.id;

-- 三张表各有多少条记录
SELECT
  (SELECT COUNT(*) FROM resident)      AS 居民数,
  (SELECT COUNT(*) FROM resident_user) AS 账号数,
  (SELECT COUNT(*) FROM sys_user)      AS 管理员数;
```

---

## 四、核对接口测试结果用的写法

```sql
-- 新增居民后：确认数据真的落库，而且字段没有错位
SELECT r_id, name, id_card, gender, birthday, phone, h_type, photo, create_time
FROM resident ORDER BY r_id DESC LIMIT 1;

-- 删除居民后：确认记录真的从库里消失了
SELECT COUNT(*) AS 还在吗 FROM resident WHERE r_id = 46;

-- 检查身份证号的唯一约束有没有被绕过（正常应该一行都查不到）
SELECT id_card, COUNT(*) AS 次数
FROM resident GROUP BY id_card HAVING COUNT(*) > 1;
```

---

## 三个容易写错的地方

**`WHERE` 和 `HAVING` 的区别**

`WHERE` 在分组**之前**筛原始数据，`HAVING` 在分组**之后**筛统计结果。

所以 `WHERE COUNT(*) > 1` 会直接报错，必须写成 `HAVING COUNT(*) > 1`。

**子句顺序是固定的**

```
SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
```

顺序调换会报语法错误。我一开始就把 `HAVING` 写在了 `GROUP BY` 前面，报的是 `ERROR 1064`。

**聚合查询里不能混普通列**

```sql
SELECT r_id, COUNT(*) FROM resident;   -- 报错
```

报 `only_full_group_by` 错误。原因是 `r_id` 有 11 个值、`COUNT(*)` 只有 1 个值，数据库不知道该显示哪一个 `r_id`。

要么只选聚合函数，要么用 `GROUP BY` 把普通列分组。

**`JOIN` 和 `LEFT JOIN` 的区别**

`JOIN`（= `INNER JOIN`）只保留两边都匹配上的行。如果有居民没绑定账号，用 `JOIN` 就查不到他；换成 `LEFT JOIN` 会保留，右边字段显示为 NULL。

检查"有没有漏掉的数据"时，通常用 `LEFT JOIN`。
