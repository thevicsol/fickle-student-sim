import random
import pygame


def main(scene, pars):
    screen = pygame.display.set_mode((1280, 720))
    background = pygame.transform.scale(pygame.image.load('sprites/minigamebg.png'), (1280, 720))
    background_rect = background.get_rect()
    font = pygame.font.SysFont('Courier', 40)

    clock = pygame.time.Clock()
    input_box = pygame.Rect(400, 180, 150, 42)
    sprites = pygame.sprite.Group()
    manualgroup = pygame.sprite.Group()
    lbracket = pygame.sprite.Sprite()
    lbracket.image = pygame.image.load("sprites/bracket.png")
    lbracket.rect = lbracket.image.get_rect()
    lbracket.rect.x = 389
    lbracket.rect.y = 166
    sprites.add(lbracket)
    rbracket = pygame.sprite.Sprite()
    rbracket.image = pygame.image.load("sprites/bracket.png")
    rbracket.image = pygame.transform.flip(rbracket.image, True, False)
    rbracket.rect = rbracket.image.get_rect()
    rbracket.rect.x = input_box.x + input_box.w - 16
    rbracket.rect.y = input_box.y - 14
    sprites.add(rbracket)
    manualbutton = pygame.sprite.Sprite()
    manualbutton.image = pygame.image.load("sprites/question.png")
    manualbutton.rect = manualbutton.image.get_rect()
    manualbutton.rect.x = 50
    manualbutton.rect.y = 570
    sprites.add(manualbutton)
    sergienko = pygame.sprite.Sprite()
    sergienko.image = pygame.image.load("sprites/88.png")
    sergienko.rect = sergienko.image.get_rect()
    sergienko.rect.x = 750
    sergienko.rect.y = 250
    sprites.add(sergienko)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = (166, 97, 181)
    color = color_inactive
    active = False
    text = ''
    exit = True
    alphabet = "abcdefghijklmnopqrstuvwxyz-абвгдеёжзийклмнопрстуфхцчшщъыьэюя'"
    cur_char = 0
    completed = 0
    cur_phrase = random.choice(list(examples.keys()))
    cur_answer = examples[cur_phrase]
    mainfont = pygame.font.SysFont('MyriadPro', 50)
    phrasestring = mainfont.render(cur_phrase, True, (166, 97, 181))
    phraserect = phrasestring.get_rect(center=(640, 100))
    wrong = mainfont.render('', True, (166, 97, 181))
    wrong_rect = wrong.get_rect()
    wrong_rect.x = 470
    wrong_rect.y = 250
    counter = mainfont.render(str(completed) + '/5', True, (76, 84, 123))
    countrect = phrasestring.get_rect()
    countrect.x = 1100
    countrect.y = 100
    timeleft = 20
    showtime = str(timeleft // 60) + ':' + str(timeleft % 60)
    if showtime[-2:] == ':0':
        showtime = showtime + '0'
    elif showtime[-2] == ':':
        showtime = showtime[:-1] + '0' + showtime[-1]
    timer = mainfont.render(showtime, True, (76, 84, 123))
    timerect = timer.get_rect()
    timerect.x = 1100
    timerect.y = 50
    second = 0
    pointer = 0
    showpointer = True
    showmessage = 0
    manual = False
    finished = False

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                if manualbutton.rect.collidepoint(event.pos):
                    manual = not manual
                    if manual:
                        manualbutton.image = pygame.image.load("sprites/back.png")
                        manualimg = pygame.sprite.Sprite()
                        manualimg.image = pygame.transform.scale(pygame.image.load("sprites/languagesmanual.png"),
                                                                 (1280, 720))
                        manualimg.rect = manualimg.image.get_rect()
                        manualimg.rect.x = 0
                        manualimg.rect.y = 0
                        manualgroup.add(manualimg)
                        manualgroup.add(manualbutton)
                    else:
                        manualbutton.image = pygame.image.load("sprites/question.png")
                        manualgroup.empty()
                if active:
                    color = color_active
                else:
                    color = color_inactive
            if not manual:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = False
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text.strip() == cur_answer:
                                cur_phrase = random.choice(list(examples.keys()))
                                cur_answer = examples[cur_phrase]
                                phrasestring = mainfont.render(cur_phrase, True, (166, 97, 181))
                                completed = completed + 1
                                if completed == 5:
                                    finished = True
                                counter = mainfont.render(str(completed) + '/5', True, (76, 84, 123))
                                text = ''
                                cur_char = 0
                                showmessage = 40
                                wrong = mainfont.render('Правильно!', True, (95, 125, 112))
                                wrong_rect = wrong.get_rect(center=(640, 320))
                            else:
                                showmessage = 40
                                wrong = mainfont.render('Неправильно', True, (187, 48, 84))
                                wrong_rect = wrong.get_rect(center=(640, 320))
                                screen.blit(wrong, wrong_rect)
                        elif event.key == pygame.K_BACKSPACE:
                            if cur_char != 0:
                                text = text[:cur_char - 1] + text[cur_char:]
                                cur_char = cur_char - 1
                        elif event.key == pygame.K_LEFT:
                            if cur_char != 0:
                                cur_char = cur_char - 1
                        elif event.key == pygame.K_RIGHT:
                            if cur_char != len(text):
                                cur_char = cur_char + 1
                        elif event.unicode.lower() in alphabet and event.unicode != '':
                            text = text[:cur_char] + event.unicode + text[cur_char:]
                            cur_char = cur_char + 1
        if manual:
            active = False
            manualgroup.draw(screen)
        elif not finished:
            second = second + 1
            if second == 40:
                second = 0
                timeleft = timeleft - 1
                showtime = str(timeleft // 60) + ':' + str(timeleft % 60)
                if showtime[-2:] == ':0':
                    showtime = showtime + '0'
                elif showtime[-2] == ':':
                    showtime = showtime[:-1] + '0' + showtime[-1]
                timer = mainfont.render(showtime, True, (76, 84, 123))
                if timeleft == 0:
                    finished = True
            screen.fill((30, 30, 30))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(background, background_rect)
            # Blit the text.
            screen.blit(txt_surface, (input_box.x + 2, input_box.y + 2))
            # Blit the input_box rect.
            rbracket.rect.x = input_box.x + input_box.w - 16
            sprites.draw(screen)
            screen.blit(phrasestring, phraserect)
            screen.blit(timer, timerect)
            screen.blit(counter, countrect)
            if active:
                pointer = pointer + 1
            if pointer == 20:
                pointer = 0
                showpointer = not showpointer
            if showpointer:
                pygame.draw.line(screen, color,
                                 [input_box.x + 24 * cur_char + 5, input_box.y + 5],
                                 [input_box.x + 24 * cur_char + 5, input_box.y + 35], 1)
            if showmessage != 0:
                screen.blit(wrong, wrong_rect)
                showmessage = showmessage - 1
            pygame.draw.rect(screen, color, input_box, 2)
        else:
            if completed == 5:
                message = mainfont.render('Вы выполнили задание! Ваша оценка - 10', True, (95, 125, 112))
                completed = -1
            elif completed != -1:
                message = mainfont.render(f'Вы выполнили задание не полностью. Ваша оценка - {completed * 2}',
                                          True, (187, 48, 84))
                completed = -1
            sprites = pygame.sprite.Group()
            backBtn = pygame.sprite.Sprite()
            backBtn.image = pygame.image.load("sprites/menuback.png")
            backBtn.rect = backBtn.image.get_rect()
            backBtn.rect.x = 200
            backBtn.rect.y = 200
            sprites.add(backBtn)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if backBtn.rect.collidepoint(event.pos):
                        scene(pars[0], pars[1], 'lesson')
                        exit = False
            messagerect = message.get_rect(center=(640, 360))
            screen.blit(background, background_rect)
            screen.blit(message, messagerect)
            sprites.draw(screen)
        pygame.display.flip()
        clock.tick(40)


with open('data/lang.txt', 'r', encoding='utf8') as f:
    languages = f.readlines()
with open('data/fam.txt', 'r', encoding='utf8') as f:
    families = f.readlines()
examples = {}
for i in range(len(languages)):
    examples[languages[i][:-1]] = families[i][:-1]

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
