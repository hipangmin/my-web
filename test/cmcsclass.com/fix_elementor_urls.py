#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_elementor_urls(file_path):
    """Fix Elementor config URLs in HTML files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace escaped URLs in JavaScript/JSON: https:\/\/pangminybm.com\/
        content = re.sub(
            r'https:\\/\\/pangminybm\.com\\/',
            '../../',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    base_dir = Path('.')
    fixed_count = 0
    
    for html_file in base_dir.rglob('*.html'):
        if fix_elementor_urls(html_file):
            print(f"Fixed: {html_file.name}")
            fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()
