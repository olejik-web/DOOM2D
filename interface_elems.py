import os, sys
import pygame
import keyboard
from pprint import pprint
from random import randrange
from tkinter import *
import getkey 


WIDTH, HEIGHT = 1200, 600
pygame.mixer.init()
SOUNDS = {
    'metal_jump': pygame.mixer.Sound(
        'music/doomguy/jump_on_a_matal/jump.wav'),
    'metal_landfall': [pygame.mixer.Sound(
        'music/doomguy/jump_on_a_matal/landfall_1.wav'),
        pygame.mixer.Sound(
            'music/doomguy/jump_on_a_matal/landfall_2.wav')
        ],
    'punch': {
        'hit': pygame.mixer.Sound(
            'music/doomguy/punch/hit.wav'),
        'miss': pygame.mixer.Sound(
            'music/doomguy/punch/miss.wav'),
    },
    'walking_on_metal': [
        pygame.mixer.Sound(
            'music/doomguy/walking_on_a_matal/1.wav'),
        pygame.mixer.Sound(
            'music/doomguy/walking_on_a_matal/2.wav'),
        pygame.mixer.Sound(
            'music/doomguy/walking_on_a_matal/3.wav'),
        pygame.mixer.Sound(
            'music/doomguy/walking_on_a_matal/4.wav'),
    ],
    'pistol_shot': [
        pygame.mixer.Sound(
            'music/doomguy/pistol_shot/1.wav'),
        pygame.mixer.Sound(
            'music/doomguy/pistol_shot/2.wav'),
        pygame.mixer.Sound(
            'music/doomguy/pistol_shot/3.wav'),
        pygame.mixer.Sound(
            'music/doomguy/pistol_shot/4.wav'),        
        pygame.mixer.Sound(
            'music/doomguy/pistol_shot/5.wav'),        
    ],
    'change_wearon': pygame.mixer.Sound(
            'music/doomguy/change_wearon.wav'),  
    'doors': [
        pygame.mixer.Sound('music/doors/1st-door.wav'),
        pygame.mixer.Sound('music/doors/2nd-door.wav'),
    ],
    'imp': {
        'deaths': [pygame.mixer.Sound('music/imp/death1.wav'),
                   pygame.mixer.Sound('music/imp/death2.wav'),],
        'punches': [pygame.mixer.Sound('music/imp/punch_1.wav'),
                   pygame.mixer.Sound('music/imp/punch_2.wav'),],
        'walking': pygame.mixer.Sound('music/imp/walking.wav'),
        'fireball': {
            'create': pygame.mixer.Sound('music/imp/fireball_create.wav'),
            'flight': pygame.mixer.Sound('music/imp/fireball_flight.wav'),
        }
    },
    'gameplay': [pygame.mixer.Sound('music/gameplay2.wav'),
                   pygame.mixer.Sound('music/gameplay1.wav'),],
    'death_screen': pygame.mixer.Sound('music/death_screen.wav')
}


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def receive_crop_image(surface, part_width, part_height, part_x, part_y):
    crop_part = pygame.Surface((part_width, part_height))
    crop_part.blit(surface, (-part_x, -part_y + 40))
    return crop_part

class DialogWindow(pygame.sprite.Sprite):
    def __init__(self):
        self.standart_image = load_image('menu/exit/want_exit_fon.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                               (self.standart_image.get_width() // 2, 
                               self.standart_image.get_height() // 2))   
        self.animation_lst = sorted([
            'menu/exit/animation_of_exit_dialog/' + elem
                 for elem in 
                 os.listdir('images/menu/exit/animation_of_exit_dialog')])
        self.animation_lst = [
            'menu/exit/animation_of_exit_dialog/{}.png'.format(i)
                 for i in range(
                     len(self.animation_lst))]
        self.animation_inx = 0
    
    def receive_next_image(self):
        if self.animation_inx < len(self.animation_lst):
            image = load_image(self.animation_lst[self.animation_inx])
            image = pygame.transform.scale(image, (image.get_width() // 2, 
                                           image.get_height() // 2))
        
            self.animation_inx += 1
            return image
        return None
        

class Button(pygame.sprite.Sprite):
    def __init__(self):
        self.hover_image = load_image('menu/exit/2.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image('menu/exit/1.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))
        
    def check_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.rect.x <= mouse_x 
            and mouse_x <= self.rect.x + self.rect.width):
            if (self.rect.y <= mouse_y 
                and mouse_y <= self.rect.y + self.rect.height):
                self.image = self.hover_image
                return True
        self.image = self.standart_image
        return False
        
    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_cursor():
                return 'mouse_click'
        return None


class YesButton(Button):
    def __init__(self):
        self.hover_image = load_image('menu/yes/yes 2.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image('menu/yes/yes.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))
    
    def check_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 3, 3)
        if self.rect.colliderect(mouse_rect):
            self.image = self.hover_image
            return True
        self.image = self.standart_image
        return False    


class NoButton(Button):
    def __init__(self):
        self.hover_image = load_image('menu/no/no 2.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image('menu/no/no.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))  
    
    def check_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 3, 3)
        if self.rect.colliderect(mouse_rect):
            self.image = self.hover_image
            return True
        self.image = self.standart_image
        return False    


class ContinueButton(NoButton):
    def __init__(self):
        self.hover_image = load_image('menu/continue/hover.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image('menu/continue/standart.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2)) 


