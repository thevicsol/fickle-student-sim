import pygame
import random
from PIL import Image


def changepiece(piece, curdir):
    dirs = [[False, 0], [False, 3], [False, 2], [True, 4], [False, 1], [False, 4], [True, 2], [True, 3]]
    piece.image = piece.image.subsurface(pygame.Rect((0, dirs[curdir][1] * 484), (194, 484)))
    if dirs[curdir][0]:
        piece.image = pygame.transform.flip(piece.image, True, False)


def main(n, home):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    curdir = 0
    background = pygame.transform.scale(pygame.image.load('sprites/minigamebg.png'), (1280, 720))
    background_rect = background.get_rect()
    sprites = pygame.sprite.Group()
    arrow1 = pygame.sprite.Sprite()
    arrow1.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow1.rect = arrow1.image.get_rect()
    arrow1.rect.x = 100
    arrow1.rect.y = 50
    sprites.add(arrow1)
    arrow2 = pygame.sprite.Sprite()
    arrow2.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow2.rect = arrow2.image.get_rect()
    arrow2.rect.x = 600
    arrow2.rect.y = 50
    sprites.add(arrow2)
    arrow3 = pygame.sprite.Sprite()
    arrow3.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow3.rect = arrow3.image.get_rect()
    arrow3.rect.x = 100
    arrow3.rect.y = 200
    sprites.add(arrow3)
    arrow4 = pygame.sprite.Sprite()
    arrow4.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow4.rect = arrow4.image.get_rect()
    arrow4.rect.x = 600
    arrow4.rect.y = 200
    sprites.add(arrow4)
    arrow5 = pygame.sprite.Sprite()
    arrow5.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow5.rect = arrow5.image.get_rect()
    arrow5.rect.x = 100
    arrow5.rect.y = 350
    sprites.add(arrow5)
    arrow6 = pygame.sprite.Sprite()
    arrow6.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow6.rect = arrow6.image.get_rect()
    arrow6.rect.x = 600
    arrow6.rect.y = 350
    sprites.add(arrow6)
    arrow7 = pygame.sprite.Sprite()
    arrow7.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow7.rect = arrow7.image.get_rect()
    arrow7.rect.x = 100
    arrow7.rect.y = 500
    sprites.add(arrow7)
    arrow8 = pygame.sprite.Sprite()
    arrow8.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow8.rect = arrow8.image.get_rect()
    arrow8.rect.x = 600
    arrow8.rect.y = 500
    sprites.add(arrow8)
    arrow9 = pygame.sprite.Sprite()
    arrow9.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow9.rect = arrow9.image.get_rect()
    arrow9.rect.x = 200
    arrow9.rect.y = 600
    sprites.add(arrow9)
    arrow10 = pygame.sprite.Sprite()
    arrow10.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow10.rect = arrow10.image.get_rect()
    arrow10.rect.x = 500
    arrow10.rect.y = 600
    sprites.add(arrow10)
    arrow11 = pygame.sprite.Sprite()
    arrow11.image = pygame.transform.scale(pygame.image.load("sprites/arrow_left.png"), (40, 40))
    arrow11.rect = arrow11.image.get_rect()
    arrow11.rect.x = 225
    arrow11.rect.y = 680
    sprites.add(arrow11)
    arrow12 = pygame.sprite.Sprite()
    arrow12.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (40, 40))
    arrow12.rect = arrow12.image.get_rect()
    arrow12.rect.x = 475
    arrow12.rect.y = 680
    sprites.add(arrow12)
    nextarr = pygame.sprite.Sprite()
    nextarr.image = pygame.transform.scale(pygame.image.load("sprites/arrow_right.png"), (70, 70))
    nextarr.rect = nextarr.image.get_rect()
    nextarr.rect.x = 1100
    nextarr.rect.y = 550
    sprites.add(nextarr)
    player = pygame.sprite.Sprite()
    player.image = pygame.image.load("sprites/skin1.png")
    player.rect = player.image.get_rect()
    player.rect.x = 275
    player.rect.y = 50
    changepiece(player, curdir)
    sprites.add(player)
    hair1 = pygame.sprite.Sprite()
    hair1.image = pygame.image.load("sprites/hair1.png")
    hair1.rect = hair1.image.get_rect()
    hair1.rect.x = 275
    hair1.rect.y = 50
    changepiece(hair1, curdir)
    sprites.add(hair1)
    body1 = pygame.sprite.Sprite()
    body1.image = pygame.image.load("sprites/body1.png")
    body1.rect = body1.image.get_rect()
    body1.rect.x = 275
    body1.rect.y = 50
    changepiece(body1, curdir)
    sprites.add(body1)
    legs1 = pygame.sprite.Sprite()
    legs1.image = pygame.image.load("sprites/legs1.png")
    legs1.rect = legs1.image.get_rect()
    legs1.rect.x = 275
    legs1.rect.y = 50
    changepiece(legs1, curdir)
    sprites.add(legs1)
    boots1 = pygame.sprite.Sprite()
    boots1.image = pygame.image.load("sprites/boots1.png")
    boots1.rect = boots1.image.get_rect()
    boots1.rect.x = 275
    boots1.rect.y = 50
    changepiece(boots1, curdir)
    sprites.add(boots1)

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1280, 720))
    exit = True

    currhair = 1
    currbody = 1
    currlegs = 1
    currboots = 1
    currskin = 1
    font = pygame.font.SysFont('Courier', 40)  # шрифт вводимого текста
    input_box = pygame.Rect(800, 500, 150, 42)  # поле ввода текста
    color_inactive = pygame.Color('lightskyblue3')  # цвет поля ввода, когда оно неактивно
    color_active = (166, 97, 181)  # когда активно
    color = color_inactive
    active = False  # активно ли поле ввода в данный момент
    text = ''  # текст, который вводит игрок
    alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя' -"  # допустимые для ввода знаки
    cur_char = 0  # позиция в фразе, после которой печатается текст (изначально - начало слова)
    pointer = 0  # как часто мигает текстовый курсор
    showpointer = True  # виден ли сейчас курсор

    while exit:
        screen.blit(background, background_rect)
        sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = False
                if active:
                    if event.key == pygame.K_BACKSPACE:  # стирание символов
                        if cur_char != 0:  # если позиция ввода - начало фразы, стирать нечего, иначе стирается
                            text = text[:cur_char - 1] + text[cur_char:]
                            cur_char = cur_char - 1
                    elif event.key == pygame.K_LEFT:  # перемещение влево по введенной фразе
                        if cur_char != 0:
                            cur_char = cur_char - 1
                    elif event.key == pygame.K_RIGHT:  # вправо
                        if cur_char != len(text):
                            cur_char = cur_char + 1
                    elif event.unicode.lower() in alphabet and event.unicode != '':  # ввод букв
                        text = text[:cur_char] + event.unicode + text[cur_char:]
                        cur_char = cur_char + 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):  # проверяется, нажал ли игрок на поле ввода текста
                    active = not active  # если нажал, ввод активируется
                else:
                    active = False
                if nextarr.rect.collidepoint(event.pos):
                    exit = False
                    skin = Image.open(f'sprites/skin{currskin}.png')
                    hair = Image.open(f'sprites/hair{currhair}.png')
                    boots = Image.open(f'sprites/boots{currboots}.png')
                    legs = Image.open(f'sprites/legs{currlegs}.png')
                    body = Image.open(f'sprites/body{currbody}.png')
                    sheet = Image.new("RGBA", skin.size)
                    sheet = Image.alpha_composite(sheet, skin)
                    sheet = Image.alpha_composite(sheet, hair)
                    sheet = Image.alpha_composite(sheet, boots)
                    sheet = Image.alpha_composite(sheet, legs)
                    sheet = Image.alpha_composite(sheet, body)
                    sheet.save(f"sprites/spritesheet{n}.png")
                    with open(f'data/save{n}.dat', 'w', encoding='utf8') as f:
                        f.write(f'{text};')
                        for i in range(2):
                            skin = Image.open(f'sprites/skin{random.randrange(1, 8)}.png')
                            hair = Image.open(f'sprites/hair{random.randrange(1, 17)}.png')
                            boots = Image.open(f'sprites/boots{random.randrange(1, 4)}.png')
                            legs = Image.open(f'sprites/legs{random.randrange(1, 9)}.png')
                            body = Image.open(f'sprites/body{random.randrange(1, 16)}.png')
                            sheet = Image.new("RGBA", skin.size)
                            sheet = Image.alpha_composite(sheet, skin)
                            sheet = Image.alpha_composite(sheet, hair)
                            sheet = Image.alpha_composite(sheet, boots)
                            sheet = Image.alpha_composite(sheet, legs)
                            sheet = Image.alpha_composite(sheet, body)
                            sheet.save(f"sprites/npc{n}_{i}.png")
                        f.write('0;480;home;999;0;0;100;100;100;1894;')
                        for i in range(7):
                            schedule_main()
                            schedule_person()
                            schedule_final()
                            f.write(f'{classes[0]}.{classes[1]}.{classes[2]}.{classes[3]}.{classes[4]}')
                            if i != 6:
                                f.write(',')
                        for i in range(8):
                            f.write('\n')

                    home(999, (0, 0), 'menu',)
                if arrow1.rect.collidepoint(event.pos):
                    currhair -= 1
                    if currhair >= 1:
                        hair1.image = pygame.image.load(f'sprites/hair{currhair}.png')
                    else:
                        hair1.image = pygame.image.load(f'sprites/hair16.png')
                        currhair = 16
                    changepiece(hair1, curdir)
                if arrow2.rect.collidepoint(event.pos):
                    currhair += 1
                    if currhair <= 16:
                        hair1.image = pygame.image.load(f'sprites/hair{currhair}.png')
                    else:
                        hair1.image = pygame.image.load(f'sprites/hair1.png')
                        currhair = 1
                    changepiece(hair1, curdir)
                if arrow3.rect.collidepoint(event.pos):
                    currbody -= 1
                    if currbody >= 1:
                        body1.image = pygame.image.load(f'sprites/body{currbody}.png')
                    else:
                        body1.image = pygame.image.load(f'sprites/body15.png')
                        currbody = 15
                    changepiece(body1, curdir)
                if arrow4.rect.collidepoint(event.pos):
                    currbody += 1
                    if currbody <= 15:
                        body1.image = pygame.image.load(f'sprites/body{currbody}.png')
                    else:
                        body1.image = pygame.image.load(f'sprites/body1.png')
                        currbody = 1
                    changepiece(body1, curdir)
                if arrow5.rect.collidepoint(event.pos):
                    currlegs -= 1
                    if currlegs >= 1:
                        legs1.image = pygame.image.load(f'sprites/legs{currlegs}.png')
                    else:
                        legs1.image = pygame.image.load(f'sprites/legs8.png')
                        currlegs = 8
                    changepiece(legs1, curdir)
                if arrow6.rect.collidepoint(event.pos):
                    currlegs += 1
                    if currlegs <= 8:
                        legs1.image = pygame.image.load(f'sprites/legs{currlegs}.png')
                    else:
                        legs1.image = pygame.image.load(f'sprites/legs1.png')
                        currlegs = 1
                    changepiece(legs1, curdir)
                if arrow7.rect.collidepoint(event.pos):
                    currboots -= 1
                    if currboots >= 1:
                        boots1.image = pygame.image.load(f'sprites/boots{currboots}.png')
                    else:
                        boots1.image = pygame.image.load(f'sprites/boots3.png')
                        currboots = 3
                    changepiece(boots1, curdir)
                if arrow8.rect.collidepoint(event.pos):
                    currboots += 1
                    if currboots <= 3:
                        boots1.image = pygame.image.load(f'sprites/boots{currboots}.png')
                    else:
                        boots1.image = pygame.image.load(f'sprites/boots1.png')
                        currboots = 1
                    changepiece(boots1, curdir)
                if arrow9.rect.collidepoint(event.pos):
                    currskin -= 1
                    if currskin >= 1:
                        player.image = pygame.image.load(f'sprites/skin{currskin}.png')
                    else:
                        player.image = pygame.image.load(f'sprites/skin3.png')
                        currskin = 7
                    changepiece(player, curdir)
                if arrow10.rect.collidepoint(event.pos):
                    currskin += 1
                    if currskin <= 7:
                        player.image = pygame.image.load(f'sprites/skin{currskin}.png')
                    else:
                        player.image = pygame.image.load(f'sprites/skin1.png')
                        currskin = 1
                    changepiece(player, curdir)
                if arrow11.rect.collidepoint(event.pos):
                    curdir = curdir - 1
                    if curdir == -1:
                        curdir = 7
                    player.image = pygame.image.load(f'sprites/skin{currskin}.png')
                    changepiece(player, curdir)
                    hair1.image = pygame.image.load(f'sprites/hair{currhair}.png')
                    changepiece(hair1, curdir)
                    body1.image = pygame.image.load(f'sprites/body{currbody}.png')
                    changepiece(body1, curdir)
                    legs1.image = pygame.image.load(f'sprites/legs{currlegs}.png')
                    changepiece(legs1, curdir)
                    boots1.image = pygame.image.load(f'sprites/boots{currboots}.png')
                    changepiece(boots1, curdir)
                if arrow12.rect.collidepoint(event.pos):
                    curdir = curdir + 1
                    if curdir == 8:
                        curdir = 0
                    player.image = pygame.image.load(f'sprites/skin{currskin}.png')
                    changepiece(player, curdir)
                    hair1.image = pygame.image.load(f'sprites/hair{currhair}.png')
                    changepiece(hair1, curdir)
                    body1.image = pygame.image.load(f'sprites/body{currbody}.png')
                    changepiece(body1, curdir)
                    legs1.image = pygame.image.load(f'sprites/legs{currlegs}.png')
                    changepiece(legs1, curdir)
                    boots1.image = pygame.image.load(f'sprites/boots{currboots}.png')
                    changepiece(boots1, curdir)
                if active:
                    color = color_active  # смена цвета поля ввода
                else:
                    color = color_inactive
        txt_surface = font.render(text, True, color)
        # если длина текста больше длины поля ввода текста, оно удлиняется
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 2, input_box.y + 2))
        if active:  # мигание текстового курсора
            pointer = pointer + 1
        if pointer == 20:  # он то отрисовывается, то нет
            pointer = 0
            showpointer = not showpointer
        if showpointer:  # отрисовка текстового курсора
            pygame.draw.line(screen, color,
                             [input_box.x + 24 * cur_char + 5, input_box.y + 5],
                             [input_box.x + 24 * cur_char + 5, input_box.y + 35], 1)
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(40)
    pygame.quit()

