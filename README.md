# AIGenFurniture FreeCAD Workbench

A FreeCAD workbench that automatically generates furniture structures from
predefined parametric cabinet boxes — dramatically reducing the manual work
involved in furniture design and manufacturing preparation.

⚠️ **Project status:** Beta / Early-stage MVP  
📦 **Current version:** v0.1.4  
🖥️ **Tested on:** Windows · Linux  _(macOS not yet tested)_

---

## 🚀 Installation via FreeCAD Addon Manager (Recommended)

The easiest way to install AIGenFurniture is via the built-in
**FreeCAD Addon Manager**:

1. Open FreeCAD
2. Go to **Tools → Addon Manager**
3. Search for **AIGenFurniture**
4. Click **Install**
5. Restart FreeCAD
6. Select **Cabinet Generator** from the workbench selector

Do not skip the dependencies installation step that is triggered during the set-up.

> **Note on platform testing:**  
> The workbench has been tested on **Windows** and **Linux**.  
> It has **not been tested on macOS** — it may work, but is not confirmed.

---

## 💾 Manual Installation (Advanced / Development)

For advanced users or development purposes, you can install manually
by copying the `CabinetWorkbench` folder into FreeCAD's `Mod` directory.

| Platform | `Mod` folder path |
|----------|-------------------|
| Windows  | `C:\Users\<USERNAME>\AppData\Roaming\FreeCAD\Mod` |
| Linux    | `~/.local/share/FreeCAD/Mod` |

> When installing manually, all Python dependencies must match
> FreeCAD's internal Python version. The Addon Manager handles
> this automatically — use it unless you have a specific reason not to.

---

## ⬇️ Direct Download (Alternative)

Prefer a direct download? You can also grab the latest release from the
[aigenfurniture.com](https://www.aigenfurniture.com):

- Windows users: **`AIGenFurniture_Setup_0.1.3.exe`** (Windows installer)
- Cross-platform: source `.zip` from the release assets

---

## ✨ What It Does

AIGenFurniture automates the transition from idea → design → manufacturing files:

1. **Design your layout** — represent cabinets as labeled simple boxes in FreeCAD
2. **Configure parameters** — assign type, dimensions, and features (drawers, shelves, fronts) to each box
3. **Generate structure** — one click replaces the box with a full cabinet assembly
4. **Export manufacturing files** — generates all production-ready outputs under one folder

---

## 🎥 Tutorials

Short video tutorials covering installation, cabinet creation, and manufacturing exports:

👉 **YouTube: [youtube.com/@AIGenFurniture](http://www.youtube.com/@AIGenFurniture)**

---

## ❤️ Support the Project

AIGenFurniture is free and open-source (LGPL 2+). If it saves you time,
consider supporting its development:

- **Ko-fi:** https://ko-fi.com/bogdan_aigenfurniture
- **PayPal:** https://www.paypal.com/donate/?hosted_button_id=UV2AFNARW4RBN

Your support directly funds new features, better documentation, and maintenance.

---

## 💬 Feedback & Issues

Early-stage feedback shapes the product. When opening a GitHub Issue, please include:

- Operating system (Windows / Linux)
- FreeCAD version
- How you installed the workbench (Addon Manager / manual / installer)

You can also reach us directly: **contact@aigenfurniture.com**

---

## 📄 License

[LGPL 2+](LICENSE)
