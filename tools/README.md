# 日志分析脚本

读 Tomcat 的访问日志，统计每个接口被调用了多少次，并按次数从多到少排序。

## 为什么写这个

排查问题时经常要回答两个问题：**哪个接口被调得最多？有没有异常状态码？**

手工翻日志很慢。这个脚本读一次就出结果，而且可以重复跑。

## 怎么用

在仓库根目录装依赖：

```
pip install -r requirements.txt
```

然后运行（日志文件路径作为参数传进去）：

```
python log_report.py <日志文件路径>
```

仓库里带了一份示例日志，可以直接跑：

```
cd tools
python log_report.py sample_access.log
```

## 输出

- 终端打印总请求数和各接口调用次数，按次数从多到少排
- 同时在**当前目录**生成 `log_report.txt`

注意第二点是相对路径：报告写在"你运行命令时所在的目录"，不是脚本所在的目录。所以建议先 `cd tools` 再跑。

## 日志格式

`sample_access.log` 是从 Tomcat 访问日志里截的一份真实样本，43 条记录。用的是 Tomcat 默认的 access log 格式：

```
127.0.0.1 - - [01/Oct/2026:18:04:42 +0800] "POST /HouseholdSystem/resident/add HTTP/1.1" 302 -
```

从左到右依次是：客户端 IP、时间、**请求方法和路径**、状态码、响应大小。

脚本处理的就是中间那对双引号里的内容——先按 `"` 切开取到请求行，再按空格切开取到路径，最后按 `?` 切掉查询参数。

## 测试

```
cd tools
pytest
```

`test_log_report.py` 里测的是 `count_paths()` 这个函数——喂给它几行构造好的日志，检查它返回的统计结果对不对。

## 文件说明

| 文件 | 说明 |
|---|---|
| `log_report.py` | 脚本本体 |
| `test_log_report.py` | 单元测试 |
| `sample_access.log` | 示例日志 |
| `log_report.txt` | 运行输出，每次重新生成，不进仓库 |