def schedule_main():
    classes_common = ['Фонетика', 'Морфология', 'Введение в лингвистику', 'Окно']
    global dict_lessons
    dict_lessons = {
    }
    global x
    x = random.randrange(1, 5)
    y = random.choice(classes_common)
    dict_lessons.update({x: y})
    global w
    w = random.randrange(1, 5)
    while w == x:
        w = random.randrange(1, 5)
        if w != x:
            break
    q = random.choice(classes_common)
    dict_lessons.update({w: q})


def schedule_person():
    classes_person = ['Иностранный язык', 'Латинский язык',
                      'Программирование', 'Окно']
    if dict_lessons != {}:
        xx = random.randrange(1, 6)
        while xx == x or xx == w:
            xx = random.randrange(1, 6)
            if xx != x and xx != w:
                break
        yy = random.choice(classes_person)
        dict_lessons.update({xx: yy})
        ww = random.randrange(1, 6)
        while ww == xx or ww == x or ww == w:
            ww = random.randrange(1, 6)
            if ww != xx and ww != x and ww != w:
                break
        qq = random.choice(classes_person)
        dict_lessons.update({ww: qq})
        cc = random.randrange(1, 6)
        while cc == xx or cc == x or cc == w or cc == ww:
            cc = random.randrange(1, 6)
            if cc != xx and cc != x and cc != w and cc != ww:
                break
        dd = random.choice(classes_person)
        dict_lessons.update({cc: dd})


def schedule_final():
    global classes
    classes = {
        0: dict_lessons[1],
        1: dict_lessons[2],
        2: dict_lessons[3],
        3: dict_lessons[4],
        4: dict_lessons[5]
    }


classes = {}