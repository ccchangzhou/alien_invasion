import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

#Git push for Git Bash 2
class AlienInvasion:
    """ 管理游戏资源和行为的类 """
    def __init__(self):
        """ 初始化游戏并创建游戏资源 """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #全屏运行游戏
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_ganme(self):
        """ 开始游戏的主循环 """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """ 响应按键和鼠标事件 """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ 响应按下 """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key ==  pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_SPACE: 
            self._fire_bullet()    
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """ 响应释放 """
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _fire_bullet(self):
        """ 创建一个子弹，并将其加入编组bullets """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ 更新子弹的位置，并删除已消失的子弹 """
        #更新子弹的位置
        self.bullets.update()

        #删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):    
        """ 响应子弹和外星人的碰撞 """
        #删除发生碰撞子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            #删除现有的子弹并穿件一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """ 检查是否有外星人位于屏幕边缘，并更新整个外星舰队的位置 """
        self._check_fleet_edges()
        self.aliens.update()

    def _create_fleet(self):
        """ 创建一个外星舰队 """
        #创建第一个外星人,再不断添加，知道没有空间添加外星人为止
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            """ 添加一行外星人后，重置x并递增y值 """
            current_x = alien_width
            current_y += 2*alien_height

    def _create_alien(self, x_position,  y_position):
        """ 创建一个外星人并将其放在当前行中 """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """ 在所有外星人到达边缘时采取相应措施 """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ 将整个外星舰队向下移动，并改变它们的方向 """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """ 更新屏幕上的图像，并切换到新屏幕 """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_ganme()