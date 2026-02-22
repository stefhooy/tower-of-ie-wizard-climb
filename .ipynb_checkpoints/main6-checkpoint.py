import os
import json
import math
import pygame
from typing import List, Tuple, Optional

# ----------------------------
# Settings
# ----------------------------
SCREEN_W, SCREEN_H = 1920, 1080
FPS = 60

ASSETS_DIR = "assets"

BACKGROUND_FILE = "background(5).png"  # game world background
MENU_BG_FILE = "menu_background(3).png"
SCOREBOARD_BG_FILE = "scoreboard_background(5).png"

CHAR_STILL_FILE = "character still.png"
CHAR_RUN_RIGHT_FILE = "character running right.png"
CHAR_RUN_LEFT_FILE = "character running left.png"

# Font
ARCADE_FONT_FILE = "ByteBounce.ttf"
SCORES_FILE = os.path.join(ASSETS_DIR, "scores.json")

# Physics size (same as your original yellow box)
PLAYER_W, PLAYER_H = 32, 48

# Sprite sizing:
SPRITE_TARGET_H = 100
FEET_OFFSET_Y = 10

# Editor defaults
DEFAULT_PLAT_W = 160
DEFAULT_PLAT_H = 16

GOAL_W, GOAL_H = 40, 60

# Platform visuals (brown)
PLATFORM_FILL = (140, 90, 45)
PLATFORM_OUTLINE = (90, 55, 25)

# Goal visuals
GOAL_RING_R = 14

