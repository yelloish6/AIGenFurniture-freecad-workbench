# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os, sys

# Package version - follows Semantic Versioning
# See: https://semver.org/
__version__ = "0.2.0"

# Make vendored dependencies available to both FreeCAD and CLI entry points.
# Prefer the active runtime's packages, especially binary packages such as numpy.
_vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
if _vendor_path not in sys.path:
    sys.path.append(_vendor_path)
