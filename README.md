# 🌌 Tower of Hanoi Solver

A high-performance, visually stunning, and highly modular **Tower of Hanoi Visualization and Solver Engine** built using Python and `CustomTkinter`. This application breaks down the classical recursive algorithm into a sleek, neon-themed desktop client featuring live multi-threaded queue operations and dynamic user controls.

---

## 🚀 Key Features

* **Asynchronous Move Queue System:** Decoupled calculation engine that queues recursive decisions and processes them through an independent clock loop, preventing UI freezing.
* **Dynamic Animation Control:** Features real-time speed adaptation (adjustable between 100ms and 2000ms delay cycles).
* **Live Metrics Status Bar:** Real-time analytics tracking mathematically calculated optimal bounds ($2^n - 1$) and countdowns for pending moves.
* **Flawless Geometry Engine:** Pixel-perfect rounded capsule rendering on canvas with absolute edge-alignment lock blocks to eliminate render drift gaps.
* **Fully Standalone Deployment:** Packaged native desktop executable setup ready for direct execution without external interpreter dependencies.

---

## 🛠️ System Architecture (Modular Pattern)

The project completely decouples UI rendering from backend logical execution across 4 atomic modules:

1.  **`config.py`** — The global environmental constants room handling coordinate mappings (`PEG_CENTERS`), window dimensions, and color pallets.
2.  **`logic.py`** — The mathematical brain containing core in-memory dictionaries representing the state arrays and the pure recursive engine (`hanoi_algo`).
3.  **`ui_components.py`** — Separated GUI layout constructor for the dashboard controller framing, sliders binding wrappers, and callback distributions.
4.  **`main.py`** — The orchestrator initiating the canvas layouts, vector rendering updates, and structural callback integrations.

---

## 💻 Tech Stack & Dependencies

* **Language:** Python 3.13+
* **GUI Framework:** CustomTkinter (Modernized Tkinter extension)
* **Packaging Framework:** PyInstaller (Binary Compilation System)

---

## ⚙️ Local Installation & Running from Source

If you prefer to review or run the codebase locally from the interpreter, follow these configurations:

1. Clone this repository to your local environment:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd Tower-Of-Hanoi-Solver
