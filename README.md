# Chronopulse: Overdrive ⚡⏳

**Chronopulse: Overdrive** is a high-fidelity, portable 3D urban endless runner built in Python using the **Ursina Engine**. It fuses classic arcade lane-dodging and curving track mechanics with an adrenaline-fueled time-shifting system and local-first SQLite data persistence.

---

## 🌟 Key Features

*   **Articulated Humanoid Runner:** A fully modeled cybernetic courier featuring procedural limb-swinging animations, tactical armor, and a glowing quantum data-core backpack.
*   **Curving Procedural Cityscape:** Dynamic roadway and skyscraper generation that bends and curves naturally using trigonometric wave offsets.
*   **Time-Shifting Epochs:** Spiking your adrenaline meter triggers an overdrive state that instantly morphs the city's architecture and color palette across Past, Present, and Future eras.
*   **Local-First Architecture:** Zero bulky asset pipelines or external servers—runs entirely offline with run histories and high scores stored in an embedded SQLite database.
*   **Portable Standalone Build:** Easily bundleable into a single self-contained Windows `.exe` using PyInstaller.

---

## 🎮 Controls

| Action | Input Keys |
| :--- | :--- |
| **Switch Lanes** | `A` / `D` or `Left` / `Right` Arrow Keys |
| **Jump Obstacles** | `Spacebar` |

---

## 🚀 Quick Setup & Installation

Open your terminal in VS Code (`Ctrl + ~`) and run the following PowerShell commands:

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade packaging tools and install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Launch the game
python main.py
📦 Building a Portable Standalone Executable
To compile Chronopulse into a standalone Windows executable (.exe) that can run on any machine without installing Python:

PowerShell
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
Once complete, your single portable executable will be waiting inside the newly created dist/ folder!