import pygame, sys, os

from pygame.locals import *
from src import constants, functions



class Menu:

    def __init__(self, clock):
        # self.surface = surface
        # self.background_img = background_img
        # self.buttonInitImg = buttonInitImg
        # self.buttonFinalImg = buttonFinalImg
        self.clock = clock
        self.font = functions.Font("images/gui/small_font.png",(255,255,255))

    # def main_menu(self, location_b1, location_b2):
    #
    #     index = 0
    #
    #     click = False
    #     running = True
    #     while running:
    #         self.surface.blit(self.background_img,(0,0))
    #
    #         mx,my = pygame.mouse.get_pos()
    #
    #         button_1 = pygame.Rect(location_b1[0], location_b1[1], self.buttonInitImg.get_width(), self.buttonInitImg.get_height())
    #         self.surface.blit(self.buttonInitImg,location_b1)
    #         self.surface.blit(self.buttonInitImg,location_b1)
    #
    #         if button_1.collidepoint(mx,my):
    #             self.surface.blit(self.buttonFinalImg, location_b1)
    #             if click:
    #                 running = False
    #                 index = 1
    #                 return index
    #
    #         button_2 = pygame.Rect(location_b2[0], location_b2[0], self.buttonInitImg.get_width(), self.buttonInitImg.get_height())
    #         self.surface.blit(self.buttonInitImg, location_b2)
    #
    #         if button_2.collidepoint(mx,my):
    #             self.surface.blit(self.buttonFinalImg, location_b2)
    #             if click:
    #                 running = False
    #                 index = 2
    #                 return index
    #
    #         click = False
    #
    #         for event in pygame.event.get():
    #             if event.type == QUIT:
    #                 sys.exit()
    #             if event.type == MOUSEBUTTONDOWN:
    #                 if event.button == 1:
    #                     click = True
    #
    #         pygame.display.update()
    #         self.clock.tick(30)





    def game_over(self, display, screen):

        running = True
        frames_ran = 0
        click = False


        while running:
            display.fill((0,0,0))

            display.blit(pygame.image.load("images/menus/game_over.png"),[0,0])

            mx,my = pygame.mouse.get_pos()
            mx = mx/5
            my = my/5

            menu_rect = pygame.rect.Rect(47,88,pygame.image.load("images/menus/game_over_main_menu_screen.png").get_width(),pygame.image.load("images/menus/game_over_main_menu_screen.png").get_height())

            if menu_rect.collidepoint(mx,my):
                display.blit(pygame.image.load("images/menus/game_over_main_menu_screen.png"), [menu_rect.x, menu_rect.y])
                if click:
                    running = False
                    return False


            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True


            surf = pygame.transform.scale(display, constants.WINDOWSIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)

    def pause(self, display,screen):
        running = True
        frames_ran = 0
        click = False

        while running:
            display.fill((0, 0, 0))

            display.blit(pygame.image.load("images/paused.png"), [0, 0])

            mx, my = pygame.mouse.get_pos()
            mx = mx / 5
            my = my / 5

            menu_rect = pygame.rect.Rect(54, 68,
                                         pygame.image.load("images/mainmenupause.png").get_width(),
                                         pygame.image.load("images/mainmenupause.png").get_height())
            if menu_rect.collidepoint(mx, my):
                display.blit(pygame.image.load("images/mainmenupause.png"),[menu_rect.x, menu_rect.y])
                if click:
                    running = False
                    return False

            exit_rect = pygame.rect.Rect(78, 85,
                                         pygame.image.load("images/quitmenupause.png").get_width(),
                                         pygame.image.load("images/quitmenupause.png").get_height())
            if exit_rect.collidepoint(mx, my):
                display.blit(pygame.image.load("images/quitmenupause.png"),[exit_rect.x,exit_rect.y])
                if click:
                    running = False
                    sys.exit()

            cont_rect = pygame.rect.Rect(57, 51,
                                         pygame.image.load("images/Continuepause.png").get_width(),
                                         pygame.image.load("images/Continuepause.png").get_height())
            if cont_rect.collidepoint(mx, my):
                display.blit(pygame.image.load("images/Continuepause.png"), [cont_rect.x, cont_rect.y])
                if click:
                    running = False
                    return True




            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            surf = pygame.transform.scale(display, constants.WINDOWSIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)

    def leaderboard(self, display, screen):

        running = True
        click = False

        while running:
            display.fill((0, 0, 0))

            display.blit(pygame.image.load("images/leaderboardmen.png"), [0, 0])

            y = 30
            x = 40
            index = 0
            f = open("cache/Leaderboard.txt", "r")
            for line in f:
                c = str.strip(line)
                self.font.render(display,"Player . . . " + c,(x,y))
                index += 1
                y += 20

            f.close()




            mx, my = pygame.mouse.get_pos()
            mx = mx / 5
            my = my / 5
            print(mx, my)

            exit_rect = pygame.rect.Rect(10, 103,
                                         pygame.image.load("images/exit2.png").get_width(),
                                         pygame.image.load("images/exit2.png").get_height())
            if exit_rect.collidepoint(mx, my):
                display.blit(pygame.image.load("images/exit2.png"), [exit_rect.x, exit_rect.y])
                if click:
                    running = False
                    return True

            clear_rect = pygame.rect.Rect(135, 103,
                                         pygame.image.load("images/press_clear.png").get_width(),
                                         pygame.image.load("images/press_clear.png").get_height())
            if clear_rect.collidepoint(mx, my):
                display.blit(pygame.image.load("images/press_clear.png"), [clear_rect.x, clear_rect.y])
                if click:
                    open('cache/Leaderboard.txt', 'w').close()




            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        click = False

            surf = pygame.transform.scale(display, constants.WINDOWSIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            self.clock.tick(constants.game_frames_per_second)


