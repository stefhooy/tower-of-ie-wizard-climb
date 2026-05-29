import os
import pygame

from .settings import ASSETS_DIR

MUSIC_FILE = "Rydeen.ogg"

# Global flag so the rest of the game knows whether audio is available
AUDIO_ENABLED = False


def init_audio() -> None:
    """
    Tries to initialize pygame mixer.
    If audio fails, the game continues without music instead of crashing.
    """
    global AUDIO_ENABLED

    try:
        # 44100 Hz matches Chrome's preferred Web Audio sample rate,
        # avoiding the resampling artifacts that cause glitchy playback.
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        AUDIO_ENABLED = True
    except pygame.error as e:
        print(f"[Audio disabled] Could not initialize mixer: {e}")
        AUDIO_ENABLED = False


def play_music(loop: bool = True) -> None:
    """
    Loads and plays background music if audio is available.
    """
    if not AUDIO_ENABLED:
        return

    path = os.path.join(ASSETS_DIR, MUSIC_FILE)

    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1 if loop else 0)
        except pygame.error as e:
            print(f"[Audio disabled] Could not play music: {e}")


def stop_music() -> None:
    """
    Stops currently playing music if audio is enabled.
    """
    if AUDIO_ENABLED:
        pygame.mixer.music.fadeout(300)