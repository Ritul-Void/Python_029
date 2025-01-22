import random
import os
import time

# ---------- Map Setup ----------
WIDTH = 20
HEIGHT = 10
CLEAR = 'cls' if os.name == 'nt' else 'clear'

def create_map():
    game_map = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1:
                row.append('#')
            else:
                row.append(' ')
        game_map.append(row)
    return game_map

# ---------- Entities ----------
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 50
        self.alive = True

    def move(self, dx, dy, game_map):
        nx, ny = self.x + dx, self.y + dy
        if game_map[ny][nx] != '#':
            self.x, self.y = nx, ny

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def move_toward(self, player, game_map):
        if not self.alive:
            return
        dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
        dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
        nx, ny = self.x + dx, self.y + dy
        if game_map[ny][nx] != '#':
            self.x, self.y = nx, ny

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.active = True

    def move(self, game_map):
        nx, ny = self.x + self.dx, self.y + self.dy
        if game_map[ny][nx] == '#':
            self.active = False
        else:
            self.x, self.y = nx, ny

# ---------- Display ----------
def draw(game_map, player, enemies, bullets):
    os.system(CLEAR)
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            char = game_map[y][x]
            if x == player.x and y == player.y:
                char = '@'
            for e in enemies:
                if e.alive and x == e.x and y == e.y:
                    char = 'Z'
            for b in bullets:
                if b.active and x == b.x and y == b.y:
                    char = '-'
            row += char
        print(row)
    print(f"HP: {player.hp} | Zombies remaining: {sum(e.alive for e in enemies)}")
    print("WASD = move | IJKL = shoot")

# ---------- Shooting ----------
def shoot(player, direction, bullets):
    dirs = {'i': (0, -1), 'k': (0, 1), 'j': (-1, 0), 'l': (1, 0)}
    if direction in dirs:
        dx, dy = dirs[direction]
        bullets.append(Bullet(player.x + dx, player.y + dy, dx, dy))

# ---------- Game ----------
def game():
    game_map = create_map()
    player = Player(2, 2)
    enemies = [Enemy(WIDTH - 3, HEIGHT - 3), Enemy(WIDTH - 3, 2), Enemy(2, HEIGHT - 3)]
    bullets = []

    while player.alive and any(e.alive for e in enemies):
        draw(game_map, player, enemies, bullets)
        move = input("Action: ").lower()

        # Movement
        dx = dy = 0
        if move == 'w': dy = -1
        elif move == 's': dy = 1
        elif move == 'a': dx = -1
        elif move == 'd': dx = 1
        player.move(dx, dy, game_map)

        # Shooting
        if move in ['i','j','k','l']:
            shoot(player, move, bullets)

        # Move bullets and check hits
        for _ in range(2):  # faster bullets
            for b in bullets:
                if not b.active:
                    continue
                b.move(game_map)
                for e in enemies:
                    if e.alive and b.x == e.x and b.y == e.y:
                        e.alive = False
                        b.active = False
            draw(game_map, player, enemies, bullets)
            time.sleep(0.03)
        bullets = [b for b in bullets if b.active]

        # Move zombies
        for e in enemies:
            if e.alive:
                e.move_toward(player, game_map)
                if e.x == player.x and e.y == player.y:
                    player.alive = False

    os.system(CLEAR)
    if player.alive:
        print("YOU SURVIVED! All zombies dead.")
    else:
        print("GAME OVER! You were eaten.")

if __name__ == "__main__":
    game()
