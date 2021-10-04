import random
import pygame
from pygame import mixer
# initializing
pygame.init()
pygame.display.set_caption("Shoot em' Up")
screen = pygame.display.set_mode((1024, 600))
pygame.display.set_icon(pygame.image.load("icon.png"))
backgroundimg = pygame.image.load("space-2.png")
titleimg = pygame.image.load("title.png")
pressspace = pygame.image.load("pressspace.png")
spaceship = pygame.image.load("science-fiction.png")
playerimg = pygame.image.load("science-fiction (2).png")
bulletimg = pygame.image.load("bullet.png")
shot2img = pygame.image.load("bullet2.png")
enemyimg1 = pygame.image.load("sp1.png")
enemyimg2 = pygame.image.load("sp2.png")
expimg = pygame.image.load("explosion.png")
font = pygame.font.Font("orange juice 2.0.ttf", 40)
destroy = pygame.mixer.Sound("destroy.wav")
laser = pygame.mixer.Sound("laser.wav")
img1y, img2y = -1024, 0
titley = 600
run = True
play = False
gameover = False
score, hscore = 0, 0
k = 0
pygame.mixer.music.load("music2.wav")
pygame.mixer.music.play(-1)
while run:
    if gameover is True:
        text = font.render("Your Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (400, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameover = False
                    k = 0
    elif play is False:
        player_x, player_y = 475, 500
        change_x = 0
        flist, elist, shot2lst, explist = [], [], [], []
        screen.blit(backgroundimg, (0, img2y))
        screen.blit(backgroundimg, (0, img1y))
        screen.blit(titleimg, (250, titley))
        if titley >= 220:
            titley -= 3
        else:
            screen.blit(spaceship, (800, 220))
            if k % 64 in range(32):
                screen.blit(pressspace, (300, 350))
        if score > hscore:
            hscore = score
        if hscore != 0:
            text = font.render("High score: "+ str(hscore), True, (0, 255, 0))
            screen.blit(text, (200, 100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = True
                    pygame.mixer.music.load("music.wav")
                    pygame.mixer.music.play(-1)
                    k = 0
                    score = 0
            if event.type == pygame.QUIT:
                run = False
    elif play is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_x = 8
                if event.key == pygame.K_LEFT:
                    change_x = -8
                if event.key == pygame.K_SPACE:
                    laser.play()
                    flist.append([player_x + 27, player_y - 20])
            if event.type == pygame.KEYUP:
                change_x = 0
        screen.blit(backgroundimg, (0, img1y))
        screen.blit(backgroundimg, (0, img2y))
        img1y = img1y + 1
        img2y = img2y + 1
        player_x += change_x
        if player_x <= 0:
            player_x = 0
        if player_x >= 959:
            player_x = 959
        if img2y == 1024:
            img2y = -1024
        if img1y == 1024:
            img1y = -1024
        screen.blit(playerimg, (player_x, player_y))
        if len(elist) < 3:
            y = random.choice([enemyimg1, enemyimg2])
            if y is enemyimg1:
                elist.append([y, -64, random.choice([64, 160, 256, 352])])
            elif y is enemyimg2:
                elist.append([y, 1088, random.choice([64, 160, 256, 352])])
        for i in range(len(elist)):
            screen.blit(elist[i][0], (elist[i][1], elist[i][2]))
            if elist[i][0] == enemyimg1:
                elist[i][1] += score // 50 + 3
                if elist[i][1] >= 1024:
                    del elist[i]
                    break
            elif elist[i][0] == enemyimg2:
                elist[i][1] -= score // 50 + 3
                if elist[i][1] <= -64:
                    del elist[i]
                    break
        if k == 60:
            for i in range(len(elist)):
                s2x = elist[i][1] + 27
                s2y = elist[i][2] + 50
                shot2lst.append([s2x, s2y])
                k = 0
        for i in range(len(shot2lst)):
            screen.blit(shot2img, (shot2lst[i][0], shot2lst[i][1]))
            shot2lst[i][1] += 4
        for i in range(len(flist)):
            if flist[i][1] <= 0:
                del flist[i]
                break
            else:
                screen.blit(bulletimg, (flist[i][0], flist[i][1]))
                flist[i][1] -= 20
        for i in range(len(elist)):
            for j in range(len(flist)):
                if (flist[j][0] - elist[i][1] - 32) ** 2 + (flist[j][1] - elist[i][2] - 32) ** 2 <= 2025:
                    del flist[j]
                    explist.append([elist[i][1], elist[i][2], 0])
                    elist[i] = random.choice([[enemyimg1, -64, random.choice([64, 160, 256, 352])],
                                              [enemyimg2, 1088, random.choice([64, 160, 256, 352])]])
                    score += 1
                    destroy.play()
                    break
        for i in range(len(explist)):
            if explist[i][2] <= 6:
                screen.blit(expimg, (explist[i][0], explist[i][1]))
                explist[i][2] += 1
            else:
                del explist[i]
                break
        for i in shot2lst:
            if (i[0] - player_x - 32) ** 2 + (i[1] - player_y - 32) ** 2 <= 2025:
                play = False
                screen.blit(expimg, (player_x, player_y))
                destroy.play()
                destroy.play()
                pygame.mixer.music.load("music2.wav")
                pygame.mixer.music.play(-1)
                gameover = True
        text = font.render("Score: " + str(score), True,  (255, 255, 255))
        screen.blit(text, (0, 0))

    k += 1
    pygame.display.update()