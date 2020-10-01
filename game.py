import cocos
from cocos.director import director
import pyglet
from pyglet.window import key
from cocos.actions import *
import cocos.collision_model as cm
import cocos.euclid as eu


#Action
class Move(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        self.vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 500
        self.vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) * 500
        self.target.velocity = (self.vel_x , self.vel_y)
        scroller.set_focus(self.target.x, self.target.y)

#Ship(Xwing)
class Ship(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('sprites/xwing.png')
        self.scale = 0.17
        self.position = 50, 50
        self.velocity = (0, 0)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)
        self.do(Move())

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)
    


class Enemy_ship_one(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('sprites/shipspace.png')
        self.scale = 0.2
        self.position = 100, 100
        self.velocity = (300, 300)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), self.width)
        self.do(Repeat(MoveTo((900, 400), 2) + MoveTo((900, 700), 2) + MoveTo((900, 100), 1) + RotateBy(360, 1)))

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)



class Enemy_ship_two(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('sprites/enemy_ship2.png')
        self.scale = 0.2
        self.position = 1200, 900
        self.velocity = (300, 300)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)
        self.do(Repeat(MoveTo((600, 400), 2) + MoveTo((1200, 900), 2) + MoveTo((600, 100), 1)))

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)


#Laser from Xwing
class Laser(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('sprites/laser2.png')
        self.scale = 0.1
        self.velocity = (30, 30)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2) 

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)


#Background space
class Space(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('Background/space3.jpg')



class BackgroundLayer(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
         
        #Load the explosion image 
        boom = pyglet.image.load('sprites/explosion2.png')

        #Animation
        img_grid = pyglet.image.ImageGrid(boom, 6, 8, item_width=256, item_height=256)
        self.anim = pyglet.image.Animation.from_image_sequence(img_grid[9:], 0.2, loop=False)

        #Sprites
        self.laser = Laser()
        self.space = Space()
        self.ship = Ship()
        self.enemy_ship_one = Enemy_ship_one()
        self.enemy_ship_two = Enemy_ship_two()

        #Space/universe position
        self.space.position = self.space.width // 2, self.space.height // 2
        self.px_width = self.space.width
        self.px_height = self.space.height

        #Add sprites to the layer 
        self.add(self.space)
        self.add(self.ship)
        self.add(self.enemy_ship_one)
        self.add(self.enemy_ship_two)

    #Event
    def on_key_release(self, symbol, modifiers):
        self.laser = Laser()
        self.laser._set_position(self.ship.position)

        if symbol == key.SPACE:
            self.laser.do(MoveTo((2000, self.ship._get_y()), 1))
            self.add(self.laser)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.ship.do(RotateTo(270, 0.1))
        if symbol == key.DOWN:
            self.ship.do(RotateTo(90, 0.1))
        if symbol == key.LEFT:
            self.ship.do(RotateTo(180, 0.1))
        if symbol == key.RIGHT:
            self.ship.do(RotateTo(0, 0.1))
        if symbol == key.C:
            self.ship.do(RotateBy(360, 0.2))



    #Event update collide
    def update(self, dt):
        self.laser.update_()
        self.enemy_ship_one.update_()
        self.enemy_ship_two.update_()
        self.ship.update_()
        explosion = cocos.sprite.Sprite(self.anim)

        if self.laser.cshape.overlaps(self.enemy_ship_one.cshape):
            explosion.position = self.enemy_ship_one._get_position()
            explosion.do(FadeOut(0.30))
            self.laser.do(FadeOut(0.01))
            self.add(explosion)

        if self.laser.cshape.overlaps(self.enemy_ship_two.cshape):
            explosion.position = self.enemy_ship_two._get_position()
            explosion.do(FadeOut(0.30))
            self.laser.do(FadeOut(0.03))
            self.add(explosion)
        


if __name__ == "__main__":
    director.init(width=1300, height=700, caption="Cocos game")
    director.window.pop_handlers()

    keyboard  = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    backgroundLayer = BackgroundLayer()

    scroller = cocos.layer.ScrollingManager()
    test_scene = cocos.scene.Scene()

    test_scene.schedule_interval(backgroundLayer.update, 1/60)

    scroller.add(backgroundLayer)
    test_scene.add(scroller)

    director.run(test_scene)