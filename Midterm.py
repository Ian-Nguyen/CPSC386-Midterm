#CPSC 386 Coding Portion

import pygame as pg

#Ship Class
class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector
        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.lasers = pg.sprite.Group()

    def __repr__(self):
        r = self.rect
        return 'Ship({},{}),v={}'.format(r.x, r.y, self.velocity)

    def fire(self):
        laser = Laser(game=self.game)
        self.lasers.add(laser)

    def remove_lasers(self): self.lasers.remove()

    def center_ship(self): self.rect.midbottom = self.screen_rect.midbottom

    def draw(self): self.screen.blit(self.image, self.rect)

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)
        
    def update(self):
        fleet = self.game.fleet
        self.move()
        self.draw()
        for laser in self.lasers.sprites():
            laser.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        aliens_hit = pg.sprite.groupcollide(fleet.aliens, self.lasers, False, True)
        if len(aliens_hit.keys()) > 0:
            print('{} aliens hit'.format(len(aliens_hit.keys())))
        for alien in aliens_hit:
            alien.hit()
            if alien.health <= 0:
                fleet.aliens.remove(alien)
        if not fleet.aliens:
            self.game.restart()

#Vector Class
class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __rmul__(self, k: float):
        return Vector(k * self.x, k * self.y)

    def __mul__(self, k: float):
        return self.__rmul__(k)

    def __sub__(self, other):
        return self.__add__(-1 * other)

    def __truediv__(self, k: float):
        return self.__rmul__(1.0 / k)

    def __neg__(self):
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def test():  # feel free to change the test code
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('u plus v is {}'.format(u + v))
        print('u minus v is {}'.format(u - v))
        print('3u is {}'.format(3 * u))
        print('-u is {}'.format(-1 * u))


def main():
    Vector.test()


if __name__ == '__main__':
    main()
