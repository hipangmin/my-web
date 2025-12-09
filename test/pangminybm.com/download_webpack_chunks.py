#!/usr/bin/env python3
"""
自动下载 Elementor Webpack Chunks
解析 webpack runtime 文件，提取所有动态加载的 chunk 文件名，并从原站点下载。
"""

import os
import re
import requests
from pathlib import Path

# 配置
BASE_DIR = Path('.')
ORIGINAL_SITE = 'https://macmasterimaritime.com'
TIMEOUT = 10

# 常见的 runtime 文件名模式
RUNTIME_PATTERNS = [
    'webpack-pro.runtime.min*.js',
    'webpack.runtime.min*.js'
]

def find_runtime_files(base_dir):
    """查找所有 webpack runtime 文件"""
    runtime_files = []
    for pattern in RUNTIME_PATTERNS:
        runtime_files.extend(list(base_dir.rglob(pattern)))
    return runtime_files

def extract_chunks(runtime_file):
    """从 runtime 文件中提取 chunk 文件名"""
    chunks = set()
    try:
        with open(runtime_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 匹配模式: "filename.hash.bundle.min.js"
        # 这种模式通常在 switch case 或三元运算符中
        matches = re.findall(r'["\']([a-zA-Z0-9-]+\.[a-f0-9]+\.bundle\.min\.js)["\']', content)
        chunks.update(matches)
        
    except Exception as e:
        print(f"⚠️  解析 {runtime_file} 失败: {e}")
    
    return chunks

def download_chunk(local_dir, chunk_name, original_base_url):
    """下载 chunk 文件"""
    local_path = local_dir / chunk_name
    
    if local_path.exists():
        print(f"⏭️  已存在: {chunk_name}")
        return False
        
    original_url = f"{original_base_url}/{chunk_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"⬇️  下载: {chunk_name}")
        import time
        time.sleep(0.5)  # Add delay
        response = requests.get(original_url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        print(f"✅  保存成功")
        return True
        
    except Exception as e:
        print(f"❌  下载失败: {e}")
        return False

def main():
    print("=" * 80)
    print("🔍 扫描 Webpack Runtime 文件...")
    print("=" * 80)
    
    runtime_files = find_runtime_files(BASE_DIR)
    print(f"找到 {len(runtime_files)} 个 runtime 文件\n")
    
    total_downloaded = 0
    
    for runtime_file in runtime_files:
        print(f"📂 处理: {runtime_file.relative_to(BASE_DIR)}")
        
        # 确定下载目录（通常与 runtime 文件在同一目录）
        target_dir = runtime_file.parent
        
        # 确定原站点对应的 URL 路径
        try:
            rel_path = target_dir.resolve().relative_to(BASE_DIR.resolve())
            original_base_url = f"{ORIGINAL_SITE}/{str(rel_path).replace(os.sep, '/')}"
        except:
            print("❌ 无法确定原站点路径，跳过")
            continue
            
        chunks = extract_chunks(runtime_file)
        print(f"   发现 {len(chunks)} 个 chunk 引用")
        
        if not chunks:
            continue
            
        print(f"   开始下载到: {target_dir}\n")
        
        for chunk in chunks:
            if download_chunk(target_dir, chunk, original_base_url):
                total_downloaded += 1
        print("-" * 40)

    print("\n" + "=" * 80)
    print(f"🎉 完成！共下载 {total_downloaded} 个新文件")
    print("=" * 80)

if __name__ == '__main__':
    main()
