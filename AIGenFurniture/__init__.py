import os, sys

# Add the vendor folder to sys.path
_vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
if _vendor_path not in sys.path:
    sys.path.insert(0, _vendor_path)
