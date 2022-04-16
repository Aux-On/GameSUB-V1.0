# Imports and Initializing Pygame
import sys, pygame
from src import functions, constants, level, Menu
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()



#Screen and Display
screen = pygame.display.set_mode(constants.WINDOWSIZE, 0, 32)
display = pygame.Surface(constants.surface_size)

#initializing levels, End and Menus
level1 = level.Level1(clock, screen, "map/level_3/map_1.txt", constants.level1_tile_image_list)
level3 = level.Level3(clock, screen, "map/level_3/map_0.txt", constants.level3_tile_image_list)
level2 = level.Level2(clock, screen, "map/level_3/map_2.txt", constants.level2_tile_image_list)
end = level.End(clock,display,screen)
menu = Menu.Menu(clock)

#initializing Main Menu
menu_image = pygame.image.load("images/Menuu.png")
click = False
game_index = "Level_1"

# music ( -1 = forever )
pygame.mixer.music.load("sounds/music/Victor.mp3")
pygame.mixer.music.play(-1)

small_font = functions.Font('images/gui/small_font.png', (255,255,255))


def dialogue_box(text, locationxy, quit_key_pygame):
    dialouge_surf = pygame.image.load("images/gui/lower_dialogue.png")
    box = pygame.image.load("images/gui/text_box.png")

    running = True
    while running:
        display.blit(pygame.image.load("images/press_w.png"), [0, 0])
        small_font.render(dialouge_surf, text, (10, 6))
        display.blit(dialouge_surf, locationxy)
        # dialouge_surf.blit(pygame.transform.scale(box, sizexy), (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == quit_key_pygame:
                    running = False
                    return False
        surf = pygame.transform.scale(display, constants.WINDOWSIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(constants.game_frames_per_second)

#Game Loop
while True:


    #Filling Display with image
    display.fill((menu_image.get_at((1, 1))[0], menu_image.get_at((1, 1))[1], menu_image.get_at((1, 1))[2]))
    display.blit(menu_image, [0, 0])

    #Gathering mouse locations (x,y) and adjusting for display
    mx, my = pygame.mouse.get_pos()
    mx = mx / 5
    my = my / 5

    #Play Button collision box
    button1_rect = pygame.rect.Rect(75, 58, 25, 9)
    #Testing Collisions
    if button1_rect.collidepoint(mx, my):
        #hovering Animation
        display.blit(pygame.image.load("images/playy.png"), [75, 58])
        #Testing for Click
        if click:
            #Adjusting for lack of test
            click = False

            #Stopping Music
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            #Checking for Current Level
            if game_index == "Level_1":
                # Adding New Player to Leaderboard
                with open("cache/Leaderboard.txt", "a") as f:
                    f.write('0\n')
                #Level 1 MUSIC
                pygame.mixer.music.load("sounds/music/McAfee.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/sounds/dripmp3-14875.wav"), -1)
                game_index = level1.game()
                pygame.mixer.Channel(1).stop()
            if game_index == "Level_2":
                ##Level 2 MUSIC
                pygame.mixer.music.load("sounds/music/SERENITY_AND.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/sounds/wind__artic__cold-6195.wav"), -1)
                game_index = level2.game()
                pygame.mixer.Channel(1).stop()
            if game_index == "Level_3":
                ##Level 3 MUSIC
                pygame.mixer.music.load("sounds/music/Finalle.mp3")
                pygame.mixer.music.play(-1)
                game_index = level3.game()
            if game_index == "End":
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                end.game()
            # Reloading menu music
            pygame.mixer.music.load("sounds/music/Victor.mp3")
            pygame.mixer.music.play(-1)

    #Intro Button
    button2_rect = pygame.rect.Rect(74, 73, pygame.image.load("images/Intro.png").get_width(),
                                    pygame.image.load("images/Intro.png").get_height())
    #Testing Collision
    if button2_rect.collidepoint(mx, my):
        display.blit(pygame.image.load("images/Intro.png"), [73, 72])
        if click:
            click = False
            display.fill((0,0,0))
            dialogue_box("Hello FBLA! Press [W] to continue! Text boxes may be continued by using this button.", (10,10), K_w)
            dialogue_box("You play the role of Guy, who finds himself inside an unusual place", (10, 10), K_w)
            dialogue_box("Follow the notes to guide Guy out of his place.", (10, 10), K_w)
            dialogue_box("Use the Arrow Keys to Maneuver, and [E] to interact with the sticky notes", (10, 10), K_w)

    #Leaderboard
    button3_rect = pygame.rect.Rect(52, 85, pygame.image.load("images/leaderboard.png").get_width(),
                                    pygame.image.load("images/leaderboard.png").get_height())
    #Teasting Collisions
    if button3_rect.collidepoint(mx, my):
        display.blit(pygame.image.load("images/leaderboard.png"), [52, 85])
        if click:
            click = False
            menu.leaderboard(display,screen)

    #Exit Button, Leave, learn, laugh, cry. Don't sit there >:(
    button4_rect = pygame.rect.Rect(76, 101, pygame.image.load("images/exit.png").get_width(),
                                    pygame.image.load("images/exit.png").get_height())
    if button4_rect.collidepoint(mx, my):
        display.blit(pygame.image.load("images/exit.png"), [76, 101])
        if click:
            sys.exit()

    #checking for events Is it applicable? yes!!!
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                click = False

    #Update surface to screen
    surf = pygame.transform.scale(display, constants.WINDOWSIZE)
    screen.blit(surf, (0, 0))

    #update Display
    pygame.display.update()
    #Tick clock
    clock.tick(constants.game_frames_per_second)
