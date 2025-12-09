import os
import re
from bs4 import BeautifulSoup

# Configuration
target_dir = r"d:\ypm\my web\test\cmcsclass.com"
new_phone = "00852-61717889"
new_phone_clean = "0085261717889"
new_email = "info@pangminybm.com"

# Regex for old phone (catch existing variations)
# Matches +90 543 150 9806 with optional spaces/dashes
old_phone_regex = re.compile(r'\+90[\s-]?543[\s-]?150[\s-]?9806')

# Regex for placeholder tel links
placeholder_tel_regex = re.compile(r'tel:123-456-7890')

def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # ---------------------------
        # 1. REMOVE LINKEDIN
        # ---------------------------
        # Find all 'a' tags with linkedin in href
        for a in soup.find_all('a', href=True):
            if 'linkedin.com' in a['href'] or 'macamsteri-maritime' in a['href']:
                # Decide what to remove: the <li> wrapper if it exists, or just the <a>
                parent_li = a.find_parent('li', class_='elementor-grid-item')
                if not parent_li:
                     parent_li = a.find_parent('li', class_='elementor-icon-list-item')
                
                if parent_li:
                    parent_li.decompose()
                else:
                    # Also try finding span wrapper for social icons
                    parent_span = a.find_parent('span', class_='elementor-grid-item')
                    if parent_span:
                        parent_span.decompose()
                    else:
                        a.decompose()
                modified = True

        # ---------------------------
        # 2. REPLACE CONTACT INFO (Text Nodes)
        # ---------------------------
        for text_node in soup.find_all(string=True):
            txt = str(text_node)
            
            # Replace Phone
            if old_phone_regex.search(txt):
                new_txt = old_phone_regex.sub(new_phone, txt)
                text_node.replace_with(new_txt)
                modified = True
                
            # Replace "Email: [email protected]" text generally if found in text node?
            # Actually, BS4 handles decoded text, so [email protected] matches are usually
            # handled by the dedicated logic below. But if "1454219507@qq.com" is left over:
            if "1454219507@qq.com" in txt:
                new_txt = txt.replace("1454219507@qq.com", new_email)
                text_node.replace_with(new_txt)
                modified = True

        # ---------------------------
        # 3. REPLACE LINKS (HREF)
        # ---------------------------
        for a in soup.find_all('a', href=True):
            href = a['href']
            
            # Fix Phone Links
            if "905431509806" in href or "123-456-7890" in href:
                a['href'] = f"tel:{new_phone_clean}"
                modified = True
                
            # Fix Mailto Links
            if "mailto:" in href:
                if "macmasteri" in href or "qq.com" in href:
                    a['href'] = f"mailto:{new_email}"
                    modified = True

        # ---------------------------
        # 4. HANDLE CLOUDFLARE EMAIL OBFUSCATION
        # ---------------------------
        # Find ANY element with class __cf_email__
        for cf_span in soup.find_all(class_='__cf_email__'):
            # Replace it with plain email
            cf_span.replace_with(new_email)
            modified = True
            
        # ---------------------------
        # 5. HANDLE [email protected] TEXT
        # ---------------------------
        # Sometimes header scripts aren't parsed by finding class above. 
        # But generally replacing the cf_span works.
        
        if modified:
            print(f"Fixed: {os.path.basename(file_path)}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

    except Exception as e:
        print(f"Error in {file_path}: {e}")

if __name__ == "__main__":
    print(f"Deep cleaning directory: {target_dir}")
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
             if file.endswith('.html'):
                 clean_file(os.path.join(root, file))
                 count += 1
    print(f"Done. Processed {count} files.")
