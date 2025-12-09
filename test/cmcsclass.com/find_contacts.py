import re
import os

file_path = r"d:\ypm\my web\test\cmcsclass.com\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Simple regex for emails
emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content))
print("Found unique emails:")
for e in emails:
    print(e)

# Simple regex for phone numbers (broad pattern to catch likely candidates)
# Looking for sequences of digits, potentially with spaces, dashes, or plus signs, 
# that are at least 8 chars long.
phones = set(re.findall(r'(?:\+?[\d\s-]{8,})', content))

print("\nPotential phone strings (filtered):")
for p in phones:
    # Filter out obvious non-phones (like CSS pixel values or long ID strings usually don't have spaces unless specific)
    # Just show ones that look like they might be content
    s = p.strip()
    if 8 < len(s) < 20 and any(c.isdigit() for c in s):
       print(s)
