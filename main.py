import os, sys
import pygame
from pprint import pprint
from random import randrange

# class Player:
#    def __init__(self):
#################################################################
        
WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 24
PRESSING_SPACE = False
PRESSING_K_1 = False
SQUARE = 0

ALL_SPRITES = pygame.sprite.Group()
BLOCK_SPRITES = pygame.sprite.Group()
WALL_SPRITES = pygame.sprite.Group()
PLAYER_GROUP = pygame.sprite.Group()

pygame.mixer.init()

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
        # print(self.lst_animations)
    
    def check_collide(self, collide_object):
        self.mask = pygame.mask.from_surface(self.image)
        collide_object.mask = pygame.mask.from_surface(collide_object.image)
        if pygame.sprite.collide_mask(self, collide_object):
            if type(collide_object) == Player:
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


class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.shooting_time = 0
        self.image = load_image('with_pistol_standing/hand/0.png')
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 5, 
            self.image.get_height() // 5))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = player.rect
        self.animation_do = False
        self.animation_downing_hand_do = True
        self.animate_list_hand_downing_with_pistol = sorted([
            'with_pistol_standing/hand_downing/' + elem
                 for elem in 
                 os.listdir('images/with_pistol_standing/hand_downing')
                 if os.path.isfile(
                     'images/with_pistol_standing/hand_downing/' + elem)])
        del self.animate_list_hand_downing_with_pistol[
            len(self.animate_list_hand_downing_with_pistol) - 2:]
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
    
    def update(self, *args):
        flag = True
        if args and args[0] == 'push_time':
            # print(player.with_pistol)
            if not player.with_pistol:
                if player.reway:
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
            self.animate_list_push_inx = 0
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
        self.rect = player.rect
        SCREEN.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.vector_x = 0
        self.vector_y = 0
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
        self.rect = self.rect.move(100, 300)
        self.animation_of_stand_inx = 1
        self.animation_of_move_inx = 0
        self.animation_of_jump_inx = 0
        self.v = 0
        self.reway = False
    
    def update(self, *args):
        # print(self.with_pistol)
        # if check_collide(self, pol):
        #     print('ok')
        # else:
        #    print('not_ok')        
        if args:
            if pygame.sprite.spritecollideany(self, WALL_SPRITES):
                if self.reway:
                    self.rect = self.rect.move(20, 0)
                else:
                    self.rect = self.rect.move(-20, 0)
                return 
            # print(args[0][pygame.K_DOWN])
            if (not self.with_pistol and self.pushing_time <= 0):
                if args[0] == 'left':
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
                    if not self.reway:
                        player_hand.image = pygame.transform.flip(
                            player_hand.image, True, False)                    
                    self.reway = True
                if args[0] == 'right':
                    self.rect = self.rect.move(14, 0)
                    self.vector_x = 14                   
                    if self.reway:
                        self.reway = False
                        self.image = pygame.transform.flip(self.image, 
                                                           True, False)
                        player_hand.image = pygame.transform.flip(
                            player_hand.image, True, False)
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

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def start_screen():
    sound = pygame.mixer.Sound('music/menu_sound.wav')
    sound.play(loops=-1)
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
    # print(video_list)
    video_list_inx = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(continue_button.rect, start_button.rect, event.pos)
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
        pygame.display.flip()
        # clock.tick(FPS)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(ALL_SPRITES)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_v = 0
    
    def update(self, *args):
        self.rect = self.rect.move(self.bullet_v, 0)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, fullname):
        super().__init__(ALL_SPRITES)
        self.image = load_image(fullname)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(30, 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.animate_list_move = sorted(['zombie_going/' + elem
                                         for elem in os.listdir('images/zombie_going')
                                         if os.path.isfile('images/zombie_going/' + elem)])
        self.animate_list_move = ['zombie_going/{}.png'.format(i)
                                  for i in range(len(self.animate_list_move))]
        self.animate_list_punch = sorted(['zombie_punching/' + elem
                                         for elem in os.listdir('images/zombie_punching')
                                         if os.path.isfile('images/zombie_punching/' + elem)])
        self.animate_list_punch = ['zombie_punching/{}.png'.format(i)
                                  for i in range(len(self.animate_list_punch))]
        self.animation_move_inx = 0
        self.animation_punch_inx = 0
        self.v = 10
        self.way = ''

    def animate_move(self):
        self.animation_move_inx += 1
        self.image = load_image(self.animate_list_move[self.animation_move_inx])
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_move_inx %= (len(self.animate_list_move) - 1)
        print(self.way)
        if self.way == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    def animate_punch(self):
        self.animation_punch_inx += 1
        self.image = load_image(self.animate_list_punch[self.animation_punch_inx])
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_punch_inx %= (len(self.animate_list_punch) - 1)
        if self.way == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    def check_collide(self, collide_object):
        self.mask = pygame.mask.from_surface(self.image)
        collide_object.mask = pygame.mask.from_surface(collide_object.image)
        if pygame.sprite.collide_mask(self, collide_object):
            if type(collide_object) == Player:
                if self.animate_inx != len(self.lst_animations) - 1:
                    if collide_object.reway:
                        collide_object.rect = collide_object.rect.move(20, 0)
                    else:
                        collide_object.rect = collide_object.rect.move(-20, 0)

    def update(self, *args):
        if not pygame.sprite.collide_mask(self, pol):
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.collide_mask(self, player):
            self.image = load_image(self.animate_list_move[0])
            self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
            self.mask = pygame.mask.from_surface(self.image)
            self.animate_punch()
        else:
            if self.rect.x - player.rect.x > 0:
                self.v = -5
                self.rect = self.rect.move(self.v, 0)
                self.way = 'right'
            elif self.rect.x - player.rect.x < 0:
                self.v = 5
                self.rect = self.rect.move(self.v, 0)
                self.way = 'left'
            self.animate_move()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj):
        obj.rect.x += self.dx
    
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


