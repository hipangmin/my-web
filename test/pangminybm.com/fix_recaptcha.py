import os
import re

def fix_recaptcha_links(directory):
    print(f"Scanning {directory} for incorrect reCAPTCHA links...")
    count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to match the incorrect relative path to google recaptcha
                # Matches src="../.../www.google.com/recaptcha/api9513.js..."
                pattern = r'src="[^"]*www\.google\.com/recaptcha/api9513\.js([^"]*)"'
                replacement = r'src="https://www.google.com/recaptcha/api.js\1"'
                
                new_content, n = re.subn(pattern, replacement, content)
                
                if n > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed {n} link(s) in {file}")
                    count += n

    print(f"Total fixed: {count}")

if __name__ == "__main__":
    fix_recaptcha_links('.')
