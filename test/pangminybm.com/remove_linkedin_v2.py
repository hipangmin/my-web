import os
from bs4 import BeautifulSoup

# Directory to scan
root_dir = r"d:\ypm\my web\test\pangminybm.com"

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Strategy 1: Find by href
        # This is the most robust way to find ANY LinkedIn link
        linkedin_links = soup.find_all('a', href=True)
        for link in linkedin_links:
            if 'linkedin.com' in link['href']:
                print(f"[Removed] Link found in {os.path.basename(file_path)}: {link['href']}")
                
                # Check if it's inside a list item (Social Icons widget usually uses <ul><li>)
                parent_li = link.find_parent('li', class_='elementor-grid-item')
                if parent_li:
                    parent_li.decompose() # Remove the whole list item
                else:
                    # Also check for social icon wrapper specific to Elementor
                    wrapper = link.find_parent('span', class_='elementor-grid-item') 
                    if wrapper:
                        wrapper.decompose()
                    else:
                        link.decompose() # Just remove the link itself
                
                modified = True

        # Strategy 2: Find by specific data-id (The one we missed in footer?)
        # Let's clean up any legacy IDs if known, but href is better.
        
        if modified:
             with open(file_path, 'w', encoding='utf-8') as f:
                 f.write(str(soup))
            
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
