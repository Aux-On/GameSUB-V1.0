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
        removed_notes = []

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
                fakenote = False

                for rnote in removed_notes:
                    if note == rnote:
                        self.notes.remove(note)
                        fakenote = True

                if not fakenote:
                    if self.player.Rect.colliderect(note.Rect):
                        self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                        if is_E_pressed:
                            is_E_pressed = False
                            removed_notes.append(note)
                            self.notes.remove(note)
                            if (note == note_1):
                                self.dialogue_box("So anyways, I am SO going to lose my marbles soon",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("Like, yeah, my 5 children are how old are they? 30 In Kindergarten I think that's the right age, I don't freaking know.",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "But like, the school they go to used to get government funding and we might starve soon without the free reduced lunch",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "I might have to apply for food stamps and that's like, extremely shameful",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("I hope I can feed my children soon",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                            if (note == note_2):
                                self.dialogue_box(
                                    "This mayor, I want to SLAP her, she has been the one cutting the funding to the school!!",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "Not only that but the chess club stopped being funded, shutting down many clubs and now I have to deal with my children longer!",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "And also they now don't let me watch my children and allow me be a Tiger Mom",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "SO NOT FAIR",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                            if (note == note_3):
                                self.dialogue_box("Nevermind, my creepy friend told me how voting works, and I think I will vote for Carmen",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("She is such a role model, and what I want my children to be like exactly like her",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("With her help, maybe we can make sure no one else will starve in this city!",
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
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
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
        removed_notes = []

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
                fakenote = False

                for rnote in removed_notes:
                    if note == rnote:
                        self.notes.remove(note)
                        fakenote = True

                if not fakenote:
                    if self.player.Rect.colliderect(note.Rect):
                        self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                        if is_E_pressed:
                            is_E_pressed = False
                            removed_notes.append(note)
                            self.notes.remove(note)
                            if (note == note_1):
                                self.dialogue_box("(! This is Alex's diary about her voting plans!) (Pollution Potholes)",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("Dear Diary, I cannot believe I have been writing this diary for 15 years",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("Well technically, I lost this diary 5 years ago... then forgot to write in it until yesterday...",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("You, Mr. or Mrs. diary, are probably slightly mad at me right now.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("But even so, I have an important decision I need to make",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("There are many potholes that has been growing around the city and I wonder if I can petition if we can get these fix before any of my friends fall into these bottomless pits…",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)

                            if (note == note_2):
                                self.dialogue_box("Dear Diary, Recently, a new mayor was elected that most of my friends did not vote for, because we did not feel like our votes mattered at all",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("But this Mayor that shall not be named? She refuses to fill in any of the potholes!",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("She is instead focused on trying to blow up the potato farms. Sure they have been very rude to us, but if a mayor only listens to the people who vote for her, how can we live?",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)

                            if (note == note_3):
                                self.dialogue_box("Dear Diary,I have decided to vote for Mayor Carmen Sadiago",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("I really like her slogan: Defend the Maidenless",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("She has some things that I disagree with, but at least she wants to fill the plot holes, potholes, and protect the people.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("Even better, she even gave us her name!",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("I will gather all 2 of my friends to vote for this person, I hope this works.",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("The Mayor that shall not be named is going DOWN!",[10,self.display.get_height() - (self.display.get_height()/2.5)],K_w)
                                self.dialogue_box("(It looks like there are 2 more people I need to secure their votes!)",
                                                  [10, self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)

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
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
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
        removed_notes = []

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
                            self.player.extMove[0] += (random.randint(-1, 1) * 15)
                            self.player.extMove[1] += -10

            for note in self.notes:
                note.update(self.player.collidable_tiles, self.player.scroll)

            for note in self.notes:
                fakenote = False

                for rnote in removed_notes:
                    if note == rnote:
                        self.notes.remove(note)
                        fakenote = True

                if not fakenote:
                    if self.player.Rect.colliderect(note.Rect):
                        self.display.blit(pygame.image.load("images/gui/pressEtoInteract.png"), [0, 0])
                        if is_E_pressed:
                            is_E_pressed = False
                            removed_notes.append(note)
                            self.notes.remove(note)
                            if (note == note_1):
                                self.dialogue_box("(! These are Nora's text files!)",
                                                  [10,
                                                   self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)
                                self.dialogue_box("I have been informed that my grandmother is still in the rehabilitation hospital from her opioid addiction.",
                                                  [10,
                                                   self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)
                                self.dialogue_box(
                                    "She however cannot leave the hospital and the hospital is planned to be destroyed",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "I may be ice cold to everyone, but she is the only warmth in my world",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("I need to make sure she will leave and be safe",
                                                  [10,
                                                   self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)
                                self.dialogue_box(
                                    "Or I will not have anything to live for.",
                                    [10,
                                     self.display.get_height() - (self.display.get_height() / 2.5)],
                                    K_w)

                            if (note == note_2):
                                self.dialogue_box(
                                    "I had thought politics was something only grandmothers loved to do Something quite boring and unwelcoming",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "But since my grandmother's coma from her addiction, I have been working hard to pay all the taxes",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "But this... mayor",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "She is the person who wants to harm my grandmother.",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "She will not see the light of victory soon.",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)

                            if (note == note_3):
                                self.dialogue_box(
                                    "My eccentric friend brought up the idea to vote for a new mayor soon.",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box(
                                    "I have a plan. I initially was going to dispose and make the current mayor move away",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
                                self.dialogue_box("But this plan is genius.",
                                                  [10,
                                                   self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)
                                self.dialogue_box("If I can stop this person from destroying the rehabilitation hospital, I will finish this by legal means. I will need to get our last friend in this plan.",
                                                  [10,
                                                   self.display.get_height() - (self.display.get_height() / 2.5)],
                                                  K_w)
                                self.dialogue_box(
                                    "(!Alright! One more person!)",
                                    [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)
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
                    with open("cache/Leaderboard.txt", "r+") as f:
                        lines = f.readlines()
                        current = int(str.strip(lines[-1]))
                        current += score
                        lines[-1] = str(current) + "\n"
                        f.seek(0)
                        f.writelines(lines)
                    return "Level_2"

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYUP:
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
        self.small_font = functions.Font('images/gui/small_font.png', (150, 100, 139))
        self.large_font = functions.Font('images/gui/large_font.png', (150, 100, 139))

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

    def game(self):

        pause = False
        click = False
        running = True
        frame = 0
        self.display.fill(pygame.image.load("images/End1.png").get_at((1,1)))
        while running:

            self.dialogue_box(
                "(Okay, that should be it. Let's hope Mayor Carmen Sandiago Santiago Sandiego wins!) Press W to close, then click anywhere",
                [10, self.display.get_height() - (self.display.get_height() / 2.5)], K_w)


            if click:
                running = False

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
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True

            frame += 1
            surf = pygame.transform.scale(self.display, constants.WINDOWSIZE)
            self.screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)

