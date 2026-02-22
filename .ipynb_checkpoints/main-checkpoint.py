"""
Main entry point for Tower of IE: The Wizard Climb.

This file is intentionally minimal. Its only responsibility
is to start the application with uv. All game logic is handled
inside the GameApp class (defined in game/app.py).
"""
#import the main application controller
from game.app import GameApp

def main() -> None:
    """
    Creates an instance of the GameApp class
    and starts the main execution loop.

    Separating this into a function makes the
    entry point explicit and keeps the script clean.
    """
    GameApp().run() #start the full game system and main loop

if __name__ == "__main__":
    main()