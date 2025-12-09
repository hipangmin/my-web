import os
from bs4 import BeautifulSoup
import re

# Configuration
target_dir = r"d:\ypm\my web\test\cmcsclass.com"
new_phone = "00852-61717889"
new_phone_clean = "0085261717889" # For tel: links
new_email = "1454219507@qq.com"

# Regex for old phone (approximate to catch variations)
# Found in source: +905431509806
old_phone_pattern = re.compile(r'\+90\s?543\s?150\s?9806')
placeholder_tel = "123-456-7890"

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # 1. Replace Email (Cloudflare obfuscated span)
        # Look for spans with class __cf_email__
        cf_emails = soup.find_all('span', class_='__cf_email__')
        for cf_span in cf_emails:
            # Check if parent is "Email:" text wrapper
            parent = cf_span.find_parent('span', class_='elementor-icon-list-text')
            if parent:
                # Replace the whole content of the parent (e.g. "Email: [email protected]")
                # We want: "Email: 123@qq.com"
                # Keep the "Email: " prefix if it exists in the parent's text but outside the cf_span?
                # Actually, simply clearing the parent and setting text is safer.
                parent.string = f"Email: {new_email}"
                modified = True
            else:
                 # Just replace the span itself with the email
                 cf_span.replace_with(new_email)
                 modified = True
                 
        # 2. Replace Phone Numbers in Text
        # We search all text nodes
        for text_node in soup.find_all(string=True):
            if old_phone_pattern.search(text_node):
                new_text = old_phone_pattern.sub(new_phone, text_node)
                text_node.replace_with(new_text)
                modified = True
                
        # 3. Replace Links (href)
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Fix placeholder tel
            if placeholder_tel in href:
                a['href'] = f"tel:{new_phone_clean}"
                modified = True
            # Fix old phone tel
            elif "905431509806" in href.replace(" ",""):
                a['href'] = f"tel:{new_phone_clean}"
                modified = True
            # Fix mailto if any (rare but possible)
            elif "mailto:" in href and "macmasteri" in href:
                 a['href'] = f"mailto:{new_email}"
                 modified = True

        if modified:
            print(f"Updating: {os.path.basename(file_path)}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    count = 0
    print(f"Scanning directory: {target_dir}")
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))
                count += 1
    print(f"Finished scanning {count} files.")
