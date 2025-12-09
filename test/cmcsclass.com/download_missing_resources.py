#!/usr/bin/env python3
"""
自动检测并下载缺失的网站资源
扫描所有 HTML 文件，提取资源链接（JS、CSS、图片等），
检查本地是否存在，如果不存在则从原站点下载
"""

import os
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote

# 配置
BASE_DIR = Path('.')  # 网站根目录
ORIGINAL_SITE = 'https://macmasterimaritime.com'  # 原站点 URL
TIMEOUT = 10  # 下载超时时间（秒）

# 需要检查的资源类型
RESOURCE_PATTERNS = {
    'script': ['src'],
    'link': ['href'],
    'img': ['src', 'data-src'],
    'source': ['srcset'],
    'video': ['src', 'poster'],
    'audio': ['src'],
}

def extract_resources_from_html(html_path):
    """从 HTML 文件中提取所有资源链接"""
    resources = set()
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 提取标签中的资源
        for tag_name, attrs in RESOURCE_PATTERNS.items():
            for tag in soup.find_all(tag_name):
                for attr in attrs:
                    value = tag.get(attr)
                    if value:
                        # 处理 srcset（可能包含多个 URL）
                        if attr == 'srcset':
                            urls = re.findall(r'([^\s,]+)', value)
                            resources.update(urls)
                        else:
                            resources.add(value)
        
        # 提取 CSS 中的 url()
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style_tag.string)
                resources.update(urls)
        
        # 提取内联 style 属性中的 url()
        for tag in soup.find_all(style=True):
            urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', tag['style'])
            resources.update(urls)
    
    except Exception as e:
        print(f"⚠️  解析 {html_path} 失败: {e}")
    
    return resources

def normalize_path(resource_url, html_path):
    """将资源 URL 转换为本地文件路径"""
    # 移除查询参数和锚点
    resource_url = resource_url.split('?')[0].split('#')[0]
    
    # 跳过外部链接和特殊协议
    if resource_url.startswith(('http://', 'https://', '//', 'data:', 'javascript:', 'mailto:')):
        return None
    
    # 处理绝对路径（以 / 开头）
    if resource_url.startswith('/'):
        return BASE_DIR / resource_url.lstrip('/')
    
    # 处理相对路径
    html_dir = Path(html_path).parent
    resource_path = html_dir / resource_url
    
    # 规范化路径（解析 ../ 等）
    try:
        return resource_path.resolve()
    except:
        return None

def download_resource(local_path, original_url):
    """从原站点下载资源并保存到本地"""
    try:
        # 创建目录
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 下载文件
        print(f"⬇️  下载: {original_url}")
        response = requests.get(original_url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        
        # 保存文件
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅  保存到: {local_path}")
        return True
    
    except Exception as e:
        print(f"❌  下载失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 80)
    print("🔍 开始扫描网站资源...")
    print("=" * 80)
    
    all_resources = {}  # {local_path: original_url}
    missing_resources = {}
    
    # 1. 扫描所有 HTML 文件
    html_files = list(BASE_DIR.rglob('*.html'))
    print(f"\n📄 找到 {len(html_files)} 个 HTML 文件\n")
    
    for html_file in html_files:
        print(f"📝 扫描: {html_file.relative_to(BASE_DIR)}")
        resources = extract_resources_from_html(html_file)
        
        for resource_url in resources:
            local_path = normalize_path(resource_url, html_file)
            
            if local_path and local_path != BASE_DIR:
                # 构造原站点 URL
                try:
                    # Ensure both are absolute
                    abs_local = local_path.resolve()
                    abs_base = BASE_DIR.resolve()
                    if abs_local.is_relative_to(abs_base):
                        relative_to_base = abs_local.relative_to(abs_base)
                        original_url = f"{ORIGINAL_SITE}/{str(relative_to_base).replace(os.sep, '/')}"
                        all_resources[local_path] = original_url
                except Exception as e:
                    pass
    
    print(f"\n✅ 总共找到 {len(all_resources)} 个资源引用\n")
    
    # 2. 检查哪些资源本地不存在
    print("=" * 80)
    print("🔎 检查缺失的资源...")
    print("=" * 80 + "\n")
    
    for local_path, original_url in all_resources.items():
        if not local_path.exists():
            missing_resources[local_path] = original_url
            print(f"❌  缺失: {local_path.relative_to(BASE_DIR)}")
    
    if not missing_resources:
        print("🎉 所有资源都存在，无需下载！")
        return
    
    print(f"\n⚠️  发现 {len(missing_resources)} 个缺失的资源\n")
    
    # 3. 询问是否下载
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--yes', '-y', action='store_true', help='Automatically confirm download')
    args, unknown = parser.parse_known_args()

    if not args.yes:
        response = input("是否从原站点下载这些资源？(y/n): ")
        if response.lower() != 'y':
            print("已取消下载")
            return
    else:
        print("已自动确认下载 (--yes)")
    
    # 4. 下载缺失的资源
    print("\n" + "=" * 80)
    print("⬇️  开始下载缺失的资源...")
    print("=" * 80 + "\n")
    
    success_count = 0
    failed_count = 0
    
    for local_path, original_url in missing_resources.items():
        if download_resource(local_path, original_url):
            success_count += 1
        else:
            failed_count += 1
        print()
    
    # 5. 总结
    print("=" * 80)
    print("📊 下载完成！")
    print("=" * 80)
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {failed_count}")
    print(f"📦 总计: {len(missing_resources)}")

if __name__ == '__main__':
    main()
