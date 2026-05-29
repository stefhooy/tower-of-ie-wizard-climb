# Tower of IE: The Wizard Climb

<p align="center">
  <b>A 2D fantasy vertical platformer built with Python & Pygame — playable in the browser</b><br>
  Deployed on itch.io via WebAssembly (Pygbag)
</p>

---

## Play Online

**[Play on itch.io](https://stefhooy.itch.io/tower-of-ie-the-wizard-climb)**

No installation required. Runs directly in your browser.

> For the best display, use your browser's zoom (Ctrl + / Ctrl -) until the game fills your screen.

---

## Game Overview

**Tower of IE: The Wizard Climb** is a 2D vertical platformer where you play as a sorcerer student at IE University. Conjure platforms to climb the tower and reach the flag at the top as fast as possible!

The game features real-time physics, collision detection, dynamic platform creation (editor mode), persistent score tracking, and looping background music.

---

## How to Play

| Key | Action |
|-----|--------|
| Arrow keys / WASD | Move and jump |
| E | Toggle editor mode |
| [ / ] | Decrease / increase platform width (editor) |
| - / + (numpad) | Decrease / increase platform height (editor) |
| Left click | Place platform (editor) |
| Right click | Remove nearest platform (editor) |
| R | Restart run (clears platforms) |
| S | View scoreboard (after finishing) |
| ESC | Return to menu |

---

## Architecture

### Core Components

**Player** — Movement, gravity, velocity, jumping, sprite rendering, collision detection.

**Platform** — Static surfaces the player can land on; created/removed in editor mode.

**Camera** — Dynamic vertical scrolling; transforms world coordinates to screen coordinates.

**GameApp** — Main loop, state machine (splash → menu → name input → game → scoreboard), rendering pipeline.

**Score System** — Stores completion times in a JSON file, ranked by fastest time.

**Audio System** — Uses the browser’s native `HTMLAudioElement` on web (bypasses SDL to avoid Chrome stuttering) and `pygame.mixer` on desktop.

---

## Project Structure

```text
tower-of-ie-wizard-climb/
│
├── assets/                          # Game assets
│   ├── background.png               # Main gameplay background (defines world size)
│   ├── first_screen.jpg             # Splash screen image
│   ├── menu_background.png          # Menu screen background
│   ├── scoreboard_background.png    # Scoreboard screen background
│   ├── character still.png          # Player idle sprite
│   ├── character running right.png  # Player run-right sprite
│   ├── character running left.png   # Player run-left sprite
│   ├── ByteBounce.ttf               # Arcade font
│   ├── Rydeen.ogg                   # Background music (OGG for web compatibility)
│   └── scores.json                  # Local scoreboard (top 10 best times)
│
├── game/                            # Main game package
│   ├── __init__.py
│   ├── settings.py                  # Constants: resolution, FPS, file paths, game states
│   ├── utils.py                     # Helpers: image loading, font, text drawing, time format
│   ├── scores.py                    # Load/save scoreboard from scores.json
│   ├── effects.py                   # Visual effects (goal glow)
│   ├── audio.py                     # Audio system: native JS Audio on web, pygame.mixer on desktop
│   ├── camera.py                    # World-to-screen coordinate transform + scrolling
│   ├── platform.py                  # Platform rendering and collision rect
│   ├── player.py                    # Physics, input, sprite animation, collision detection
│   ├── screens.py                   # Splash, menu, name input, scoreboard screens
│   └── app.py                       # GameApp: state machine, main loop, rendering pipeline
│
├── build/web/                       # Pygbag web build output (generated — do not edit)
│   ├── index.html                   # Auto-generated HTML/WASM wrapper
│   ├── video_game_2.apk             # Game files packaged for itch.io
│   ├── video_game_2.tar.gz          # Game files packaged for local dev server
│   ├── Rydeen.ogg                   # Copied here post-build so JS Audio API can load it
│   └── browserfs.min.js             # Virtual filesystem for the browser
│
├── main.py                          # Entry point (asyncio.run for Pygbag compatibility)
├── pygbag.ini                       # Pygbag build config and ignore list
├── pyproject.toml                   # Project metadata and dependencies
└── README.md
```

---

## Web Build

The game is compiled to WebAssembly using [Pygbag](https://pygame-web.github.io/) 0.9.3.

### Build command

```bash
python -m pygbag --build main.py
```

This regenerates `build/web/index.html`, `build/web/video_game_2.apk`, and `build/web/video_game_2.tar.gz`.

### Package for itch.io upload

```powershell
# Copy the audio file so the browser can load it (it lives outside the .apk bundle)
Copy-Item "assets\Rydeen.ogg" "build\web\Rydeen.ogg" -Force

# Zip everything in build/web/
Compress-Archive -Path "build\web\*" -DestinationPath "tower-of-ie-web.zip" -Force
```

Upload `tower-of-ie-web.zip` to itch.io.

---

## Technical Highlights

- Object-Oriented Python with modular package architecture
- Game loop design with async/await for browser compatibility
- Physics simulation (gravity, velocity, delta-time movement)
- Collision detection system
- Camera abstraction (world-to-screen transformation)
- JSON score persistence
- Cross-platform audio: `HTMLAudioElement` on web, `pygame.mixer` on desktop
- WebAssembly deployment via Pygbag

---

## Author

Stephan Pentchev
Master's in Business Analytics and Data Science IE University

Developed as part of a Python object-oriented programming coursework project.