class StartInControlPointButton(NoButton):
    def __init__(self):
        self.hover_image = load_image(
            'menu/game_over/start_in_control_dot/put.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image(
            'menu/game_over/start_in_control_dot/not_put.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))     


class ExitOnWorkTableButton(NoButton):
    def __init__(self):
        self.hover_image = load_image(
            'menu/game_over/exit_on_work_table/put.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image(
            'menu/game_over/exit_on_work_table/not_put.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))


class GameOverExitButton(Button):
    def __init__(self):
        self.hover_image = load_image(
            'menu/game_over/exit_from_game/put.png')
        self.hover_image = pygame.transform.scale(self.hover_image, 
                                         (self.hover_image.get_width() // 2, 
                                         self.hover_image.get_height() // 2))
        self.standart_image = load_image(
            'menu/game_over/exit_from_game/not_put.png')
        self.standart_image = pygame.transform.scale(self.standart_image, 
                                         (self.standart_image.get_width() // 2, 
                                         self.standart_image.get_height() // 2))    


class InterfaceWindow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('interface/base_window.png')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(-20, 0)


class Hp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('interface/hp.png')
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // 2, 
                                             self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 465)
        self.full_hp = self.image.get_width()
        self.full_hp_image = self.image
    
    def update(self, *args):
        if args and type(args[0]) == int:
            hp = args[0]
            if hp > 0:
                new_hp = pygame.Surface((self.full_hp * hp // 10, 
                                         self.image.get_height()))
                new_hp = new_hp.convert()
                new_hp.set_colorkey(new_hp.get_at((0, 0)))
                new_hp.blit(self.full_hp_image, (0, 0))
                self.image = new_hp
            else:
                new_hp = pygame.Surface((20, 20))                
                new_hp.set_alpha(0)
                self.image = new_hp


class Armor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('interface/armor.png')
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // 2, 
                                             self.image.get_height() // 2 + 30))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 455)
        self.full_armor = self.image.get_width()
        self.full_armor_image = self.image
    
    def update(self, *args):
        if args and type(args[0]) == int:
            armor = args[0]
            if armor > 0:
                new_armor = pygame.Surface((self.full_armor * armor // 10, 
                                         self.image.get_height()))
                new_armor = new_armor.convert()
                new_armor.set_colorkey(new_armor.get_at((0, 0)))
                new_armor.blit(self.full_armor_image, (0, 0))
                self.image = new_armor
            else:
                new_armor = pygame.Surface((20, 20))                
                new_armor.set_alpha(0)
                self.image = new_armor


class WearonLogo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pistol_image = load_image('interface/pistol_gal.png')
        self.shoutgun_image = load_image('interface/shoutgun_gal.png')
        self.pistol_image = pygame.transform.scale(self.pistol_image, 
                                            (self.pistol_image.get_width() // 2, 
                                             self.pistol_image.get_height()
                                             // 2))
        self.shoutgun_image = pygame.transform.scale(self.shoutgun_image, 
                                            (self.shoutgun_image.get_width() 
                                             // 3, 
                                            self.shoutgun_image.get_height() 
                                            // 3))        
        self.rect = self.pistol_image.get_rect()
        self.rect = self.rect.move(0, 400)
        self.simple_image = pygame.Surface((self.rect.width, self.rect.height))
        self.simple_image.set_alpha(0)
        self.image = self.simple_image
        self.wearons = {'pistol': False, 'shoutgun': False}
        self.sound = SOUNDS['change_wearon']
        self.sound.set_volume(0.6)
        
    def receive_wearon(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                self.wearons['pistol'] = not self.wearons['pistol']
                if self.wearons['pistol']:
                    self.wearons['shoutgun'] = False
                self.sound.play()
            if event.key == pygame.K_2:
                self.wearons['shoutgun'] = not self.wearons['shoutgun']
                if self.wearons['shoutgun']:
                    self.wearons['pistol'] = False             
                self.sound.play()
        if self.wearons['pistol']:
            self.image = self.pistol_image
        elif self.wearons['shoutgun']:
            self.image = self.shoutgun_image
        else:
            self.image = self.simple_image


class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('interface/infinity.png')
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // 5, 
                                             self.image.get_height() // 5))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 495)
        

class Key(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width(), 
                                             self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)    
        self.key = ''
        self.make_visible = False      

    def update(self, key='not key'):
        if key == self.key and not self.make_visible:
            key_move_up_x = self.rect.x
            key_move_up_y = self.rect.y
            if self.key == 'up':
                self.image = load_image('training/up_2.png')
            if self.key == 'left':
                self.image = load_image('training/left_2.png')
            if self.key == 'space':
                self.image = load_image('training/space_2.png')
            if self.key == 'wearon':
                self.image = load_image('training/first_weapon_2.png')
            if self.key == 'wearon2':
                self.image = load_image('training/second_weapon_2.png')
            if self.key == 'wearon3':
                self.image = load_image('training/third_weapon_2.png')
            if self.key == 'right':
                self.image = load_image('training/right_2.png')
            self.image = pygame.transform.scale(self.image, 
                                                (self.image.get_width(), 
                                                 self.image.get_height()))
            self.rect = self.image.get_rect()         
            self.rect = self.rect.move(key_move_up_x, 
                                                     key_move_up_y)            
            self.make_visible = True
        if self.make_visible and key == 'visible':
            try:
                self.image.set_alpha(self.image.get_alpha() - 10)
            except Exception:
                self.kill()            


class Text(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width(), 
                                             self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)    
        self.key = ''
        self.make_visible = False

    def update(self, key='not key'):
        if key == self.key and not self.make_visible:
            self.make_visible = True
        if self.make_visible and key == 'visible':
            try:
                self.image.set_alpha(self.image.get_alpha() - 10)
            except Exception:
                self.kill()  

pygame.mixer.quit()