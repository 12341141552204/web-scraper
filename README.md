# 网页内容抓取工具 (web-scraper)

抓取网页正文、链接、图片等内容。

## 功能

- 提取网页标题和正文
- 提取所有链接和图片
- 自动处理编码
- 输出 Markdown 格式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
# 抓取并显示
python main.py https://example.com

# 保存到文件
python main.py https://example.com -o result.md
```

## 依赖

- requests
- beautifulsoup4
