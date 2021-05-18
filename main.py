# -*- coding: utf-8 -*-
import os, sys
import pygame
import keyboard
from pprint import pprint
from random import randrange, choice
from tkinter import *
import getkey 
from interface_elems import Button, DialogWindow, YesButton, NoButton
from interface_elems import ContinueButton, InterfaceWindow, Hp, Armor
from interface_elems import WearonLogo, Ammo, StartInControlPointButton
from interface_elems import ExitOnWorkTableButton, GameOverExitButton
from interface_elems import Text, Key
from opponents import Opponent
import arcade

# class Player:
#    def __init__(self):
#################################################################

class PauseForm():
    def __init__(self):
        self.pressing_Esc = False
     
WIDTH, HEIGHT = 1200, 600
FPS = 24
PRESSING_SPACE = False
PRESSING_K_1 = False
SQUARE = 0

ALL_SPRITES = pygame.sprite.Group()
BLOCK_SPRITES = pygame.sprite.Group()
WALL_SPRITES = pygame.sprite.Group()
PLAYER_GROUP = pygame.sprite.Group()
FIRST_LEVEL_GROUP = pygame.sprite.Group()
INTERFACE_GROUP = pygame.sprite.Group()
OPPONENTS = pygame.sprite.Group()
TRAINING_SPRITES = pygame.sprite.Group()
pygame.mixer.init()
SOUNDS = {
    'load_music': pygame.mixer.Sound(
        'music/doomguy/jump_on_a_matal/jump.wav'),
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


def check_collide(obj, group):
    if type(group) == pygame.sprite.Group:
        for elem in group:
            if pygame.sprite.collide_mask(obj, elem):
                return True
        return False
    else:
        if pygame.sprite.collide_mask(obj, group):
            return True        
        return False
    

class PlayerDead(pygame.sprite.Sprite):
    def __init__(self):
        self.animate_list_die = sorted(['doomguy_die/' + elem
             for elem in os.listdir('images/doomguy_die')
             if os.path.isfile('images/doomguy_die/' + elem)])
        self.animate_list_die = ['doomguy_die/{}.png'.format(i) 
                              for i in range(len(self.animate_list_die))]
        self.animate_inx = 0
        self.gravity = 10
        self.image = load_image(self.animate_list_die[0])
        self.rect = player.rect
        
    def update_place_of_dead(self):
        if not player.must_make_hide_of_dead:
            self.rect = player.rect        
    
    def update(self):
        if not check_collide(self, BLOCK_SPRITES):
            self.rect = self.rect.move(0, self.gravity)        
        if self.animate_inx < len(self.animate_list_die):
            self.image = load_image(self.animate_list_die[self.animate_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, 
                self.image.get_height() // 5))
            if player.reway:
                self.image = pygame.transform.flip(self.image, True, 
                                                     False)
            self.animate_inx += 1
            return False
        else:
            return True


class GameOpponent(Opponent):
    def update(self, *args):
        if self.animate_list_fire:
            self.animate_fire()
            return         
        for elem in ALL_SPRITES:
            if (pygame.sprite.collide_mask(self, elem) and type(elem) == Bullet 
                and not self.animate_list_fire):
                self.hp -= 2
                elem.kill()
        if (player_hand.animate_list_push_inx == 3 
            and pygame.sprite.collide_mask(self, player_hand)):
            self.hp -= 1
        if not check_collide(self, BLOCK_SPRITES):
            self.rect = self.rect.move(0, self.gravity)
            self.image = load_image(self.animate_list_stand[0])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))                        
        else:
            r = player.rect.x - self.rect.x
            if self.hp > 0:
                if abs(r) < 800 and abs(r) > 60:
                    self.animate_moving()
                    if r < 0:
                        self.reway = True
                        self.rect = self.rect.move(-3, 0)
                    else:
                        self.reway = False
                        self.rect = self.rect.move(3, 0)  
                    self.animate_fight_inx = 0
                elif abs(r) > 0:
                    self.animate_beating()
                    if (self.animate_fight_inx == 20 
                        and pygame.sprite.collide_mask(self, player)):
                        if player.armor > 0:
                            player.armor -= 2
                            armor.update(player.armor)
                        elif player.hp > 0:
                            player.hp -= 2
                            hp.update(player.hp)
                else:
                    self.animate_fight_inx = 0
                    self.animate_standing()
            else:
                if self.make_kayo_animation:
                    self.kayo_time = 0
                    player.must_make_hide_of_enemy = True
                    player_hand.must_make_hide_of_enemy = True
                    if self.animate_fatal_dead():
                        self.kill()
                        player.must_make_hide_of_enemy = False
                        player_hand.must_make_hide_of_enemy = False
                        if player.hp < 10:
                            player.hp += 1
                            hp.update(player.hp)                        
                else:
                    if self.kayo_time > 0:
                        self.animate_kayo()
                        self.kayo_time -= 1
                        if (player.pushing_time == 10 
                            and pygame.sprite.collide_mask(self, player_hand)):
                            self.make_kayo_animation = True
                    else:
                        if self.animate_dieng():
                            self.kill()
        # print(pygame.sprite.collide_mask(self, pol), pol.rect.y)
        if pygame.sprite.collide_mask(self, stolb):
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)                


