---

# Tower of IE: The Wizard Climb

**Tower of IE: The Wizard Climb** is a 2D vertical platformer built with **Python** and **Pygame**.

In this game, the player controls a wizard climbing a magical tower by jumping across platforms while the camera follows vertically. The objective is to reach the flag at the top in the fastest possible time without falling.

The game also includes background music integrated through Pygame’s audio system to enhance immersion.

This project focuses on clean architecture, modular design, and object-oriented programming principles.

---

## Project Architecture

The game was originally developed as a single script and later refactored into a modular package structure for better readability, scalability, and maintainability.

### Core Components

**Player**
Handles movement, gravity, velocity, jumping mechanics, and collision detection.

**Platform**
Represents static surfaces the player can land on.

**Camera**
Manages vertical scrolling and transforms world coordinates into screen coordinates.

**GameApp**
Controls the main loop, state transitions (menu, name input, scoreboard, gameplay), and rendering pipeline.

**Score System**
Uses JSON persistence to store and rank completion times.

**Audio System**
Implemented in `audio.py`, responsible for initializing `pygame.mixer` and playing looping background music from the `assets/` folder.

---

## Project Structure

```text
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
│   ├── audio.py            # Background music management
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

This structure separates concerns clearly and makes the project easier to extend in the future. For example, new features such as additional sound effects or gameplay mechanics can be added without modifying unrelated modules.

---

## Environment Management (uv)

This project uses `uv` for dependency and virtual environment management.

Create environment:

```bash
uv venv
```

Install dependencies:

```bash
uv add pygame
```

Run the game:

```bash
uv run python main.py
```

---

## Technical Focus

This project demonstrates:

* Object-Oriented Programming in Python
* Modular package architecture
* Game loop design
* Physics simulation (gravity and velocity systems)
* Collision detection handling
* Camera offset and world-to-screen transformations
* JSON-based score persistence
* Background music integration using `pygame.mixer`
* Refactoring from monolithic script to structured package

---

## Author

Stephan Pentchev
Master’s in Business Analytics and Data Science

Developed as part of Python for Data Analysis II coursework project.

---