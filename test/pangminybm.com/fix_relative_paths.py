import os
import re

def fix_relative_paths(root_dir):
    print(f"Scanning {root_dir} to fix relative paths...")
    
    # 根目录的绝对路径
    abs_root = os.path.abspath(root_dir)
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # 计算当前文件相对于根目录的深度
                rel_path = os.path.relpath(root, abs_root)
                if rel_path == '.':
                    depth = 0
                else:
                    depth = len(rel_path.split(os.sep))
                
                # 生成回退前缀 (例如 "../../")
                prefix = "../" * depth if depth > 0 else ""
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. 修复以 wp-content 或 wp-includes 开头的路径 (如果它们没有前缀)
                # 查找: src="wp-content/..." 且前面没有 ../
                # 替换为: src="{prefix}wp-content/..."
                
                def replace_path(match):
                    attr = match.group(1) # src= or href=
                    quote = match.group(2) # " or '
                    path = match.group(3) # wp-content/...
                    
                    # 如果路径已经是绝对路径 (http/https/file) 或以 / 开头，或者是相对回退 ../，则跳过
                    if path.startswith(('http:', 'https:', 'file:', '/', '../')):
                        return match.group(0)
                        
                    return f'{attr}{quote}{prefix}{path}{quote}'

                # 匹配 src="wp-content/..." 或 href="wp-includes/..."
                # 这里的正则比较宽泛，匹配所有 wp- 开头的资源
                pattern = r'(src=|href=)(["\'])(wp-(?:content|includes)/[^"\']+)(["\'])'
                
                new_content = re.sub(pattern, replace_path, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed paths in {file} (Depth: {depth}, Prefix: '{prefix}')")

if __name__ == "__main__":
    fix_relative_paths('.')
