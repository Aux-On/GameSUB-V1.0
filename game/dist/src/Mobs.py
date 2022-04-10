import sys, pygame
from pygame.locals import *
from src import functions, animations, constants

class Mobs:
    def __init__(self, image_path, is_collidable, init_locationxy, display, idle_animation_length_list, moving_animation_length_list, jump_animation_frame_list):
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]
        self.display = display
        #self.mob_image = pygame.image.load(image_path)
        self.location = init_locationxy
        self.movement = [0,0]
        self.locationScale = [1,1]
        self.is_collidable = is_collidable
        self.Rect = pygame.Rect(init_locationxy[0], init_locationxy[1],16, 16)
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.collidable_tiles = []
        self.is_movingRight = False
        self.is_movingLeft = False
        self.playerdy = 0

        self.health = 10

        self.animate = animations.MobAnimations(image_path,idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list)
        self.is_flip = False
        self.is_moving = False
        self.is_jumping = False

    def loadhealth(self, display, locationxy):
        image = "images/gui/health/health_" + str(self.health) + ".png"


        display.blit(pygame.image.load(image),locationxy)

    def updatehealth (self, linear_health_transformation):

        if (self.health+ linear_health_transformation < 11 and self.health+ linear_health_transformation > -1):
            self.health += linear_health_transformation

    def adjust_for_collision(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.Rect.x += self.movement[0]
        hit_list = functions.collision_test(self.Rect, tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.Rect.right = tile.left
                self.collision_types['right'] = True
            elif self.movement[0] < 0:
                self.Rect.left = tile.right
                self.collision_types['left'] = True
        self.Rect.y += self.movement[1]
        hit_list = functions.collision_test(self.Rect, tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.Rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.Rect.top = tile.bottom
                self.collision_types['top'] = True




    def scaleLocation_by_tile(self, TILESIZExy):
        self.locationScale[0] = TILESIZExy[0]
        self.locationScale[1] = TILESIZExy[1]
        self.Rect = pygame.Rect(self.location[0] * self.locationScale[0], self.location[1] * self.locationScale[1],
                                self.mob_image.get_width(), self.mob_image.get_height())

    def scale_image(self,scale_toxy):
        self.mob_image = pygame.transform.scale(self.mob_image,scale_toxy)



    def load_sprite(self,display):
        #self.Rect = pygame.Rect(self.location[0]*self.locationScale[0],self.location[1]*self.locationScale[1],self.mob_image.get_width(),self.mob_image.get_height())
        display.blit(self.animate.output_current_image(self.is_flip,self.is_moving,self.is_jumping),(self.Rect.x - self.scroll[0],self.Rect.y - self.scroll[1]))

    def is_moving(self):
        if self.movement[0] != 0 or self.movement[1] != 0:
            return True
        else:
            return False





########################################################################################################################


class Player(Mobs):
    def __init__(self, image_path, is_collidable, init_xy, display, idle_animation_length_list,
                 moving_animation_length_list, jump_animation_frame_list):
        Mobs.__init__(self, image_path, is_collidable, init_xy, display, idle_animation_length_list,
                      moving_animation_length_list, jump_animation_frame_list)

        #super.__init__(image_path, is_collidable, init_xy)
        self.Rect = pygame.Rect(init_xy[0]+1, init_xy[1], 15, 15)
        self.jump_index = 0
        self.is_gravity = True
        self.extMove = [0,0]



    def update(self):
        self.movement = [0, 0]

        if self.is_movingLeft:
            self.is_moving = True
            self.is_flip = False
            self.movement[0] -= 3


        if self.is_movingRight:
            self.is_flip = True
            self.is_moving = True
            self.movement[0] += 3


        if self.playerdy > 2:
            self.playerdy = 2

        if self.is_gravity:
            self.playerdy += 1
            self.movement[1] += self.playerdy


        self.loadhealth(self.display,( 125 , 5 ))

        self.movement[0] += self.extMove[0]
        self.movement[1] += self.extMove[1]

        self.location[0] += self.movement[0]
        self.location[1] += self.movement[1]

        self.adjust_for_collision(self.collidable_tiles)
        self.load_sprite(self.display)

        self.true_scroll[0] += (self.Rect.x - self.true_scroll[0] - self.display.get_width()/2)/10
        self.true_scroll[1] += (self.Rect.y - self.true_scroll[1] - self.display.get_height()/2)/20
        self.scroll[0] = int(self.true_scroll[0])
        self.scroll[1] = int(self.true_scroll[1])

        if self.collision_types['bottom']:
            self.playerdy = 0
            self.jump_index = 0
            self.is_jumping = False
        else:
            self.is_jumping = True
        if self.collision_types['top']:
            self.playerdy = 0

        self.is_moving = False
        self.extMove = [0,0]


    def toggle_platform_gravity(self, is_on):
        if is_on:
            self.is_gravity = True
        else:
            self.is_gravity = False

    def check_event(self, event):

        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.jump_index += 1
                if self.jump_index == 1:
                    self.playerdy = -8
                if self.jump_index == 2:
                    self.playerdy = -8

            if event.key == K_LEFT:
                self.is_movingLeft = True
            if event.key == K_RIGHT:
                self.is_movingRight = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                self.is_movingLeft = False
            if event.key == K_RIGHT:
                self.is_movingRight = False






#########################################################################################################################

class Slime:
    def __init__(self,display, initial_locationxy, base_image_location, hitboxsizexy,
                 idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list):
        self.display = display
        self.position = initial_locationxy
        self.image_location = base_image_location
        self.Rect = pygame.Rect(self.position[0], self.position[1],hitboxsizexy[0],hitboxsizexy[1])
        self.health = 10

        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.animate = animations.MobAnimations(base_image_location, idle_animation_length_list, moving_animation_length_list,
                                                jump_animation_frame_list)
        self.is_flipA = False
        self.is_movingA = False
        self.is_jumpingA = False

        self.movement = [0,0]
        self.dy = 0
        self.is_movingL = False
        self.is_movingR = False

        self.frame = 0
        self.motion_index = 0

    def load_image(self, scroll):
        self.display.blit(self.animate.output_current_image(self.is_flipA, self.is_movingA, self.is_jumpingA), (self.Rect.x - scroll[0], self.Rect.y - scroll[1]))
        self.loadhealth(self.display, ((self.Rect.x - 4) - scroll[0], (self.Rect.y - 10) - scroll[1]))

    def loadhealth(self, display, locationxy):
        image = "images/gui/health/health_" + str(int(self.health)) + ".png"


        display.blit(pygame.transform.scale(pygame.image.load(image),[24,4]),locationxy)

    def updatehealth (self, linear_health_transformation):

        if (int(self.health+ linear_health_transformation) < 11 and int(self.health+ linear_health_transformation) > -1):
            self.health += linear_health_transformation

    def adjust_for_collision(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.Rect.x += self.movement[0]
        hit_list = functions.collision_test(self.Rect, tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.Rect.right = tile.left
                self.collision_types['right'] = True
            elif self.movement[0] < 0:
                self.Rect.left = tile.right
                self.collision_types['left'] = True
        self.Rect.y += self.movement[1]
        hit_list = functions.collision_test(self.Rect, tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.Rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.Rect.top = tile.bottom
                self.collision_types['top'] = True



    def interval_motion(self):
        if self.motion_index == 0:
            self.is_movingL  = False
            self.is_movingR = False
        if self.motion_index == 1:
            self.is_movingL = False
            self.is_movingR = True
        if self.motion_index == 2:
            self.is_movingL = False
            self.is_movingR = False
        if self.motion_index == 3:
            self.is_movingL = True
            self.is_movingR = False

    def update(self, collide_tiles, scrollxy):

        self.frame += 1
        self.movement = [0, 0]

        if self.is_movingL:
            self.is_movingA = True
            self.is_flipA = False
            self.movement[0] -= 1

        if self.is_movingR:
            self.is_flipA = True
            self.is_movingA = True
            self.movement[0] += 1

        if self.dy > 2:
            self.dy = 2
        self.movement[1] += self.dy

        self.adjust_for_collision(collide_tiles)
        self.load_image(scrollxy)



        if self.collision_types['bottom']:
            self.dy = 0
            self.is_jumpingA = False
        else:
            self.is_jumpingA = True


        self.is_movingA = False
        self.dy += 1

        if self.frame % 90 == 0:
            self.interval_motion()
            self.motion_index +=1
        if self.motion_index > 3:
            self.motion_index = 0

class Snakeworm(Slime):
    def __init__(self,display, initial_locationxy, base_image_location, hitboxsizexy,
                 idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list):
        Slime.__init__(self,display, initial_locationxy, base_image_location, hitboxsizexy,
                 idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list)

    def interval_motion(self):
        if self.motion_index == 0:
            self.is_movingL  = False
            self.is_movingR = False
        if self.motion_index == 1:
            self.is_movingL = False
            self.is_movingR = True
        if self.motion_index == 2:
            self.is_movingL = True
            self.is_movingR = False
        if self.motion_index == 3:
            self.is_movingL = False
            self.is_movingR = True

    def update(self, collide_tiles, scrollxy):

        self.frame += 1
        self.movement = [0, 0]

        if self.collision_types['left'] or self.collision_types['right']:
            self.dy = -4

        if self.is_movingL:
            self.is_movingA = True
            self.is_flipA = False
            self.movement[0] -= 1

        if self.is_movingR:
            self.is_flipA = True
            self.is_movingA = True
            self.movement[0] += 1

        if self.dy > 2:
            self.dy = 2
        self.movement[1] += self.dy

        self.adjust_for_collision(collide_tiles)
        self.load_image(scrollxy)

        if self.collision_types['bottom']:
            self.dy = 0
            self.is_jumpingA = False
        else:
            self.is_jumpingA = True


        self.is_movingA = False
        self.dy += 1

        if self.frame % 30 == 0:
            self.interval_motion()
            self.motion_index +=1
        if self.motion_index > 3:
            self.motion_index = 0


class Ghost(Slime):
    def __init__(self,display, initial_locationxy, base_image_location, hitboxsizexy,
                 idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list):
        Slime.__init__(self,display, initial_locationxy, base_image_location, hitboxsizexy,
                 idle_animation_length_list,moving_animation_length_list,jump_animation_frame_list)

    def interval_motion(self):
        if self.motion_index == 0:
            self.is_movingL  = False
            self.is_movingR = False
            self.dy = 2
        if self.motion_index == 1:
            self.is_movingL = False
            self.is_movingR = True
            self.dy = 0
        if self.motion_index == 2:
            self.is_movingL = True
            self.is_movingR = False
            self.dy = 0.5
        if self.motion_index == 3:
            self.is_movingL = False
            self.is_movingR = True
            self.dy = 0

    def update(self, collide_tiles, scrollxy):

        self.frame += 1
        self.movement = [0, 0]

        if self.collision_types['left'] or self.collision_types['right']:
            self.dy = -4

        if self.is_movingL:
            self.is_movingA = True
            self.is_flipA = False
            self.movement[0] -= 1

        if self.is_movingR:
            self.is_flipA = True
            self.is_movingA = True
            self.movement[0] += 1

        if self.dy > 2:
            self.dy = 2
        self.movement[1] += self.dy

        self.adjust_for_collision(collide_tiles)
        self.load_image(scrollxy)

        if self.collision_types['bottom']:
            self.is_jumpingA = False
        else:
            self.is_jumpingA = True


        self.is_movingA = False

        if self.frame % 30 == 0:
            self.interval_motion()
            self.motion_index +=1
        if self.motion_index > 3:
            self.motion_index = 0











class Stickyfingers(Slime):
    def __init__(self,display, initial_locationxy, base_image_location):
        Slime.__init__(self,display, initial_locationxy, 'images/level_3/Slime', [16,16],
                 [1],[1],[1])

        self.image_location2 = base_image_location



    def load_image(self, scroll):
        self.display.blit(pygame.image.load(self.image_location2), (self.Rect.x - scroll[0], self.Rect.y - scroll[1]))


    def update(self, collide_tiles, scrollxy):

        self.frame += 1
        self.movement = [0, 0]

        if self.collision_types['left'] or self.collision_types['right']:
            self.dy = -4


        if self.dy > 2:
            self.dy = 2
        self.movement[1] += self.dy

        self.adjust_for_collision(collide_tiles)
        self.load_image(scrollxy)

        if self.collision_types['bottom']:
            self.dy = 0
            self.is_jumpingA = False

