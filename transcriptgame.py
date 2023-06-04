import random
import pygame


def main(scene, pars, time1, n):
    screen = pygame.display.set_mode((1280, 720))
    background = pygame.transform.scale(pygame.image.load('sprites/minigamebg.png'), (1280, 720))
    background_rect = background.get_rect()
    font = pygame.font.SysFont('Courier', 40)  # шрифт вводимого текста
    mainfont = pygame.font.SysFont('Arial', 50)  # шрифт всего остального текста
    clock = pygame.time.Clock()
    input_box = pygame.Rect(400, 180, 150, 42)   # поле ввода текста
    sprites = pygame.sprite.Group()
    manualgroup = pygame.sprite.Group()  # группа спрайтов, в которую добавляется спрайт инструкции
    lbracket = pygame.sprite.Sprite()  # левая скобка транскрипции
    lbracket.image = pygame.image.load("sprites/bracket.png")
    lbracket.rect = lbracket.image.get_rect()
    lbracket.rect.x = 389
    lbracket.rect.y = 166
    sprites.add(lbracket)
    rbracket = pygame.sprite.Sprite()  # правая скобка транскрипции
    rbracket.image = pygame.image.load("sprites/bracket.png")
    rbracket.image = pygame.transform.flip(rbracket.image, True, False)
    rbracket.rect = rbracket.image.get_rect()
    rbracket.rect.x = input_box.x + input_box.w - 16
    rbracket.rect.y = input_box.y - 14
    sprites.add(rbracket)
    manualbutton = pygame.sprite.Sprite()  # кнопка открытия инструкции
    manualbutton.image = pygame.image.load("sprites/question.png")
    manualbutton.rect = manualbutton.image.get_rect()
    manualbutton.rect.x = 50
    manualbutton.rect.y = 570
    sprites.add(manualbutton)
    bbsprite = pygame.sprite.Group()
    backBtn = pygame.sprite.Sprite()
    backBtn.image = pygame.image.load("sprites/menuback.png")
    backBtn.rect = backBtn.image.get_rect()
    backBtn.rect.x = 20
    backBtn.rect.y = 20
    bbsprite.add(backBtn)

    color_inactive = pygame.Color('lightskyblue3')  # цвет поля ввода, когда оно неактивно
    color_active = (166, 97, 181)  # когда активно
    color = color_inactive
    active = False  # активно ли поле ввода в данный момент
    text = ''  # текст, который вводит игрок
    exit = True
    alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя' "  # допустимые для ввода знаки
    cur_char = 0  # позиция в фразе, после которой печатается текст (изначально - начало слова)
    completed = 0  # сколько фраз затранскрибировано
    cur_phrase = random.choice(list(examples.keys()))  # фраза, которую надо затранскрибировать
    cur_answer = examples[cur_phrase]  # то, как должна выглядеть транскрипция фразы
    phrasestring = mainfont.render(cur_phrase, True, (166, 97, 181))  # отрисовка фразы
    phraserect = phrasestring.get_rect(center=(640, 100))
    wrong = mainfont.render('', True, (166, 97, 181))  # надпись правильно/неправильно
    wrong_rect = wrong.get_rect()
    wrong_rect.x = 470
    wrong_rect.y = 250
    counter = mainfont.render(str(completed) + '/5', True, (76, 84, 123))  # счетчик затранскрибированных фраз
    countrect = phrasestring.get_rect()
    countrect.x = 1100
    countrect.y = 100
    timeleft = 150  # сколько осталось секунд
    showtime = str(timeleft // 60) + ':' + str(timeleft % 60)  # оставшееся время в формате мм:сс
    if showtime[-2:] == ':0':  # добавление нужных нулей где их нет
        showtime = showtime + '0'
    elif showtime[-2] == ':':
        showtime = showtime[:-1] + '0' + showtime[-1]
    timer = mainfont.render(showtime, True, (76, 84, 123))  # таймер
    timerect = timer.get_rect()
    timerect.x = 1100
    timerect.y = 50
    second = 0  # счетчик, считающий проход секунды
    pointer = 0  # как часто мигает текстовый курсор
    showpointer = True  # виден ли сейчас курсор
    showmessage = 0  # счетчик, сколько показывается сообщение правильно/неправильно
    manual = False  # открыта ли инструкция
    finished = False  # закончена ли игра

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):  # проверяется, нажал ли игрок на поле ввода текста
                    active = not active  # если нажал, ввод активируется
                else:
                    active = False
                if backBtn.rect.collidepoint(event.pos) and finished:
                    if 570 <= time1 <= 650:
                        minute = 10
                        second = 51
                        time1 = 651
                    if 670 <= time1 <= 750:
                        minute = 12
                        second = 31
                        time1 = 751

                    if 780 <= time1 <= 860:
                        minute = 14
                        second = 21
                        time1 = 861
                    if 880 <= time1 <= 960:
                        minute = 16
                        second = 1
                        time1 = 961
                    if 980 <= time1 <= 1060:
                        minute = 17
                        second = 41
                        time1 = 1061
                    exit = False
                    with open(f'data/save{n}.dat', 'r', encoding='utf8') as f:
                        data = f.readlines()
                    if data[6] == '\n':
                        data[6] = f'{grade * 2}\n'
                    else:
                        data[6] = data[6][:-1] + f',{grade * 2}\n'
                    with open(f'data/save{n}.dat', 'w', encoding='utf8') as f:
                        for line in data:
                            f.writelines(line)
                    scene(pars[0], pars[1], 'lessonФонетика', n, (minute, second, time1), grade * 2)
                if manualbutton.rect.collidepoint(event.pos):  # если нажимается кнопка открытия/закрытия инструкции
                    manual = not manual  # инструкция открывается, если не открыта, и закрывается, если открыта
                    if manual:  # если открывается
                        manualbutton.image = pygame.image.load("sprites/back.png")  # меняется иконка кнопки
                        manualimg = pygame.sprite.Sprite()  # показывается инструкция поверх элементов игры
                        manualimg.image = pygame.transform.scale(pygame.image.load("sprites/transcribemanual.png"),
                                                                 (1280, 720))
                        manualimg.rect = manualimg.image.get_rect()
                        manualimg.rect.x = 0
                        manualimg.rect.y = 0
                        manualgroup.add(manualimg)
                        manualgroup.add(manualbutton)  # группа спрайтов, показывающихся при открытой инструкции
                    else:  # если закрывается
                        manualbutton.image = pygame.image.load("sprites/question.png")
                        manualgroup.empty()  # при закрытии инструкции меняется иконка кнопки и удаляется инструкция
                if active:
                    color = color_active  # смена цвета поля ввода
                else:
                    color = color_inactive
            if not manual:  # если инструкция не открыта
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = False
                    if active:
                        if event.key == pygame.K_RETURN:  # отправка ответа
                            if text.strip() == cur_answer:  # если ответ правильный
                                cur_phrase = random.choice(list(examples.keys()))  # выбор новой фразы
                                cur_answer = examples[cur_phrase]
                                phrasestring = mainfont.render(cur_phrase, True, (166, 97, 181))   # отрисовка новой фра
                                completed = completed + 1  # обновление счетчика выполненных транскрипций
                                if completed == 5:  # если сделаны все 5 транскрипций, игра завершается
                                    finished = True
                                counter = mainfont.render(str(completed) + '/5', True, (76, 84, 123))  # обновл. счетчик
                                text = ''  # набранный текст стирается
                                cur_char = 0
                                showmessage = 40  # столько показывается надпись правильно
                                wrong = mainfont.render('Правильно!', True, (95, 125, 112))
                                wrong_rect = wrong.get_rect(center=(640, 320))
                            else:
                                showmessage = 40  # столько показывается надпись неправильно
                                wrong = mainfont.render('Неправильно', True, (187, 48, 84))
                                wrong_rect = wrong.get_rect(center=(640, 320))
                                screen.blit(wrong, wrong_rect)
                        elif event.key == pygame.K_BACKSPACE:  # стирание символов
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
        if manual:  # отрисовка инструкции
            active = False
            manualgroup.draw(screen)
        elif not finished:  # если не инструкция и игра не завершена
            second = second + 1  # каждые сорок кадров сменяется секунда (это прописано в клок тике)
            if second == 40:  # прошло 40 кадров, сменилась секунда, осталось на секунду меньше времени
                second = 0
                timeleft = timeleft - 1
                showtime = str(timeleft // 60) + ':' + str(timeleft % 60)  # обновление таймера
                if showtime[-2:] == ':0':
                    showtime = showtime + '0'
                elif showtime[-2] == ':':
                    showtime = showtime[:-1] + '0' + showtime[-1]
                timer = mainfont.render(showtime, True, (76, 84, 123))
                if timeleft == 0:  # если времени не осталось, игра завершается
                    finished = True
            screen.fill((30, 30, 30))
            # отрисовка текста
            txt_surface = font.render(text, True, color)
            # если длина текста больше длины поля ввода текста, оно удлиняется
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(background, background_rect)
            screen.blit(txt_surface, (input_box.x + 2, input_box.y + 2))
            rbracket.rect.x = input_box.x + input_box.w - 16
            sprites.draw(screen)
            screen.blit(phrasestring, phraserect)
            screen.blit(timer, timerect)
            screen.blit(counter, countrect)
            if active:  # мигание текстового курсора
                pointer = pointer + 1
            if pointer == 20:  # он то отрисовывается, то нет
                pointer = 0
                showpointer = not showpointer
            if showpointer:  # отрисовка текстового курсора
                pygame.draw.line(screen, color,
                                 [input_box.x + 24 * cur_char + 5, input_box.y + 5],
                                 [input_box.x + 24 * cur_char + 5, input_box.y + 35], 1)
            if showmessage != 0:  # отрисовка надписи правильно/неправильно
                screen.blit(wrong, wrong_rect)
                showmessage = showmessage - 1
            pygame.draw.rect(screen, color, input_box, 2)
        else:  # если игра завершена
            if completed == 5:  # если решены все 5 примеров
                grade = completed
                message = mainfont.render('Вы выполнили задание! Ваша оценка - 10', True, (95, 125, 112))
                completed = -1
            elif completed != -1:  # если решены не все примеры
                grade = completed
                message = mainfont.render(f'Вы выполнили задание не полностью. Ваша оценка - {completed * 2}',
                                          True, (187, 48, 84))
                completed = -1
            messagerect = message.get_rect(center=(640, 360))
            screen.blit(background, background_rect)
            screen.blit(message, messagerect)
            bbsprite.draw(screen)
        pygame.display.flip()
        clock.tick(40)


with open('data/orthogr2grams.txt', 'r', encoding='utf8') as f:  # открытие файла с фразами
    orthogr = f.readlines()
with open('data/transcr2grams.txt', 'r', encoding='utf8') as f:  # открытие файла с транскрипциями
    transcr = f.readlines()
examples = {}
for i in range(len(orthogr)):
    examples[orthogr[i][:-1]] = transcr[i][:-1]  # создается словарь, где фразам соответствуют транскрипции

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
