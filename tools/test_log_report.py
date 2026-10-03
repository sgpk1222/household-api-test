from log_report import count_paths


def test_count_paths_统计正确():
    lines = [
        '127.0.0.1 - - [01/Oct/2026:10:00:00 +0800] "GET /a HTTP/1.1" 200 100\n',
        '127.0.0.1 - - [01/Oct/2026:10:00:01 +0800] "GET /a HTTP/1.1" 200 100\n',
        '127.0.0.1 - - [01/Oct/2026:10:00:02 +0800] "GET /b HTTP/1.1" 404 99\n',
    ]

    result = count_paths(lines)

    assert result["/a"] == 2
    assert result["/b"] == 1