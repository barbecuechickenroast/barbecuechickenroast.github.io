# cleaner.py
import re

boot_path = "js/boot0-0796dd8d.js"

if not os.path.exists(boot_path):
    print(f"Error: Could not find {boot_path}. Ensure this script is placed in the root directory.")
    exit(1)

with open(boot_path, "r", encoding="utf-8") as f:
    code = f.read()

print("Original code length:", len(code))

# 1. Force anti-piracy domain matching logic to always evaluate to true/passed
# We look for common hostname/location checks or window comparison blocks and bypass them
patched_code = re.sub(r'location\s*\.\s*hostname\s*!==?\s*["']deltarunesim\.com["']', 'false', code)
patched_code = re.sub(r'window\s*\.\s*location\s*\.\s*hostname\s*!==?\s*["']deltarunesim\.com["']', 'false', code)

# 2. Inject an environment spoof at the absolute beginning of the file execution
# This forces the window context to lie about its location to any framework router scripts
spoof_prefix = ';(function(){try{Object.defineProperty(window,"location",{writable:true,value:Object.create(window.location)});Object.defineProperty(window.location,"hostname",{value:"deltarunesim.com",writable:false});Object.defineProperty(window.location,"host",{value:"deltarunesim.com",writable:false});}catch(e){}})();'

final_code = spoof_prefix + patched_code

with open(boot_path, "w", encoding="utf-8") as f:
    f.write(final_code)

print("Patch successfully applied! Please commit and push the changes.")
