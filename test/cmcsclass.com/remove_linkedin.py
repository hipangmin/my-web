import os
from bs4 import BeautifulSoup

# Directory to scan
root_dir = r"d:\ypm\my web\test\pangminybm.com"

# The ID of the element to remove (LinkedIn icon wrapper)
target_id = "24922ad6"

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the element by data-id
        # Elementor uses specific class structure, but unique data-id is most reliable
        target_div = soup.find('div', attrs={'data-id': target_id})
        
        if target_div:
            # check if it looks like the linked in button (extra safety)
            if 'elementor-widget-button' in target_div.get('class', []):
                 print(f"Removing LinkedIn icon from: {file_path}")
                 target_div.decompose()
                 
                 # Save back
                 with open(file_path, 'w', encoding='utf-8') as f:
                     f.write(str(soup))
        else:
            # print(f"Target not found in: {file_path}")
            pass
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    count = 0
    print(f"Scanning directory: {root_dir}")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))
                count += 1

    print(f"Finished scanning {count} HTML files.")