if __name__ == '__main__':
    potolok = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((2247, 400))
    tmp_image.blit(potolok.image, (0, 0))
    potolok.image = tmp_image
    potolok.image = pygame.transform.scale(potolok.image, (
        potolok.image.get_width() // 2 + 2500, potolok.image.get_height() // 2))
    potolok.rect = potolok.image.get_rect()
    potolok.rect = potolok.rect.move(0, -100)
    BLOCK_SPRITES.add(potolok)
    pol = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((6347, 300))
    tmp_image.set_alpha(0)
    pol.image = tmp_image
    pol.image = pygame.transform.scale(pol.image, (
        pol.image.get_width() // 2, pol.image.get_height() // 2))
    pol.rect = pol.image.get_rect()
    pol.rect = pol.rect.move(0, 433)
    pol.image.fill((255, 0, 0))
    BLOCK_SPRITES.add(pol)
    wall1 = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((40, 2000))
    # tmp_image.set_alpha(0)
    wall1.image = tmp_image
    wall1.image = pygame.transform.scale(wall1.image, (
        wall1.image.get_width() // 2, wall1.image.get_height() // 2))
    wall1.rect = wall1.image.get_rect()
    wall1.rect = wall1.rect.move(-20, 0)
    WALL_SPRITES.add(wall1)
    zombie = Zombie('zombie_going/0.png')
    '''wall2 = GameObject('locations/start_location/pol.png')
    tmp_image = pygame.Surface((75, 2000))
    tmp_image.set_alpha(0)
    wall2.image = tmp_image
    wall2.image.fill((255, 0, 0))
    wall2.rect = wall2.image.get_rect()
    wall2.rect = wall2.rect.move(1125, 0)'''
    # ALL_SPRITES.add(door1)
    pygame.init()
    running = True
    start_screen()
    player = Player()
    player_hand = Hand()
    PLAYER_GROUP.add(player)
    PLAYER_GROUP.add(player_hand)
    ALL_SPRITES.add(player)
    ALL_SPRITES.add(pol)
    door1 = Door('locations/start_location/door_1/door_animation/0.png')
    door1.image = pygame.transform.scale(door1.image, 
                                         (door1.image.get_width() // 2, 
                                          door1.image.get_height() // 2))
    door1.rect = door1.image.get_rect()
    door1.rect = door1.rect.move(954, 168)    
    # ALL_SPRITES.add(platform)
    SCREEN.fill((0, 0, 0))
    moving_player = False
    way = ''
    clock = pygame.time.Clock()
    pygame.key.set_repeat(10, 10)
    count_jumps = 0
    jumping_way = ''
    count_updates_of_hand = 0
    hand_reway = False
    time_shooting = 0
    pistol_patron = load_image('pistol_patron.png')
    pistol_patron = pygame.transform.scale(pistol_patron, 
                                           (pistol_patron.get_width() // 18, 
                                          pistol_patron.get_height() // 18))
    pistol_patron_x = player.rect.x
    pistol_patron_y = player.rect.y + 57
    pistol_patron_v = 20
    pistol_shooting = False
    global_shooting_time = 0
    player_pushing = False
    level_fon = pygame.Surface((8482, HEIGHT))
    start_room = load_image('locations/start_location/fon.png')
    start_room = pygame.transform.scale(start_room, 
                                        (start_room.get_width() // 2, 
                                         start_room.get_height() // 2))
    place_for_costume_fon = load_image('locations/place_for_costume/3-fon.png')
    place_for_costume_fon = pygame.transform.scale(place_for_costume_fon, 
                                        (place_for_costume_fon.get_width() // 2, 
                                         place_for_costume_fon.get_height() // 2
                                          + 100))
    start_room_fon_pol = load_image('locations/start_location/pol.png')
    start_room_fon_pol = pygame.transform.scale(start_room_fon_pol, 
                                        (start_room_fon_pol.get_width() // 2, 
                                         start_room_fon_pol.get_height() // 2))  
    stolb = GameObject('locations/start_location/stolb.png')
    stolb.image = pygame.transform.scale(stolb.image, 
                                         (stolb.image.get_width() // 2, 
                                           stolb.image.get_height() // 2))
    stolb.rect = stolb.rect.move(210, 0)
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
    perehod_2_pol = load_image('locations/perehod/2-pol.png')
    perehod_2_pol = pygame.transform.scale(perehod_2_pol, 
                                        (perehod_2_pol.get_width() // 2, 
                                        perehod_2_pol.get_height() // 2 + 100))    
    surf2 = pygame.Surface((1753, perehod_2_pol.get_height()))
    surf2.blit(perehod_2_pol, (-1753, -500))
    perehod_2_pol = surf2
    sarc_rect = sarc_image.get_rect()
    sarc_rect = sarc_rect.move(0, -120)
    # print(sarc_rect)
    level_fon.blit(start_room, (0, -100))
    level_fon.blit(start_room_fon_pol, (0, -100))
    level_fon.blit(sarc_image, sarc_rect)
    level_fon.blit(place_for_costume_pol, (1220, 168))
    level_fon.blit(place_for_costume_fon, (1220, -10))
    level_fon.blit(light_in_place_for_costume, (1220, 60))
    level_fon.blit(perehod_1_fon, (1870, -360))
    level_fon.blit(perehod_1_pol, (2040, 439))
    level_fon.blit(perehod_2_pol, (3900, 339))
    squares = [pygame.Rect(1230, randrange(60, 300), 
                           randrange(30, 70), randrange(30, 70))
               for i in range(100)]
    time = 0
    pressing_K_L = False
    pressing_K_R = False
    pressing_K_e = False
    debug_n = 0
    # k = 3800
    # door1.rect = door1.rect.move(-k, 0)
    stolb.rect = stolb.rect.move(800, 0)
    player_path = 0
    camera = Camera()
    sound = pygame.mixer.Sound('music/gameplay_sound.wav')
    sound.play(loops=-1)        
    while running:
        camera.update(player)
        player_path += camera.dx
        if player_path >= 31:
            player_path -= camera.dx
            camera.dx = 0        
        pressing_K_e = False
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(level_fon, (player_path, 0))
        for sprite in ALL_SPRITES:
            if sprite != pol:
                camera.apply(sprite)
        # print(jumping_way)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    way = 'left'
                    jumping_way = 'left'
                    pressing_K_L = True                    
                if event.key == pygame.K_RIGHT:
                    way = 'right'
                    jumping_way = 'right'             
                    pressing_K_R = True
                if event.key == pygame.K_UP:
                    way = 'up'
                    for elem in PLAYER_GROUP:
                        if pygame.sprite.spritecollideany(elem, BLOCK_SPRITES):
                            count_jumps = 16
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    pressing_K_e = True                
                if event.key == pygame.K_1:
                    PRESSING_K_1 = not PRESSING_K_1
                    # print(PRESSING_SPACE)
                    if PRESSING_K_1:
                        player_hand.animation_do = False
                        player_hand.animation_downing_hand_do = True
                    else:
                        player_hand.animation_downing_hand_do = False
                        player_hand.animation_do = True
                        count_updates_of_hand = 9
                        # pass
                if event.key == pygame.K_LEFT:
                    way = ''
                    jumping_way = ''
                    pressing_K_L = False
                if event.key == pygame.K_RIGHT:
                    way = ''
                    jumping_way = ''                
                    pressing_K_R = False
                if event.key == pygame.K_SPACE:
                    if (player.with_pistol and player_hand.shooting_time == 0):
                        # and global_shooting_time <= 0
                        player_hand.shooting_time = 16
                        global_shooting_time = 10
                        pistol_patron_y = player.rect.y + 57
                        if player.reway:
                            pistol_patron_v = -10
                            pistol_patron_x = player.rect.x - 10 * 2
                        else:
                            pistol_patron_v = 10
                            pistol_patron_x = player.rect.x + 10 * 6
                        pistol_bullet = Bullet(pistol_patron)
                        pistol_bullet.rect.x = pistol_patron_x
                        pistol_bullet.rect.y = pistol_patron_y
                        pistol_bullet.bullet_v = pistol_patron_v
                        ALL_SPRITES.add(pistol_bullet)
                    elif not player.with_pistol:
                        # print('ok', debug_n)
                        # debug_n += 1
                        if player.pushing_time <= 0:
                            player_pushing = True
                            player.pushing_time = 17
                    else:
                        player_hand.shooting_time = 0
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
        if count_jumps > 0 and way == 'up':
            ALL_SPRITES.update(way, jumping_way)
            count_jumps -= 1
        else:
            ALL_SPRITES.update(way)
        # print(way)
        # ALL_SPRITES.update()
        # print(player_hand in ALL_SPRITES)     
        ALL_SPRITES.draw(SCREEN)
        if PRESSING_K_1:
            player_hand.update()
            player.with_pistol = True
        elif count_updates_of_hand > 0:
            count_updates_of_hand -= 1
            player_hand.update()
            player.with_pistol = True
        else:
            player.with_pistol = False
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
        # print(pistol_patron_x)
        if player.pushing_time <= 0:
            # print('ok', debug_n)
            # debug_n += 1            
            player_pushing = False
            player_hand.animate_list_push_inx = 0
        else:
            player_hand.update('push_time')
        # print(player.rect.colliderect(door1.rect))
        # print(pressing_K_e)
        if player.rect.colliderect(door1.rect) and pressing_K_e:
            door1.closed_door = not door1.closed_door
        if door1.closed_door:
            door1.update('close')
        else:
            door1.update('open')
        # if player.collide
        # print(player.pushing_time)
        door1.check_collide(player)
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
    pygame.quit()
    pygame.mixer.quit()