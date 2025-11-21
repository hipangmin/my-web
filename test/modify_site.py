import os
import shutil

# --- CONFIGURATION ---
# Edit these values to your desired domain and site name
OLD_DOMAIN = "macmasterimaritime.com"
NEW_DOMAIN = "pangminybm.com"  # e.g., mysite.com

OLD_NAME = "Macmasteri Maritime"
NEW_NAME = "Center Marine Certificate Service"     # e.g., My Maritime Services

# Directory to process (current directory by default)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ---------------------

def replace_in_file(file_path):
    try:
        # Try reading as text (utf-8)
        # Removed errors='ignore' to avoid corrupting binary files if they are mistakenly processed
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace(OLD_DOMAIN, NEW_DOMAIN)
        new_content = new_content.replace(OLD_NAME, NEW_NAME)
        
        # Additional replacements for variations
        additional_replacements = {
            "MacMasteri": "Center Marine",
            "Macmasteri": "Center Marine",
            "macmasteri": "center marine",
            "MACMASTERI MARITIME": "CENTER MARINE CERTIFICATE SERVICE",
            "MACMASTERI": "CENTER MARINE",
        }
        for old, new in additional_replacements.items():
            new_content = new_content.replace(old, new)
        
        # Basic cleanup of HTTrack comments
        if "HTTrack Website Copier" in new_content:
            new_content = new_content.replace("<!-- Mirrored from", "<!-- Original from")
            new_content = new_content.replace("<!-- /Added by HTTrack -->", "")
            # Remove the specific meta tag added by HTTrack if present
            # <meta http-equiv="content-type" content="text/html;charset=UTF-8" />
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Modified: {file_path}")
            return True
    except UnicodeDecodeError:
        # If it fails to decode as UTF-8, it's likely a binary file, so we skip it.
        pass
    except Exception as e:
        print(f"Skipping file {file_path}: {e}")
    return False

def process_directory(directory):
    print(f"Processing directory: {directory}")
    
    extensions = ['.html', '.css', '.js', '.json', '.xml', '.txt', '.php']

    # Walk through all files
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            # Skip this script itself
            if file == os.path.basename(__file__):
                continue
                
            file_path = os.path.join(root, file)
            
            # Check extension
            _, ext = os.path.splitext(file)
            # Process if it has a target extension OR if it has NO extension (potential text file like in wp-json)
            if ext in extensions or ext == '':
                replace_in_file(file_path)
        
        # Rename directories if they contain the old domain
        for name in dirs:
            if OLD_DOMAIN in name:
                old_dir_path = os.path.join(root, name)
                new_dir_name = name.replace(OLD_DOMAIN, NEW_DOMAIN)
                new_dir_path = os.path.join(root, new_dir_name)
                
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed directory: {old_dir_path} -> {new_dir_path}")
                except OSError as e:
                    print(f"Error renaming directory {old_dir_path}: {e}")

def main():
    print("--- Website Modification Script ---")
    print(f"Old Domain: {OLD_DOMAIN}")
    print(f"New Domain: {NEW_DOMAIN}")
    print(f"Old Name:   {OLD_NAME}")
    print(f"New Name:   {NEW_NAME}")
    print("-" * 30)
    
    if NEW_DOMAIN == "YOUR_NEW_DOMAIN.com":
        print("WARNING: You have not set a custom NEW_DOMAIN yet.")
        print("Please edit this script and set NEW_DOMAIN and NEW_NAME variables.")
        confirm = input("Do you want to proceed anyway? (y/n): ")
        if confirm.lower() != 'y':
            return

    target_dir = os.path.join(BASE_DIR, OLD_DOMAIN)
    
    # If the old domain directory doesn't exist, maybe it was already renamed or we should look in current dir
    if not os.path.exists(target_dir):
        # Check if we are already inside the folder or if it's named differently
        # Try looking for the new domain folder first
        new_target_dir = os.path.join(BASE_DIR, NEW_DOMAIN)
        if os.path.exists(new_target_dir):
             print(f"Target directory '{target_dir}' not found, but '{new_target_dir}' exists.")
             print(f"Processing '{new_target_dir}'...")
             process_directory(new_target_dir)
        else:
            print(f"Target directory '{target_dir}' not found.")
            print(f"Scanning current directory: {BASE_DIR}")
            process_directory(BASE_DIR)
    else:
        process_directory(target_dir)
        
        # Finally, rename the main folder if it matches
        if os.path.basename(target_dir) == OLD_DOMAIN:
            new_target_dir = os.path.join(BASE_DIR, NEW_DOMAIN)
            try:
                os.rename(target_dir, new_target_dir)
                print(f"Renamed main directory: {target_dir} -> {new_target_dir}")
            except OSError as e:
                print(f"Error renaming main directory: {e}")

    print("Done!")

if __name__ == "__main__":
    main()
