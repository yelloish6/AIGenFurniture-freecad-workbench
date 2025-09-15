# AIGenFurniture-freecad-workbench
A FreeCAD workbench intended to automatically generate furniture based on predefined simple boxes.

## 🔧 Installation

1. **Locate your FreeCAD `Mod` folder**  
   Copy the entire folder **`CabinetWorkbench`** into your FreeCAD `Mod` directory.  
   The location of the `Mod` folder depends on your operating system and installation type:

   | OS / Install Type          | User `Mod` folder (recommended) | System-wide / App folder (may require admin/root) |
   |----------------------------|---------------------------------|--------------------------------------------------|
   | **Windows (standard install)** | `C:\Users\<USERNAME>\AppData\Roaming\FreeCAD\Mod` | `C:\Program Files\FreeCAD <version>\Mod` |
   | **Windows (portable .zip)**    | `<FreeCAD-Portable-Folder>\AppData\Roaming\FreeCAD\Mod` | `<FreeCAD-Portable-Folder>\Mod` |
   | **Linux (package manager)**    | `~/.local/share/FreeCAD/Mod` | `/usr/lib/freecad/Mod` or `/usr/share/freecad/Mod` |
   | **macOS (.dmg / .app)**        | `~/Library/Preferences/FreeCAD/Mod` | `/Applications/FreeCAD.app/Contents/Mod` |
   | **Linux (AppImage)**           | `~/.local/share/FreeCAD/Mod` | *(inside AppImage, read-only)* |
   | **Linux (Snap)**               | `~/snap/freecad/current/.local/share/FreeCAD/Mod` | `/snap/freecad/current/usr/share/freecad/Mod` |
   | **Linux (Flatpak)**            | `~/.var/app/org.freecadweb.FreeCAD/data/FreeCAD/Mod` | `/var/lib/flatpak/app/org.freecadweb.FreeCAD/current/active/files/Mod` |

   👉 **Tip:** Always prefer the **user folder**, so your workbench survives FreeCAD updates.

---

2. **Install Python dependencies**  
   
   This workbench requires the following Python packages:
   - openpyxl==3.1.5 (vendored and distributed in ./AIGenFurniture/vendor)
   - tripy==1.0.0 (vendored and distributed in ./AIGenFurniture/vendor)
   - reportlab==4.4.3 (vendored and distributed in ./AIGenFurniture/vendor)
   - numpy==2.3.2 (not vendored)
   - numpy-stl==3.1.2 (not vendored)
   - PyMuPDF==1.24.14 (not vendored)

   ### a) Standard installs (Windows/Linux/macOS) 
   From inside the `CabinetWorkbench/AIGenFurniture` folder, run:

      ```bash
      pip install -r requirements.txt
   ```

   ### b) Portable FreeCAD on Windows

   Portable FreeCAD uses its own Python. You must install binary dependencies into that Python, while pure-Python ones are already vendored.

   FreeCAD’s Python:

      ```bash
      <FreeCAD-Portable>\bin\python.exe
   ```

    Install binary packages into it:

      ```bash
      <FreeCAD-Portable>\bin\python.exe -m pip install numpy==2.3.2 numpy-stl==3.1.2 PyMuPDF==1.24.14
   ```

    Pure-Python dependencies (openpyxl, tripy, reportlab) are bundled inside the workbench (vendor/), so no extra steps are needed.
    On Windows, make sure to use the Python environment that FreeCAD uses.
    (If you use portable FreeCAD, the Python executable is usually inside bin\python.exe in the portable folder.)

    On Linux/macOS, you may need to run:

        python3 -m pip install -r requirements.txt

3. **Launch FreeCAD**  
   Restart FreeCAD. You should now see CabinetWorkbench in the Workbench selector.