class Imp(GameOpponent):
    def __init__(self):
        super().__init__()
        self.hp = 8
        self.make_kayo_animation = False
        self.image = load_image('imp/imp_stand/0.png')
        self.animate_list_fire = sorted(['fire' + elem
                 for elem in os.listdir('images/fire')
                 if os.path.isfile('images/fire/' + elem)])
        self.animate_list_fire = ['fire/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_fire))]        
        self.animate_list_move = sorted(['imp/imp_run/' + elem
                 for elem in os.listdir('images/imp/imp_run')
                 if os.path.isfile('images/imp/imp_run/' + elem)])
        self.animate_list_move = ['imp/imp_run/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_move))]
        self.animate_list_stand = sorted(['imp/imp_stand/' + elem
                 for elem in os.listdir('images/imp/imp_stand')
                 if os.path.isfile('images/imp/imp_stand/' + elem)])
        self.animate_list_stand = ['imp/imp_stand/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_stand))]
        self.animate_list_beat = sorted(['imp/imp_beating/' + elem
                 for elem in os.listdir('images/imp/imp_beating')
                 if os.path.isfile('images/imp/imp_beating/' + elem)])
        self.animate_list_beat = ['imp/imp_beating/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_beat))]
        self.animate_list_die = sorted(['imp/imp_dieng/' + elem
                 for elem in os.listdir('images/imp/imp_dieng')
                 if os.path.isfile('images/imp/imp_dieng/' + elem)])
        self.animate_list_die = ['imp/imp_dieng/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_die))]        
        self.animate_list_kayo = sorted(['imp/imp_kayo/' + elem
                 for elem in os.listdir('images/imp/imp_kayo')
                 if os.path.isfile('images/imp/imp_kayo/' + elem)])
        self.animate_list_kayo = ['imp/imp_kayo/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_kayo))]
        self.animate_list_fatal_dead = sorted(['imp/imp_fatal_dead/' + elem
                 for elem in os.listdir('images/imp/imp_fatal_dead')
                 if os.path.isfile('images/imp/imp_fatal_dead/' + elem)])
        self.animate_list_fatal_dead = ['imp/imp_fatal_dead/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_fatal_dead))]        
        self.animate_list_crawl = sorted(['imp/imp_crawling/' + elem
                 for elem in os.listdir('images/imp/imp_crawling')
                 if os.path.isfile('images/imp/imp_crawling/' + elem)])
        self.animate_list_crawl = ['imp/imp_crawling/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_crawl))]
        self.animate_list_shot = sorted(['imp/imp_fireboll/' + elem
                 for elem in os.listdir('images/imp/imp_fireboll')
                 if os.path.isfile('images/imp/imp_fireboll/' + elem)])
        self.animate_list_shot = ['imp/imp_fireboll/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_shot))]        
        self.animate_list_crawl_shot = sorted(['imp/imp_fire_wall/' + elem
                 for elem in os.listdir('images/imp/imp_fire_wall')
                 if os.path.isfile('images/imp/imp_fire_wall/' + elem)])
        self.animate_list_crawl_shot = ['imp/imp_fire_wall/{}.png'.format(i) 
                                  for i in range(len(
                                      self.animate_list_crawl_shot))]
        self.animate_list_crawl_shot = sorted(['imp/imp_fire_wall/' + elem
                 for elem in os.listdir('images/imp/imp_fire_wall')
                 if os.path.isfile('images/imp/imp_fire_wall/' + elem)])
        self.animate_list_crawl_shot = ['imp/imp_fire_wall/{}.png'.format(i) 
                                  for i in range(len(
                                      self.animate_list_crawl_shot))] 
        self.animate_list_jump = sorted(['imp/imp_jump/' + elem
                 for elem in os.listdir('images/imp/imp_jump')
                 if os.path.isfile('images/imp/imp_jump/' + elem)])
        self.animate_list_jump = ['imp/imp_jump/{}.png'.format(i + 1) 
                                  for i in range(len(
                                      self.animate_list_jump))]
        self.animate_list_fire = sorted(['fire' + elem
                 for elem in os.listdir('images/fire')
                 if os.path.isfile('images/fire/' + elem)])
        self.animate_list_fire = ['fire/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_fire))]                   
        self.fireball_image = load_image('imp/fireboll.png')
        self.fireball_image = pygame.transform.scale(self.fireball_image, (
            self.fireball_image.get_width() // 6, 
            self.fireball_image.get_height() // 6))
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 5, self.image.get_height() // 5))
        self.gravity = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 120)
        self.animate_inx = 0
        self.animate_fight_inx = 0
        self.animate_kayo_inx = 0
        self.animate_dead_inx = 0
        self.animate_jump_inx = 0
        self.reway = False
        self.kayo_time = 160 
        self.animate_crawl_inx = 0
        self.animate_shot_inx = 0
        self.animate_crawl_shot_inx = 0
        self.crawling = False
        self.flag = False
        self.shoting = False
        self.jumping = False
        self.up_v = 0
        self.sound = ''
        self.step_const = randrange(9, 13)
        self.step_time = self.step_const        
    
    def animate_jumping(self):
        try:
            self.image = load_image(self.animate_list_jump[
                self.animate_jump_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_jump_inx += 1
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_jump_inx = 0            
    
    def animate_shoting(self):
        try:
            self.image = load_image(self.animate_list_shot[
                self.animate_shot_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_inx %= len(self.animate_list_shot)
            if self.animate_inx < len(self.animate_list_shot) - 1:
                self.animate_shot_inx += 1
            else:
                self.animate_shot_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_shot_inx = 0        
        
    def animate_crawling(self):
        try:
            self.image = load_image(self.animate_list_crawl[
                self.animate_crawl_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_inx %= len(self.animate_list_crawl)
            if self.animate_inx < len(self.animate_list_crawl) - 1:
                self.animate_crawl_inx += 1
            else:
                self.animate_crawl_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_crawl_inx = 0
    
    def animate_crawl_shoting(self):
        try:
            self.image = load_image(self.animate_list_crawl_shot[
                self.animate_crawl_shot_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_inx %= len(self.animate_list_crawl_shot)
            if self.animate_inx < len(self.animate_list_crawl_shot) - 1:
                self.animate_crawl_shot_inx += 1
            else:
                self.animate_crawl_shot_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_crawl_shot_inx = 0
    
    def update(self, *args):
        self.rect = self.rect.move(0, self.up_v)                        
        if self.up_v < 0:
            self.up_v += self.gravity
        if self.animate_list_fire:
            self.animate_fire()
            return
        for elem in ALL_SPRITES:
            if pygame.sprite.collide_mask(self, elem) and type(elem) == Bullet:
                self.hp -= 2
                elem.kill()
        if (player_hand.animate_list_push_inx == 3 
            and pygame.sprite.collide_mask(self, player_hand)):
            self.hp -= 1
        if not check_collide(self, BLOCK_SPRITES):
            if not self.flag:
                self.rect = self.rect.move(0, self.gravity)
        else:
            self.jumping = False
        r = player.rect.x - self.rect.x
        self.flag = False
        self.shoting = False
        self.crawling = False
        for elem in WALL_SPRITES:
            if self.rect.colliderect(elem.rect):        
                self.crawling = True
        if self.hp > 0:
            if self.animate_fight_inx == 18:
                self.sound = choice(SOUNDS['imp']['punches'])
                self.sound.set_volume(0.6)
                self.sound.play()
            if (self.animate_inx != 0 
                and self.animate_inx % self.step_const == 0):
                self.step_const = randrange(9, 13)
                self.sound = SOUNDS['imp']['walking']
                self.sound.set_volume(0.6)
                self.sound.play()                       
            for elem in ALL_SPRITES:
                if type(elem) == Bullet:
                    if (abs(elem.rect.x - self.rect.x) < 600 and abs(elem.rect.x - self.rect.x) > 100
                        and check_collide(self, BLOCK_SPRITES)):
                        if (self.reway and 
                            elem.bullet_v // abs(elem.bullet_v) > 0 
                            or not self.reway 
                            and elem.bullet_v // abs(elem.bullet_v) < 0):
                            # print('inx =', self.animate_jump_inx)
                            # not self.reway and elem.rect.x > self.rect.x
                            self.jumping = True
                            self.up_v = -60                
            if abs(r) < 800 and abs(r) > 60:
                if abs(r) < 700 and abs(r) > 500:
                    for elem in WALL_SPRITES:
                        if self.rect.colliderect(elem.rect) and not self.jumping:
                            if self.rect.y > 200:
                                self.animate_crawling()
                                # self.crawling = True
                                self.rect = self.rect.move(0, -3)
                            else:
                                self.animate_crawl_shoting()
                                if self.animate_crawl_shot_inx == 1:
                                    self.sound = SOUNDS['imp']['fireball']['create']
                                    self.sound.set_volume(0.05)
                                    self.sound.play()                                                             
                                if self.animate_crawl_shot_inx == 22:
                                    self.fireball = FireBall(
                                        self.fireball_image)
                                    if not self.reway:
                                        r2 = self.rect.y - player.rect.y
                                        self.fireball.bullet_v = -abs(r) // 10
                                        self.fireball.bullet_y = -r2 // 10
                                        self.fireball.rect = self.fireball.rect.move(
                                            self.rect.x, self.rect.y + 10)                                                    
                                    else:
                                        r2 = self.rect.y - player.rect.y
                                        self.fireball.bullet_v = abs(r) // 10
                                        self.fireball.bullet_y = -r2 // 10
                                        self.fireball.rect = self.fireball.rect.move(
                                            self.rect.x + 60, self.rect.y + 10)                                                                               
                                # print(self.rect.y)
                            self.flag = True
                            break
                        elif abs(elem.rect.x - self.rect.x) < 500:
                            self.flag = False
                            if not self.jumping:
                                self.animate_moving()
                            else:
                                self.animate_jumping()
                            if pygame.sprite.spritecollideany(self, 
                                                              WALL_SPRITES):
                                if self.rect.colliderect(elem.rect):
                                    if self.reway:
                                        self.rect = self.rect.move(9, 0)
                                    else:
                                        self.rect = self.rect.move(-9, 0)                            
                            if elem.rect.x - self.rect.x < 0:
                                self.rect = self.rect.move(-9, 0)
                                self.reway = True
                            else:
                                self.rect = self.rect.move(9, 0)
                                self.reway = False
                            break
                        elif not self.crawling:
                            print(self.crawling)
                            if self.animate_shot_inx == 1:
                                self.sound = SOUNDS['imp']['fireball']['create']
                                self.sound.set_volume(0.05)
                                self.sound.play()                                    
                            if self.animate_shot_inx == 17:                         
                                self.fireball = FireBall(self.fireball_image)
                                if self.reway:
                                    self.fireball.bullet_v = -35
                                    self.fireball.rect = self.fireball.rect.move(
                                        self.rect.x, self.rect.y + 5)                                                    
                                else:
                                    self.fireball.bullet_v = 35
                                    self.fireball.rect = self.fireball.rect.move(
                                        self.rect.x + 60, self.rect.y + 5)                                               
                            self.animate_shoting()
                            self.shoting = True
                if not self.flag:
                    if not self.shoting:
                        if pygame.sprite.spritecollideany(self, WALL_SPRITES):
                            if self.rect.colliderect(elem.rect):
                                if self.reway:
                                    self.rect = self.rect.move(9, 0)
                                else:
                                    self.rect = self.rect.move(-9, 0)                        
                        if not self.jumping:
                            self.animate_moving()
                        else:
                            self.animate_jumping()                        
                        if r < 0:
                            self.reway = True
                            self.rect = self.rect.move(-9, 0)
                        else:
                            self.reway = False
                            self.rect = self.rect.move(9, 0)  
                    self.animate_fight_inx = 0
                    # self.crawling = False
            elif abs(r) > 0 and not self.jumping:
                self.animate_beating()                  
                if (self.animate_fight_inx == 20 
                    and pygame.sprite.collide_mask(self, player)):
                    if player.armor > 0:
                        player.armor -= 4
                        armor.update(player.armor)
                    elif player.hp > 0:
                        player.hp -= 4
                        hp.update(player.hp)
            elif not self.jumping:
                self.animate_fight_inx = 0
                self.animate_standing()
        else:
            if self.make_kayo_animation:
                self.kayo_time = 0
                player.must_make_hide_of_enemy = True
                player_hand.must_make_hide_of_enemy = True
                self.reway = player.reway
                if self.animate_fatal_dead():
                    self.kill()
                    player.must_make_hide_of_enemy = False
                    player_hand.must_make_hide_of_enemy = False
                    if player.hp < 10:
                        if player.hp > 8:
                            player.hp += 10 - player.hp 
                        else:
                            player.hp += 2
                        hp.update(player.hp)
            else:
                if self.kayo_time > 0:
                    self.animate_kayo()
                    self.kayo_time -= 1
                    if (player.pushing_time == 10 
                        and pygame.sprite.collide_mask(self, player_hand)):
                        self.make_kayo_animation = True
                else:
                    if self.animate_dieng():
                        self.kill()
                    if self.animate_dead_inx == 6:
                        self.sound = choice(SOUNDS['imp']['deaths'])
                        self.sound.set_volume(0.3)
                        self.sound.play()  
        if pygame.sprite.collide_mask(self, stolb):
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255) 


class HiddenSprite(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
    
    def check_collide(self, collide_object):
        if self.rect.colliderect(collide_object.rect):
            if type(collide_object) == Player:
                collide_object.rect = collide_object.rect.move(
                    -collide_object.vector_x, -collide_object.vector_y)
                print(collide_object.vector_x, collide_object.vector_y)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, object_image):
        super().__init__(ALL_SPRITES)
        self.image = load_image(object_image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def check_collide(self, collide_object):
        self.mask = pygame.mask.from_surface(self.image)
        collide_object.mask = pygame.mask.from_surface(collide_object.image)
        if pygame.sprite.collide_mask(self, collide_object):
            if (type(collide_object) == Player 
                or type(collide_object) == GameOpponent 
                or type(collide_object) == Imp):
                if collide_object.reway:
                    collide_object.rect = collide_object.rect.move(20, 0)
                else:
                    collide_object.rect = collide_object.rect.move(-20, 0)    
    
    def update(self, *args):
        pass


class Door(GameObject):
    def __init__(self, object_image):
        super().__init__(object_image)
        self.image = load_image(object_image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)    
        self.closed_door = True
        self.animate_inx = 0
        self.lst_animations = [
            'locations/start_location/door_1/door_animation/' + elem
                 for elem in 
                 os.listdir(
                     'images/locations/start_location/door_1/door_animation')]
        self.lst_animations = [
                'locations/start_location/door_1/door_animation/{}.png'.format(
                    i)
                     for i in range(
                         len(self.lst_animations))]
        self.sound = SOUNDS['doors'][0]
        # print(self.lst_animations)
    
    def check_collide(self, collide_object):
        self.mask = pygame.mask.from_surface(self.image)
        collide_object.mask = pygame.mask.from_surface(collide_object.image)
        if pygame.sprite.collide_mask(self, collide_object):
            if (type(collide_object) == Player 
                or type(collide_object) == GameOpponent 
                or type(collide_object) == Imp):
                if self.animate_inx != len(self.lst_animations) - 1:
                    if collide_object.reway:
                        collide_object.rect = collide_object.rect.move(20, 0)
                    else:
                        collide_object.rect = collide_object.rect.move(-20, 0)
    
    def animate_close(self):
        if self.animate_inx > 0:
            self.animate_inx -= 1
        self.image = load_image(self.lst_animations[self.animate_inx])
        self.image = pygame.transform.scale(self.image, 
                                         (self.image.get_width() // 2, 
                                          self.image.get_height() // 2 + 20))
    
    def animate_open(self):
        # print(self.animate_inx)
        if self.animate_inx < len(self.lst_animations) - 1:
            self.animate_inx += 1
        self.image = load_image(self.lst_animations[self.animate_inx])
        self.image = pygame.transform.scale(self.image, 
                                         (self.image.get_width() // 2, 
                                          self.image.get_height() // 2 + 20))
    
    def update(self, *args):
        if args:
            if args[0] == 'close':
                self.animate_close()
                # pass
            elif args[0] == 'open':
                self.animate_open()
                # pass


class PerehodDoor(Door):
    def __init__(self, object_image):
        super().__init__(object_image)
        self.image = load_image(object_image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.closed_door = True
        self.animate_inx = 0
        self.standart_image = ''
        self.lst_animations = [
            'locations/perehod/door_animation/' + elem
                 for elem in 
                 os.listdir(
                     'images/locations/perehod/door_animation')]
        self.lst_animations = [
                'locations/perehod/door_animation/{}.png'.format(
                    i)
                     for i in range(
                         len(self.lst_animations))]
        self.door_way = ''
        self.sound = SOUNDS['doors'][1]
        
    def animate_close(self):
        if self.animate_inx > 0:
            self.animate_inx -= 1
        self.image = load_image(self.lst_animations[
            len(self.lst_animations) - self.animate_inx - 2])
        self.image = pygame.transform.scale(self.image, 
                                         (self.image.get_width() // 3 + 40, 
                                          self.image.get_height() // 3 + 100))    
        if self.door_way == 'left':
            self.image = pygame.transform.flip(self.image, True, False)        
    
    def animate_open(self):
        # print(self.animate_inx)
        if self.animate_inx < len(self.lst_animations) - 2:
            self.animate_inx += 1
        self.image = load_image(self.lst_animations[self.animate_inx])
        self.image = pygame.transform.scale(self.image, 
                                         (self.image.get_width() // 3 + 40, 
                                          self.image.get_height() // 3 + 100))
        if self.door_way == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
    
    def update(self, *args):
        if args:
            if args[0] == 'close':
                self.animate_close()
                # pass
            elif args[0] == 'open':
                self.animate_open()    
        if (self.animate_inx == 0 
            or self.animate_inx == len(self.lst_animations) - 2):
            self.image = self.standart_image
            self.rect.y = 66
            player.must_make_hide = False
            player_hand.must_make_hide = False
            if player.reway:
                self.door_way = 'left'
            else:
                self.door_way = 'right'
        else:
            if player.reway:
                player.rect.x = self.rect.x - 100
            else:
                player.rect.x = self.rect.x + 160
            player.must_make_hide = True
            player_hand.must_make_hide = True
            self.rect.y = 6
            

class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.must_make_hide = False
        self.shooting_time = 0
        self.image = load_image('with_pistol_standing/hand/0.png')
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 5, 
            self.image.get_height() // 5))
        self.mask = pygame.mask.from_surface(self.image)
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect = player.rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.set_alpha(0)
        self.animation_do = False
        self.animation_downing_hand_do = True
        self.animate_list_moving_shoutgun = sorted([
            'shoutgun/wearon_moving/' + elem
                 for elem in 
                 os.listdir('images/shoutgun/wearon_moving')
                 if os.path.isfile(
                     'images/shoutgun/wearon_moving' + elem)])
        '''self.animate_list_moving_shoutgun = [
            'with_pistol_standing/hand_shooting/{}.png'.format(i)
                 for i in range(
                     len(self.animate_list_hand_shooting_with_pistol))]'''
        self.animate_list_hand_downing_with_pistol = sorted([
            'with_pistol_standing/hand_downing/' + elem
                 for elem in 
                 os.listdir('images/with_pistol_standing/hand_downing')
                 if os.path.isfile(
                     'images/with_pistol_standing/hand_downing/' + elem)])
        # del self.animate_list_hand_downing_with_pistol[
        #    len(self.animate_list_hand_downing_with_pistol) - 2:]
        self.animate_list_hand_downing_with_pistol_inx = 0
        self.animate_list_hand_upping_with_pistol = sorted([
            'with_pistol_standing/hand_upping/' + elem
                 for elem in 
                 os.listdir('images/with_pistol_standing/hand_upping')
                 if os.path.isfile(
                     'images/with_pistol_standing/hand_upping/' + elem)])
        self.animate_list_hand_upping_with_pistol_inx = 0
        self.animate_list_hand_shooting_with_pistol = sorted([
            'with_pistol_standing/hand_shooting/' + elem
                 for elem in 
                 os.listdir('images/with_pistol_standing/hand_shooting')
                 if os.path.isfile(
                     'images/with_pistol_standing/hand_shooting/' + elem)])
        self.animate_list_hand_shooting_with_pistol = [
            'with_pistol_standing/hand_shooting/{}.png'.format(i)
                 for i in range(
                     len(self.animate_list_hand_shooting_with_pistol))]
        self.animate_list_hand_shooting_with_pistol_inx = 0
        self.animate_list_push = sorted(['player_pushed/' + elem
                 for elem in os.listdir('images/player_pushed')
                 if os.path.isfile('images/player_pushed/' + elem)])
        self.animate_list_push = ['player_pushed/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_push))]  
        self.animate_list_push_inx = 0
        self.animation_do = True
        self.must_make_hide_of_enemy = False
        self.must_make_hide_of_dead = False
        self.rotate = False
        self.sound = ''
    
    def update(self, *args):
        if (self.must_make_hide or self.must_make_hide_of_enemy 
            or self.must_make_hide_of_dead):
            self.image.set_alpha(0)
            return   
        else:
            self.image.set_alpha(255)
        # pass
        flag = True
        if player.pushing_time <= 0 and not player.with_pistol:
            self.image.set_alpha(0)
        if args and args[0] == 'push_time':
            # print(player.with_pistol)
            if not player.with_pistol:
                if player.reway:
                    print(self.animate_list_push_inx)
                    if player.pushing_time > 0:
                        tmp = self.animate_list_push_inx
                        if tmp < len(self.animate_list_push):
                            self.image = load_image(
                                self.animate_list_push[tmp])
                            self.image = pygame.transform.flip(self.image, 
                                                               True, False)
                            self.image = pygame.transform.scale(self.image, (
                                self.image.get_width() // 5 - 8, 
                                self.image.get_height() // 5))
                            self.rect = self.image.get_rect()
                            self.rect = player.rect
                            self.rect = self.rect.move(-6, 0)
                        self.animate_list_push_inx = (tmp + 1)
                        player.pushing_time -= 1
                else:
                    # print(player.pushing_time)
                    if player.pushing_time > 0:
                        tmp = self.animate_list_push_inx
                        # print(tmp)
                        if tmp < len(self.animate_list_push):
                            self.image = load_image(
                                self.animate_list_push[tmp])
                            self.image = pygame.transform.scale(self.image, (
                                self.image.get_width() // 5, 
                                self.image.get_height() // 5))
                            self.rect = self.image.get_rect()
                            self.rect = player.rect
                            self.rect = self.rect.move(3, 0)                           
                        self.animate_list_push_inx = (tmp + 1)
                        player.pushing_time -= 1
                # print(self.rect, player.rect)
                # SCREEN.blit(self.image, self.rect)
                flag = False
                # return 
        else:
            # self.animate_list_push_inx = 0
            if player.reway:
                # print(self.animation_downing_hand_do)
                if not self.animation_do:
                    tmp = self.animate_list_hand_upping_with_pistol_inx
                    # print('ok0')
                    if tmp < len(self.animate_list_hand_upping_with_pistol):
                        # print('ok1')
                        self.image = load_image(
                            self.animate_list_hand_upping_with_pistol[tmp])
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))
                        self.rect = self.image.get_rect()     
                        self.rect = player.rect
                        self.animate_list_hand_upping_with_pistol_inx = (tmp + 1)
                    else:
                        self.animation_do = True
                        self.animate_list_hand_upping_with_pistol_inx = 0
                elif not self.animation_downing_hand_do:
                    # print(self.animation_downing_hand_do)
                    tmp = self.animate_list_hand_downing_with_pistol_inx
                    # print('ok0')
                    if tmp < len(self.animate_list_hand_downing_with_pistol):
                        # print('ok1')
                        self.image = load_image(
                            self.animate_list_hand_downing_with_pistol[tmp])
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))
                        self.rect = self.image.get_rect()       
                        self.rect = player.rect
                        self.animate_list_hand_downing_with_pistol_inx = (tmp + 1)
                    else:
                        self.animation_downing_hand_do = True
                        self.animate_list_hand_downing_with_pistol_inx = 0
                        self.image = pygame.Surface(
                            (self.rect.width, self.rect.height))
                        self.image.set_alpha(0)
                        player.with_pistol = False
                if (self.shooting_time > 0 and 
                    self.animation_downing_hand_do and self.animation_do):
                    for i in range(3):
                        # print(self.shooting_time)
                        if self.shooting_time > 0:
                            tmp = self.animate_list_hand_shooting_with_pistol_inx
                            self.image = load_image(
                                self.animate_list_hand_shooting_with_pistol[tmp])
                            self.image = pygame.transform.flip(self.image, 
                                                               True, False)
                            self.image = pygame.transform.scale(self.image, (
                                self.image.get_width() // 5, 
                                self.image.get_height() // 5))
                            self.rect = self.image.get_rect()        
                            self.rect = player.rect
                            tmp += 1
                            tmp %= len(self.animate_list_hand_shooting_with_pistol)
                            self.animate_list_hand_shooting_with_pistol_inx = tmp
                            self.shooting_time -= 1
                else:
                    self.animate_list_hand_shooting_with_pistol_inx = 0
            else:
                if not self.animation_do:
                    tmp = self.animate_list_hand_upping_with_pistol_inx
                    # print('ok0')
                    if tmp < len(self.animate_list_hand_upping_with_pistol):
                        # print('ok1')
                        self.image = load_image(
                            self.animate_list_hand_upping_with_pistol[tmp])
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))
                        self.rect = self.image.get_rect()            
                        self.rect = player.rect
                        self.animate_list_hand_upping_with_pistol_inx = (tmp + 1)
                    else:
                        self.animation_do = True
                        self.animate_list_hand_upping_with_pistol_inx = 0
                elif not self.animation_downing_hand_do:
                    # print(self.animation_downing_hand_do)
                    tmp = self.animate_list_hand_downing_with_pistol_inx
                    # print('ok0')
                    if tmp < len(self.animate_list_hand_downing_with_pistol):
                        # print('ok1')
                        self.image = load_image(
                            self.animate_list_hand_downing_with_pistol[tmp])
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))
                        self.rect = self.image.get_rect()      
                        self.rect = player.rect
                        self.animate_list_hand_downing_with_pistol_inx = (tmp + 1)
                    else:
                        self.animation_downing_hand_do = True
                        self.animate_list_hand_downing_with_pistol_inx = 0
                        self.image = pygame.Surface(
                            (self.rect.width, self.rect.height))
                        self.image.set_alpha(0)                  
                        player.with_pistol = False
                if (self.shooting_time > 0 and 
                    self.animation_downing_hand_do and self.animation_do):
                    for i in range(3):
                        # print(self.shooting_time)
                        if self.shooting_time > 0:
                            tmp = self.animate_list_hand_shooting_with_pistol_inx
                            self.image = load_image(
                                self.animate_list_hand_shooting_with_pistol[tmp])
                            self.image = pygame.transform.scale(self.image, (
                                self.image.get_width() // 5, 
                                self.image.get_height() // 5))
                            self.rect = self.image.get_rect()
                            self.rect = player.rect
                            tmp += 1
                            tmp %= len(self.animate_list_hand_shooting_with_pistol)
                            self.animate_list_hand_shooting_with_pistol_inx = tmp
                            self.shooting_time -= 1
                else:
                    self.animate_list_hand_shooting_with_pistol_inx = 0
            # self.animation_do = False
            # print('ok2')
        # print(self.animate_list_hand_upping_with_pistol_inx)
        if player.reway and not self.rotate:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate = True
        elif not player.reway and self.rotate:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate = False
        # else:
        #    self.image = pygame.transform.flip(self.image, True, False)
        # self.animation_downing_hand_do and self.animation_do
        self.rect = player.rect
        # SCREEN.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.vector_x = 0
        self.vector_y = 0
        self.armor = 10
        self.hp = 10
        self.with_pistol = False
        self.pushing_time = 0
        self.image_hand = 0
        self.animate_list_move = sorted(['doomguy_going/' + elem
                 for elem in os.listdir('images/doomguy_going')
                 if os.path.isfile('images/doomguy_going/' + elem)])
        self.animate_list_move = ['doomguy_going/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_move))]
        self.animate_list_stand = sorted(['doomguy_standing/' + elem
                 for elem in os.listdir('images/doomguy_standing')
                 if os.path.isfile('images/doomguy_standing/' + elem)])
        self.animate_list_stand = ['doomguy_standing/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_stand))]        
        self.animate_list_jump = sorted(['doomguy_jumping/' + elem
                 for elem in os.listdir('images/doomguy_jumping')
                 if os.path.isfile('images/doomguy_jumping/' + elem)])
        self.animate_list_jump = ['doomguy_jumping/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_jump))]                
        self.hand_path = 'with_pistol_standing\hand\0.gif'
        # print(self.animate_list_hand_downing_with_pistol)
        # print(self.animate_list_hand_upping_with_pistol)
        # print(self.animate_list_hand_shooting_with_pistol)
        #################################################################
        self.animate_list_stand_not_hand = sorted([
            'with_pistol_standing/not_hand/' + elem
                 for elem in os.listdir('images/with_pistol_standing/not_hand')
                 if os.path.isfile(
                     'images/with_pistol_standing/not_hand/' + elem)])
        self.animate_list_stand_not_hand_inx = 0
        self.animate_list_stand_not_hand = [
            'with_pistol_standing/not_hand/{}.png'.format(i) 
            for i in range(len(self.animate_list_stand_not_hand))]        
        self.animate_list_move_not_hand = sorted([
            'with_pistol_going/not_hand/' + elem
                 for elem in os.listdir('images/with_pistol_going/not_hand')
                 if os.path.isfile(
                     'images/with_pistol_going/not_hand/' + elem)])
        self.animate_list_move_not_hand_inx = 0
        self.animate_list_move_not_hand = [
            'with_pistol_going/not_hand/{}.png'.format(i) 
                                  for i in range(
                                      len(self.animate_list_move_not_hand))]        
        self.animate_list_stand_not_hand = [
            'with_pistol_standing/not_hand/{}.png'.format(i) 
            for i in range(len(self.animate_list_stand_not_hand))]
        
        self.animate_list_jump_not_hand = sorted([
            'with_pistol_jumping/not_hand/' + elem
                 for elem in os.listdir('images/with_pistol_jumping/not_hand')
                 if os.path.isfile(
                     'images/with_pistol_jumping/not_hand/' + elem)])        
        self.animate_list_jump_not_hand = [
            'with_pistol_jumping/not_hand/{}.png'.format(i) 
                                  for i in range(
                                      len(self.animate_list_jump_not_hand))]        
        self.animate_list_jump_not_hand = [
            'with_pistol_jumping/not_hand/{}.png'.format(i) 
            for i in range(len(self.animate_list_jump_not_hand))]
        # print(sorted(self.animate_list_stand_not_hand))
        #################################################################
        self.image = load_image(self.animate_list_stand[0])
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 5, self.image.get_height() // 5))                
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(700, 200)
        self.animation_of_stand_inx = 1
        self.animation_of_move_inx = 0
        self.animation_of_jump_inx = 0
        self.v = 0
        self.reway = False
        self.must_make_hide = False
        self.must_make_hide_of_enemy = False
        self.must_make_hide_of_dead = False
        self.sound_type = ''
        self.sound = choice(SOUNDS['walking_on_metal'])
        self.step_const = randrange(3, 5)
        self.step_time = self.step_const
        self.tmp_for_sound_jump = 0
    
    def update(self, *args):     
        sprite_collide = pygame.sprite.spritecollideany(self, BLOCK_SPRITES)
        # print(self.must_make_hide)
        if args:
            if (self.must_make_hide or self.must_make_hide_of_enemy
                or self.must_make_hide_of_dead):
                self.image.set_alpha(0)
                print('ok')
                return
            for elem in WALL_SPRITES:
                if self.rect.colliderect(elem.rect):
                    if self.rect.x > elem.rect.x:
                        self.rect = self.rect.move(20, 0)
                    elif self.rect.x < elem.rect.x:
                        self.rect = self.rect.move(-20, 0)
                    else:
                        if self.reway:
                            self.rect = self.rect.move(20, 0)
                        else:
                            self.rect = self.rect.move(-20, 0)
                    return 
            if (not self.with_pistol and self.pushing_time <= 0):
                if args[0] == 'left':
                    self.sound_type = 'walk'
                    self.rect = self.rect.move(-14, 0)
                    self.vector_x = -14                    
                    self.image = load_image(
                        self.animate_list_move[self.animation_of_move_inx])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                    self.image = pygame.transform.flip(self.image, True, False)
                    length = len(self.animate_list_move)
                    tmp = self.animation_of_move_inx
                    self.animation_of_move_inx = (tmp + 1)
                    self.animation_of_move_inx %= length              
                    self.reway = True
                if args[0] == 'right':
                    self.sound_type = 'walk'
                    self.rect = self.rect.move(14, 0)
                    self.vector_x = 14                   
                    if self.reway:
                        self.reway = False
                        self.image = pygame.transform.flip(self.image, 
                                                           True, False)
                        self.animation_of_move_inx = 0
                    self.image = load_image(
                        self.animate_list_move[self.animation_of_move_inx])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                    length = len(self.animate_list_move)
                    tmp = self.animation_of_move_inx
                    self.animation_of_move_inx = (tmp + 1)
                    self.animation_of_move_inx %= length
                if args[0] == 'up':
                    # pygame.sprite.collide_mask(self, collide_object)                        
                    if pygame.sprite.spritecollideany(self, BLOCK_SPRITES):
                        self.v = -50
                        self.rect = self.rect.move(0, self.v)
                        self.vector_y = self.v               
                if not pygame.sprite.spritecollideany(self, BLOCK_SPRITES):
                    self.rect = self.rect.move(0, 10)
                    self.rect = self.rect.move(0, self.v)
                    self.vector_y = self.v 
                    if self.v <= 0:
                        self.v += 10
                    # print(self.v)
                    # print(args[1])
                    # print('jump')
                    if self.reway:
                        if len(args) > 1 and args[1] == 'left':
                            self.rect = self.rect.move(-20, 0)
                            self.vector_x = -20                            
                        tmp = self.animation_of_jump_inx
                        self.image = load_image(
                            self.animate_list_jump[tmp]) 
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))         
                        self.image = pygame.transform.flip(self.image, 
                                                           True, False)
                        length = len(self.animate_list_jump)
                        tmp = self.animation_of_jump_inx
                        self.animation_of_jump_inx = (tmp + 1)
                        self.animation_of_jump_inx %= length                                        
                    else:
                        if len(args) > 1 and args[1] == 'right':
                            self.rect = self.rect.move(20, 0)
                            self.vector_x = 20                           
                        # print('jump')
                        tmp = self.animation_of_jump_inx
                        self.image = load_image(
                            self.animate_list_jump[tmp]) 
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))                    
                        length = len(self.animate_list_jump)
                        tmp = self.animation_of_jump_inx
                        self.animation_of_jump_inx = (tmp + 1)
                        self.animation_of_jump_inx %= length      
                # print(self.animation_of_stand_inx, args)
                if (not args[0] 
                    and pygame.sprite.spritecollideany(self, BLOCK_SPRITES)):
                    # if self.animation_of_stand_inx < len(self.animate_list_stand)
                    self.vector_x = 0
                    self.vector_y = 0                    
                    if self.v <= 0:
                        self.v += 10
                    self.image = load_image(
                        self.animate_list_stand[self.animation_of_stand_inx])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                    if self.reway:
                        self.image = pygame.transform.flip(self.image, 
                                                           True, False)
                    length = len(self.animate_list_stand)
                    tmp = self.animation_of_stand_inx
                    self.animation_of_stand_inx = (tmp + 1)
                    self.animation_of_stand_inx %= length
                    # clock.tick(20)
                    # self.animate_list_hand_upping_with_pistol_inx = 0
            if (self.pushing_time > 0 or self.with_pistol):
                # print('ok3')
                # print('this', PLAYER_HAND)
                if args[0] == 'left':
                    self.sound_type = 'walk'
                    self.rect = self.rect.move(-14, 0)
                    self.vector_x = -14                    
                    length = len(self.animate_list_move_not_hand)
                    tmp = self.animation_of_move_inx
                    self.animation_of_move_inx = (tmp + 1)
                    self.animation_of_move_inx %= length                    
                    tmp = self.animation_of_move_inx
                    self.image = load_image(
                        self.animate_list_move_not_hand[tmp])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                    self.image = pygame.transform.flip(self.image, True, False)
                if args[0] == 'right':
                    self.sound_type = 'walk'
                    self.rect = self.rect.move(14, 0)
                    self.vector_x = 14                   
                    if self.reway:
                        self.reway = False
                        self.animation_of_move_inx = 0
                    length = len(self.animate_list_move_not_hand)
                    tmp = self.animation_of_move_inx
                    self.animation_of_move_inx = (tmp + 1)
                    self.animation_of_move_inx %= length
                    tmp = self.animation_of_move_inx
                    self.image = load_image(
                        self.animate_list_move_not_hand[tmp])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                if args[0] == 'up':
                    if pygame.sprite.spritecollideany(self, BLOCK_SPRITES):
                        self.v = -50
                        self.rect = self.rect.move(0, self.v)
                        self.vector_y = -50
                if not pygame.sprite.spritecollideany(self, BLOCK_SPRITES):
                    self.rect = self.rect.move(0, 10)
                    self.rect = self.rect.move(0, self.v)
                    self.vector_y = self.v
                    if self.v <= 0:
                        self.v += 10
                    # print(self.v)
                    # print(args[1])
                    # print('jump')
                    if self.reway:
                        if len(args) > 1 and args[1] == 'left':
                            self.rect = self.rect.move(-20, 0)
                            self.vector_x = -20                            
                        tmp = self.animation_of_jump_inx
                        length = len(self.animate_list_jump_not_hand)
                        self.animation_of_jump_inx = (tmp + 1)
                        self.animation_of_jump_inx %= length         
                        tmp = self.animation_of_jump_inx
                        self.image = load_image(
                            self.animate_list_jump_not_hand[tmp]) 
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))         
                        self.image = pygame.transform.flip(self.image, 
                                                           True, False)
                    else:
                        if len(args) > 1 and args[1] == 'right':
                            self.rect = self.rect.move(20, 0)
                            self.vector_x = 20                            
                        # print('jump')
                        tmp = self.animation_of_jump_inx
                        length = len(self.animate_list_jump_not_hand)
                        self.animation_of_jump_inx = (tmp + 1)
                        self.animation_of_jump_inx %= length         
                        tmp = self.animation_of_jump_inx
                        self.image = load_image(
                            self.animate_list_jump_not_hand[tmp]) 
                        self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 5, 
                            self.image.get_height() // 5))                        
                # print(self.animation_of_stand_inx, args)
                if (not args[0] 
                    and pygame.sprite.spritecollideany(self, BLOCK_SPRITES)):
                    # if self.animation_of_stand_inx < len(self.animate_list_stand)
                    # print('stand')
                    self.vector_x = 0
                    self.vector_y = 0                    
                    if self.v <= 0:
                        self.v += 10                    
                    tmp = self.animate_list_stand_not_hand_inx
                    self.image = load_image(
                        self.animate_list_stand_not_hand[tmp])
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 5, 
                        self.image.get_height() // 5))
                    if self.reway:
                        self.image = pygame.transform.flip(self.image, True, False)
                    length = len(self.animate_list_stand_not_hand)
                    self.animate_list_stand_not_hand_inx = (tmp + 1)
                    self.animate_list_stand_not_hand_inx %= length
                    # clock.tick(20)
        if not sprite_collide:
            self.tmp_for_sound_jump += 1
        if (self.sound_type == 'walk'
            and pygame.sprite.spritecollideany(self, BLOCK_SPRITES)):
            self.sound = choice(SOUNDS['walking_on_metal'])
            if self.step_time <= 0:
                self.step_const = randrange(3, 5)
                self.step_time = self.step_const
        else:
            self.sound_type = ''
        if self.v == -40:
            self.sound = SOUNDS['metal_jump']
            self.sound_type = 'jump'
        elif self.tmp_for_sound_jump > 3 and sprite_collide:
            self.sound = choice(SOUNDS['metal_landfall'])
            self.sound_type = 'landfall'    
            self.tmp_for_sound_jump = 0
        print('sound_type:', self.sound_type)
        if self.sound_type == '':
            self.sound.stop()
        elif self.sound_type == 'walk':
            self.sound.set_volume(0.9)
            if self.step_time == self.step_const:
                self.sound.play()
        elif self.sound_type == 'jump':
            self.sound.set_volume(0.9)
            self.sound.play()
        elif self.sound_type == 'landfall':
            self.sound.set_volume(0.9)
            self.sound.play()            
        self.sound_type = ''
        print('step_time:', self.step_time)
        self.step_time -= 1


def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print('Not found this image!')
        print(name)
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def receive_crop_image(surface, part_width, part_height, part_x, part_y):
    crop_part = pygame.Surface((part_width, part_height))
    crop_part.blit(surface, (-part_x, -part_y + 40))
    return crop_part


class Loader(pygame.sprite.Sprite):
    def __init__(self):
        self.animate_list = [
            'menu/loading/animation_loading_word/(loading).png',
            'menu/loading/animation_loading_word/(loading.).png',
            'menu/loading/animation_loading_word/(loading..).png',
            'menu/loading/animation_loading_word/(loading...).png'
        ]
        self.image = load_image(self.animate_list[0])
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(900, 0)
        self.animate_inx = 0
    
    def update(self):
        try:
            self.image = load_image(self.animate_list[
                self.animate_inx])
            self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 2, self.image.get_height() // 2))                        
            self.animate_inx += 1
        except Exception:
            self.animate_inx = 0
            self.image = load_image(self.animate_list[
                self.animate_inx])    
            self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 2, self.image.get_height() // 2))    


def load_game(): 
    load_screen = LoadScreen()
    gradient = load_image(
        'menu/loading/animation_loading_word/black_gradient_up.png')
    gradient = pygame.transform.scale(gradient, (WIDTH, 400))
    press_space = load_image(
        'menu/loading/animation_loading_word/press_space.png')
    press_space = pygame.transform.scale(press_space, (
        press_space.get_width() // 2, press_space.get_height() // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(load_screen.image, load_screen.rect)
        SCREEN.blit(gradient, (0, 0))
        SCREEN.blit(press_space, (650, 0))
        load_screen.update()
        # clock.tick(FPS)
        pygame.display.flip()       

def start_screen():
    sound = pygame.mixer.Sound('music/menu_sound.wav')
    sound.play(loops=-1)
    sound.set_volume(1)
    fon_image = load_image('menu/start_fon.png')
    ser = load_image('menu/particles/' + 'part000.jpg')
    video_list = ['menu/particles/' + elem
                  for elem in os.listdir('images/menu/particles')]
    # pprint(video_list)
    fon_image = pygame.transform.scale(fon_image, (WIDTH, HEIGHT))
    start_button = pygame.sprite.Sprite()
    start_button.image = load_image('menu/new_game/standart.png')
    start_button.image = pygame.transform.scale(start_button.image, 
                                                (300, 60))
    start_button.rect = start_button.image.get_rect()
    start_button.rect = start_button.rect.move(25, 170)
    continue_button = pygame.sprite.Sprite()
    continue_button.image = load_image('menu/continue/standart.png')
    continue_button.image = pygame.transform.scale(continue_button.image, 
                                                (300, 60))
    continue_button.rect = continue_button.image.get_rect()
    continue_button.rect = continue_button.rect.move(13, 230)
    customs_button = pygame.sprite.Sprite()
    customs_button.image = load_image('menu/customs/standart.png')
    customs_button.image = pygame.transform.scale(customs_button.image, 
                                                (300, 60))
    customs_button.rect = customs_button.image.get_rect()
    customs_button.rect = customs_button.rect.move(13, 350)
    load_game_button = pygame.sprite.Sprite()
    load_game_button.image = load_image('menu/load_game/standart.png')
    load_game_button.image = pygame.transform.scale(load_game_button.image, 
                                                (300, 60))
    load_game_button.rect = load_game_button.image.get_rect()
    load_game_button.rect = load_game_button.rect.move(26, 290)
    # print(start_button.rect == continue_button.rect)
    clock = pygame.time.Clock()
    exit_button = Button()
    exit_button.image = load_image('menu/exit/1.png')
    exit_button.image = exit_button.standart_image
    exit_button.rect = exit_button.image.get_rect()
    exit_button.rect = exit_button.rect.move(25, 410)
    exit_dialog = DialogWindow()
    exit_dialog.image = load_image('menu/exit/want_exit_fon.png')
    exit_dialog.image = pygame.transform.scale(exit_dialog.image, 
                                        (exit_dialog.image.get_width() // 2, 
                                        exit_dialog.image.get_height() // 2))
    exit_dialog.rect = exit_dialog.image.get_rect()
    exit_dialog.rect = exit_dialog.rect.move(350, 150)
    exit_dialog.need_show = False
    yes_button = YesButton()
    yes_button.image = load_image('menu/yes/yes.png')
    yes_button.image = yes_button.standart_image
    yes_button.rect = yes_button.image.get_rect()  
    yes_button.rect = yes_button.rect.move(380, 380)
    no_button = NoButton()
    no_button.image = load_image('menu/no/no.png')
    no_button.image = no_button.standart_image
    no_button.rect = no_button.image.get_rect()      
    no_button.rect = no_button.rect.move(700, 380)
    # print(video_list)
    video_list_inx = 0
    while True:
        if not exit_dialog.need_show:
            exit_button.check_cursor()
        exit_dialog.update()
        yes_button.check_cursor()
        no_button.check_cursor()
        for event in pygame.event.get():
            if (not exit_dialog.need_show 
                and exit_button.check_event(event) == 'mouse_click'):
                exit_dialog.need_show = True
            if (exit_dialog.need_show 
                and yes_button.check_event(event) == 'mouse_click'):
                terminate()
            if (exit_dialog.need_show 
                and no_button.check_event(event) == 'mouse_click'):
                exit_dialog.need_show = False
                exit_dialog.animation_inx = 0
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(continue_button.rect, start_button.rect, event.pos)
                if not exit_dialog.need_show:
                    if (event.pos[0] >= start_button.rect.x and 
                        event.pos[0] <= 
                        start_button.rect.x + start_button.rect.width):
                        if (event.pos[1] >= start_button.rect.y and 
                            event.pos[1] <= 
                            start_button.rect.y + start_button.rect.height):
                            sound.stop()
                            return 
            if event.type == pygame.MOUSEMOTION:
                flag = False
                if not exit_dialog.need_show:
                    if (event.pos[0] >= start_button.rect.x and 
                        event.pos[0] <= 
                        start_button.rect.x + start_button.rect.width):
                        if (event.pos[1] >= start_button.rect.y and 
                            event.pos[1] <= 
                            start_button.rect.y + start_button.rect.height):
                            flag = True
                            start_button.image = load_image(
                                'menu/new_game/hover.png')
                            start_button.image = pygame.transform.scale(
                                start_button.image, (320, 60))
                            start_button.rect = start_button.image.get_rect()
                            start_button.rect = start_button.rect.move(22, 175)                 
                    if not flag:
                        # print(event.pos)
                        start_button.image = load_image(
                            'menu/new_game/standart.png')
                        start_button.image = pygame.transform.scale(
                            start_button.image, (300, 60))
                        start_button.rect = start_button.image.get_rect()
                        start_button.rect = start_button.rect.move(25, 170)                    
                    flag = False
                    if (event.pos[0] >= continue_button.rect.x and 
                        event.pos[0] <= 
                        start_button.rect.x + continue_button.rect.width):
                        if (event.pos[1] >= continue_button.rect.y and 
                            event.pos[1] <= 
                            continue_button.rect.y + continue_button.rect.height):
                            flag = True
                            continue_button.image = load_image(
                                'menu/continue/hover.png')
                            continue_button.image = pygame.transform.scale(
                                continue_button.image, (300, 60))
                    if not flag:
                        # print(event.pos)
                        continue_button.image = load_image(
                            'menu/continue/standart.png')
                        continue_button.image = pygame.transform.scale(
                            continue_button.image, (300, 60))    
                    flag = False
                    if (event.pos[0] >= load_game_button.rect.x and 
                        event.pos[0] <= 
                        start_button.rect.x + load_game_button.rect.width):
                        if (event.pos[1] >= load_game_button.rect.y and 
                            event.pos[1] <= 
                            load_game_button.rect.y + load_game_button.rect.height):
                            flag = True
                            load_game_button.image = load_image(
                                'menu/load_game/hover.png')
                            load_game_button.image = pygame.transform.scale(
                                load_game_button.image, (300, 60))
                    if not flag:
                        # print(event.pos)
                        load_game_button.image = load_image(
                            'menu/load_game/standart.png')
                        load_game_button.image = pygame.transform.scale(
                            load_game_button.image, (300, 60))   
                    flag = False
                    if (event.pos[0] >= customs_button.rect.x and 
                        event.pos[0] <= 
                        customs_button.rect.x + customs_button.rect.width):
                        if (event.pos[1] >= customs_button.rect.y and 
                            event.pos[1] <= 
                            customs_button.rect.y + customs_button.rect.height):
                            flag = True
                            customs_button.image = load_image(
                                'menu/customs/hover.png')
                            customs_button.image = pygame.transform.scale(
                                customs_button.image, (300, 60))
                    if not flag:
                        # print(event.pos)
                        customs_button.image = load_image(
                            'menu/customs/standart.png')
                        customs_button.image = pygame.transform.scale(
                            customs_button.image, (300, 60))                 
        SCREEN.fill((0, 0, 0))
        particles = load_image(video_list[video_list_inx])
        particles = pygame.transform.scale(particles, (WIDTH, HEIGHT))
        # print(particles)
        video_list_inx = (video_list_inx + 1) % len(video_list)
        SCREEN.blit(particles, (0, 0))
        SCREEN.blit(fon_image, (0, 0))
        SCREEN.blit(start_button.image, start_button.rect)
        SCREEN.blit(continue_button.image, continue_button.rect)
        SCREEN.blit(load_game_button.image, load_game_button.rect)
        SCREEN.blit(customs_button.image, customs_button.rect)        
        SCREEN.blit(exit_button.image, exit_button.rect)        
        if exit_dialog.need_show:
            if exit_dialog.receive_next_image() != None:
                exit_dialog.image = exit_dialog.receive_next_image()
            SCREEN.blit(exit_dialog.image, exit_dialog.rect)
            if exit_dialog.receive_next_image() == None:
                SCREEN.blit(no_button.image, no_button.rect) 
                SCREEN.blit(yes_button.image, yes_button.rect) 
        pygame.display.flip()
        # clock.tick(FPS)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(ALL_SPRITES)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_v = 0
        self.bullet_y = 3
        self.step_const = 8
        self.step_time = self.step_const
        self.sound = SOUNDS['imp']['fireball']['flight']        
    
    def update(self, *args):
        self.rect = self.rect.move(self.bullet_v, 0)
        for elem in BLOCK_SPRITES:
            if self.rect.colliderect(elem.rect):
                self.kill()             
        if self.rect.colliderect(wall1.rect):
            self.kill()     
        if pygame.sprite.collide_mask(self, door1):
            self.kill()     
        if self.rect.colliderect(wall2.rect):
            self.kill()
        if self.rect.colliderect(wall3.rect):
            self.kill() 
        if pygame.sprite.collide_mask(self, door2):
            self.kill()     
        if pygame.sprite.collide_mask(self, stolb):
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)     


class FireBall(Bullet):
    def update(self, *args):
        self.rect = self.rect.move(self.bullet_v, self.bullet_y)
        for elem in BLOCK_SPRITES:
            if self.rect.colliderect(elem.rect):
                self.kill()               
        if self.rect.colliderect(wall1.rect):
            self.kill()     
        if pygame.sprite.collide_mask(self, door1):
            self.kill()     
        if self.rect.colliderect(wall2.rect):
            self.kill()
        if self.rect.colliderect(wall3.rect):
            self.kill() 
        if pygame.sprite.collide_mask(self, door2):
            self.kill() 
        if pygame.sprite.collide_mask(self, player):
            self.kill()
            if player.armor > 0:
                player.armor -= 2
                armor.update(player.armor)
            elif player.hp > 0:
                player.hp -= 2
                hp.update(player.hp)
        if pygame.sprite.collide_mask(self, stolb):
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)    
        if self.step_time <= 0:
            self.step_time = self.step_const
            self.sound.set_volume(0.05)
            self.sound.play()
        self.step_time -= 1


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj):
        if obj in INTERFACE_GROUP and player.rect.x > 545:
            if type(obj) == InterfaceWindow:
                obj.rect.x = player.rect.x - 560
            if type(obj) == Hp:
                obj.rect.x = player.rect.x + 320
            if type(obj) == Armor:
                obj.rect.x = player.rect.x + 335
            if type(obj) == WearonLogo:
                if obj.wearons['shoutgun']:
                    obj.rect.x = player.rect.x - 555
                else:
                    obj.rect.x = player.rect.x - 545
            if type(obj) == Ammo:
                obj.rect.x = player.rect.x - 300
        else:
            if obj != pol:
                obj.rect.x += self.dx
    
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


def func_pressed_space():
    if (player.with_pistol and player_hand.shooting_time == 0):
        # and global_shooting_time <= 0
        player_hand.shooting_time = 52
        global_shooting_time = 52
        pistol_patron_y = player.rect.y + 57
        if player.reway:
            pistol_patron_v = -40
            pistol_patron_x = player.rect.x - 10 * 2
        else:
            pistol_patron_v = 40
            pistol_patron_x = player.rect.x + 10 * 6
        pistol_bullet = Bullet(pistol_patron)
        pistol_bullet.rect.x = pistol_patron_x
        pistol_bullet.rect.y = pistol_patron_y
        pistol_bullet.bullet_v = pistol_patron_v
        ALL_SPRITES.add(pistol_bullet)
    elif not player.with_pistol:
        # print(player.pushing_time)
        # print('ok', debug_n)
        # debug_n += 1
        tmp = len(player_hand.animate_list_push)
        if (player.pushing_time <= 0):
            player_pushing = True
            player.pushing_time = 17   


class GameOverHead(pygame.sprite.Sprite):
    def __init__(self):
        self.animate_list_start = sorted(['menu/game_over/head_start' + elem
                 for elem in os.listdir('images/menu/game_over/head_start')
                 if os.path.isfile('images/menu/game_over/head_start/' + elem)])
        self.animate_list_start = ['menu/game_over/head_start/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_start))]
        self.animate_list_end = sorted(['menu/game_over/head_end' + elem
                 for elem in os.listdir('images/menu/game_over/head_end')
                 if os.path.isfile('images/menu/game_over/head_end/' + elem)])
        self.animate_list_end = ['menu/game_over/head_end/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_end))]
        self.image = load_image(self.animate_list_start[0])
        self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() // 2, 
                    self.image.get_height() // 2))        
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(120, -80)
        self.animate_inx = 0
    
    def update(self):
        if self.animate_list_start:
            self.image = load_image(self.animate_list_start[0])
            del self.animate_list_start[0]
            self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() // 2, 
                        self.image.get_height() // 2))                    
        else:
            try:
                self.image = load_image(self.animate_list_end[
                    self.animate_inx])
                self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 2, 
                            self.image.get_height() // 2))                        
                self.animate_inx += 1
            except Exception:
                self.animate_inx = 0
                self.image = load_image(self.animate_list_end[
                    self.animate_inx])    
                self.image = pygame.transform.scale(self.image, (
                            self.image.get_width() // 3, 
                            self.image.get_height() // 3))                        


def game_over():
    sound = SOUNDS['death_screen']
    sound.set_volume(1)
    sound.play(loops=-1)
    head = GameOverHead()
    fon_image1 = load_image('menu/game_over/die_fon_dark.png')
    fon_image1 = pygame.transform.scale(fon_image1, (WIDTH, HEIGHT))
    fon_image2 = load_image('menu/game_over/die_fon_red.png')
    fon_image2 = pygame.transform.scale(fon_image2, (WIDTH, HEIGHT))    
    exit_button = GameOverExitButton()
    exit_button.image = load_image('menu/exit/1.png')
    exit_button.image = exit_button.standart_image
    exit_button.rect = exit_button.image.get_rect()
    exit_button.rect = exit_button.rect.move(33, 500)
    start_in_control_button = StartInControlPointButton()
    start_in_control_button.image = start_in_control_button.standart_image
    start_in_control_button.rect = start_in_control_button.image.get_rect()
    start_in_control_button.rect = start_in_control_button.rect.move(48, 420)    
    button3 = ExitOnWorkTableButton()
    button3.image = button3.standart_image
    button3.rect = button3.image.get_rect()
    button3.rect = button3.rect.move(40, 460)
    exit_dialog = DialogWindow()
    exit_dialog.image = load_image('menu/exit/want_exit_fon.png')
    exit_dialog.image = pygame.transform.scale(exit_dialog.image, 
                                        (exit_dialog.image.get_width() // 2, 
                                        exit_dialog.image.get_height() // 2))
    exit_dialog.rect = exit_dialog.image.get_rect()
    exit_dialog.rect = exit_dialog.rect.move(350, 150)
    exit_dialog.need_show = False
    yes_button = YesButton()
    yes_button.image = load_image('menu/yes/yes.png')
    yes_button.image = yes_button.standart_image
    yes_button.rect = yes_button.image.get_rect()
    yes_button.rect = yes_button.rect.move(380, 380)
    no_button = NoButton()
    no_button.image = load_image('menu/no/no.png')
    no_button.image = no_button.standart_image
    no_button.rect = no_button.image.get_rect()      
    no_button.rect = no_button.rect.move(700, 380)
    while True:
        if not exit_dialog.need_show:
            exit_button.check_cursor()        
            start_in_control_button.check_cursor()        
            button3.check_cursor()        
        yes_button.check_cursor()
        no_button.check_cursor()
        for event in pygame.event.get():
            if not exit_dialog.need_show:
                if exit_button.check_event(event) == 'mouse_click':
                    exit_dialog.need_show = True
            if yes_button.check_event(event) == 'mouse_click':
                terminate()
            if no_button.check_event(event) == 'mouse_click':
                exit_dialog.need_show = False
                exit_dialog.animation_inx = 0
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(fon_image1, (0, 0))
        SCREEN.blit(fon_image2, (0, 0))
        SCREEN.blit(exit_button.image, exit_button.rect)
        SCREEN.blit(start_in_control_button.image, start_in_control_button.rect)
        SCREEN.blit(button3.image, button3.rect)
        SCREEN.blit(head.image, head.rect)
        # print(head.animate_list_start)
        if exit_dialog.need_show:
            if exit_dialog.receive_next_image() != None:
                exit_dialog.image = exit_dialog.receive_next_image()
            SCREEN.blit(exit_dialog.image, exit_dialog.rect)
            if exit_dialog.receive_next_image() == None:
                SCREEN.blit(no_button.image, no_button.rect) 
                SCREEN.blit(yes_button.image, yes_button.rect) 
        head.update()
        pygame.display.flip()    


# root = Tk()
# root.bind('<space>', print_info('space'))

def show_pause():
    sound = pygame.mixer.Sound('music/menu_sound.wav')
    sound.play(loops=-1)
    video_list = ['menu/particles_pause/' + elem
                  for elem in os.listdir('images/menu/particles_pause')]
    video_list_inx = 0
    fon_image = load_image('menu/pause_fon.png')
    fon_image = pygame.transform.scale(fon_image, (WIDTH, HEIGHT))
    continue_button = ContinueButton()
    continue_button.image = continue_button.standart_image
    continue_button.rect = continue_button.image.get_rect()
    continue_button.rect = continue_button.rect.move(25, 180)
    exit_button = Button()
    exit_button.image = load_image('menu/exit/1.png')
    exit_button.image = exit_button.standart_image
    exit_button.rect = exit_button.image.get_rect()
    exit_button.rect = exit_button.rect.move(33, 240)
    exit_dialog = DialogWindow()
    exit_dialog.image = load_image('menu/exit/want_exit_fon.png')
    exit_dialog.image = pygame.transform.scale(exit_dialog.image, 
                                        (exit_dialog.image.get_width() // 2, 
                                        exit_dialog.image.get_height() // 2))
    exit_dialog.rect = exit_dialog.image.get_rect()
    exit_dialog.rect = exit_dialog.rect.move(350, 150)
    exit_dialog.need_show = False
    yes_button = YesButton()
    yes_button.image = load_image('menu/yes/yes.png')
    yes_button.image = yes_button.standart_image
    yes_button.rect = yes_button.image.get_rect()
    yes_button.rect = yes_button.rect.move(380, 380)
    no_button = NoButton()
    no_button.image = load_image('menu/no/no.png')
    no_button.image = no_button.standart_image
    no_button.rect = no_button.image.get_rect()      
    no_button.rect = no_button.rect.move(700, 380)
    player_image = receive_crop_image(SCREEN, 120, 190, 
                                      player.rect.x, player.rect.y)
    player_image.blit(player.image, (20, 40))
    player_image.blit(player_hand.image, (20, 40))
    player_image = pygame.transform.scale(player_image, 
                                          (player_image.get_width() * 3, 
                                           player_image.get_height() * 3))
    while True:
        if not exit_dialog.need_show:
            exit_button.check_cursor()        
            continue_button.check_cursor()
        yes_button.check_cursor()
        no_button.check_cursor()
        for event in pygame.event.get():
            if not exit_dialog.need_show:
                if continue_button.check_event(event) == 'mouse_click':
                    sound.stop()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sound.stop()
                        return
                if exit_button.check_event(event) == 'mouse_click':
                    exit_dialog.need_show = True
            if yes_button.check_event(event) == 'mouse_click':
                terminate()
            if no_button.check_event(event) == 'mouse_click':
                exit_dialog.need_show = False
                exit_dialog.animation_inx = 0
            if event.type == pygame.QUIT:
                terminate()
        particles = load_image(video_list[video_list_inx])
        particles = pygame.transform.scale(particles, (WIDTH, HEIGHT))
        video_list_inx = (video_list_inx + 1) % len(video_list)
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(player_image, (750, 10))
        SCREEN.blit(particles, (0, 0))
        SCREEN.blit(fon_image, (0, 0))
        SCREEN.blit(continue_button.image, continue_button.rect)
        SCREEN.blit(exit_button.image, exit_button.rect)
        if exit_dialog.need_show:
            if exit_dialog.receive_next_image() != None:
                exit_dialog.image = exit_dialog.receive_next_image()
            SCREEN.blit(exit_dialog.image, exit_dialog.rect)
            if exit_dialog.receive_next_image() == None:
                SCREEN.blit(no_button.image, no_button.rect) 
                SCREEN.blit(yes_button.image, yes_button.rect) 
        pygame.display.flip()


class Room:
    def __init__(self, enemys):
        self.activated = False
        self.enemys = pygame.sprite.Group()
        enemys[0].rect = enemys[0].rect.move(300, 100)
        enemys[1].rect = enemys[1].rect.move(600, 100)
        '''enemys[2].rect = enemys[2].rect.move(200, 200)        
        enemys[3].rect = enemys[3].rect.move(400, 200)        
        enemys[4].rect = enemys[4].rect.move(500, 200)             
        enemys[5].rect = enemys[5].rect.move(600, 200)             
        enemys[6].rect = enemys[6].rect.move(700, 200)'''
        for elem in enemys:
            self.enemys.add(elem)
    
    def active(self):
        self.activated = True
        print('len self.enemys =', len(self.enemys))
        for elem in self.enemys:
            ALL_SPRITES.add(elem)
        
    def all_enemys_dead(self):
        if not self.enemys:
            return True
        return False


class Room2(Room):
    def __init__(self, enemys):
        self.activated = False
        self.enemys = pygame.sprite.Group()
        '''enemys[0].rect = enemys[0].rect.move(1650, 100)
        enemys[1].rect = enemys[1].rect.move(2050, 200)        
        enemys[2].rect = enemys[2].rect.move(2450, 200)        
        enemys[3].rect = enemys[3].rect.move(1500, 200)             
        enemys[4].rect = enemys[4].rect.move(1600, 200)             
        enemys[5].rect = enemys[5].rect.move(1700, 200)'''
        for elem in enemys:
            self.enemys.add(elem)    


class Room3(Room):
    def __init__(self, enemys):
        self.activated = False
        self.enemys = pygame.sprite.Group()
        enemys[0].rect = enemys[0].rect.move(5500, 100)
        '''enemys[1].rect = enemys[1].rect.move(6500, 200)        
        enemys[2].rect = enemys[2].rect.move(7200, 200)        
        enemys[3].rect = enemys[3].rect.move(1500, 200)             
        enemys[4].rect = enemys[4].rect.move(1600, 200)             
        enemys[5].rect = enemys[5].rect.move(1700, 200)'''
        for elem in enemys:
            self.enemys.add(elem)    


class LoadScreen(pygame.sprite.Sprite):
    def __init__(self):
        self.animate_list = sorted(['menu/loading/animation_picture' + elem
                 for elem in os.listdir('images/menu/loading/animation_picture')
                 if os.path.isfile('images/menu/loading/animation_picture/' + 
                                   elem)])
        self.animate_list = ['menu/loading/animation_picture/{}.png'.format(i) 
                                  for i in range(len(self.animate_list))]
        self.image = load_image(self.animate_list[0])
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)
        self.animate_inx = 0
    
    def update(self):
        try:
            self.image = load_image(self.animate_list[
                self.animate_inx])
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))                        
            self.animate_inx += 1
        except Exception:
            self.animate_inx = 0
            self.image = load_image(self.animate_list[
                self.animate_inx])    
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))




################################################################################
##########################GameWithArcadeLibrary#################################
################################################################################
            
import arcade
import os

SPRITE_SCALING = 0.5
RIGHT_FACING = 0
LEFT_FACING = 1
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "DOOM 2D"
CHARACTER_SCALING = 0.4
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100
PLAYER_MOVEMENT_SPEED = 14
GRAVITY = 1
PLAYER_JUMP_SPEED = 25

VIEWPORT_MARGIN = 40

MOVEMENT_SPEED = 5

def load_texture_pair(filename):
    try:
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]
    except Exception:
        print('NotFoundImage')


class ArcadePlayer(arcade.Sprite):
    def __init__(self, walk_textures):
        super().__init__()
        self.face_direction = RIGHT_FACING
        self.walk_inx = 0
        self.scale = CHARACTER_SCALING
        self.walk_textures = walk_textures
        self.texture = self.walk_textures[0][self.face_direction]
        self.set_hit_box(self.texture.hit_box_points)
    
    def update_animation(self, delta_time: float = 0.00003):
        if self.change_x != 0:
            if self.change_x < 0:
                self.face_direction = LEFT_FACING
            if self.change_x > 0:
                self.face_direction = RIGHT_FACING
            try:
                self.texture = self.walk_textures[self.walk_inx][self.face_direction]
                self.walk_inx += 1
            except Exception:
                self.walk_inx = 0
                self.texture = self.walk_textures[self.walk_inx][self.face_direction]
                self.walk_inx += 1


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 
                         fullscreen=True)
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.AMAZON)
        self.doomguy_walking = []
        for elem in os.listdir('images/doomguy_going'):
            texture = load_texture_pair('images/doomguy_going/{}'.format(elem))
            self.doomguy_walking.append(texture)   
        self.animations = {
            'doomguy': {
                'walking': self.doomguy_walking
            }
        }        
        self.textures = {
            'lift': {
                'hall-background': arcade.load_texture(
                    "images/locations/lift/fon.png"),
                'over-door': arcade.load_texture(
                    'images/locations/lift/over_door.png'),
                'spusk-lift': arcade.load_texture(
                    'images/locations/lift/spusk_lift.png'),
                'stolb': arcade.load_texture(
                    'images/locations/lift/stolb.png'),
            }
        }
        self.sprite_image_paths = {
            'lift': {
                'ceiling': 'images/locations/komnata/ceiling.png', 
                'pol': 'images/locations/komnata/ceiling.png',
                'door': 'images/locations/lift/door/animation/{}'.format(
                    os.listdir('images/locations/lift/door/animation')[0]),
                'spusk-door': 'images/locations/lift/lift_all.png'
            }
        }
        self.view_bottom = 0
        self.view_left = 0        
        self.player_list = None
        self.wall_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.jump_pressed = False
        self.move_left = False
        self.move_right = False
        self.player_sprite = ArcadePlayer(self.animations['doomguy']['walking'])

    def setup(self):
        self.view_bottom = 0
        self.view_left = 0        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        player_image_source = 'images/doomguy_going/0.png'
        self.lift_ceiling = arcade.Sprite(
            self.sprite_image_paths['lift']['ceiling'], 0.69)
        self.lift_pol = arcade.Sprite(
            self.sprite_image_paths['lift']['pol'], 0.83)
        self.lift_door = arcade.Sprite(
            self.sprite_image_paths['lift']['door'], 0.57)
        self.spusk_door = arcade.Sprite(
            self.sprite_image_paths['lift']['spusk-door'], 0.57)        
        self.lift_door.center_x = -200
        self.lift_door.center_y = 333
        self.spusk_door.center_x = 1620
        self.spusk_door.center_y = 410
        self.lift_pol.center_x = 556
        self.lift_pol.center_y = 2      
        self.lift_ceiling.center_x = 710
        self.lift_ceiling.center_y = 765                
        self.wall_list.append(self.lift_ceiling) 
        self.wall_list.append(self.lift_pol) 
        self.wall_list.append(self.lift_door) 
        self.wall_list.append(self.spusk_door) 
        self.player_sprite.center_x = 364
        self.player_sprite.center_y = 428
        self.player_list.append(self.player_sprite) 
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, 
                                                         self.wall_list, 
                                                         GRAVITY)
        
    def on_draw(self):
        arcade.start_render()           
        width = self.textures['lift']['spusk-lift'].width * 0.45
        height = self.textures['lift']['spusk-lift'].height * 0.45
        arcade.draw_texture_rectangle(
            1630, 400, width, height, self.textures['lift']['spusk-lift'])                 
        width = self.textures['lift']['hall-background'].width * 0.7
        height = self.textures['lift']['hall-background'].height * 0.7
        arcade.draw_texture_rectangle(
            700, 400, width, height, self.textures['lift']['hall-background'])
        width = self.textures['lift']['over-door'].width * 0.6
        height = self.textures['lift']['over-door'].height * 0.6
        arcade.draw_texture_rectangle(
            -207, 639, width, height, self.textures['lift']['over-door'])        
        self.player_list.draw()
        self.wall_list.draw()
        width = self.textures['lift']['stolb'].width * 0.6
        height = self.textures['lift']['stolb'].height * 0.6
        arcade.draw_texture_rectangle(
            0, 500, width, height, self.textures['lift']['stolb'])                
        left, screen_width, bottom, screen_height = self.get_viewport()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
            self.move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            self.move_right = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.jump_pressed = False
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.F12:
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.jump_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.move_left = True
            self.move_right = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.move_right = True
            self.move_left = False
    
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update_animation(delta_time)
        changed = False
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.jump_pressed and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if self.move_right:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        if self.move_left:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def arcade_main():
    window = MyGame()
    window.setup()
    arcade.run()

################################################################################
################################################################################
################################################################################



if __name__ == '__main__':
    arcade_main()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    wearon_1 = Key('training/first_weapon_1.png')
    wearon_1.rect = wearon_1.rect.move(-20, 140)
    wearon_1.key = 'wearon'
    TRAINING_SPRITES.add(wearon_1)
    wearon_2 = Key('training/second_weapon_1.png')
    wearon_2.rect = wearon_2.rect.move(100, 140)
    wearon_2.key = 'wearon2'
    TRAINING_SPRITES.add(wearon_2)    
    wearon_3 = Key('training/third_weapon_1.png')
    wearon_3.rect = wearon_3.rect.move(220, 140)
    wearon_3.key = 'wearon3'
    TRAINING_SPRITES.add(wearon_3)        
    key_move_left = Key('training/left_1.png')
    key_move_left.rect = key_move_left.rect.move(380, 140)
    key_move_left.key = 'left'
    TRAINING_SPRITES.add(key_move_left)   
    key_move_up = Key('training/up_1.png')
    key_move_up.rect = key_move_up.rect.move(500, 140)
    key_move_up.key = 'up'
    TRAINING_SPRITES.add(key_move_up)        
    key_move_r = Key('training/right_1.png')
    key_move_r.rect = key_move_r.rect.move(620, 140)
    key_move_r.key = 'right'
    TRAINING_SPRITES.add(key_move_r)    
    key_space = Key('training/space_1.png')
    key_space.rect = key_space.rect.move(790, 120)
    key_space.key = 'space'
    TRAINING_SPRITES.add(key_space)
    key_word_wearon_1 = Text('training/words/weapon_1.png')
    key_word_wearon_1.rect = key_word_wearon_1.rect.move(30, 150)
    key_word_wearon_1.key = 'wearon'
    TRAINING_SPRITES.add(key_word_wearon_1)
    key_word_wearon_2 = Text('training/words/weapon_2.png')
    key_word_wearon_2.rect = key_word_wearon_2.rect.move(145, 150)
    key_word_wearon_2.key = 'wearon2'
    TRAINING_SPRITES.add(key_word_wearon_2)    
    key_word_wearon_3 = Text('training/words/weapon_3.png')
    key_word_wearon_3.rect = key_word_wearon_3.rect.move(260, 150)
    key_word_wearon_3.key = 'wearon3'
    TRAINING_SPRITES.add(key_word_wearon_3)        
    key_word_left = Text('training/words/left_word.png')
    key_word_left.rect = key_word_left.rect.move(435, 160)
    key_word_left.key = 'left'
    TRAINING_SPRITES.add(key_word_left)            
    key_word_jump = Text('training/words/jump_word.png')
    key_word_jump.rect = key_word_jump.rect.move(555, 160)
    key_word_jump.key = 'up'
    TRAINING_SPRITES.add(key_word_jump)                  
    key_word_right = Text('training/words/right_word.png')
    key_word_right.rect = key_word_right.rect.move(670, 160)
    key_word_right.key = 'right'
    TRAINING_SPRITES.add(key_word_right)              
    key_word_shoot_punch = Text('training/words/shoot_punch.png')
    key_word_shoot_punch.rect = key_word_shoot_punch.rect.move(840, 150)
    key_word_shoot_punch.key = 'space'
    TRAINING_SPRITES.add(key_word_shoot_punch)             
    loader = Loader()
    # start_screen()
    sound = choice(SOUNDS['gameplay'])
    sound.set_volume(1)
    sound_channel = sound.play(loops=-1)
    clock = pygame.time.Clock()
    load_screen = LoadScreen()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    load_screen.update()
    # clock.tick(FPS)
    pygame.display.flip()
    potolok = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((2247, 400))
    tmp_image.blit(potolok.image, (0, 0))
    potolok.image = tmp_image
    potolok.image = pygame.transform.scale(potolok.image, (
        potolok.image.get_width() // 2 + 2500, potolok.image.get_height() // 2))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    load_screen.update()
    # clock.tick(FPS)
    pygame.display.flip()    
    potolok.rect = potolok.image.get_rect()
    potolok.rect = potolok.rect.move(0, -100)
    potolok.mask = pygame.mask.from_surface(potolok.image)
    BLOCK_SPRITES.add(potolok)
    pol = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((24000, 300))
    tmp_image.set_alpha(0)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    pol.image = tmp_image
    pol.image = pygame.transform.scale(pol.image, (
        pol.image.get_width() // 2, pol.image.get_height() // 2))
    pol.rect = pol.image.get_rect()
    pol.rect = pol.rect.move(-8000, 433)
    pol.mask = pygame.mask.from_surface(pol.image)
    pol.image.fill((255, 0, 0))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    BLOCK_SPRITES.add(pol)
    wall1 = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((40, 2000))
    # tmp_image.set_alpha(0)
    wall1.image = tmp_image
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    wall1.image = pygame.transform.scale(wall1.image, (
        wall1.image.get_width() // 2, wall1.image.get_height() // 2))
    wall1.rect = wall1.image.get_rect()
    wall1.rect = wall1.rect.move(-20, 0)
    wall3 = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((100, 300))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    wall3.image = tmp_image
    # tmp_image.set_alpha(0)
    wall3.image.fill((255, 0, 0))
    wall3.rect = wall3.image.get_rect()
    wall3.rect = wall3.rect.move(6300, 360)
    wall3.mask = pygame.mask.from_surface(wall3.image)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    WALL_SPRITES.add(wall1)
    WALL_SPRITES.add(wall3)
    wall2 = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((75, 2000))
    # tmp_image.set_alpha(0)
    wall2.image = tmp_image
    tmp_image.set_alpha(0)
    wall2.image.fill((255, 0, 0))
    wall2.rect = wall2.image.get_rect()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    wall2.rect = wall2.rect.move(8160, 0)
    WALL_SPRITES.add(wall2)
    # ALL_SPRITES.add(door1)
    pygame.init()
    running = True
    door1 = Door('locations/start_location/door_1/door_animation/0.png')
    door1.image = pygame.transform.scale(door1.image, 
                                         (door1.image.get_width() // 2, 
                                          door1.image.get_height() // 2))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    door1.rect = door1.image.get_rect()
    door1.rect = door1.rect.move(954, 168)           
    boina_fon = GameObject('locations/boina/3-fon.png')
    boina_fon.image = pygame.transform.scale(boina_fon.image, 
                                        (boina_fon.image.get_width() // 3, 
                                        boina_fon.image.get_height() // 3))
    boina_fon.rect = boina_fon.image.get_rect()
    boina_fon.rect = boina_fon.rect.move(6390, -16)        
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    descent = GameObject('locations/boina/2-.png')
    descent.image = pygame.transform.scale(descent.image, 
                                        (descent.image.get_width() // 3, 
                                        descent.image.get_height() // 3))
    descent.rect = descent.image.get_rect()
    descent.rect = descent.rect.move(6390, -16)            
    boina_fon2 = GameObject('locations/boina/1-fon.png')
    boina_fon2.image = pygame.transform.scale(boina_fon2.image, 
                                        (boina_fon2.image.get_width() // 3, 
                                        boina_fon2.image.get_height() // 3))  
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    boina_fon2.rect = boina_fon2.image.get_rect()
    boina_fon2.rect = boina_fon2.rect.move(6390, -16)          
    room_fon = GameObject('locations/komnata/3-fon.png')
    room_fon.image = pygame.transform.scale(room_fon.image, 
                                        (room_fon.image.get_width() // 2, 
                                        room_fon.image.get_height() // 2))  
    room_fon.rect = room_fon.image.get_rect()
    room_fon.rect = room_fon.rect.move(5254, -156)    
    room_fon2 = GameObject('locations/komnata/1-fon.png')
    room_fon2.image = pygame.transform.scale(room_fon2.image, 
                                        (room_fon2.image.get_width() // 2, 
                                        room_fon2.image.get_height() // 2))  
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    room_fon2.rect = room_fon2.image.get_rect()
    room_fon2.rect = room_fon2.rect.move(5254, -156)        
    room_pol = GameObject('locations/komnata/pol.png')
    room_pol.image = pygame.transform.scale(room_pol.image, 
                                        (room_pol.image.get_width() // 2 + 80, 
                                        room_pol.image.get_height() // 2))  
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    room_pol.rect = room_pol.image.get_rect()
    room_pol.mask = pygame.mask.from_surface(room_pol.image)
    room_pol.rect = room_pol.rect.move(5254, 334)
    BLOCK_SPRITES.add(room_pol)
    room_ceiling = GameObject('locations/komnata/ceiling.png')
    room_ceiling.image = pygame.transform.scale(room_ceiling.image, 
                                        (room_ceiling.image.get_width() // 2 + 70, 
                                        room_ceiling.image.get_height() // 2))  
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    room_ceiling.rect = room_ceiling.image.get_rect()
    room_ceiling.rect = room_ceiling.rect.move(5264, -80)          
    door2 = PerehodDoor('locations/perehod/door_image.png')
    door2.image = pygame.transform.scale(door2.image, 
                                         (door2.image.get_width() // 2, 
                                          door2.image.get_height() // 2))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    door2.standart_image = door2.image
    door2.rect = door2.image.get_rect()
    door2.rect = door2.rect.move(5220, 6)        
    perehod_2_pol_2 = GameObject('locations/perehod/2-po1_cut.png')
    perehod_2_pol_2.image = pygame.transform.scale(perehod_2_pol_2.image, 
                                        (perehod_2_pol_2.image.get_width() // 2, 
                                        perehod_2_pol_2.image.get_height() // 2))  
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    perehod_2_pol_2.rect = perehod_2_pol_2.image.get_rect()
    BLOCK_SPRITES.add(perehod_2_pol_2)
    # ALL_SPRITES.add(platform)
    SCREEN.fill((0, 0, 0))
    player = Player()
    player_hand = Hand()
    player_dead = PlayerDead()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    PLAYER_GROUP.add(player)
    PLAYER_GROUP.add(player_hand)
    ALL_SPRITES.add(player)
    ALL_SPRITES.add(pol)    
    moving_player = False
    way = ''
    pygame.key.set_repeat(10, 10)
    count_jumps = 0
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    jumping_way = ''
    count_updates_of_hand = 0
    hand_reway = False
    time_shooting = 0
    pistol_patron = load_image('pistol_patron.png')
    pistol_patron = pygame.transform.scale(pistol_patron, 
                                           (pistol_patron.get_width() // 18, 
                                          pistol_patron.get_height() // 18))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    pistol_patron_x = player.rect.x
    pistol_patron_y = player.rect.y + 57
    pistol_patron_v = 20
    pistol_shooting = False
    global_shooting_time = 0
    player_pushing = False
    level_fon = pygame.Surface((8482, HEIGHT))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    start_room = load_image('locations/start_location/fon.png')
    start_room = pygame.transform.scale(start_room, 
                                        (start_room.get_width() // 2, 
                                         start_room.get_height() // 2))
    place_for_costume_fon = load_image('locations/place_for_costume/3-fon.png')
    place_for_costume_fon = pygame.transform.scale(place_for_costume_fon, 
                                        (place_for_costume_fon.get_width() // 2, 
                                         place_for_costume_fon.get_height() // 2
                                          + 100))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    start_room_fon_pol = load_image('locations/start_location/pol.png')
    start_room_fon_pol = pygame.transform.scale(start_room_fon_pol, 
                                        (start_room_fon_pol.get_width() // 2, 
                                         start_room_fon_pol.get_height() // 2))  
    start_room_fon_pol_mask = pygame.mask.from_surface(start_room_fon_pol)
    # ALL_SPRITES.add(demonical)
    # ALL_SPRITES.add(imp)
    stolb = GameObject('locations/start_location/stolb.png')
    stolb.image = pygame.transform.scale(stolb.image, 
                                         (stolb.image.get_width() // 2, 
                                           stolb.image.get_height() // 2))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    stolb.rect = stolb.rect.move(210, 0)
    stolb.mask = pygame.mask.from_surface(stolb.image)
    place_for_costume_pol = load_image('locations/place_for_costume/2-pol.png')
    place_for_costume_pol = pygame.transform.scale(place_for_costume_pol, 
                                        (place_for_costume_pol.get_width() // 2, 
                                         place_for_costume_pol.get_height() // 2
                                         ))
    light_in_place_for_costume = load_image(
        'locations/place_for_costume/1-light.png')
    light_in_place_for_costume = pygame.transform.scale(
        light_in_place_for_costume, (light_in_place_for_costume.get_width() // 2, 
                                light_in_place_for_costume.get_height() // 2
                                    ))
    surf = pygame.Surface((place_for_costume_pol.get_width(), 
                           place_for_costume_pol.get_height() - 100))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    surf.blit(place_for_costume_pol, (0, -100))
    place_for_costume_pol = surf
    sarc_image = load_image('locations/start_location/sarkofag.png')
    sarc_image = pygame.transform.scale(sarc_image, 
                                        (sarc_image.get_width() // 2, 
                                        sarc_image.get_height() // 2 + 40))
    perehod_1_fon = load_image('locations/perehod/3-fon.png')
    perehod_1_fon = pygame.transform.scale(perehod_1_fon, 
                                        (perehod_1_fon.get_width() // 2, 
                                        perehod_1_fon.get_height() // 2 + 380))
    perehod_1_pol = load_image('locations/perehod/2-pol.png')
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    perehod_1_pol = pygame.transform.scale(perehod_1_pol, 
                                        (perehod_1_pol.get_width() // 2, 
                                        perehod_1_pol.get_height() // 2 + 100))
    surf = pygame.Surface((perehod_1_pol.get_width() - 1753, 
                           perehod_1_pol.get_height() - 640))
    surf.blit(perehod_1_pol, (-165, -595))
    perehod_1_pol = surf
    perehod_1_pol = pygame.transform.scale(perehod_1_pol, 
                                        (perehod_1_pol.get_width(), 
                                        perehod_1_pol.get_height() + 15))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    perehod_2_pol = GameObject('locations/perehod/2-pol-3.png')
    perehod_2_pol.image = pygame.transform.scale(perehod_2_pol.image, 
                                        (perehod_2_pol.image.get_width() // 2, 
                                        perehod_2_pol.image.get_height() // 2 + 60))    
    sarc_rect = sarc_image.get_rect()
    sarc_rect = sarc_rect.move(0, -120)
    # print(sarc_rect)
    level_fon.blit(start_room, (0, -100))
    level_fon.blit(start_room_fon_pol, (0, -100))
    level_fon.blit(sarc_image, sarc_rect)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    level_fon.blit(place_for_costume_pol, (1220, 168))
    level_fon.blit(place_for_costume_fon, (1220, -10))
    level_fon.blit(light_in_place_for_costume, (1220, 60))
    level_fon.blit(perehod_1_fon, (1870, -320))
    level_fon.blit(perehod_1_pol, (2040, 439))
    perehod_2_pol.mask = pygame.mask.from_surface(perehod_2_pol.image)
    perehod_2_pol.rect = perehod_2_pol.rect.move(3890, 265)
    perehod_2_pol_2.rect = perehod_2_pol_2.rect.move(4285, 335)
    time = 0
    pressing_K_L = False
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    pressing_K_R = False
    pressing_K_e = False
    debug_n = 0
    # k = 3800
    # door1.rect = door1.rect.move(-k, 0)
    stolb.rect = stolb.rect.move(800, 0)
    player_path = 0
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    load_screen.update()
    # clock.tick(FPS)
    pygame.display.flip()    
    camera = Camera()
    w = 22
    h = 30
    x = 3895
    y = 434
    ladders = pygame.sprite.Group()
    interface_window = InterfaceWindow()
    hp = Hp()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    armor = Armor()
    wearon_logo = WearonLogo()
    ammo = Ammo()
    room_1_enemys = Room([Imp(), GameOpponent()]) #GameOpponent(), 
    room_2_enemys = Room2([]) #Imp(), GameOpponent(), Imp(), Imp()
    main_enemy = Imp()
    room_3_enemys = Room3([main_enemy])
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip() 
    ALL_SPRITES.add(interface_window)
    ALL_SPRITES.add(hp)
    ALL_SPRITES.add(armor)
    ALL_SPRITES.add(wearon_logo)
    ALL_SPRITES.add(ammo)
    INTERFACE_GROUP.add(interface_window)
    INTERFACE_GROUP.add(hp)
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()    
    INTERFACE_GROUP.add(armor)
    INTERFACE_GROUP.add(wearon_logo)
    INTERFACE_GROUP.add(ammo)
    for i in range(18):
        block = pygame.sprite.Sprite()
        block.rect = pygame.Rect(x, y, w, h)
        block.image = pygame.Surface((block.rect.width, block.rect.height))
        block.image.fill((255, 0, 0))
        block.image.set_alpha(0)
        ALL_SPRITES.add(block)
        ladders.add(block)
        BLOCK_SPRITES.add(block)
        x += w
        y -= 6
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(load_screen.image, load_screen.rect)
    load_screen.update()
    SCREEN.blit(loader.image, loader.rect)
    loader.update()    
    # clock.tick(FPS)
    pygame.display.flip()
    pauseform = PauseForm()
    load_game()
    if sound == SOUNDS['gameplay'][1]:
        sound.set_volume(0.05)
    else:
        sound.set_volume(0.4)    
    while running:
        TRAINING_SPRITES.update('visible')        
        sound_channel.queue(choice(SOUNDS['gameplay']))
        # print(demonical.print_info())
        pauseform.pressing_Esc = False
        for elem in ALL_SPRITES:
            if pygame.sprite.spritecollideany(elem, ladders):
                if (type(elem) == Imp or type(elem) == Player 
                    or type(elem) == GameOpponent):
                    elem.rect = elem.rect.move(0, -20)
        # root.bind('up', print('up', end=' '))
        # root.bind('left', print('left'))
        # print(keyboard.is_pressed('space'), keyboard.is_pressed('a'),
        #      keyboard.is_pressed('right'), keyboard.is_pressed('w'))
        # print(player_hand.shooting_time)
        # print(key)
        if keyboard.is_pressed('space'):
            func_pressed_space()
        if keyboard.is_pressed('up'):
            way = 'up'
            for elem in PLAYER_GROUP:
                if pygame.sprite.spritecollideany(elem, BLOCK_SPRITES):
                    count_jumps = 16
        '''if keyboard.is_pressed('left'):
            # print('ok')
            way = 'left'
            jumping_way = 'left'
            pressing_K_L = True'''
        camera.update(player)
        player_path += camera.dx
        if player_path >= 31:
            player_path -= camera.dx
            camera.dx = 0        
        pressing_K_e = False
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(level_fon, (player_path, 0))
        for sprite in ALL_SPRITES:
            if sprite != pol and sprite != player_hand:
                camera.apply(sprite)
        # print(jumping_way)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                TRAINING_SPRITES.update('wearon')            
            if keys[pygame.K_2]:
                TRAINING_SPRITES.update('wearon2')
            if keys[pygame.K_3]:
                TRAINING_SPRITES.update('wearon3')
            if keys[pygame.K_SPACE]:
                TRAINING_SPRITES.update('space')
            wearon_logo.receive_wearon(event)
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_UP]:
                way = 'up'
                for elem in PLAYER_GROUP:
                    if pygame.sprite.spritecollideany(elem, BLOCK_SPRITES):
                        count_jumps = 16   
                print('up')
                TRAINING_SPRITES.update('up')
            if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                way = 'up'
                for elem in PLAYER_GROUP:
                    if pygame.sprite.spritecollideany(elem, BLOCK_SPRITES):
                        count_jumps = 16                
                jumping_way = 'left'
                pressing_K_L = True 
                player.reway = True
            elif keys[pygame.K_LEFT]:
                TRAINING_SPRITES.update('left')
                way = 'left'
                jumping_way = 'left'
                pressing_K_L = True    
                player.reway = True
            elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                way = 'up'
                for elem in PLAYER_GROUP:
                    if pygame.sprite.spritecollideany(elem, BLOCK_SPRITES):
                        count_jumps = 16                
                jumping_way = 'right'             
                pressing_K_R = True         
                player.reway = False
            elif keys[pygame.K_RIGHT]:
                TRAINING_SPRITES.update('right')
                way = 'right'
                jumping_way = 'right'
                pressing_K_R = True
                player.reway = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    func_pressed_space()                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    pressing_K_e = True
                if event.key == pygame.K_ESCAPE:
                    sound_channel.pause()
                    show_pause()
                    sound_channel.unpause()
                if event.key == pygame.K_1 or keys[pygame.K_1]:
                    PRESSING_K_1 = not PRESSING_K_1
                    if PRESSING_K_1:
                        player_hand.animation_do = False
                        player_hand.animation_downing_hand_do = True
                    else:
                        player_hand.animation_downing_hand_do = False
                        player_hand.animation_do = True
                        # pass
                if event.key == pygame.K_RIGHT:
                    way = ''
                    jumping_way = ''                
                    pressing_K_R = False
                if event.key == pygame.K_LEFT:
                    way = ''
                    jumping_way = ''
                    pressing_K_L = False
                if event.key != pygame.K_SPACE and event.key != pygame.K_1:
                    moving_player = False
                    way = ''
                    jumping_way = ''
        if pressing_K_R and way != 'up':
            way = 'right'
            jumping_way = 'right'
        else:
            if pressing_K_L and way != 'up':
                way = 'left'
                jumping_way = 'left'
            elif way != 'up':
                way = ''
        # print(pressing_K_R, pressing_K_L)
        if PRESSING_K_1:
            player_hand.update()
            player.with_pistol = True        
        if player.with_pistol:
            player_hand.update()
        if way == 'up':
            # print(jumping_way)
            ALL_SPRITES.update(way, jumping_way)
        else:
            ALL_SPRITES.update(way)
        # print(way)
        # ALL_SPRITES.update()
        # print(player_hand in ALL_SPRITES)
        player_dead.update_place_of_dead()
        for elem in ALL_SPRITES:
            if elem not in INTERFACE_GROUP:
                SCREEN.blit(elem.image, elem.rect)
        for elem in ALL_SPRITES:
            if elem in INTERFACE_GROUP:
                SCREEN.blit(elem.image, elem.rect)
        TRAINING_SPRITES.draw(SCREEN)
        if player.hp <= 0 and player.armor <= 0:
            player.must_make_hide_of_dead = True
            player_hand.must_make_hide_of_dead = True
            if player_dead.update():
                sound_channel.pause()
                game_over()
                sound_channel.unpause()
            else:
                SCREEN.blit(player_dead.image, player_dead.rect)        
        if (player_hand.shooting_time > 0):
            if (player.with_pistol and 
                player_hand.animation_downing_hand_do 
                and player_hand.animation_do and pistol_patron_x <= WIDTH):
                pistol_shooting = True
        if pistol_shooting:
            for elem in ALL_SPRITES:
                if type(elem) == Bullet:
                    elem.update()
        else:
            pistol_shooting = False
        for elem in ALL_SPRITES:
            if type(elem) == FireBall:
                elem.update()
        # print(pistol_patron_x)
        tmp = len(player_hand.animate_list_push)
        if player_hand.animate_list_push_inx == tmp:
            player_hand.animate_list_push_inx = 0
        if player.pushing_time <= 0:
            # print('ok', debug_n)
            # debug_n += 1            
            player_pushing = False
            # player_hand.animate_list_push_inx = 0
        else:
            player_hand.update('push_time')
        # print(player.rect.colliderect(door1.rect))
        # print(pressing_K_e)
        if room_1_enemys.all_enemys_dead():
            if player.rect.colliderect(door1.rect) and pressing_K_e:
                door1.closed_door = not door1.closed_door            
            if door1.closed_door:
                door1.update('close')
            else:
                door1.update('open')
        if room_2_enemys.all_enemys_dead():
            if player.rect.colliderect(door2.rect) and pressing_K_e:
                door2.closed_door = not door2.closed_door            
            if door2.closed_door:
                door2.update('close')
            else:
                door2.update('open')
        if room_3_enemys.all_enemys_dead():
            pygame.quit()
        # if player.collide
        # print(player.pushing_time)
        door1.check_collide(player)
        door2.check_collide(player)
        for elem in room_3_enemys.enemys:
            door1.check_collide(elem)
            door2.check_collide(elem)    
        for elem in room_2_enemys.enemys:
            door1.check_collide(elem)
            door2.check_collide(elem)
        for elem in room_1_enemys.enemys:
            door1.check_collide(elem)
            door2.check_collide(elem)
        '''surf = HiddenSprite(100, 150, 1030, 120)
        SCREEN.blit(surf.image, surf.rect)
        surf.check_collide(player)
        surf2 = pygame.Surface((100, 150))
        surf2.set_alpha(70)
        SCREEN.blit(surf2, (1030, 430)) '''
        # surf2.check_collide(player)
        clock.tick(FPS)            
        global_shooting_time -= 1    
        pygame.display.flip()
        tmp = False
        if player_hand.animate_list_push_inx == 6:
            for elem in ALL_SPRITES:
                if (pygame.sprite.collide_mask(player_hand, elem) 
                    and (type(elem) == Imp or type(elem) == GameOpponent)):
                    tmp = True
                    break
            if tmp:
                player_hand.sound = SOUNDS['punch']['hit']
                player_hand.sound.set_volume(0.9)
                player_hand.sound.play()
            else:
                player_hand.sound = SOUNDS['punch']['miss']
                player_hand.sound.set_volume(0.1)
                player_hand.sound.play()  
        print(player_hand.shooting_time)
        if player_hand.shooting_time == 34:
            player_hand.sound = choice(SOUNDS['pistol_shot'])
            player_hand.sound.set_volume(0.9)
            player_hand.sound.play() 
        if not door1.closed_door:
            if door1.animate_inx == 2:
                door1.sound.set_volume(0.4)
                door1.sound.play()
        else:
            if door1.animate_inx == 28:
                door1.sound.set_volume(0.4)
                door1.sound.play()            
        if door2.animate_inx == 52 and player.rect.x < door2.rect.x:
            door2.sound.set_volume(0.4)
            door2.sound.play()                   
        if door2.animate_inx == 2 and player.rect.x > door2.rect.x:
            door2.sound.set_volume(0.4)
            door2.sound.play()
        for elem in ALL_SPRITES:
            if (room_ceiling.rect.colliderect(elem.rect) 
                and (type(elem) == Player or type(elem) == Imp)):
                elem.rect = elem.rect.move(0, 30)
        for elem in WALL_SPRITES:
            elem.check_collide(player)
        for elem in ALL_SPRITES:
            if (elem.rect.colliderect(wall3.rect)
                and (type(elem) == Imp or type(elem) == GameOpponent)):
                    if elem.reway:
                        elem.rect = elem.rect.move(9, 0)
                    else:
                        elem.rect = elem.rect.move(-9, 0)
        print('way:', way)
        if (not any([elem.image.get_alpha() for elem in TRAINING_SPRITES]) 
            and not room_1_enemys.activated):
            room_1_enemys.active()
            room_2_enemys.active()
            room_3_enemys.active()        
    pygame.quit()
    pygame.mixer.quit()