import os
import pygame

from .settings import ASSETS_DIR

MUSIC_FILE = "Rydeen.mp3"  #music of choice

def init_audio() -> None:
    """
    Initializes the pygame mixer module.
    This must be called before playing any sounds or music.
    """
    pygame.mixer.init()


def play_music(loop: bool = True) -> None:
    """
    Loads and plays background music.
    If loop=True, the music will repeat indefinitely.
    """
    path = os.path.join(ASSETS_DIR, MUSIC_FILE)

    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)  # 50% volume
        pygame.mixer.music.play(-1 if loop else 0)


def stop_music() -> None:
    """
    Stops the currently playing music.
    """
    pygame.mixer.music.stop()