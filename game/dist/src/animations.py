import sys, pygame, os
from src import constants, functions
from pygame.locals import *


class Animations:
    def __init__(self, base_file_path):
        self.base_file_path = base_file_path

class MobAnimations(Animations):
    def __init__(self,base_file_path, idle_animation_length_list, moving_animation_length_list, jump_animation_frame_list):
        Animations.__init__(self,base_file_path)
        self.moving_animations = []
        self.moving_frame = 0
        self.idle_animations = []
        self.idle_frame = 0
        self.idle_animations_flipped = []
        self.moving_animations_flipped = []
        self.idle_frame_list = idle_animation_length_list
        self.moving_frame_list = moving_animation_length_list
        self.jump_animation = []
        self.jump_frame_list = jump_animation_frame_list
        self.jump_frame = 0
        self.jump_animation_flipped = []
        self.add_animations()

    def add_animations(self):

        for dir in os.listdir(self.base_file_path):
            if dir == 'idle':
                for file in os.listdir(self.base_file_path+"/"+dir):
                    n = 0
                    for i in range(self.idle_frame_list[n]):
                        self.idle_animations.append(pygame.image.load(self.base_file_path + "/idle/"+file))
                    n += 1
            elif dir == 'moving':
                for file in os.listdir(self.base_file_path+"/"+dir):
                    n = 0
                    for i in range(self.moving_frame_list[n]):
                        self.moving_animations.append(pygame.image.load(self.base_file_path + "/moving/"+file))
                    n += 1
            elif dir == 'jump':
                for file in os.listdir(self.base_file_path+"/"+dir):
                    n = 0
                    for i in range(self.jump_frame_list[n]):
                        self.jump_animation.append(pygame.image.load(self.base_file_path + "/jump/"+file))
                    n += 1


        self.idle_animations_flipped = functions.applyFunctionToAllInList(self.idle_animations, pygame.transform.flip)
        self.moving_animations_flipped = functions.applyFunctionToAllInList(self.moving_animations, pygame.transform.flip)
        self.jump_animation_flipped = functions.applyFunctionToAllInList(self.jump_animation, pygame.transform.flip)

    def update_frame(self):
        self.moving_frame += 1
        self.idle_frame += 1

        if self.moving_frame >= len(self.moving_animations):
            self.moving_frame = 0
        if self.idle_frame >= len(self.idle_animations):
            self.idle_frame = 0
        if self.jump_frame >= len(self.jump_animation):
            self.jump_frame = 0

    def output_current_image(self, is_flip, is_moving, is_jumping):
        self.update_frame()
        if is_flip:
            if is_jumping:
                return self.jump_animation[self.jump_frame]
            elif is_moving:
                return self.moving_animations_flipped[self.moving_frame]
            elif not is_moving:
                return self.idle_animations_flipped[self.moving_frame]

        if not is_flip:
            if is_jumping:
                return self.jump_animation_flipped[self.jump_frame]
            elif is_moving:
                return self.moving_animations[self.moving_frame]
            elif not is_moving:
                return self.idle_animations[self.moving_frame]
