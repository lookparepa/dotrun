import arcade.key
from random import randint

GRAVITY = -1
MAX_VX = 10
ACCX = 1
JUMP_VY = 15

DOT_RADIUS = 40
PLATFORM_MARGIN = 5

COIN_RADIUS = 32
COIN_Y_OFFSET = 20
COIN_MARGIN = 12
COIN_HIT_MARGIN = 12

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

        
class Dot(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
        self.is_jump = False

        self.platform = None
        
    def jump(self):
        if not self.platform:
            return
        
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY
        
    def animate(self, delta):
        if self.vx < MAX_VX:
            self.vx += ACCX

        self.x += self.vx

        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0
            
    def bottom_y(self):
        return self.y - (DOT_RADIUS // 2)
                
    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + (DOT_RADIUS // 2)

        
    def is_on_platform(self, platform, margin=PLATFORM_MARGIN):
        if not platform.in_top_range(self.x):
            return False
        
        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    
    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False
        
        if self.bottom_y() - self.vy > platform.y > self.bottom_y():
            return True
        
        return False
        

    def find_touching_platform(self):
        platforms = self.world.platforms
        for p in platforms:
            if self.is_falling_on_platform(p):
                return p
        return None

class Coin:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_collected = False

    def hit(self, dot):
        return ((abs(self.x - dot.x) < COIN_HIT_MARGIN) and
                (abs(self.y - dot.y) < COIN_HIT_MARGIN))
    
    
class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_top_range(self, x):
        return self.x <= x <= self.x + self.width

    def right_most_x(self):
        return self.x + self.width

    def spawn_coins(self):
        coins = []
        x = self.x + COIN_MARGIN
        while x + COIN_MARGIN <= self.right_most_x():
            coins.append(Coin(x, self.y + COIN_Y_OFFSET,
                              COIN_RADIUS, COIN_RADIUS))
            x += COIN_MARGIN + COIN_RADIUS
        return coins

    
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.dot = Dot(self, 0, 120)
        self.init_platforms()
        
        self.dot.set_platform(self.platforms[0])

        self.score = 0

    def init_platforms(self):
        self.platforms = [
            Platform(self, 0, 100, 500, 50),
            Platform(self, 550, 150, 500, 50),
            Platform(self, 1100, 100, 500, 50),
        ]
        self.coins = []
        for p in self.platforms:
            self.coins += p.spawn_coins()        

    def animate(self, delta):
        self.dot.animate(delta)
        self.recycle_platform()
        self.collect_coins()
        self.remove_old_coins()

        
    def collect_coins(self):
        for c in self.coins:
            if (not c.is_collected) and (c.hit(self.dot)):
                c.is_collected = True
                self.score += 1

                
    def too_far_left_x(self):
        return self.dot.x - self.width


    def remove_old_coins(self):
        far_x = self.too_far_left_x()
        if self.coins[0].x >= far_x:
            return
        self.coins = [c for c in self.coins if c.x >= far_x]

            
    def recycle_platform(self):
        far_x = self.too_far_left_x()
        for p in self.platforms:
            if p.right_most_x() < far_x:
                last_x = max([pp.right_most_x() for pp in self.platforms])
                p.x = last_x + randint(50,200)
                p.y = randint(100,200)
                self.coins += p.spawn_coins()


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.dot.jump()
