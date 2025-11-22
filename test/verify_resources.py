import os
import re
import requests
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

# Configuration
BASE_URL = "http://localhost:8080/"
ROOT_DIR = r"d:\ypm\my web\test\pangminybm.com"

# Sets to store URLs
visited_urls = set()
broken_links = []
valid_links = set()

# Extensions to ignore (optional, but good for speed if we only care about specific types)
# IGNORE_EXTS = ['.pdf', '.zip'] 

def is_internal(url):
    """Check if the URL belongs to the local server."""
    return url.startswith(BASE_URL)

def get_local_path(url):
    """Convert a URL to a local file path."""
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    if path == '' or path.endswith('/'):
        path += 'index.html'
    
    # Handle query parameters if they point to a file (simple heuristic)
    # For static sites, we usually map URL path directly to file system
    return os.path.join(ROOT_DIR, path.replace('/', os.sep))

def check_url(url):
    """Check if a URL is reachable (200 OK)."""
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            valid_links.add(url)
            print(f"[OK] {url}")
        else:
            broken_links.append((url, f"Status: {response.status_code}"))
            print(f"[FAIL] {url} (Status: {response.status_code})")
    except Exception as e:
        broken_links.append((url, str(e)))
        print(f"[ERROR] {url} ({e})")

def extract_links_from_file(file_path, base_url):
    """Extract all links (href, src) from a local HTML/CSS file."""
    links = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Regex for href and src attributes
        # This is a simple regex and might miss some complex cases or JS generated links
        matches = re.findall(r'(?:href|src)=["\'](.*?)["\']', content)
        
        for match in matches:
            # Clean up the link
            link = match.strip()
            
            # Skip empty links, anchors, javascript:, mailto:, tel:
            if not link or link.startswith('#') or link.startswith('javascript:') or link.startswith('mailto:') or link.startswith('tel:'):
                continue
            
            # Resolve relative URLs
            full_url = urljoin(base_url, link)
            
            # Only check internal links or resources hosted locally
            if is_internal(full_url):
                links.add(full_url)
                
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        
    return links

def crawl_and_verify():
    """Main function to crawl and verify resources."""
    print(f"Starting verification for {BASE_URL}...")
    print(f"Root directory: {ROOT_DIR}")
    
    # Queue of URLs to process (starting with homepage)
    queue = [BASE_URL]
    processed_files = set()

    # We will use a ThreadPool for checking URLs concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        while queue:
            current_url = queue.pop(0)
            
            # If we've already processed this file's content for links, skip extracting
            # But we still might need to check if the URL itself is valid (handled in check_url)
            
            # 1. Check if the URL is valid (HEAD request)
            future = executor.submit(check_url, current_url)
            future.result() # Wait for result to ensure we don't flood too fast and to update lists
            
            # 2. If it's an HTML file, extract links from it and add to queue
            # Map URL to local file to read content
            local_path = get_local_path(current_url)
            
            if local_path not in processed_files and os.path.exists(local_path):
                processed_files.add(local_path)
                
                # Only parse HTML or CSS files for more links
                if local_path.endswith('.html') or local_path.endswith('.css'):
                    new_links = extract_links_from_file(local_path, current_url)
                    for link in new_links:
                        if link not in visited_urls and link not in queue:
                            queue.append(link)
            elif not os.path.exists(local_path) and is_internal(current_url):
                 # If local file doesn't exist but it's an internal URL we expect to find
                 # This might be caught by check_url returning 404, but good to note
                 pass

    print("\n" + "="*30)
    print("VERIFICATION COMPLETE")
    print("="*30)
    print(f"Total URLs checked: {len(visited_urls)}")
    print(f"Valid links: {len(valid_links)}")
    print(f"Broken links: {len(broken_links)}")
    
    if broken_links:
        print("\nBroken Links Found:")
        for url, reason in broken_links:
            print(f"- {url} : {reason}")
    else:
        print("\nNo broken links found! All resources are loadable.")

if __name__ == "__main__":
    # Ensure the server is running before executing this script
    # You can run 'python -m http.server 8080' in the root dir in a separate terminal
    crawl_and_verify()
