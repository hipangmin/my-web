import os
from bs4 import BeautifulSoup
import re

# Configuration
target_dir = r"d:\ypm\my web\test\cmcsclass.com"
old_email = "1454219507@qq.com"  # The one we just put in
new_email = "info@pangminybm.com" # The test domain email

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple string replacement is safe here because the old email is unique and we just put it there.
        # We don't need complex parsing for this specific swap.
        if old_email in content:
            new_content = content.replace(old_email, new_email)
            
            # Also check for mailto links just in case
            # mailto:1454219507@qq.com -> mailto:info@pangminybm.com
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {os.path.basename(file_path)}")
                
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
