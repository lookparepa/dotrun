import arcade
from models import World
import pyglet.gl as gl

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()
        

class DotRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.GRAY)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.dot_sprite = ModelSprite('images/dot.png',
                                      model=self.world.dot)

        self.coin_texture = arcade.load_texture('images/coin.png')

        
    def animate(self, delta):
        self.world.animate(delta)


    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_rectangle_filled(p.x + p.width // 2,
                                         p.y - p.height // 2,
                                         p.width, p.height,
                                         arcade.color.WHITE)
        
    def draw_coins(self, coins):
        for c in coins:
            if not c.is_collected:
                arcade.draw_texture_rectangle(c.x, c.y, c.width, c.height,
                                              self.coin_texture)
        

    def on_draw(self):
        arcade.set_viewport(self.world.dot.x - SCREEN_WIDTH // 2,
                            self.world.dot.x + SCREEN_WIDTH // 2,
                            0, SCREEN_HEIGHT)

        arcade.start_render()
        self.draw_platforms(self.world.platforms)
        self.draw_coins(self.world.coins)

        self.dot_sprite.draw()
        gl.glDisable(gl.GL_TEXTURE_2D)

        arcade.draw_text(str(self.world.score),
                         self.world.dot.x + (SCREEN_WIDTH // 2) - 60,
                         self.height - 30,
                         arcade.color.WHITE, 20)
        

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

 
if __name__ == '__main__':
    window = DotRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
