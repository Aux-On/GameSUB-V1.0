import random
import sys, pygame, math

from src import constants, Mobs, functions, fileManager

from src import Menu as men

from pygame.locals import *



#Base Level Class
class Level:
    def __init__(self, clock, screen, game_map_location):
        self.clock = clock
        self.display = pygame.Surface(constants.surface_size)
        self.screen = screen
        self.player_image = 'images/level_3/Guyy'
        self.game_map_location = game_map_location
        self.TILESIZE = 16
        self.small_font = functions.Font('images/gui/small_font.png', (150,100,139))
        self.large_font = functions.Font('images/gui/large_font.png',(150,100,139))
        self.blank = pygame.image.load("images/blank_screen.png")
        self.menu = men.Menu(self.clock)
        self.mob_objects = []
        self.notes = []

#Loading Level score board
    def load_score(self,score, locationxy):
        self.blank.fill((0,0,0))
        self.blank.set_colorkey((0,0,0))
        self.small_font.render(self.blank, "score: " + str(score), (0, 0))
        self.display.blit(self.blank, locationxy)

#dialogue box
    def dialogue_box(self,text, locationxy, quit_key_pygame):
        dialouge_surf = pygame.image.load("images/gui/lower_dialogue.png")
        box = pygame.image.load("images/gui/text_box.png")

        running = True
        while running:
            self.display.blit(pygame.image.load("images/press_w.png"),[0,0])
            self.small_font.render(dialouge_surf,text,(10,6))
            self.display.blit(dialouge_surf,locationxy)
            #dialouge_surf.blit(pygame.transform.scale(box, sizexy), (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == quit_key_pygame:
                        running = False
                        return False

            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)



########################################################################################################################
#                                                    SUB CLASS
########################################################################################################################

