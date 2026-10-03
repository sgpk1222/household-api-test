import sys

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def count_paths(lines):
    counts = {}
    for line in lines:
        parts = line.split('"')
        if len(parts) < 2:
            continue
        seg = parts[1].split(" ")
        if len(seg) < 2:
            continue
        p = seg[1].split("?")[0]
        counts[p] = counts.get(p, 0) + 1
    return counts

def main():
    if len(sys.argv) < 2:
        print("用法：python log_report.py <日志文件路径>")
        sys.exit(1)

    path = sys.argv[1]
    lines = read_lines(path)
    counts = count_paths(lines)

    print(f"总请求数：{len(lines)}")
    print("---- 各接口调用次数（从多到少）----")
    for k, v in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{v:6d}  {k}")

    with open("log_report.txt", "w", encoding="utf-8") as f:
        f.write(f"日志文件：{path}\n")
        f.write(f"总请求数：{len(lines)}\n\n")
        f.write("各接口调用次数（从多到少）：\n")
        for k, v in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
            f.write(f"{v:6d}  {k}\n")


if __name__ == "__main__":
    main()