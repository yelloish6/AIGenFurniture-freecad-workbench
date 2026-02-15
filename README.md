# AIGenFurniture FreeCAD Workbench

A FreeCAD workbench intended to automatically generate furniture based on predefined simple boxes.

⚠️ **Project status:** early-stage / experimental  
🖥️ **Supported platform:** **Windows only**

---

## 🖥️ Platform Support

At the moment, **AIGenFurniture is only supported on Windows**.

- ✅ Windows: supported and tested
- ❌ macOS: not yet supported
- ❌ Linux: not yet supported

Earlier commits mentioned macOS/Linux installation paths, but these were never fully tested and may not work.  
Please use the Windows installer described below.

---

## 🚀 Recommended Installation (Windows)

The **recommended and supported installation method** is via the **`.exe` installer** available on the GitHub Releases page.

✔ No manual dependency installation  
✔ Uses the correct Python environment automatically  
✔ Tested setup

### Steps

1. Go to the **Releases** section of this repository
2. Download the latest **`AIGenFurniture-Setup.exe`**
3. Close FreeCAD if it is running
4. Run the installer
5. Launch FreeCAD

After installation, you should see **CabinetWorkbench** in the FreeCAD workbench selector.

---

## 🔧 Manual Installation (Advanced / Not Recommended)

Manual installation is provided **only for advanced users** or development purposes.  
It is **not the recommended setup** and may require troubleshooting.

> If you are new to the project, **use the `.exe` installer instead**.

### 1. Install the workbench

Copy the entire folder **`CabinetWorkbench`** into your FreeCAD `Mod` directory:

| Windows install type | User `Mod` folder (recommended) |
|----------------------|----------------------------------|
| Standard installer   | `C:\Users\<USERNAME>\AppData\Roaming\FreeCAD\Mod` |
| Portable (.zip)      | `<FreeCAD-Portable-Folder>\AppData\Roaming\FreeCAD\Mod` |

---

### 2. Dependencies

When installing manually, all required Python dependencies **must match FreeCAD’s Python version**.

The recommended way to avoid dependency issues is to use the `.exe` installer instead.

---

### 3. Launch FreeCAD

Restart FreeCAD and select **CabinetWorkbench** from the workbench selector.

---

## 🎥 Tutorials & Walkthroughs

I’m recording short video tutorials that show how to use **AIGenFurniture** in real FreeCAD workflows, including:

- Installation via the `.exe` installer
- Creating simple cabinet layouts
- Generating furniture from placeholder boxes
- Exporting production-ready outputs

You can find the tutorials here:  
👉 **YouTube: http://www.youtube.com/@AIGenFurniture**

The videos follow the same early-stage evolution as the project, so feedback and suggestions are very welcome.


## 💬 Feedback & Issues

If you encounter issues, please make sure that:

- you are running **Windows**
- you installed via the **latest `.exe` installer**
- you are using a supported FreeCAD version

When opening a GitHub issue, include:
- Windows version
- FreeCAD version
- installation method (`.exe` installer or manual)

Early feedback is very welcome and helps shape the future of the project. Please report issues or suggestions via:
- GitHub Issues
- Email (if you prefer direct feedback) at: contact@aigenfurniture.com