#Level 3
class Level3(Level):
    def __init__(self, clock, display,game_map_location,pygame_tile_image_list):
        Level.__init__(self, clock, display,game_map_location)
        #super.__init__(clock,display,game_map_location)
        self.player = Mobs.Player(self.player_image, True, [50, 50], self.display, [30], [30], [30])


        self.map_dictionary = {}
        n = 1
        for image in pygame_tile_image_list:
            self.map_dictionary[str(n)] = image
            # { '1' : pygame_image_1 , '2' : pyga,e_image_2 ....  }
            n += 1


    #Return Collidable Tiles to the player, as well as load basic game map
    def loadANDreturn_collidable_tiles(self, colidable_index_list):
        game_map = functions.read_map(self.game_map_location)

        # list: [ [3,0,0,...] , [3,0,0,...] , ...]
        collidable_tiles = []

        y =0
        for row in game_map:
            x = 0
            for tile_num in row:
                #not include"filer" blocks
                if tile_num != '0' and tile_num != '3':
                    self.display.blit(self.map_dictionary[tile_num], (x*self.TILESIZE - self.player.scroll[0],y*self.TILESIZE - self.player.scroll[1]))
                #Collidable blocks
                if tile_num == '1' or tile_num == '2' or tile_num == '3':
                    collidable_tiles.append(pygame.Rect(x * self.TILESIZE,y * self.TILESIZE,self.TILESIZE,self.TILESIZE))
                x += 1

            y += 1

        return collidable_tiles


    #Running Game Method
    def game(self):

        diobox_test = False
        running = True

        #Cloud
        cloudyvals = functions.rand_list(2*16,12*16,50)
        cloud_idexes = functions.rand_list(0,1,50)


        #Loading Mobs
        self.player = Mobs.Player(self.player_image, True, [50, 50], self.display, [30], [30], [30])
        slime = Mobs.Slime(self.display, [16 * 12, 10 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])
        slime2 = Mobs.Slime(self.display, [16 * 67, 3 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])
        slime3 = Mobs.Slime(self.display, [16 * 98, 9 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])
        slime4 = Mobs.Slime(self.display, [16 * 116, 11 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])
        slime5 = Mobs.Slime(self.display, [16 * 123, 7 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])
        slime6 = Mobs.Slime(self.display, [16 * 167, 3 * 13], 'images/level_3/Slime', [16, 16], [30, 30], [30], [30])

        #Loading Notes
        note_1 = Mobs.Stickyfingers(self.display, [16 * 32, 5 * 16], "images/stickyfingers.png")
        note_2 = Mobs.Stickyfingers(self.display, [16 * 92, 12 * 16], "images/stickyfingers.png")
        note_3 = Mobs.Stickyfingers(self.display, [16 * 163, 7 * 16], "images/stickyfingers.png")

        #appending to lisst
        self.mob_objects.append(slime)
        self.mob_objects.append(slime2)
        self.mob_objects.append(slime3)
        self.mob_objects.append(slime4)
        self.mob_objects.append(slime5)
        self.mob_objects.append(slime6)
        self.notes.append(note_1)
        self.notes.append(note_2)
        self.notes.append(note_3)

        #Setting up some variables
        progress = 0
        self.player.health = 10
        score = 0
        is_E_pressed = False
        pause = False

        while running:

            #Base Sky Color
            self.display.fill((240, 128 , 128))

            # Sut up the Amazing Sunset
            pygame.draw.rect(self.display, (17, 29, 94), pygame.Rect(0, self.player.scroll[0] * 0.04 - 300, 180, 300))
            # Violet
            pygame.draw.rect(self.display, (80, 38, 167), pygame.Rect(0, self.player.scroll[0] * 0.1 - 200, 180, 200))
            #purple
            pygame.draw.rect(self.display, (141, 68, 139), pygame.Rect(0, self.player.scroll[0]*0.15 - 100, 180, 120))
            # pink-purple
            pygame.draw.rect(self.display, (204, 106, 135), pygame.Rect(0, self.player.scroll[0] * 0.25 - 100, 180, 120))
            # beige
            pygame.draw.rect(self.display, (236, 205, 143), pygame.Rect(0, self.player.scroll[0] * 0.5 - 100, 180, 300))

            #The Red Sun
            sun = pygame.draw.circle(self.display,(255,255,255), (90,30 + (self.player.scroll[0])*0.05),24,0)
            pygame.draw.circle(self.display, (255, 249, 178), (90, 30 + (self.player.scroll[0]) * 0.05), 24, 10)
            #pygame.draw.circle(self.display, (247, 110, 17), (90, 30 + (self.player.scroll[0]) * 0.05), 24, 7)
            #pygame.draw.circle(self.display, (205, 24, 24), (90, 30 + (self.player.scroll[0]) * 0.05), 24, 5)
            pygame.draw.circle(self.display, (244, 225, 133), (90, 30 + (self.player.scroll[0]) * 0.05), 24, 3)

            #Cloud Generation
            functions.generate_clouds(self.display,50,['images/cloud1.png','images/cloud2.png'], cloud_idexes,2,cloudyvals,[self.player.scroll[0]*.5, self.player.scroll[1]*1.2])

            #update player's potential collisions
            self.player.collidable_tiles = self.loadANDreturn_collidable_tiles(constants.level3_collidable_indexs)
            self.player.update()

            #Update Mobs
            for mobs in self.mob_objects:
                mobs.update(self.player.collidable_tiles,self.player.scroll)

            if diobox_test:
                diobox_test = self.dialogue_box("FBLA COMPETITION 2004",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                self.player.is_movingRight = False
                self.player.is_movingLeft = False

            #Update Notes
            for note in self.notes:
                note.update(self.player.collidable_tiles, self.player.scroll)

            #Scanning Notes
            for note in self.notes:
                if self.player.Rect.colliderect(note.Rect):
                    self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                    if is_E_pressed:
                        is_E_pressed = False
                        self.notes.remove(note)
                        if (note == note_1):
                            self.dialogue_box("Hello friend.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("I don't know why, but this place makes you oddly happy.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "It's ordinary, but there is no one around anymore to judge your existence.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "If only you can live in a rule-less place forever.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("...Where are we?",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                        if (note == note_2):
                            self.dialogue_box(
                                "Oh dear, are you having too much fun now?",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "I'm not going to beat around the bush anymore.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "I'm not going to run from the truth anymore, like you.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "You're pathetic for never reaching out to anyone near you.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "You played video games like these levels, but no one understood you.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "How will you escape loneliness if you never let people hear your voice?",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "You must contemplate your dark thoughts.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                        if (note == note_3):
                            self.dialogue_box(
                                "This place reminds you of all the time you put into playing video games.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("But no one around you liked or understood the things you did.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("No one bothered to value you with their precious time.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("And when they did, you ignored them and continued to play your games.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("I hope this place makes you contemplate your past. ",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("Remember? I'm just your conscience, an imaginary friend. Wake up.",
                                              [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                        progress += 1
                        score += 20


            if progress == 0:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_1.png"),[0,-10])
            if progress == 1:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_2.png"),[0,-10])
            if progress == 2:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_3.png"),[0,-10])
            if progress == 3:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_4.png"), [0,-10])
                running = False

            self.load_score(score, [4, 4])

            if pause:
                running = self.menu.pause(self.display,self.screen)
                pause = False
                self.player.is_movingLeft = False
                self.player.is_movingRight = False

            if self.player.health == 0:
                running = self.menu.game_over(self.display, self.screen)


            if not running:
                self.display.fill((0, 0, 0))
                if progress == 3:
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
                    return "End"
                else:
                    return "Level_3"

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        running = False
                        return "End"
                    if event.key == K_ESCAPE:
                        pause = True
                    if event.key == K_q:
                        diobox_test = True
                    if event.key == K_e:
                        is_E_pressed = True
                self.player.check_event(event)

            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)


########################################################################################################################
#                                                    SUB CLASS
########################################################################################################################

class Level1(Level):
    def __init__(self, clock, display,game_map_location,pygame_tile_image_list):
        Level.__init__(self, clock, display,game_map_location)
        #super.__init__(clock,display,game_map_location)

#mobs and players

        self.map_dictionary = {}
        n = 0
        for image in pygame_tile_image_list:
            self.map_dictionary[str(n)] = image
            # { '1' : pygame_image_1 , '2' : pyga,e_image_2 ....  }
            n += 1

    def loadANDreturn_collidable_tiles(self, colidable_index_list):
        game_map = functions.read_map(self.game_map_location)
        # list: [ [3,0,0,...] , [3,0,0,...] , ...]
        collidable_tiles = []

        y =0
        for row in game_map:
            x = 0
            for tile_num in row:
                if tile_num != '3':
                    self.display.blit(self.map_dictionary[tile_num], (x*self.TILESIZE - self.player.scroll[0],y*self.TILESIZE - self.player.scroll[1]))
                if tile_num == '1' or tile_num == '2' or tile_num == '3':
                    collidable_tiles.append(pygame.Rect(x * self.TILESIZE,y * self.TILESIZE,self.TILESIZE,self.TILESIZE))
                x += 1

            y += 1

        return collidable_tiles
#           ^color stuff for background here!!

    def game(self):
#snakes mobs set up
        snake1 = Mobs.Snakeworm(self.display, [16 * 66, 10 * 16 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30],
                                [30])
        snake2 = Mobs.Snakeworm(self.display, [16 * 112, 12 * 16 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30], [30])
        snake3 = Mobs.Snakeworm(self.display, [16 * 31, 16 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake4 = Mobs.Snakeworm(self.display, [16 * 23, 16 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake5 = Mobs.Snakeworm(self.display, [16 * 119, 19 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake6 = Mobs.Snakeworm(self.display, [16 * 33, 10 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake7 = Mobs.Snakeworm(self.display, [16 * 98, 11 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake8 = Mobs.Snakeworm(self.display, [16 * 69, 19 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake9 = Mobs.Snakeworm(self.display, [16 * 187, 3 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                [30, 30], [30])
        snake10 = Mobs.Snakeworm(self.display, [16 * 154, 18 * 14 - 2], 'images/level_1/Snakeworm', [16, 16], [30, 30],
                                 [30, 30], [30])

        note_1 = Mobs.Stickyfingers(self.display, [16 * 16, 17 * 16], "images/stickyfingers.png")
        note_2 = Mobs.Stickyfingers(self.display, [16 * 122, 6 * 16], "images/stickyfingers.png")
        note_3 = Mobs.Stickyfingers(self.display, [16 * 133, 16 * 16], "images/stickyfingers.png")

        self.mob_objects.append(snake1)
        self.mob_objects.append(snake2)
        self.mob_objects.append(snake3)
        self.mob_objects.append(snake4)
        self.mob_objects.append(snake5)
        self.mob_objects.append(snake6)
        self.mob_objects.append(snake7)
        self.mob_objects.append(snake8)
        self.mob_objects.append(snake9)
        self.mob_objects.append(snake10)
        self.notes.append(note_1)
        self.notes.append(note_2)
        self.notes.append(note_3)

        diobox_test = False
        pause = False

        #RUNNING
        running = True

        self.player = Mobs.Player(self.player_image, True, [16 * 9, 16 * 16 + 1], self.display, [30], [30], [30])
        collided = False

        self.player.health = 10
        cloudyvals = functions.rand_list(8*16,16*16,50)
        cloud_idexes = functions.rand_list(0,1,50)
        r = 0
        g = 0
        b = 0
        isr = False
        isg = False
        isb = False
        progress = 0
        score = 0
        is_E_pressed = False
 #copy dialogue here
        self.dialogue_box("Where...?",[10,10],K_w)

        while running:

            self.display.fill((r, g , b))

            self.player.collidable_tiles = self.loadANDreturn_collidable_tiles(constants.level3_collidable_indexs)
            self.player.update()
            # self.slime.update(self.player.collidable_tiles, self.player.scroll)
            # self.slime2.update(self.player.collidable_tiles, self.player.scroll)

            for mobs in self.mob_objects:
                mobs.update(self.player.collidable_tiles,self.player.scroll)


#mob collision, else is the idle
            for mob in self.mob_objects:
                if self.player.Rect.colliderect(mob.Rect):
                    score -= 1
                    if self.player.is_movingLeft:
                        self.player.is_movingLeft = False
                        self.player.updatehealth(-1)
                        self.player.extMove[0] += 15
                        self.player.extMove[1] += -10
                    elif self.player.is_movingRight:
                        self.player.is_movingRight = False
                        self.player.updatehealth(-1)
                        self.player.extMove[0] += -15
                        self.player.extMove[1] += -10
                    else:
                        if mob.is_movingL:
                            self.player.updatehealth(-1)
                            self.player.extMove[0] += -15
                            self.player.extMove[1] += -10
                        elif mob.is_movingR:
                            self.player.updatehealth(-1)
                            self.player.extMove[0] += 15
                            self.player.extMove[1] += -10
                        else:
                            self.player.extMove[0] += (random.randint(-1,1)*15)
                            self.player.extMove[1] += -10

#here, EDIT the notes. but is each self.display for each note? 9 in total also need to keep in mind the false and true for the loops
            for note in self.notes:
                note.update(self.player.collidable_tiles,self.player.scroll)
    
            for note in self.notes:
                if self.player.Rect.colliderect(note.Rect):
                    self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                    if is_E_pressed:
                        is_E_pressed = False
                        self.notes.remove(note)
                        if (note == note_1):
                            self.dialogue_box("Hello friend!",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("I hope it's you that's reading this...",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("I seem to be lost in a cave, so if you could, meet me somewhere brighter.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("I'll leave 2 other notes in this cave since I still have more pieces of paper left on me.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("See you friend!",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)

                        if (note == note_2):
                            self.dialogue_box("You know, while I am here, I do want to address something that's been on my mind.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("I know that you are my best friend, but I hope you find other people to talk to.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("Not that I don't want to still hangout with you, but you are always alone, you know?",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)

                        if (note == note_3):
                            self.dialogue_box("This cave is really creepy. I barely managed to dodge the snake-worm... thingys...",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("They really sting, but just jump over them, and they can't reach you.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("Remember, even if you are afraid of what's in the dark...",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("Breathe and step forward, like we have done before.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("On a brighter note, I finally see light! It's quite chilly though.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                            self.dialogue_box("See you soon hopefully?",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)

                        progress += 1
                        score += 20

            if self.player.health == 0:
                running = self.menu.game_over(self.display,self.screen)


            ##LIGHT for cave only
            for y in range(self.display.get_height()):
                for x in range(self.display.get_width()):
                    dist = [self.player.Rect.x + 8 - x - self.player.true_scroll[0], self.player.Rect.y - y - self.player.true_scroll[1]]
                    if math.sqrt((dist[0]*dist[0]) + (dist[1]*dist[1])) < 32:
                        color = self.display.get_at((x,y))
                        fc = []
                        for col in color:
                            if col+50 > 255:
                                fc.append(col)
                            else:
                                fc.append(col+50)

                        self.display.set_at((x,y), (fc[0], fc[1],fc[2]))
            ##DIMS EVERYTHING ELSE (For Cave map*)
            for y in range(self.display.get_height()):

                for x in range(self.display.get_width()):
                    color = self.display.get_at((x, y))
                    fc = []
                    for col in color:
                        if col - 50 < 0:
                            fc.append(50)
                        else:
                            fc.append(col - 50)

                    self.display.set_at((x, y), (fc[0], fc[1], fc[2]))






            if progress == 0:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_1.png"),[0,-10])
            if progress == 1:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_2.png"),[0,-10])
            if progress == 2:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_3.png"),[0,-10])
            if progress == 3:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_4.png"), [0,-10])
                running = False

            self.load_score(score, [4, 4])


            if diobox_test:
                diobox_test = self.dialogue_box("HELLO FBLA",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                self.player.is_movingRight = False
                self.player.is_movingLeft = False


            if pause:
                running = self.menu.pause(self.display,self.screen)
                pause = False
                self.player.is_movingLeft = False
                self.player.is_movingRight = False

            if not running:
                self.display.fill((0, 0, 0))
                if progress == 3:
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
                    return "Level_2"
                else:
                    return "Level_1"

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_r:
                        isr = False
                    if event.key == K_g:
                        isg = False
                    if event.key == K_b:
                        isb = False
                    if event.key == K_w:
                        is_E_pressed = False
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        running = False
                        return "Level_2"
                    if event.key == K_ESCAPE:
                        pause = True
                    if event.key == K_q:
                        diobox_test = True
                    if event.key == K_e:
                        is_E_pressed = True
                    if event.key == K_r:
                        isr = True
                    if event.key == K_g:
                        isg = True
                    if event.key == K_b:
                        isb = True
                self.player.check_event(event)

            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)
            ########################################################################################################################
            #                                                    SUB CLASS                                                         #
            ########################################################################################################################
#Attempt of level 2 begins here!
class Level2(Level):
    def __init__(self, clock, display, game_map_location, pygame_tile_image_list):
        Level.__init__(self, clock, display, game_map_location)
        # super.__init__(clock,display,game_map_location)

        self.snowFall = []
        for i in range(50):
            x = random.randrange(0, 180)
            y = random.randrange(0, 120)
            self.snowFall.append([x, y])

        # mobs and players (Ghosty will be here for level 2)
        self.player = Mobs.Player(self. player_image, True, [16 * 5, 16*11 -1], display, [30], [30], [30])

        self.map_dictionary = {}
        n = 1
        for image in pygame_tile_image_list:
            self.map_dictionary[str(n)] = image
            # { '1' : pygame_image_1 , '2' : pyga,e_image_2 ....  }
            n += 1

    def loadANDreturn_collidable_tiles(self, colidable_index_list):
        game_map = functions.read_map(self.game_map_location)
        # list: [ [3,0,0,...] , [3,0,0,...] , ...]
        collidable_tiles = []

        y = 0
        for row in game_map:
            x = 0
            for tile_num in row:
                if tile_num != '3' and tile_num != '0':
                    self.display.blit(self.map_dictionary[tile_num], (
                    x * self.TILESIZE - self.player.scroll[0], y * self.TILESIZE - self.player.scroll[1]))
                if tile_num == '1' or tile_num == '2' or tile_num == '3':
                    collidable_tiles.append(
                        pygame.Rect(x * self.TILESIZE, y * self.TILESIZE, self.TILESIZE, self.TILESIZE))
                x += 1

            y += 1

        return collidable_tiles

    def game(self):
        diobox_test = False
        pause = False

        # RUNNING
        running = True

        self.player = Mobs.Player(self.player_image, True, [16 * 5, 16*11 -1], self.display, [30], [30], [30])

        ghost1 = Mobs.Ghost(self.display, [16 * 15, 16 * 9 - 1], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost2 = Mobs.Ghost(self.display, [16 * 49, 16 * 5 - 2], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost3 = Mobs.Ghost(self.display, [16 * 77, 10 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])

        ghost4 = Mobs.Ghost(self.display, [16 * 188, 8 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost5 = Mobs.Ghost(self.display, [16 * 187, 16 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost6 = Mobs.Ghost(self.display, [16 * 143, 5 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost7 = Mobs.Ghost(self.display, [16 * 217, 17 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        ghost8 = Mobs.Ghost(self.display, [16 * 114, 6 * 16], 'images/level_2/ghosty', [16, 16], [30, 30], [30, 30],
                            [30])
        note_1 = Mobs.Stickyfingers(self.display, [16 * 7, 16 * 15], "images/stickyfingers.png")
        note_2 = Mobs.Stickyfingers(self.display, [16 * 133, 4 * 16], "images/stickyfingers.png")
        note_3 = Mobs.Stickyfingers(self.display, [16 * 180, 16 * 16], "images/stickyfingers.png")

        self.mob_objects.append(ghost1)
        self.mob_objects.append(ghost2)
        self.mob_objects.append(ghost3)
        self.mob_objects.append(ghost4)
        self.mob_objects.append(ghost5)
        self.mob_objects.append(ghost6)
        self.mob_objects.append(ghost7)
        self.mob_objects.append(ghost8)
        self.notes.append(note_1)
        self.notes.append(note_2)
        self.notes.append(note_3)

        collided = False

        self.player.health = 10
        cloudyvals = functions.rand_list(8 * 16, 16 * 16, 50)
        cloud_idexes = functions.rand_list(0, 1, 50)
        r = 0
        g = 0
        b = 0
        isr = False
        isg = False
        isb = False
        progress = 0
        score = 0
        is_E_pressed = False

        #randomize snow fall location

        while running:

            self.display.fill((157, 248, 249))

            self.player.collidable_tiles = self.loadANDreturn_collidable_tiles(constants.level3_collidable_indexs)
            self.player.update()
            # self.slime.update(self.player.collidable_tiles, self.player.scroll)
            # self.slime2.update(self.player.collidable_tiles, self.player.scroll)

            for i in range(len(self.snowFall)):
                pygame.draw.circle(self.display, [255,255,255], self.snowFall[i], 2)

                # Move the snowFall down one pixel
                self.snowFall[i][1] += 1

                # If the snowFall has moved off the bottom of the screen
                if self.snowFall[i][1] > 120:
                    # Reset it just above the top
                    y = random.randrange(-50, -10)
                    self.snowFall[i][1] = y

                    # Give it a new x position
                    x = random.randrange(0, 180)
                    self.snowFall[i][0] = x

            for mobs in self.mob_objects:
                mobs.update(self.player.collidable_tiles, self.player.scroll)

            # mob collision, else is the idle
            for mob in self.mob_objects:
                if self.player.Rect.colliderect(mob.Rect):
                    if self.player.is_movingLeft:
                        self.player.is_movingLeft = False
                        self.player.updatehealth(-1)
                        self.player.extMove[0] += 15
                        self.player.extMove[1] += -10
                    elif self.player.is_movingRight:
                        self.player.is_movingRight = False
                        self.player.updatehealth(-1)
                        self.player.extMove[0] += -15
                        self.player.extMove[1] += -10
                    else:
                        if mob.is_movingL:
                            self.player.updatehealth(-1)
                            self.player.extMove[0] += -15
                            self.player.extMove[1] += -10
                        elif mob.is_movingR:
                            self.player.updatehealth(-1)
                            self.player.extMove[0] += 15
                            self.player.extMove[1] += -10
                        else:
                            self.player.extMove[0] += (random.randint(-1, 1) * 15)
                            self.player.extMove[1] += -10

            for note in self.notes:
                note.update(self.player.collidable_tiles, self.player.scroll)

            for note in self.notes:
                if self.player.Rect.colliderect(note.Rect):
                    self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                    if is_E_pressed:
                        is_E_pressed = False
                        self.notes.remove(note)
                        if (note == note_1):
                            self.dialogue_box("Hello friend!",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box("If you made it out of there, you should be in some snowy place.",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box(
                                "I may not know what you think of this place, but it is relaxing.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "I could honestly use this as a break, but I'm afraid of frostbite...",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("I'll leave more notes, so you know where I am!",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box(
                                "In the meantime, I'm going to explore, feel free to take in the scenery.",
                                [10,
                                 self.display.get_height() - (self.display.get_height() / 2.5)],
                                K_w)
                            self.dialogue_box("P.S. be careful of the ghosts, they look nice, but they suck!",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box("See you friend!",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)

                        if (note == note_2):
                            self.dialogue_box(
                                "I do know that you have been feeling quite depressed these days.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "You think people are scary, but what if we work together to face them?",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "Not every person should be too terrible",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "Someone out there would care about you.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "Just please try, but don't push yourself.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                        if (note == note_3):
                            self.dialogue_box(
                                "I really hope you have been taking in the scenery.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box(
                                "This icy weather reminds me-",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("Remember that one time you found an apple still growing in the winter?",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box("Then you cooked an apple pie just for you?",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                            self.dialogue_box(
                                "It was burnt and crispy, but still delicious. Memories like these do warm me.",
                                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                            self.dialogue_box("You do feel something is warmer up ahead, see you soon...",
                                              [10,
                                               self.display.get_height() - (self.display.get_height() / 2.5)],
                                              K_w)
                        progress += 1
                        score += 20
            # here, EDIT the notes. but is each self.display for each note? 9 in total also need to keep in mind the false and true for the loops
                    # copy dialogue here

            if self.player.health == 0:
                running = self.menu.game_over(self.display, self.screen)

            if pause:
                running = self.menu.pause(self.display, self.screen)
                pause = False
                self.player.is_movingLeft = False
                self.player.is_movingRight = False

            if progress == 0:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_1.png"), [0, -10])
            if progress == 1:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_2.png"), [0, -10])
            if progress == 2:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_3.png"), [0, -10])
            if progress == 3:
                self.display.blit(pygame.image.load("images/gui/progress bar/progress_4.png"), [0, -10])
                running = False

            self.load_score(score, [4, 4])

            if diobox_test:
                diobox_test = self.dialogue_box("HELLO FBLA",
                                                [10, self.display.get_height() - (self.display.get_height() / 2.5)],
                                                K_w)
                self.player.is_movingRight = False
                self.player.is_movingLeft = False

            # no afterimage
            if not running:
                self.display.fill((0, 0, 0))
                if progress == 3:
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
                    return "Level_3"
                else:
                    return "Level_2"

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_r:
                        isr = False
                    if event.key == K_g:
                        isg = False
                    if event.key == K_b:
                        isb = False
                    if event.key == K_w:
                        is_E_pressed = False
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        running = False
                        return "Level_3"
                    if event.key == K_ESCAPE:
                        pause = True
                    if event.key == K_q:
                        diobox_test = True
                    if event.key == K_e:
                        is_E_pressed = True
                    if event.key == K_r:
                        isr = True
                    if event.key == K_g:
                        isg = True
                    if event.key == K_b:
                        isb = True
                self.player.check_event(event)

            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)



class End:
    def __init__(self, clock, display, screen):
        self.clock = clock
        self.display = display
        self.screen = screen
        self.menu = men.Menu(self.clock)

    def game(self):

        pause = False
        running = True
        frame = 0
        self.display.fill(pygame.image.load("images/End1.png").get_at((1,1)))
        while running:
            if frame == 0:
                self.display.blit(pygame.image.load("images/End1.png"),(10,0))

            if frame > 50:
                if frame < 80:
                    self.display.blit(pygame.image.load("images/End2.png"),(10,0))
                elif frame < 130:
                    if frame % 25 == 0:
                        self.display.blit(pygame.image.load("images/End2.png"),(10,0))
                    if frame % 50 == 0:
                        self.display.blit(pygame.image.load("images/End1.png"), (10, 0))
                elif frame > 150:
                    self.display.blit(pygame.image.load("images/Endcry.png"), (10, 0))

            if pause:
                running = self.menu.pause(self.display, self.screen)
                pause = False


            if not running:
                self.display.fill((0, 0, 0))
                return "Level_1"

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = True
                    if event.key == K_q:
                        diobox_test = True

            frame += 1
            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)

