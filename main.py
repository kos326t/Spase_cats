import time
from sprite import *
import pygame as pg


def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(spase, (0, 0))
    screen.blit(sprite.image, sprite.rect)

    text1 = font.render(text[text_number], True, "white")
    screen.blit(text1, (280, 450))

    if text_number < len(text) - 1:
        text2 = font.render(text[text_number + 1], True, "white")
        screen.blit(text2, (280, 470))


pg.init()
pg.mixer.init()

size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()

is_running = True
mode = "start_scene"

heart = pg.image.load("heart.png").convert_alpha()
heart = pg.transform.scale(heart, (30, 30))
heart_count = 3

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()
starship = Starship()

spase = pg.image.load("фон.png")

start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, синие амогусы,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и синие в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите синих!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? жёлтые? фиолетовые?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден скибиди тоилет.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "Я выйграл!!! >:)",
              "",
              "...",
              "",
              "ты чего не закрываешь окно?",
              "игра закончена",
              "чего ты хочешь?",
              "тут больше делать нечего",
              "закрывай игру",
              "это её конец",
              "bruh",
              "-_-",
              "тогда я просто тебе ничего не буду говорить",
              ">:)",
              "...",
              "...",
              "конец"
              ""]

text_number = 0
font = pg.font.Font("шрифт.otf", 25)

pg.mixer.music.load("musik.wav")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play()

laser_sound = pg.mixer.Sound("laser_sound.wav")
laser_sound.set_volume(0.2)
win_sound = pg.mixer.Sound("win_sound.wav")

captain = Captain()
alien = Alien()

while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
            if mode == "start_scene":
                text_number += 2
                if text_number > len(start_text):
                    text_number = 0
                    mode = "meteorites"
                    start_time = time.time()

            if mode == "alien_scene":
                text_number += 2
                if text_number > len(alien_text):
                    text_number = 0
                    alien.rect.topleft = (-30, 600)
                    alien.mode = "up"
                    mode = "moon"
                    starship.switch_mode()
                    ochki = 0
                    heart_count = 3

            if mode == "final_scene":
                text_number += 2
                if text_number > len(final_text):
                    text_number = 0
                    mode = "end"

        if event.type == pg.MOUSEBUTTONDOWN:
            if mode == "moon":
                if event.button == 1:
                    lasers.add(Laser(starship.rect.center))
                    laser_sound.play()

    # ОБНОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(captain, start_text)

    if mode == "meteorites":
        if time.time() - start_time > 25.0:
            mode = "alien_scene"

        if random.randint(1, 50) == 2:
            meteorites.add(Meteorite())

        meteorites.update()
        starship.update()

        hits = pg.sprite.spritecollide(starship, meteorites, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        screen.blit(spase, (0,0))
        meteorites.draw(screen)
        screen.blit(starship.image, starship.rect)

        for i in range(heart_count):
            screen.blit(heart, (i * 30, 0))

    if mode == "alien_scene":
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        if ochki == 25:
            mode = "final_scene"
            pg.mixer.music.fadeout(3)
        #     mode = "final_scene"
        #     pg.mixer.music.fadeout(3)
        #     win_sound.play()

        if random.randint(1, 50) == 2:
            mice.add(Mouse_starship())

        mice.update()
        starship.update()
        lasers.update()

        hits = pg.sprite.spritecollide(starship, mice, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        hits = pg.sprite.groupcollide(lasers, mice, True, True)
        ochki += len(hits)

        screen.blit(spase, (0, 0))
        mice.draw(screen)
        screen.blit(starship.image, starship.rect)
        lasers.draw(screen)

        for i in range(heart_count):
            screen.blit(heart, (i * 30, 0))

    if mode == "final_scene":
        dialogue_mode(alien, final_text)

    pg.display.flip()
    clock.tick(FPS)
