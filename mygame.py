import random
import arcade


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Air Planes"
SPRITE_SCALING_PLAYER = 0.8
ENEMY_COUNT = 3
SPRITE_SPEED = 3
PLAYER_SPEED = 9
BULLET_SPEED = 12
EXPLOSION_TEXTURE_COUNT = 60
NO_OF_LIVES = 5


class Enemy(arcade.Sprite):

    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT - 20, SCREEN_HEIGHT + 120)
        self.center_x = random.randrange(SCREEN_WIDTH)
    
    def update(self):
        self.center_y -= 3   


class Explosion(arcade.Sprite):
    
    def __init__(self, texture_list):
        super().__init__()

        self.current_texture = 0
        self.textures = texture_list

    def update(self):
    
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(SCREEN_WIDTH , SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        self.explosion_texture_list = []
        self.player_list = None
        self.enemy_list = None
        self.explosions_list = None
        self.player_sprite = None
        self.enemy_sprite = None
        self.score = 0
        self.lives = 0

        self.hit_sound = arcade.load_sound("boom.wav")
        self.gun_sound = arcade.load_sound("shoot.wav")

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = "explosion.png"

        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("ship.png", 1) 
        self.score = 0
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite) 

        self.bullet_list = arcade.SpriteList()

        self.explosions_list = arcade.SpriteList()

        self.is_pause = True
        self.lives = NO_OF_LIVES
        self.is_Game_Over = False

        for i in range(ENEMY_COUNT):
            enemy = Enemy("enemy_ship.png", SPRITE_SCALING_PLAYER)
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = 600
            self.enemy_list.append(enemy)

    def on_draw(self):

        arcade.start_render()
        if not self.is_Game_Over :
            self.enemy_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
            self.explosions_list.draw()

        score_output = f"SCORE : {self.score}"
        life_output = f"LIVES : {self.lives}"

        arcade.draw_text(score_output, 10, 20, arcade.color.AMAZON, 14)
        arcade.draw_text(life_output, 10, SCREEN_HEIGHT - 20 , arcade.color.ANTIQUE_BRONZE, 14)

        if self.is_pause and not self.is_Game_Over :
            arcade.draw_text("GAME IS PAUSED. PRESS P TO START", SCREEN_WIDTH/2 - 300, SCREEN_HEIGHT/2 + 30, arcade.color.ALABAMA_CRIMSON, 25)

        if self.is_Game_Over :
            arcade.draw_text(score_output, SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 30, arcade.color.AMAZON, 30)
            arcade.draw_text("GAME OVER. PRESS ENTER TO RESTART", SCREEN_WIDTH/2 - 320, SCREEN_HEIGHT/2 + 30, arcade.color.ALABAMA_CRIMSON, 25)                                                                                     

    def on_update(self, delta_time):

        if self.lives <= 0 :
            self.is_pause = True 
            self.is_Game_Over = True
            
        if not self.is_pause :
            self.enemy_list.update()
            self.player_list.update()
            self.bullet_list.update()
            self.explosions_list.update()

        if self.player_sprite.center_x < 0 :
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH :
            self.player_sprite.center_x = 0

        if self.player_sprite.center_y < 0 :
            self.player_sprite.center_y = SCREEN_HEIGHT
        elif self.player_sprite.center_y > SCREEN_HEIGHT :
            self.player_sprite.center_y = 0

        for bullet in self.bullet_list :

            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(hit_list) > 0 : 

                explosion = Explosion(self.explosion_texture_list) 
                explosion.center_x = hit_list[0].center_x 
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                self.explosions_list.append(explosion)
                arcade.play_sound(self.hit_sound)
                bullet.remove_from_sprite_lists()
                self.score += 1

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()
            
            for enemy in hit_list :
                enemy.reset_pos()
                hit_list.remove(enemy)

        for enemy in self.enemy_list :
            if enemy.top < 0:
                self.lives -= 1
                enemy.reset_pos()
          
    def on_key_press(self, key, key_modifiers):
        
        if key == arcade.key.UP :
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN :
            self.player_sprite.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT :
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT :
            self.player_sprite.change_x = PLAYER_SPEED

        if key == arcade.key.SPACE and not self.is_pause :
            bullet = arcade.Sprite("12.png", 0.25)
            bullet.angle = 90
            bullet.change_y = BULLET_SPEED
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top 
            self.bullet_list.append(bullet)
            arcade.play_sound(self.gun_sound) 
        
        if key == arcade.key.P : 
            self.is_pause = not self.is_pause

        if self.is_Game_Over :
            if key == arcade.key.ENTER :
                self.setup()
    
    def on_key_release(self, key, key_modifiers):
        
        if key == arcade.key.UP or key == arcade.key.DOWN :
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT :
            self.player_sprite.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

