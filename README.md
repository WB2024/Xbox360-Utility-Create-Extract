# 360 Utility Batch Create Extract — Linux Fork

A Linux port of the original Windows-only Xbox 360 utility.  
Batch extraction and creation of Xbox 360 and Original Xbox ISOs from game folders containing `.xex` or `.xbe` files.

---

<!-- Screenshot: Main window -->

---

## Requirements

### System dependencies
```bash
sudo apt install python3-tk   # tkinter for the GUI
sudo apt install wine         # required to run the bundled Windows tools
```

### Tool binary
Place a Linux build of `extract-xiso` inside `x_tool/` and make it executable:
```bash
chmod +x x_tool/extract-xiso
```
You can build it from source: [https://github.com/XboxDev/extract-xiso](https://github.com/XboxDev/extract-xiso)

---

## Running

```bash
python3 main.pyw
```

The `x_tool/` and `x_ISO/` folders must be in the same directory as `main.pyw`.  
If `x_ISO/` does not exist, create it before running.

---

## 1. Batch Extraction of ISOs

- Place your `.iso` files into the folder named `x_ISO/`

<!-- Screenshot: x_ISO folder with ISOs inside -->

- Click **Extract Game Folders from ISOs**
- Extracted game folders will be created next to `x_ISO/`, each containing `.xex` or `.xbe` files

---

## 2. Batch Creation of ISOs from Game Folders

- Place your game folders next to `x_ISO/` (not inside it)

<!-- Screenshot: game folders next to x_ISO -->

- Click **Create ISOs from Game Folders**
- New `.iso` files will be saved next to `x_ISO/`

> **Note:** Newly created ISOs may need fixing before they work with Xbox Image Browser.  
> Use the **360mpGui v1.5.0.0** button (runs via wine) to fix them one by one.

---

## Bundled Tools (run via wine)

| Button | Tool |
|---|---|
| 360mpGui v1.5.0.0 (Fix ISOs One by One) | Repairs ISO headers |
| ISO to GOD | Converts ISOs to Games on Demand format |
| GOD to ISO | Converts GOD format back to ISO |
| Xbox Image Browser | Browse/inspect Xbox ISO contents |

---

## Notes

- This is a Linux-only fork. Windows is not supported.
- The bundled `.exe` tools require `wine` to be installed.
- `extract-xiso` must be the Linux native binary placed at `x_tool/extract-xiso`.

---

## Credits & Acknowledgements

- BLAHPR (original author)
- XboxDev
- rikyperdana
- raburton
- rapperskull
- iliazeus
- r4dius
- eliecharra
- markus-oberhumer
- upx Team
- &lt;in@fishtank.com&gt;
- Redline99
- 360mpGui Team
- God2Iso Team
- Iso2God Team

Original project: [https://github.com/BLAHPR/Xbox360-Utility-Create-Extract](https://github.com/BLAHPR/Xbox360-Utility-Create-Extract)  
Contact: geebob273@gmail.com
