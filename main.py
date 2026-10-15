#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页内容抓取工具
抓取指定 URL 的文本内容、标题、链接、图片等
"""

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def scrape_page(url, output_file=None):
    """抓取网页内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
    except Exception as e:
        print(f"[错误] 请求失败: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # 提取标题
    title = soup.title.string.strip() if soup.title else "无标题"
    print(f"标题: {title}")
    print(f"URL: {url}")

    # 提取正文文本
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    # 清理多余空行
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    text = "\n".join(lines)

    # 提取链接
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        text_link = a.get_text(strip=True)
        if href and text_link:
            links.append((text_link, href))

    # 提取图片
    images = []
    for img in soup.find_all("img", src=True):
        src = urljoin(url, img["src"])
        alt = img.get("alt", "")
        images.append((alt, src))

    # 输出
    result = f"# {title}\n\nURL: {url}\n\n## 正文\n{text}\n\n"
    result += f"## 链接 ({len(links)} 个)\n"
    for t, h in links[:50]:
        result += f"- [{t}]({h})\n"

    result += f"\n## 图片 ({len(images)} 张)\n"
    for alt, src in images[:50]:
        result += f"- {alt}: {src}\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[完成] 已保存到 {output_file}")
    else:
        print("\n" + result[:2000])
        if len(result) > 2000:
            print("\n... (内容过长，使用 -o 保存到文件)")

    print(f"\n统计: {len(lines)} 行文本, {len(links)} 个链接, {len(images)} 张图片")


def main():
    parser = argparse.ArgumentParser(description="网页内容抓取工具")
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("-o", "--output", default=None, help="输出到文件")
    args = parser.parse_args()

    scrape_page(args.url, args.output)


if __name__ == "__main__":
    main()
