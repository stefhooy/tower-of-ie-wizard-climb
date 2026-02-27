# 🧙‍♂️ Tower of IE: The Wizard Climb

<p align="center">
  <b>A 2D fantasy vertical platformer built with Python & Pygame</b><br>
  Designed with modular object-oriented architecture and clean package structure.
</p>

---

## 🎮 Game Overview

**Tower of IE: The Wizard Climb** is a 2D vertical platformer where the player controls a wizard climbing a magical tower by jumping across platforms while the camera follows dynamically.

The objective is simple:

> Reach the glowing flag at the top in the fastest possible time without falling.

The game features real-time physics, collision detection, dynamic platform creation (editor mode), persistent score tracking, and looping background music for a more immersive experience.

---

## 🏗 Architecture

The project was initially developed as a single script and later refactored into a modular package structure to improve readability, maintainability, and scalability.

### Core Components

**Player**
Handles movement, gravity, velocity, jumping mechanics, sprite rendering, and collision detection.

**Platform**
Represents static surfaces that the player can land on.

**Camera**
Manages vertical scrolling and transforms world coordinates into screen coordinates.

**GameApp**
Controls the main loop, state transitions (menu, name input, scoreboard, gameplay), and rendering pipeline.

**Score System**
Stores completion times in a JSON file and ranks players by fastest time.

**Audio System (`audio.py`)**
Initializes `pygame.mixer` and plays looping background music from the `assets/` folder.

---

## 📂 Project Structure

```text id="n93krv"
tower-of-ie-wizard-climb/
│
├── assets/                 # Backgrounds, sprites, fonts, music, scores.json
│
├── game/                   # Main package
│   ├── __init__.py
│   ├── settings.py
│   ├── utils.py
│   ├── scores.py
│   ├── effects.py
│   ├── audio.py
│   ├── camera.py
│   ├── platform.py
│   ├── player.py
│   ├── screens.py
│   └── app.py
│
├── main.py                 # Entry point
├── pyproject.toml
└── README.md
```

The modular design ensures separation of concerns and makes the project easy to extend with new features.

---

## ⚙️ Environment Setup (uv)

This project uses `uv` for dependency and virtual environment management.

Create the environment:

```bash id="o0yxaf"
uv venv
```

Install dependencies:

```bash id="z6r91f"
uv add pygame
```

Run the game:

```bash id="h0jv8k"
uv run python main.py
```

---

## 🧠 Technical Highlights

* Object-Oriented Programming in Python
* Modular package architecture
* Game loop design
* Physics simulation (gravity & velocity)
* Collision detection system
* Camera abstraction (world-to-screen transformation)
* JSON score persistence
* Background music integration using `pygame.mixer`
* Refactoring from monolithic script to scalable package

---

## 👨‍💻 Author

Stephan Pentchev
Master’s in Business Analytics and Data Science

Developed as part of a Python object-oriented programming coursework project.

---