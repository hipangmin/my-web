import os
import re

def fix_relative_paths(root_dir):
    print(f"Scanning {root_dir} to fix relative paths and Elementor config...")
    
    abs_root = os.path.abspath(root_dir)
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # 计算深度
                rel_path = os.path.relpath(root, abs_root)
                if rel_path == '.':
                    depth = 0
                else:
                    depth = len(rel_path.split(os.sep))
                
                # 生成正确的前缀 (例如 "../../../")
                prefix = "../" * depth if depth > 0 else ""
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content

                # -------------------------------------------------
                # 1. 修复 Elementor JSON 配置中的路径
                # -------------------------------------------------
                # 查找 "assets": "..." 并替换
                # 注意：JSON 中的斜杠可能被转义为 \/
                
                def replace_json_path(match):
                    # match.group(1): "assets":"
                    # match.group(2): existing path content
                    # match.group(3): "
                    
                    # 我们不管原来的路径是什么，直接用正确的 prefix + 路径后缀替换
                    # 但是要小心，assets 路径通常指向 .../assets/
                    
                    # 简单起见，我们只替换 ../wp-content... 这种形式的
                    # 或者直接重写整个 assets 路径
                    
                    return f'{match.group(1)}{prefix}wp-content\\/plugins\\/elementor\\/assets\\/"'

                # 替换 elementorFrontendConfig 中的 assets
                escaped_prefix = prefix.replace("/", r"\/")
                
                # "assets":".../wp-content/plugins/elementor/assets/"
                pattern_core = r'("assets":")((?:\\.|[^"\\])*wp-content\\/plugins\\/elementor\\/assets\\/)(")'
                content = re.sub(pattern_core, lambda m: f'{m.group(1)}{escaped_prefix}wp-content\/plugins\/elementor\/assets\/{m.group(3)}', content)

                # 替换 ElementorProFrontendConfig 中的 assets
                # "assets":".../wp-content/plugins/elementor-pro/assets/"
                pattern_pro = r'("assets":")((?:\\.|[^"\\])*wp-content\\/plugins\\/elementor-pro\\/assets\\/)(")'
                content = re.sub(pattern_pro, lambda m: f'{m.group(1)}{escaped_prefix}wp-content\/plugins\/elementor-pro\/assets\/{m.group(3)}', content)

                # -------------------------------------------------
                # 1.5 修复 wpemojiSettings 中的路径
                # -------------------------------------------------
                # "concatemoji":".../wp-includes/js/wp-emoji-release.min.js..."
                pattern_emoji = r'("concatemoji":")((?:\\.|[^"\\])*wp-includes\\/js\\/wp-emoji-release\.min\.js)'
                content = re.sub(pattern_emoji, lambda m: f'{m.group(1)}{escaped_prefix}wp-includes\/js\/wp-emoji-release.min.js', content)

                # -------------------------------------------------
                # 2. 修复 HTML 标签中的路径 (src/href)
                # -------------------------------------------------
                def replace_html_path(match):
                    attr = match.group(1) # src= or href=
                    quote = match.group(2) # " or '
                    path = match.group(3) # wp-content/... or ../wp-content/...
                    
                    # 如果是绝对路径，跳过
                    if path.startswith(('http:', 'https:', 'file:', '/')):
                        return match.group(0)
                    
                    # 移除所有现有的 ../ 前缀，还原为纯 wp-content/...
                    clean_path = re.sub(r'^(\.\./)+', '', path)
                    
                    # 如果不是以 wp-content 或 wp-includes 开头，跳过 (可能是其他相对路径)
                    if not clean_path.startswith(('wp-content/', 'wp-includes/')):
                        return match.group(0)
                        
                    return f'{attr}{quote}{prefix}{clean_path}{quote}'

                # 匹配 src="..." 或 href="..."，且包含 wp-content 或 wp-includes
                # 允许前面有任意数量的 ../
                pattern_html = r'(src=|href=)(["\'])((?:(?:\.\./)*)(?:wp-content|wp-includes)/[^"\']+)(["\'])'
                content = re.sub(pattern_html, replace_html_path, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed {file} (Depth: {depth})")

if __name__ == "__main__":
    fix_relative_paths('.')