# ----------------------------
# Helpers
# ----------------------------
def safe_load_image(path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
    if not os.path.exists(path):
        return None
    img = pygame.image.load(path)
    return img.convert_alpha() if convert_alpha else img.convert()


def scale_to_target_height(img: pygame.Surface, target_h: int) -> pygame.Surface:
    w, h = img.get_size()
    if h == 0:
        return img
    scale = target_h / h
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    return pygame.transform.smoothscale(img, (new_w, new_h))


def clamp(v, lo, hi):
    return max(lo, min(v, hi))


def load_scores() -> List[dict]:
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_scores(scores: List[dict]) -> None:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def add_score(player_name: str, time_seconds: float) -> None:
    scores = load_scores()
    scores.append({"name": player_name, "time": float(time_seconds)})
    scores.sort(key=lambda x: x["time"])
    scores = scores[:20]
    save_scores(scores)


def format_time(t: float) -> str:
    minutes = int(t // 60)
    seconds = t - minutes * 60
    return f"{minutes:02d}:{seconds:05.2f}"


def get_font(size: int) -> pygame.font.Font:
    """
    Tries to load an arcade TTF from assets, otherwise falls back to default font.
    """
    font_path = os.path.join(ASSETS_DIR, ARCADE_FONT_FILE)
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    return pygame.font.Font(None, size)


def draw_goal_glow(screen: pygame.Surface, pos: Tuple[int, int]):
    """
    Draw a pulsing glow around the goal circle using an alpha surface.
    """
    x, y = pos
    t = pygame.time.get_ticks() / 1000.0

    pulse = 0.5 + 0.5 * math.sin(t * 3.0)
    outer_r = int(34 + pulse * 10)
    inner_r = GOAL_RING_R

    glow_surf = pygame.Surface((outer_r * 2 + 2, outer_r * 2 + 2), pygame.SRCALPHA)
    cx, cy = outer_r + 1, outer_r + 1

    for r, a in [(outer_r, 30), (outer_r - 6, 55), (outer_r - 12, 80)]:
        if r > 0:
            pygame.draw.circle(glow_surf, (0, 255, 120, a), (cx, cy), r)

    screen.blit(glow_surf, (x - cx, y - cy))

    pygame.draw.circle(screen, (0, 255, 0), (x, y), inner_r, 3)
    pygame.draw.circle(screen, (200, 255, 220), (x, y), 3)


# ----------------------------
# Core Classes
# ----------------------------
class Camera:
    def __init__(self, screen_w: int, screen_h: int, world_w: int, world_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.world_w = world_w
        self.world_h = world_h
        self.offset_x = 0
        self.offset_y = 0

    def follow(self, target_x: float, target_y: float):
        desired_x = target_x - self.screen_w / 2
        desired_y = target_y - self.screen_h / 2
        self.offset_x = clamp(desired_x, 0, self.world_w - self.screen_w)
        self.offset_y = clamp(desired_y, 0, self.world_h - self.screen_h)

    def apply(self, world_x: float, world_y: float) -> Tuple[int, int]:
        return int(world_x - self.offset_x), int(world_y - self.offset_y)


class Platform:
    def __init__(self, x: int, y: int, w: int, h: int = 12):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen: pygame.Surface, camera: Camera):
        x, y = camera.apply(self.rect.x, self.rect.y)

        # Rounded platform look (collision stays rectangular)
        radius = max(2, self.rect.h // 2)
        pygame.draw.rect(
            screen,
            PLATFORM_FILL,
            pygame.Rect(x, y, self.rect.w, self.rect.h),
            border_radius=radius,
        )
        pygame.draw.rect(
            screen,
            PLATFORM_OUTLINE,
            pygame.Rect(x, y, self.rect.w, self.rect.h),
            2,
            border_radius=radius,
        )


class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PLAYER_W, PLAYER_H)

        # Physics
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 260.0
        self.jump_strength = 650.0
        self.gravity = 1400.0
        self.on_ground = False

        # Facing direction
        self.facing_right = True

        # Sprites
        still_path = os.path.join(ASSETS_DIR, CHAR_STILL_FILE)
        run_r_path = os.path.join(ASSETS_DIR, CHAR_RUN_RIGHT_FILE)
        run_l_path = os.path.join(ASSETS_DIR, CHAR_RUN_LEFT_FILE)

        still = safe_load_image(still_path, convert_alpha=True)
        run_r = safe_load_image(run_r_path, convert_alpha=True)
        run_l = safe_load_image(run_l_path, convert_alpha=True)

        if still is None or run_r is None or run_l is None:
            raise FileNotFoundError(
                "Missing one or more character sprites in assets. "
                "Check CHAR_STILL_FILE, CHAR_RUN_RIGHT_FILE, CHAR_RUN_LEFT_FILE."
            )

        self.sprite_idle = scale_to_target_height(still, SPRITE_TARGET_H)
        self.sprite_run_r = scale_to_target_height(run_r, SPRITE_TARGET_H)
        self.sprite_run_l = scale_to_target_height(run_l, SPRITE_TARGET_H)

    def reset(self, x: int, y: int):
        self.rect.topleft = (x, y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = True

    def handle_input(self, keys):
        self.vx = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.facing_right = True

    def try_jump(self, keys):
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

    def clamp_to_world_x(self, world_w: int):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > world_w:
            self.rect.right = world_w

    def _pick_sprite(self) -> pygame.Surface:
        moving = abs(self.vx) > 1e-3

        # If no movement, always idle (ground or air)
        if not moving:
            return self.sprite_idle

        if self.vx < -1e-3:
            return self.sprite_run_l
        if self.vx > 1e-3:
            return self.sprite_run_r

        return self.sprite_run_r if self.facing_right else self.sprite_run_l

    def draw(self, screen: pygame.Surface, camera: Camera):
        sprite = self._pick_sprite()
        sx, sy = camera.apply(self.rect.x, self.rect.y)

        sprite_rect = sprite.get_rect()
        sprite_rect.midbottom = (sx + self.rect.w // 2, sy + self.rect.h + FEET_OFFSET_Y)
        screen.blit(sprite, sprite_rect)

    def move_and_collide(self, dt: float, platforms: List[Platform]):
        self.vy += self.gravity * dt
        self.on_ground = False

        # X
        self.rect.x += int(self.vx * dt)
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                elif self.vx < 0:
                    self.rect.left = p.rect.right

        # Y
        self.rect.y += int(self.vy * dt)
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0.0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.rect.bottom
                    self.vy = 0.0


def load_background_world() -> pygame.Surface:
    path = os.path.join(ASSETS_DIR, BACKGROUND_FILE)
    img = safe_load_image(path, convert_alpha=False)
    if img is None:
        raise FileNotFoundError(f"Background not found at: {path}")
    return img


# ----------------------------
# UI Screens
# ----------------------------
STATE_MENU = "menu"
STATE_NAME = "name"
STATE_SCOREBOARD = "scoreboard"
STATE_GAME = "game"


def draw_center_text(screen, font, text, y, color=(0, 0, 0)):
    surf = font.render(text, True, color)
    x = (screen.get_width() - surf.get_width()) // 2
    screen.blit(surf, (x, y))


def run_menu(screen, clock) -> str:
    menu_bg = safe_load_image(os.path.join(ASSETS_DIR, MENU_BG_FILE), convert_alpha=False)

    font_title = get_font(96)
    font_body = get_font(40)

    TITLE_Y = 120
    LINE1_Y = 260
    LINE2_Y = 310
    OPT1_Y = 470
    OPT2_Y = 530
    OPT3_Y = 590

    while True:
        _ = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return STATE_NAME
                if event.key == pygame.K_s:
                    return STATE_SCOREBOARD
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        if menu_bg:
            screen.blit(menu_bg, (0, 0))
        else:
            screen.fill((10, 10, 25))

        draw_center_text(screen, font_title, "TOWER OF IE: THE WIZARD CLIMB", TITLE_Y)
        draw_center_text(
            screen,
            font_body,
            "Welcome, sorcerer student of IE. Conjure platforms to climb the tower.",
            LINE1_Y,
        )
        draw_center_text(
            screen,
            font_body,
            "Reach the flag at the top and prove your mastery with the fastest time!",
            LINE2_Y,
        )

        draw_center_text(screen, font_body, "PRESS ENTER TO START", OPT1_Y, (255, 255, 255))
        draw_center_text(screen, font_body, "PRESS S FOR SCOREBOARD", OPT2_Y, (255, 255, 255))
        draw_center_text(screen, font_body, "PRESS ESC TO QUIT", OPT3_Y, (255, 255, 255))

        pygame.display.flip()


def run_name_input(screen, clock) -> Optional[str]:
    menu_bg = safe_load_image(os.path.join(ASSETS_DIR, MENU_BG_FILE), convert_alpha=False)
    font_title = get_font(72)
    font_body = get_font(44)

    name = ""

    while True:
        _ = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_RETURN:
                    cleaned = name.strip()
                    if cleaned:
                        return cleaned
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if event.unicode and len(event.unicode) == 1:
                        if event.unicode.isprintable() and len(name) < 16:
                            name += event.unicode

        if menu_bg:
            screen.blit(menu_bg, (0, 0))
        else:
            screen.fill((10, 10, 25))

        draw_center_text(screen, font_title, "ENTER YOUR NAME", 200, (0, 0, 0))
        draw_center_text(screen, font_body, "TYPE THEN PRESS ENTER", 290, (0, 0, 0))

        box_w, box_h = 700, 80
        box_x = (SCREEN_W - box_w) // 2
        box_y = 420
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(box_x, box_y, box_w, box_h), 2)

        name_surf = font_body.render(name, True, (255, 255, 255))
        screen.blit(name_surf, (box_x + 18, box_y + 18))

        draw_center_text(screen, font_body, "ESC TO GO BACK", 540, (255, 255, 255))
        pygame.display.flip()


def run_scoreboard(screen, clock) -> str:
    sb_bg = safe_load_image(os.path.join(ASSETS_DIR, SCOREBOARD_BG_FILE), convert_alpha=False)
    font_title = get_font(90)
    font_body = get_font(44)

    while True:
        _ = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return STATE_MENU

        if sb_bg:
            screen.blit(sb_bg, (0, 0))
        else:
            screen.fill((10, 10, 25))

        draw_center_text(screen, font_title, "SCOREBOARD", 90)

        scores = load_scores()
        if not scores:
            draw_center_text(screen, font_body, "NO SCORES YET. BE THE FIRST.", 240)
        else:
            start_y = 220
            line_h = 52
            for i, s in enumerate(scores[:10], start=1):
                line = f"{i:02d}. {s['name']}  {format_time(s['time'])}"
                draw_center_text(screen, font_body, line, start_y + (i - 1) * line_h)

        draw_center_text(screen, font_body, "PRESS ENTER OR ESC TO RETURN", 950, (255, 255, 0))
        pygame.display.flip()


# ----------------------------
# Main Game Loop
# ----------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("TOWER OF IE: THE WIZARD CLIMB")
    clock = pygame.time.Clock()

    font_hud = get_font(42)
    font_editor = get_font(32)

    background = load_background_world()
    world_w, world_h = background.get_width(), background.get_height()
    camera = Camera(SCREEN_W, SCREEN_H, world_w, world_h)

    # Fresh run defaults (NO level file)
    platforms: List[Platform] = [Platform(0, world_h - 40, world_w, 40)]

    goal_rect = pygame.Rect(world_w // 2, 120, GOAL_W, GOAL_H)
    spawn_x, spawn_y = 80, world_h - 140

    # Editor state
    editor_mode = False
    plat_w = DEFAULT_PLAT_W
    plat_h = DEFAULT_PLAT_H

    # Game state
    state = STATE_MENU
    player_name = "Unknown"
    win = False

    # Timer
    run_start_ms: Optional[int] = None
    final_time_s: Optional[float] = None

    player = Player(spawn_x, spawn_y)

    def reset_run(clear_platforms: bool):
        nonlocal win, run_start_ms, final_time_s, platforms
        win = False
        run_start_ms = pygame.time.get_ticks()
        final_time_s = None
        player.reset(spawn_x, spawn_y)

        if clear_platforms:
            platforms = [Platform(0, world_h - 40, world_w, 40)]

    while True:
        if state == STATE_MENU:
            next_state = run_menu(screen, clock)
            if next_state == "quit":
                break
            state = next_state

        elif state == STATE_NAME:
            name = run_name_input(screen, clock)
            if name is None:
                state = STATE_MENU
            else:
                player_name = name
                reset_run(clear_platforms=True)
                state = STATE_GAME

        elif state == STATE_SCOREBOARD:
            next_state = run_scoreboard(screen, clock)
            if next_state == "quit":
                break
            state = next_state

        elif state == STATE_GAME:
            dt = clock.tick(FPS) / 1000.0

            if run_start_ms is None:
                run_start_ms = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    # R = restart AND clear platforms
                    if event.key == pygame.K_r:
                        reset_run(clear_platforms=True)

                    # ESC = back to menu
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                    # Toggle editor
                    if event.key == pygame.K_e:
                        editor_mode = not editor_mode

                    if editor_mode:
                        # Width controls
                        if event.key == pygame.K_LEFTBRACKET:
                            plat_w = max(40, plat_w - 20)
                        if event.key == pygame.K_RIGHTBRACKET:
                            plat_w = min(600, plat_w + 20)

                        # Height controls
                        if event.key == pygame.K_MINUS:
                            plat_h = max(8, plat_h - 4)
                        if event.key == pygame.K_EQUALS:  # "+" usually is shift + "="
                            plat_h = min(80, plat_h + 4)

                if event.type == pygame.MOUSEBUTTONDOWN and editor_mode:
                    mx, my = pygame.mouse.get_pos()
                    wx = mx + camera.offset_x
                    wy = my + camera.offset_y

                    if event.button == 1:
                        x = int(wx - plat_w / 2)
                        y = int(wy - plat_h / 2)
                        platforms.append(Platform(x, y, plat_w, plat_h))

                    if event.button == 3 and len(platforms) > 1:
                        def dist2(p: Platform):
                            cx, cy = p.rect.center
                            return (cx - wx) ** 2 + (cy - wy) ** 2

                        nearest = min(platforms[1:], key=dist2)  # avoid deleting base floor
                        platforms.remove(nearest)

            keys = pygame.key.get_pressed()

            if not editor_mode and not win:
                player.handle_input(keys)
                player.try_jump(keys)
                player.move_and_collide(dt, platforms)
                player.clamp_to_world_x(world_w)

                if player.rect.colliderect(goal_rect):
                    win = True
                    player.vx = 0.0
                    player.vy = 0.0

                    if run_start_ms is not None and final_time_s is None:
                        elapsed_ms = pygame.time.get_ticks() - run_start_ms
                        final_time_s = elapsed_ms / 1000.0
                        add_score(player_name, final_time_s)
            else:
                player.vx = 0.0
                player.vy = 0.0

            if player.rect.top > world_h + 400:
                reset_run(clear_platforms=False)

            camera.follow(player.rect.centerx, player.rect.centery)

            # Draw world
            screen.blit(background, (-camera.offset_x, -camera.offset_y))

            # Spawn marker (fixed)
            sx, sy = camera.apply(spawn_x, spawn_y)
            pygame.draw.circle(screen, (255, 165, 0), (sx, sy), 6)

            # Goal marker (magical glow)
            gx, gy = camera.apply(goal_rect.centerx, goal_rect.centery)
            draw_goal_glow(screen, (gx, gy))

            # Editor overlay
            if editor_mode:
                mx, my = pygame.mouse.get_pos()
                wx = mx + camera.offset_x
                wy = my + camera.offset_y

                ghost_x = int(wx - plat_w / 2)
                ghost_y = int(wy - plat_h / 2)
                gx2, gy2 = camera.apply(ghost_x, ghost_y)
                ghost_rect = pygame.Rect(gx2, gy2, plat_w, plat_h)

                ghost_r = max(2, plat_h // 2)
                pygame.draw.rect(screen, (150, 200, 255), ghost_rect, 2, border_radius=ghost_r)

                hud = font_editor.render(
                    "EDITOR ON | [ ] width | -/+ height | LMB add | RMB remove | E toggle | R restart",
                    True,
                    (0, 0, 0),
                )
                screen.blit(hud, (20, 20))

            for p in platforms:
                p.draw(screen, camera)

            player.draw(screen, camera)

            # HUD: name + timer
            if run_start_ms is not None and final_time_s is None:
                elapsed_s = (pygame.time.get_ticks() - run_start_ms) / 1000.0
                timer_text = format_time(elapsed_s)
            elif final_time_s is not None:
                timer_text = format_time(final_time_s)
            else:
                timer_text = "00:00.00"

            hud_name = font_hud.render(f"PLAYER: {player_name}", True, (0, 0, 0))
            hud_time = font_hud.render(f"TIME: {timer_text}", True, (0, 0, 0))
            screen.blit(hud_name, (20, 70))
            screen.blit(hud_time, (20, 120))

            # Win overlay
            if win and final_time_s is not None:
                big = get_font(84)
                small = get_font(44)

                msg1 = big.render("YOU REACHED THE FLAG!", True, (255, 255, 255))
                msg2 = small.render(f"YOUR TIME: {format_time(final_time_s)}", True, (255, 255, 255))
                msg3 = small.render("R RESTART (CLEARS PLATFORMS) | ESC MENU | S SCOREBOARD", True, (255, 255, 255))

                box_w = max(msg1.get_width(), msg2.get_width(), msg3.get_width()) + 80
                box_h = msg1.get_height() + msg2.get_height() + msg3.get_height() + 80
                box_x = (SCREEN_W - box_w) // 2
                box_y = (SCREEN_H - box_h) // 2

                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(box_x, box_y, box_w, box_h))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(box_x, box_y, box_w, box_h), 2)

                screen.blit(msg1, (box_x + 40, box_y + 25))
                screen.blit(msg2, (box_x + 40, box_y + 25 + msg1.get_height() + 15))
                screen.blit(msg3, (box_x + 40, box_y + 25 + msg1.get_height() + msg2.get_height() + 30))

                if pygame.key.get_pressed()[pygame.K_s]:
                    state = STATE_SCOREBOARD

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()