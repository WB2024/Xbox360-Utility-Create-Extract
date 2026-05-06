# 360 Utility Batch Create Extract — Linux Fork

> A fully native Linux port of the original Windows-only Xbox 360 utility by BLAHPR.  
> No wine. No Windows tools. All binaries are built from source on Linux.

Batch extraction and creation of Xbox 360 and Original Xbox ISOs, with native Linux tools for ISO ↔ GOD conversion and ISO verification/fixing.

---

## Features

| Button | What it does |
|---|---|
| **Extract Game Folders from ISOs** | Batch-extracts all `.iso` files in `x_ISO/` into game folders |
| **Create ISOs from Game Folders** | Batch-creates `.iso` files from game folders containing `.xex` / `.xbe` |
| **Extract and Delete ISO Files** | Same as above, permanently deletes source ISOs after extraction |
| **Delete Game Folders** | Permanently deletes extracted game folders containing `.xex` / `.xbe` |
| **Fix ISO (abgx360)** | Verifies and auto-fixes ISO headers, stealth sectors, and video padding |
| **ISO to GOD** | Converts an ISO to Games on Demand format (Xbox 360 and Original Xbox) |
| **GOD to ISO** | Reconstructs an ISO from a GOD package |

---

## Requirements

### System packages

```bash
sudo apt install python3-tk                           # GUI toolkit
sudo apt install cargo                                # Rust (for iso2god and god2iso)
sudo apt install gcc libcurl4-openssl-dev zlib1g-dev  # C build tools (for abgx360)
```

### extract-xiso (Linux binary)

`extract-xiso` handles batch ISO extraction and creation. You must provide the Linux binary yourself:

```bash
# Build from source
git clone https://github.com/XboxDev/extract-xiso.git
cd extract-xiso && cmake . && make
cp extract-xiso /path/to/repo/x_tool/extract-xiso
chmod +x /path/to/repo/x_tool/extract-xiso
```

---

## Setup

Clone the repo and build all native tool binaries with the provided build script:

```bash
git clone https://github.com/your-fork/Xbox360-Utility-Create-Extract.git
cd Xbox360-Utility-Create-Extract
```

Place the `extract-xiso` Linux binary into `x_tool/` (see above), then run:

```bash
bash build.sh
```

`build.sh` will:
1. Build `iso2god` from `x_tool/iso2god-rs/` (Rust — requires `cargo`)
2. Build `god2iso` from `x_tool/god2iso-rs/` (Rust — requires `cargo`)
3. Build `abgx360` from `x_tool/abgx360-src/` (C — requires `gcc`, `libcurl`, `zlib`)
4. Bundle everything into a single executable via PyInstaller into `dist/`

### Manual build (without PyInstaller)

If you just want to run from source without bundling:

```bash
# Build iso2god
cd x_tool/iso2god-rs && cargo build --release
cp target/release/iso2god ../iso2god && cd ../..

# Build god2iso
cd x_tool/god2iso-rs && cargo build --release
cp target/release/god2iso ../god2iso && cd ../..

# Build abgx360
cd x_tool/abgx360-src && ./configure && make -j$(nproc)
cp src/abgx360 ../abgx360 && cd ../..
```

---

## Running

```bash
python3 main.pyw
```

The `x_tool/` and `x_ISO/` directories must be in the same directory as `main.pyw`.  
Create `x_ISO/` if it doesn't exist:

```bash
mkdir -p x_ISO
```

---

## Usage Guide

### 1. Batch Extract ISOs → Game Folders

1. Place your `.iso` files inside the `x_ISO/` folder
2. Click **Extract Game Folders from ISOs**
3. Each ISO is extracted to a game folder next to `x_ISO/` — containing `.xex` or `.xbe` files

> Use **Extract and Delete ISO Files** to automatically remove the source ISOs after extraction.

---

### 2. Batch Create ISOs from Game Folders

1. Place your game folders next to `x_ISO/` (not inside it) — each must contain `.xex` or `.xbe` files
2. Click **Create ISOs from Game Folders**
3. A `.iso` file is created for each game folder, saved next to `x_ISO/`

