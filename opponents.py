import os, sys
import pygame
import keyboard
from pprint import pprint
from random import randrange
from tkinter import *
import getkey 


WIDTH, HEIGHT = 1200, 600


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 3
        self.make_kayo_animation = False
        self.image = load_image('demonical/demonical_standing/0.png')
        self.animate_list_move = sorted(['demonical/demonical_going/' + elem
                 for elem in os.listdir('images/demonical/demonical_going')
                 if os.path.isfile('images/demonical/demonical_going/' + elem)])
        self.animate_list_move = ['demonical/demonical_going/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_move))]
        self.animate_list_stand = sorted(['demonical/demonical_standing/' + elem
                 for elem in os.listdir('images/demonical/demonical_standing')
                 if os.path.isfile('images/demonical/demonical_standing/' + elem)])
        self.animate_list_stand = ['demonical/demonical_standing/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_stand))]
        self.animate_list_beat = sorted(['demonical/demonical_beating/' + elem
                 for elem in os.listdir('images/demonical/demonical_beating')
                 if os.path.isfile('images/demonical/demonical_beating/' + elem)])
        self.animate_list_beat = ['demonical/demonical_beating/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_beat))]
        self.animate_list_die = sorted(['demonical/demonical_dieng/' + elem
                 for elem in os.listdir('images/demonical/demonical_dieng')
                 if os.path.isfile('images/demonical/demonical_dieng/' + elem)])
        self.animate_list_die = ['demonical/demonical_dieng/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_die))]        
        self.animate_list_kayo = sorted(['demonical/demonical_kayo/' + elem
                 for elem in os.listdir('images/demonical/demonical_kayo')
                 if os.path.isfile('images/demonical/demonical_kayo/' + elem)])
        self.animate_list_kayo = ['demonical/demonical_kayo/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_kayo))]
        self.animate_list_fatal_dead = sorted(['demonical/demonical_fatal_dead/' + elem
                 for elem in os.listdir('images/demonical/demonical_fatal_dead')
                 if os.path.isfile('images/demonical/demonical_fatal_dead/' + elem)])
        self.animate_list_fatal_dead = ['demonical/demonical_fatal_dead/{}.png'.format(i) 
                                  for i in range(len(self.animate_list_fatal_dead))]        
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
        self.reway = False
        self.kayo_time = 160
    
    def animate_fatal_dead(self):
        try:
            self.image = load_image(self.animate_list_fatal_dead[self.animate_dead_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_dead_inx += 1
            if self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
            return False
        except Exception:
            return True
    
    def animate_standing(self):
        try:
            self.image = load_image(self.animate_list_stand[self.animate_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_inx %= len(self.animate_list_stand)
            if self.animate_inx < len(self.animate_list_stand) - 1:
                self.animate_inx += 1
            else:
                self.animate_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_inx = 0
    
    def animate_moving(self):
        self.image = load_image(self.animate_list_move[self.animate_inx])
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() // 5, self.image.get_height() // 5))
        self.animate_inx += 1
        self.animate_inx = self.animate_inx % len(self.animate_list_move)
        if not self.reway:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def animate_beating(self):
        try:
            self.image = load_image(self.animate_list_beat[self.animate_fight_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_fight_inx %= len(self.animate_list_beat)
            if self.animate_fight_inx < len(self.animate_list_beat) - 1:
                self.animate_fight_inx += 1
            else:
                self.animate_fight_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_inx = 0    
    
    def animate_kayo(self):
        self.mask = pygame.mask.from_surface(self.image)
        try:
            self.image = load_image(self.animate_list_kayo[self.animate_kayo_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_kayo_inx %= len(self.animate_list_kayo)
            if self.animate_kayo_inx < len(self.animate_list_kayo) - 1:
                self.animate_kayo_inx += 1
            else:
                self.animate_kayo_inx = 0
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
        except Exception:
            self.animate_kayo_inx = 0
    
    def animate_dieng(self):
        try:
            self.image = load_image(self.animate_list_die[self.animate_dead_inx])
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() // 5, self.image.get_height() // 5))
            self.animate_dead_inx += 1
            if not self.reway:
                self.image = pygame.transform.flip(self.image, True, False)
            return False
        except Exception:
            return True
    
    def print_info(self):
        print(self.animate_list_stand)