import os
import re

def optimize_recaptcha(directory):
    print(f"Scanning {directory} for Google reCAPTCHA links...")
    count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace www.google.com/recaptcha with www.recaptcha.net/recaptcha
                # This is the official mirror for China
                pattern = r'www\.google\.com/recaptcha'
                replacement = r'www.recaptcha.net/recaptcha'
                
                new_content, n = re.subn(pattern, replacement, content)
                
                if n > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Optimized {n} link(s) in {file}")
                    count += n

    print(f"Total optimized: {count}")

if __name__ == "__main__":
    optimize_recaptcha('.')