> Newly created ISOs may have incorrect headers. Run **Fix ISO (abgx360)** on them afterwards.

---

### 3. Fix ISO (abgx360)

Fixes ISO headers, stealth sectors, and video padding so ISOs are burnable and compatible.

1. Click **Fix ISO (abgx360)**
2. Select the `.iso` file to fix
3. abgx360 runs with:
   - `--af3` — AutoFix level 3 (always fix, even if uncertain)
   - `-p` — fix video padding
   - `-s` — no colour codes (clean status output)
   - `-o` — offline mode (no network required)
4. Output streams live into the status window

---

### 4. ISO to GOD (Games on Demand)

Converts an Xbox 360 or Original Xbox ISO into GOD format for use on a console hard drive.

1. Click **ISO to GOD (GAMES ON DEMAND)**
2. Select your source `.iso` file
3. Select an output folder
4. The `iso2god` binary converts it — the resulting GOD package is written to the output folder

---

### 5. GOD to ISO

Reconstructs an ISO from a Games on Demand package.

1. Click **GOD to ISO (GAMES ON DEMAND)**
2. Select the GOD **package header file** — this is the file *without* an extension (not the `.data` folder)
3. Select an output folder
4. The `god2iso` binary reconstructs the `.iso` in the output folder

> The `god2iso` tool also supports a `--fix` flag on the CLI for the optional CreateIsoGood header fix.

---

### 6. Cleanup Buttons

| Button | Behaviour |
|---|---|
| **Delete Game Folders** | Permanently deletes all folders next to `x_ISO/` that contain `.xex` / `.xbe` files |

> Both destructive buttons are coloured red and prompt no confirmation — use with care.

---

## Project Structure

```
Xbox360-Utility-Create-Extract/
├── main.pyw              # Main GUI application
├── x_create.pyw          # ISO creation logic
├── x_extract.pyw         # ISO extraction logic
├── translations.py       # UI string translations
├── build.sh              # Build script (tools + PyInstaller bundle)
├── Required.txt          # Dependency notes
├── x_ISO/                # Drop ISO files here for extraction
├── Images/               # App icon
└── x_tool/
    ├── extract-xiso      # ← you provide this (Linux binary)
    ├── iso2god           # ← built by build.sh
    ├── god2iso           # ← built by build.sh
    ├── abgx360           # ← built by build.sh
    ├── iso2god-rs/       # Source: ISO → GOD converter (Rust)
    ├── god2iso-rs/       # Source: GOD → ISO converter (Rust)
    └── abgx360-src/      # Source: ISO fix/verify tool (C)
```

---

## Troubleshooting

**`extract-xiso` not found**  
Make sure the Linux binary is at `x_tool/extract-xiso` and is executable (`chmod +x x_tool/extract-xiso`).

**`iso2god` / `god2iso` / `abgx360` not found**  
Run `bash build.sh` or follow the manual build steps above. The binaries must be at `x_tool/iso2god`, `x_tool/god2iso`, and `x_tool/abgx360`.

**abgx360 configure fails**  
Ensure build dependencies are installed: `sudo apt install gcc libcurl4-openssl-dev zlib1g-dev`

**Cargo not found**  
Install Rust: `sudo apt install cargo` or via [rustup.rs](https://rustup.rs)

---

## Credits & Acknowledgements

| Contributor | Role |
|---|---|
| BLAHPR | Original utility author |
| XboxDev | `extract-xiso` |
| iliazeus | `iso2god-rs` (Rust ISO→GOD) |
| raburton | Original `god2iso` (C#) |
| Seacrest / Bakasura | `abgx360` / `abgx360-reloaded` |
| rikyperdana | Contributions |
| rapperskull | Contributions |
| r4dius | Contributions |
| eliecharra | Contributions |
| markus-oberhumer + upx Team | UPX packer |
| &lt;in@fishtank.com&gt; | XISO format work |

---

Original Windows project: [github.com/BLAHPR/Xbox360-Utility-Create-Extract](https://github.com/BLAHPR/Xbox360-Utility-Create-Extract)  
Contact: geebob273@gmail.com
