import random
import pygame

def schedule_main():
    classes_common = ['Фонетика', 'Морфология', 'Социолингвистика', 'Дискретная математика', 'Окно']
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
    classes_person = ['Иностранный язык', 'Английский язык', 'НИС', 'Латинский язык', 'Старославянский язык',
                      'Академическое письмо', 'Программирование', 'Окно']
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
    global dict_classes
    dict_classes = {
    '9:30-10:50': dict_lessons[1],
    '11:10-12:30': dict_lessons[2],
    '13:00-14:20': dict_lessons[3],
    '14:40-16:00': dict_lessons[4],
    '16:20-17:40': dict_lessons[5]
    }

def main():
    sch = str(dict_classes)
    sch1 = sch.replace("'", '')
    sch2 = sch1.replace('{', '')
    sch3 = sch2.replace('}', '')
    sch4 = sch3.split(', ')
    exit = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    background = pygame.transform.scale(pygame.image.load('sprites/minigamebg.png'), (1280, 720))
    background_rect = background.get_rect()
    mainfont = pygame.font.SysFont('MyriadPro', 50)
    text1 = mainfont.render(sch4[0], True, (166, 67, 181))
    text1_rect = text1.get_rect()
    text1_rect.x = 350
    text1_rect.y = 150
    text2 = mainfont.render(sch4[1], True, (166, 67, 181))
    text2_rect = text2.get_rect()
    text2_rect.x = 350
    text2_rect.y = 230
    text3 = mainfont.render(sch4[2], True, (166, 67, 181))
    text3_rect = text3.get_rect()
    text3_rect.x = 350
    text3_rect.y = 310
    text4 = mainfont.render(sch4[3], True, (166, 67, 181))
    text4_rect = text4.get_rect()
    text4_rect.x = 350
    text4_rect.y = 390
    text5 = mainfont.render(sch4[4], True, (166, 67, 181))
    text5_rect = text5.get_rect()
    text5_rect.x = 350
    text5_rect.y = 470
    head = mainfont.render('Расписание', True, (166, 67, 181))
    head_rect = head.get_rect()
    head_rect.x = 540
    head_rect.y = 70
    while exit:
        screen.blit(background, background_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text4, text4_rect)
        screen.blit(text5, text5_rect)
        screen.blit(head, head_rect)
        pygame.display.flip()
        clock.tick(40)

schedule_main()
schedule_person()
schedule_final()
pygame.init()
main()
pygame.quit()