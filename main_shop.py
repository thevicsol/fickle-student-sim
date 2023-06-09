import random
import pygame
import transcriptgame
import dictantgame

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 1000
HEIGHT = 625  # размер экрана


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.sheet = pygame.transform.scale(pygame.image.load("sprites/spritesheet.png"), (292, 910))  # лист спрайтов
        self.image = self.sheet.subsurface(pygame.Rect((0, 0), (73, 182)))  # вырезаем кадр из листа спрайтов
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dirs = {'r': [3, 2, 0], 'l': [3, 2, 0], 'u': [4, 1, 0], 'd': [4, 0, 0], 'ru': [4, 4, 0],
                     'rd': [4, 3, 0], 'lu': [4, 4, 0], 'ld': [4, 3, 0]}
        # аргументы в списках: 1 - сколько кадров у анимации, 2 - какую строчку листа занимает, 3 - какой текущий кадр
        self.dir = ''  # текущее направление игрока

        pygame.draw.rect(self.image, color, self.rect)
        self.rect = self.image.get_rect()

    def animate(self, dir, stop=False):  # функция, обновляющая анимацию игрока. стоп - анимация стояния (не ходьбы)
        self.image = self.sheet.subsurface(pygame.Rect((self.dirs[dir][2] * 73, self.dirs[dir][1] * 182), (73, 182)))
        if stop:  # если персонаж стоит, выбирается первый кадр анимации ходьбы соответствующего направления
            self.image = self.sheet.subsurface(pygame.Rect((0, self.dirs[dir][1] * 182), (73, 182)))
            self.dir = ''  # направление назначается нулевым, чтобы показать, что персонаж стоит
        if dir in ['r', 'rd', 'lu']:  # спрайты отражаются зеркально
            self.image = pygame.transform.flip(self.image, True, False)
        if not stop:  # смена кадра при ходьбе
            self.dirs[dir][2] = self.dirs[dir][2] + 1
            if self.dirs[dir][2] == self.dirs[dir][0]:  # возвращение к первому кадру по достижении последнего
                self.dirs[dir][2] = 0
            self.dir = dir


class CollisionMask(pygame.sprite.Sprite):  # неотображаемые рамки, благодаря которым игрок не ходит сквозь стены
    def __init__(self, color, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        pygame.draw.rect(self.image, color, self.rect)
        self.rect = self.image.get_rect()


class RoomElement(pygame.sprite.Sprite):  # класс для элементов комнат: полов '', стен 'wall' и других объектов 'obj'
    def __init__(self, id, parent=None, dist=None, neighbours={}, rtype='', typen=''):
        """ id - уникальный номер комнаты, parent - id соседней комнаты, в которой игрок был до этого и к которой
        как бы 'привязана' эта комната, dist - расстояние между левым верхним углом родительской комнаты и левым верхним
        углом данной комнаты, neighbours - список id соседних комнат, rtype - тип элемента (пол, стена, объект),
        typen - номер стены или объекта по счету (пол может быть только один, так что для него не указывается)"""
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        if rtype == '':  # соседи не указываются у стен и объектов
            self.neighbours = list(neighbours)
        else:
            self.typen = typen  # номер по счету (отличающийся от id) есть только у объектов и стен
        self.image = pygame.image.load("rooms/room" + str(id) + rtype + str(typen) + '.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        if parent is None:  # координаты самой первой комнаты
            self.rect.x = 0
            self.rect.y = 0
        else:
            global map
            for room in map:
                if room.id == parent:
                    self.rect.x = room.rect.x + dist[0]  # координаты комнаты рассчитываются относительно родительской
                    self.rect.y = room.rect.y + dist[1]

    def moveRight(self, pixels):  # при перемещении игрока движется карта
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):  # контролирует скорость
        self.rect.y += speed * speed / 5

    def moveBack(self, speed):
        self.rect.y -= speed * speed / 5


class NPC(Player):
    def __init__(self, color, id, coords, path):
        super().__init__(color)
        self.id = id  # айди нпс
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.path = path  # траектория, по которой идет нпс
        self.curdot = coords  # координаты текущей точки, к которой идет нпс
        self.ndot = 0  # номер текущей точки в траектории
        self.curroom = dots[self.path[0]][0]  # текущая команата
        self.prevndot = len(self.path) - 1
        self.prevroom = dots[self.path[len(self.path) - 1]][0]

    def move(self, mapxys, animatecount):
        speed = 5
        if self.curroom == self.prevroom and self.curroom not in mapxys.keys():
            self.kill()
        else:
            ''' координаты точки рассчитываются относительно текущих координат комнаты, внутри которой она находится.
            mapxys - словарь с текущими координатами комнат'''
            if self.curroom != self.prevroom and self.prevroom in mapxys.keys():
                self.curdot = (mapxys[self.prevroom][0] + rooms[self.curroom][self.prevroom][0] +
                               dots[self.path[self.ndot]][1][0],
                               mapxys[self.prevroom][1] + rooms[self.curroom][self.prevroom][1] +
                               dots[self.path[self.ndot]][1][1] - 73)
            else:
                self.curdot = (mapxys[self.curroom][0] + dots[self.path[self.ndot]][1][0],
                               mapxys[self.curroom][1] + dots[self.path[self.ndot]][1][1] - 73)
            npcdir = 'r'
            if self.rect.x - self.curdot[0] not in (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5):  # перемещение нпс
                if self.rect.x < self.curdot[0]:  # сравниваются координаты нпс и координаты точки, к которой он идет
                    self.rect.x += speed
                    npcdir = 'l'
                elif self.rect.x > self.curdot[0]:
                    self.rect.x -= speed
                    npcdir = 'r'
            if self.rect.y - self.curdot[1] not in (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5):
                if self.rect.y < self.curdot[1]:
                    self.rect.y += speed
                    npcdir = npcdir + 'd'
                elif self.rect.y > self.curdot[1]:
                    self.rect.y -= speed
                    npcdir = npcdir + 'u'
            elif (self.rect.x - self.curdot[0] in (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5) and
                  self.rect.y - self.curdot[1] in (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5)):
                self.ndot = self.ndot + 1
                self.prevndot = self.prevndot + 1
                if self.ndot == len(self.path):
                    self.ndot = 0
                if self.prevndot == len(self.path):
                    self.prevndot = 0
                self.curroom = dots[self.path[self.ndot]][0]
                self.prevroom = dots[self.path[self.prevndot]][0]
            if animatecount == 0:
                self.animate(npcdir)  # смена спрайта нпс

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):  # контролирует скорость
        self.rect.y += speed * speed / 5

    def moveBack(self, speed):
        self.rect.y -= speed * speed / 5

    def animate(self, dir, stop=False):
        super().animate(dir, stop)


def mapupdate(id, neighbours):  # смена отображаемых комнат, когда заходишь в другую комнату
    neighwalls = neighbours.copy()  # это просто технический момент, чтобы работал алгоритм
    xylist = {}
    for room in map:  # удаляем те комнаты, которые больше не соседние
        xylist[room.id] = (room.rect.x, room.rect.y)
        if room.id not in neighbours and room.id != id:
            room.kill()
        elif room.id in neighbours:
            neighbours.remove(room.id)
    walls.empty()  # удаляем все стены
    for obj in objects:  # удаляем объекты в соседних комнатах
        if obj.id not in neighwalls:
            obj.kill()
    npcids = set()
    for npc1 in studentgroup:
        if npc1.curroom not in neighwalls and npc1.prevroom not in neighwalls and npc1.curroom != id:  # удаляем ненужных нпс
            npc1.kill()
        else:
            npcids.add(npc1.id)
    for roomid in neighbours:  # добавляем новые соседние комнаты
        room = RoomElement(roomid, id, rooms[roomid][id], rooms[roomid].keys())
        xylist[room.id] = (room.rect.x, room.rect.y)
        map.add(room)
    for roomid in neighwalls:  # добавляем стены соседних комнат
        if roomid in wallist.keys():
            for wallid in wallist[roomid]['out'][id]:
                wall = RoomElement(roomid, roomid, wallist[roomid][wallid], rtype='wall', typen=wallid)
                walls.add(wall)
        if roomid in npclist.keys():  # добавляем нпс, которых еще нет
            for key in npclist[roomid].keys():
                if key not in npcids:
                    npc_2 = NPC((255, 0, 0), key, (xylist[roomid][0] + npclist[roomid][key][0],
                                                   xylist[roomid][1] + npclist[roomid][key][1]), paths[key])
                    studentgroup.add(npc_2)
    if id in wallist.keys():  # добавляем стены текущей комнаты
        for wallid in wallist[id]['in']:
            wall = RoomElement(id, id, wallist[id][wallid], rtype='wall', typen=wallid)
            walls.add(wall)
    if id in objlist.keys():  # добавляем объекты текущей комнаты
        for objid in objlist[id].keys():
            obj = RoomElement(id, id, objlist[id][objid], rtype='obj', typen=objid)
            objects.add(obj)


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()

class Shop:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]


        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#40E0D0"

        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#DFFF00"

        self.text_surf = font.render(text, True, "white")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global foodmenu
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.top_color = "#FFBF00"

                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#40E0D0"




class Food:
    global food_options
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.width = 400
        self.space = 10
        self.padding = 8
        self.options = list(food_options.keys())
        self.setup()
        self.index = 0

        self.timer = Timer(200)



    def input(self):

        keys = pygame.key.get_pressed()
        self.timer.update()
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
        if keys[pygame.K_SPACE]:
            global money_wallet
            self.timer.activate()
            cuurent_food = self.options[self.index]
            price = prices[cuurent_food]
            if money_wallet >= price:
                money_wallet -= prices[cuurent_food]
                fullness(10)





        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def setup(self):
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = font.render(item, True, pygame.Color("black"))
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        self.image_food = pygame.image.load("sprites/06_apple_pie_dish.png")
        self.image_food_2 = pygame.image.load("sprites/94_spaghetti.png")
        self.image_food_3 = pygame.image.load("sprites/82_pizza_dish.png")
        self.image_food_4 = pygame.image.load("sprites/33_curry_dish.png")
        self.image_food_5 = pygame.image.load("sprites/banana.png")


    def show_entry(self, text_surf, amount, top, selected):
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, "white", bg_rect, 0, 4)
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)
        amount_surf = font.render(str(amount), True, "black")
        amount_rect = amount_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery))
        screen.blit(amount_surf, amount_rect)
        if selected:
            pygame.draw.rect(self.display_surface, "black", bg_rect, 4, 4)
            if self.index == 1:
                pos_rect = self.image_food.get_rect(midleft=(self.main_rect.left + 270, bg_rect.centery))
                self.display_surface.blit(self.image_food, pos_rect)
            if self.index == 2:
                pos_rect_2 = self.image_food_2.get_rect(midleft=(self.main_rect.left + 270, bg_rect.centery))
                self.display_surface.blit(self.image_food_2, pos_rect_2)
            if self.index == 0:
                pos_rect_3 = self.image_food_3.get_rect(midleft=(self.main_rect.left + 270, bg_rect.centery))
                self.display_surface.blit(self.image_food_3, pos_rect_3)
            if self.index == 3:
                pos_rect_4 = self.image_food_4.get_rect(midleft=(self.main_rect.left + 270, bg_rect.centery))
                self.display_surface.blit(self.image_food_4, pos_rect_4)
            if self.index == 4:
                pos_rect_5 = self.image_food_5.get_rect(midleft=(self.main_rect.left + 270, bg_rect.centery))
                self.display_surface.blit(self.image_food_5, pos_rect_5)


    def update(self):
        self.input()
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(food_options.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)

pygame.init()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("fickle-student-sim")
font = pygame.font.SysFont("comicsansms", 25)

button = Shop("Магазин", 100, 40, (850, 580), 6)
food_options = {"пицца": 150, "яблочный пирог": 120, "спагетти": 100, "карри": 100, "банан": 30}
prices = {"пицца": 150, "яблочный пирог": 120, "спагетти": 100, "карри": 100, "банан": 30}
foodmenu = Food()
game_paused = False
def toggle_menu():
    global game_paused
    game_paused = not game_paused

all_sprites_list = pygame.sprite.Group()
map = pygame.sprite.Group()  # полы комнат
walls = pygame.sprite.Group()  # стены
objects = pygame.sprite.Group()  # объекты
playergroup = pygame.sprite.Group()  # игрок
studentgroup = pygame.sprite.Group()  # npc
collision = pygame.sprite.Group()  # неотображаемые рамки для столкновения со стенами
rooms = {0: {1: (-38, 752), 6: (-1040, -90)}, 1: {0: (38, -752), 2: (440, 420)}, 2: {1: (-440, -420), 3: (-876, -85)},
         3: {2: (876, 85), 4: (-333, 420), 5: (-1569, 209)}, 4: {3: (333, -420)},
         5: {3: (1569, -209), 6: (1005, -1385)}, 6: {5: (-1005, 1385), 0: (1040, 90)}}
dots = {0: [0, (1000, 180)], 1: [0, (550, 180)], 2: [0, (470, 100)], 3: [0, (720, 80)],
        4: [5, (1000, 1380)], 5: [5, (550, 1380)], 6: [5, (470, 1300)], 7: [5, (720, 1180)],
        8: [6, (255, 0)], 9: [6, (444, 41)]}
paths = {0: [0, 1, 2, 3, 8, 9, 8, 3], 1: [4, 5, 6, 7]}
''' словарь точек. в кажом соответствующем точке списке первый аргумент - комната, внутри которой точка, второй - 
координаты точки относительно левого верхнего угла комнаты'''
#  для каждой комнаты здесь указано, на каком расстоянии от нее находятся соседние ей комнаты
wallist = {2: {'out': {1: (2, 3), 3: (0, 2)}, 'in': (0, 1), 0: (4, -439), 1: (831, -439), 2: (4, -439), 3: (246, -20)}}
"""  для комнат, у которых есть стены, указывается, какие стены отображаются при нахождении в соседних комнатах и 
непосредственно внутри данной, а также расстояние между левым верхним углом пола и верхним левым углом каждой стены """
objlist = {5: {0: (1255, 1156)}}  # то же самое, что со стенами, но объекты видно только при нахождении в данной комнате
npclist = {0: {0: (500, 240)}, 5: {1: (500, 240)}}  # словарь нпс, ключи - комнаты, в которых нпс спавнятся, и id нпс


def hse(firstid, firstcoords, wherefrom):
    global minute, second, time1
    for room in map:
        room.kill()
    playergroup.empty()

    player = Player((255, 0, 0))
    collup = CollisionMask((255, 0, 0), 'sprites/collup.png')  # рамки для столкновения со стенами
    collision.add(collup)
    collupwall = CollisionMask((255, 0, 0), 'sprites/collupwall.png')
    collision.add(collupwall)
    colldown = CollisionMask((255, 0, 0), 'sprites/colldown.png')
    collision.add(colldown)
    colleft = CollisionMask((255, 0, 0), 'sprites/colleft.png')
    collision.add(colleft)
    collright = CollisionMask((255, 0, 0), 'sprites/collright.png')
    collision.add(collright)

    for sprite in collision:
        sprite.rect.x = 400
        sprite.rect.y = 240
    player.rect.x = 400
    player.rect.y = 240

    background = pygame.image.load('sprites/bg.jpg').convert()
    background_rect = background.get_rect()

    playergroup.add(player)
    room0 = RoomElement(firstid, None, None, rooms[firstid].keys())
    room0.rect.x = firstcoords[0]
    room0.rect.y = firstcoords[1]
    map.add(room0)
    curroom = firstid  # id текущей комнаты
    animatecount = -1
    if firstid == 0 and wherefrom != 'pause':
        npc_0 = NPC((255, 0, 0), 0, (500, 240), paths[0])
        studentgroup.add(npc_0)
    mapupdate(firstid, room0.neighbours.copy())
    exit = True
    clock = pygame.time.Clock()

    sprites = pygame.sprite.Group()

    pauseBtn = pygame.sprite.Sprite()
    pauseBtn.image = pygame.image.load("sprites/pause.png")
    pauseBtn.rect = pauseBtn.image.get_rect()
    pauseBtn.rect.x = 50
    pauseBtn.rect.y = 50
    sprites.add(pauseBtn)
    countseconds = 0

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exit = False
                elif event.key == pygame.K_h:
                    exit = False
                    home()
                elif event.key == pygame.K_ESCAPE:
                    toggle_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pauseBtn.rect.collidepoint(event.pos):
                    exit = False
                    pause_menu(hse, (curroom, mapxys[curroom]))

        front = pygame.sprite.Group()  # объекты, находящиеся перед игроком, следовательно, рисующиеся поверх него
        animatecount = animatecount + 1  # счетчик, отвечающий за скорость анимации - она сменяется каждый третий кадр
        if animatecount == 3:
            animatecount = 0
        keys = pygame.key.get_pressed()
        direction = ''  # нажатые пользователем стрелки
        cango = set()  # множество направлений, в которые может двигаться игрок в данный кадр

        health()
        button.draw()
        draw_time(countseconds)
        health()
        screen.fill((0, 0, 0))
        screen.blit(background, background_rect)
        all_sprites_list.draw(screen)
        map.draw(screen)
        walls.draw(screen)
        objects.draw(screen)
        studentgroup.draw(screen)
        playergroup.draw(screen)
        front.draw(screen)
        sprites.draw(screen)
        if game_paused:
            foodmenu.update()
        else:

            for room in map:  # если игрок с какой-то стороны заходит за пределы пола, он не может идти в этом направлении
                roomgo = 0
                if pygame.sprite.spritecollide(colleft, [room], False, pygame.sprite.collide_mask):
                    cango.add('r')  # проверяется, что игрок пересекается с полом, т.е. находится на нем
                    roomgo += 1
                if pygame.sprite.spritecollide(collright, [room], False, pygame.sprite.collide_mask):
                    cango.add('l')
                    roomgo += 1
                if pygame.sprite.spritecollide(colldown, [room], False, pygame.sprite.collide_mask):
                    cango.add('d')
                    roomgo += 1
                if pygame.sprite.spritecollide(collup, [room], False, pygame.sprite.collide_mask):
                    cango.add('u')
                    roomgo += 1
                if roomgo == 4:
                    if room.id != curroom:  # если комната не равна текущей, значит, игрок зашел в другую и надо обновить карту
                        curroom = room.id
                        mapupdate(curroom, room.neighbours.copy())  # передается id новой текущей комнаты и список соседних
            for wall in walls:  # столкновение именно со стенами, где они есть - на тестовой карте это 2 дверных проема
                if pygame.sprite.spritecollide(collright, [wall], False, pygame.sprite.collide_mask):
                    cango.discard('l')
                if pygame.sprite.spritecollide(collupwall, [wall], False, pygame.sprite.collide_mask):
                    cango.discard('u')
            mapxys = {}
            if keys[pygame.K_LEFT] and 'r' in cango:  # перемещение игрока в тех направлениях, в которых можно двигаться
                for sprite in map:
                    sprite.moveRight(5)
                for sprite in walls:
                    sprite.moveRight(5)
                for sprite in objects:
                    sprite.moveRight(5)
                for sprite in studentgroup:
                    sprite.moveRight(5)
                direction = 'r'
            if keys[pygame.K_RIGHT] and 'l' in cango:
                for sprite in map:
                    sprite.moveLeft(5)
                for sprite in walls:
                    sprite.moveLeft(5)
                for sprite in objects:
                    sprite.moveLeft(5)
                for sprite in studentgroup:
                    sprite.moveLeft(5)
                direction = 'l'
            if keys[pygame.K_DOWN] and 'd' in cango:
                for sprite in map:
                    sprite.moveBack(5)
                for sprite in walls:
                    sprite.moveBack(5)
                for sprite in objects:
                    sprite.moveBack(5)
                for sprite in studentgroup:
                    sprite.moveBack(5)
                direction += 'd'
            if keys[pygame.K_UP] and 'u' in cango:
                for sprite in map:
                    sprite.moveForward(5)
                for sprite in walls:
                    sprite.moveForward(5)
                for sprite in objects:
                    sprite.moveForward(5)
                for sprite in studentgroup:
                    sprite.moveForward(5)
                direction += 'u'
            for sprite in map:
                mapxys[sprite.id] = (sprite.rect.x, sprite.rect.y)  # собираем координаты комнат
            if len(direction) > 2:  # если нажато более 2 стрелок одновременно, учитываются только 2 из них
                direction = direction[:1]
            if 'du' in direction:  # если нажаты и вверх, и вниз, одно из этих направлений не учитывается
                direction = direction[:-2]
            if direction != '':  # смена анимации
                if animatecount == 0:
                    player.animate(direction)
            elif player.dir != '':  # если игрок не перемещается, включается анимация стояния
                player.animate(player.dir, True)
            for obj in objects:  # если игрок оказывается за объектом, объект рисуется поверх, иначе сверху рисуется игрок
                if obj.rect.bottom - 5 > player.rect.bottom:
                    front.add(obj)
            for i in studentgroup:  # то же, что с объектами, только с нпс
                if i.rect.bottom - 5 > player.rect.bottom:
                    front.add(i)
                i.move(mapxys, animatecount)  # движение нпс по траекториям
            all_sprites_list.update()

        countseconds = countseconds + 1
        if countseconds == 30:
            countseconds = 0

        draw_time(countseconds)
        health()

        for lesson in limits:
            if dict_classes[lesson[2]] != 'Окно':
                mintime = lesson[0][0] * 60 + lesson[0][1]
                maxtime = lesson[1][0] * 60 + lesson[1][1]
                if mintime <= time1 <= maxtime and curroom == dict_rooms[dict_classes[lesson[2]]]:
                    exit = False
                    studying(hse, (curroom, mapxys[curroom]), curroom)

        pygame.display.flip()
        clock.tick(30)  # скорость перемещения


def home():  # сцена дома
    exit = True
    while exit:
        screen.fill((255, 255, 255))

        sprites = pygame.sprite.Group()

        pauseBtn = pygame.sprite.Sprite()
        pauseBtn.image = pygame.image.load("sprites/pause.png")
        pauseBtn.rect = pauseBtn.image.get_rect()
        pauseBtn.rect.x = 50
        pauseBtn.rect.y = 50
        sprites.add(pauseBtn)

        sprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exit = False
                elif event.key == pygame.K_u:
                    schedule_main()
                    schedule_person()
                    schedule_final()
                    hse(0, (0, 0), 'home')  # переключает сцену
                    exit = False
                    # scene_change(scene_hse)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pauseBtn.rect.collidepoint(event.pos):
                    exit = False
                    pause_menu(home)


limits = [[(9, 30), (10, 50), '09:30-10:50'], [(11, 10), (12, 30), '11:10-12:30'], [(13, 0), (14, 20), '13:00-14:20'],
          [(14, 40), (16, 0), '14:40-16:00'], [(16, 20), (17, 40), '16:20-17:40']]
max_sleep = 100
current_sleep = 10
bar_topleft = (160, 532)
bar_max_width = 180
bar_height = 15
max_hunger = 100
current_hunger = 100
hunger_bar_topleft = (160, 562)
hunger_bar_max_width = 180
hunger_bar_max_height = 15

max_socialize = 100
current_socialize = 100
socialize_bar_topleft = (160, 592)
socialize_bar_max_width = 180
socialize_bar_max_height = 15


def health():
    sleep_bar = pygame.image.load("sprites/Item5.png")
    sleep_bar_surface = pygame.transform.scale(sleep_bar, (200, 30))
    sleep_bar_rect = sleep_bar_surface.get_rect(center=(250, 540))
    screen.blit(sleep_bar_surface, sleep_bar_rect)
    current_health_ratio = current_sleep / max_sleep
    current_bar_width = bar_max_width * current_health_ratio
    health_bar_rect = pygame.Rect(bar_topleft, (current_bar_width, bar_height))
    pygame.draw.rect(screen, "#4682B4", health_bar_rect, border_radius=15)

    hunger_bar = pygame.image.load("sprites/Item5.png")
    hunger_bar_surface = pygame.transform.scale(hunger_bar, (200, 30))
    hunger_bar_rect = hunger_bar_surface.get_rect(center=(250, 570))
    screen.blit(hunger_bar_surface, hunger_bar_rect)
    current_hunger_ratio = current_hunger / max_hunger
    current_hunger_width = hunger_bar_max_width * current_hunger_ratio
    hunger_bar2_rect = pygame.Rect(hunger_bar_topleft, (current_hunger_width, hunger_bar_max_height))
    pygame.draw.rect(screen, "#4682B4", hunger_bar2_rect, border_radius=15)

    socialize_bar = pygame.image.load("sprites/Item5.png")
    socialize_bar_surface = pygame.transform.scale(socialize_bar, (200, 30))
    socialize_bar_rect = socialize_bar_surface.get_rect(center=(250, 600))
    screen.blit(socialize_bar_surface, socialize_bar_rect)
    current_socialize_ratio = current_socialize / max_socialize
    current_socialize_width = socialize_bar_max_width * current_socialize_ratio
    socialize_bar2_rect = pygame.Rect(socialize_bar_topleft, (current_socialize_width, socialize_bar_max_height))
    pygame.draw.rect(screen, "#4682B4", socialize_bar2_rect, border_radius=15)


def tired(amount):
    global current_sleep
    if current_sleep > 0:
        current_sleep -= amount
    if current_sleep <= 0:
        current_sleep = 0


def get_hunger(amount):
    global current_hunger
    if current_hunger > 0:
        current_hunger -= amount
    if current_hunger <= 0:
        current_hunger = 0


def recharge(amount):
    global current_sleep, max_sleep
    if current_sleep < max_sleep:
        current_sleep += amount
    if current_sleep >= max_sleep:
        current_sleep = max_sleep


def fullness(amount):
    global current_hunger, max_hunger
    if current_hunger < max_hunger:
        current_hunger += amount
    if current_hunger >= max_hunger:
        current_hunger = max_hunger


def update():
    health()


current_module = 1
weekdays_box = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
minute = 9
second = 10
time1 = 550
current_day = 0
lessonsattended = []
money_wallet = 1894
invincible = False
invincibility = 400
start_time_inv = 0
grades = {
    'Морфология': [],
    'Введение в лингвистику': [],
    'Иностранный язык': [],
    'Латинский язык': [],
    'Программирование': [],
    'Фонетика': []
}
dict_rooms = {
    'Морфология': 4,
    'Введение в лингвистику': 5,
    'Иностранный язык': 2,
    'Латинский язык': 6,
    'Программирование': 3,
    'Фонетика': 1
}
dict_classes = {}


def draw_time(countseconds):
    global minute, second, current_day, current_module, time1, grades, dict_classes
    global output_string
    global date
    if countseconds == 29:
        time1 = time1 + 1
        minute = time1 // 60  # количество минут = часы в игре
        second = time1 % 60  # количество секунд = минуты в игре
        if time1 == 651 and '09:30-10:50' not in lessonsattended and dict_classes['09:30-10:50'] != 'Окно':
            grades[dict_classes['09:30-10:50']].append(0)
        if time1 == 751 and '11:10-12:30' not in lessonsattended and dict_classes['11:10-12:30'] != 'Окно':
            grades[dict_classes['11:10-12:30']].append(0)
        if time1 == 861 and '13:00-14:20' not in lessonsattended and dict_classes['13:00-14:20'] != 'Окно':
            grades[dict_classes['13:00-14:20']].append(0)
        if time1 == 961 and '14:40-16:00' not in lessonsattended and dict_classes['14:40-16:00'] != 'Окно':
            grades[dict_classes['14:40-16:00']].append(0)
        if time1 == 1061 and '16:20-17:40' not in lessonsattended and dict_classes['16:20-17:40'] != 'Окно':
            grades[dict_classes['16:20-17:40']].append(0)
    output_string = "{0:02}:{1:02}".format(minute, second)
    time_surface = font.render(output_string, True, pygame.Color("white"))
    time_rect = time_surface.get_rect(center=(80, 600))
    screen.blit(time_surface, time_rect)

    date = f"{weekdays_box[current_day]}, {current_module} модуль"
    date_text = font.render(date, True, pygame.Color("white"))
    date_rect = date_text.get_rect(center=(80, 540))
    screen.blit(date_text, date_rect)


def money(amount):
    global money_wallet
    wallet = pygame.image.load("sprites/wallet.png")
    wallet_surf = pygame.transform.scale(wallet, (50, 50))
    wallet_rect = wallet.get_rect(topleft=(700, 576))
    screen.blit(wallet_surf, wallet_rect)
    money_amount_surf = font.render(str(amount), True, pygame.Color("white"))
    money_amount_rect = money_amount_surf.get_rect(midleft=(wallet_rect.right - 70, 600))
    screen.blit(money_amount_surf, money_amount_rect)


def tm():
    global invincibility, invincible, start_time_inv, money_wallet, current_day, current_module
    if not invincible:
        if time1 == 10:
            money_wallet += 1
            invincible = True
            start_time_inv = time1
        if time1 == 2400:
            current_day += 1
        if current_day == 7:
            current_day = 0
            current_module += 1
        if current_module == 5:
            current_module = 1
    if invincible:
        current_time = time1
        if current_time - start_time_inv >= invincibility:
            invincible = False

    money(money_wallet), tm()


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
    global dict_classes
    dict_classes = {
        '09:30-10:50': dict_lessons[1],
        '11:10-12:30': dict_lessons[2],
        '13:00-14:20': dict_lessons[3],
        '14:40-16:00': dict_lessons[4],
        '16:20-17:40': dict_lessons[5]
    }


def schedule(scene, pars):
    global dict_classes
    sch = str(dict_classes)
    sch1 = sch.replace("'", '')
    sch2 = sch1.replace('{', '')
    sch3 = sch2.replace('}', '')
    sch4 = sch3.split(', ')
    exit = True
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
    button = pygame.sprite.Group()
    backbutton = pygame.sprite.Sprite()  # кнопка открытия инструкции
    backbutton.image = pygame.image.load("sprites/back.png")
    backbutton.rect = backbutton.image.get_rect()
    backbutton.rect.x = 50
    backbutton.rect.y = 570
    button.add(backbutton)
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbutton.rect.collidepoint(event.pos):  # если нажимается кнопка открытия/закрытия инструкции
                    exit = False
                    pause_menu(scene, pars)
        screen.blit(background, background_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text4, text4_rect)
        screen.blit(text5, text5_rect)
        screen.blit(head, head_rect)
        button.draw(screen)
        pygame.display.flip()


def authors():
    screen.fill((255, 255, 255))
    background = pygame.image.load('sprites/authorsbg.png').convert()
    background_rect = background.get_rect()
    background_rect.x = 0
    background_rect.y = 0
    screen.blit(background, background_rect)
    sprites = pygame.sprite.Group()
    quitBtn = pygame.sprite.Sprite()
    quitBtn.image = pygame.image.load("sprites/menuback.png")
    quitBtn.rect = quitBtn.image.get_rect()
    quitBtn.rect.x = WIDTH / 2 - 100
    quitBtn.rect.y = 100
    sprites.add(quitBtn)

    sprites.draw(screen)
    pygame.display.flip()
    exit = True
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quitBtn.rect.collidepoint(event.pos):
                    main_menu()
                    exit = False


def main_menu():  # сцена главного меню

    exit = True
    screen.fill((200, 255, 255))

    sprites = pygame.sprite.Group()

    playBtn = pygame.sprite.Sprite()
    playBtn.image = pygame.image.load("sprites/play.png")
    playBtn.rect = playBtn.image.get_rect()
    playBtn.rect.x = WIDTH / 2 - 100
    playBtn.rect.y = HEIGHT / 2 - 150
    sprites.add(playBtn)

    authorsBtn = pygame.sprite.Sprite()
    authorsBtn.image = pygame.image.load("sprites/authors.png")
    authorsBtn.rect = authorsBtn.image.get_rect()
    authorsBtn.rect.x = WIDTH / 2 - 100
    authorsBtn.rect.y = HEIGHT / 2 - 50
    sprites.add(authorsBtn)

    savesBtn = pygame.sprite.Sprite()
    savesBtn.image = pygame.image.load("sprites/saves.png")
    savesBtn.rect = savesBtn.image.get_rect()
    savesBtn.rect.x = WIDTH / 2 - 100
    savesBtn.rect.y = HEIGHT / 2 + 50
    sprites.add(savesBtn)

    quitBtn = pygame.sprite.Sprite()
    quitBtn.image = pygame.image.load("sprites/quit.png")
    quitBtn.rect = quitBtn.image.get_rect()
    quitBtn.rect.x = WIDTH / 2 - 100
    quitBtn.rect.y = HEIGHT / 2 + 150
    sprites.add(quitBtn)

    sprites.draw(screen)
    pygame.display.flip()
    while exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if playBtn.rect.collidepoint(event.pos):
                    home()
                    exit = False
                elif authorsBtn.rect.collidepoint(event.pos):
                    authors()
                    exit = False
                elif savesBtn.rect.collidepoint(event.pos):
                    # доделать тут сцену с сейвами
                    exit = False
                elif quitBtn.rect.collidepoint(event.pos):
                    exit = False
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_x:
            #         exit = False
            #     elif event.key == pygame.K_u:
            #         scene_hse() # переключает сцену
            #         exit = False
            #     elif event.key == pygame.K_h:
            #         home()
            #         exit = False
            #         # scene_change(scene_hse)


def pause_menu(scene, pars):
    exit = True
    screen.fill((255, 255, 255))

    sprites = pygame.sprite.Group()

    backBtn = pygame.sprite.Sprite()
    backBtn.image = pygame.image.load("sprites/menuback.png")
    backBtn.rect = backBtn.image.get_rect()
    backBtn.rect.x = WIDTH / 2 - 100
    backBtn.rect.y = HEIGHT / 2 + 100
    sprites.add(backBtn)

    menuBtn = pygame.sprite.Sprite()
    menuBtn.image = pygame.image.load("sprites/menu.png")
    menuBtn.rect = menuBtn.image.get_rect()
    menuBtn.rect.x = WIDTH / 2 - 100
    menuBtn.rect.y = HEIGHT / 2
    sprites.add(menuBtn)

    schedulebutton = pygame.sprite.Sprite()  # кнопка открытия расписания
    schedulebutton.image = pygame.image.load("sprites/question.png")
    schedulebutton.rect = schedulebutton.image.get_rect()
    schedulebutton.rect.x = 50
    schedulebutton.rect.y = 570
    sprites.add(schedulebutton)

    background = pygame.image.load('sprites/pausebg.png').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    sprites.draw(screen)
    pygame.display.flip()

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backBtn.rect.collidepoint(event.pos):
                    scene(pars[0], pars[1], 'pause')
                    exit = False
                elif menuBtn.rect.collidepoint(event.pos):
                    main_menu()
                    exit = False
                elif schedulebutton.rect.collidepoint(event.pos):
                    schedule(scene, pars)
                    exit = False


def bit_late(scene, pars):
    global minute, second, time1
    exit = True
    screen = pygame.display.set_mode((1000, 625))
    screen.fill((255, 255, 255))

    sprites = pygame.sprite.Group()

    backBtn = pygame.sprite.Sprite()
    backBtn.image = pygame.image.load("sprites/menuback.png")
    backBtn.rect = backBtn.image.get_rect()
    backBtn.rect.x = WIDTH / 2 - 100
    backBtn.rect.y = HEIGHT / 2 + 100
    sprites.add(backBtn)

    background = pygame.image.load('sprites/minigamebg.png').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    mainfont = pygame.font.SysFont('MyriadPro', 50)
    message = mainfont.render('Опоздал на пару, но пришёл! Оценка - 6', True, (166, 67, 181))
    message_rect = message.get_rect()
    message_rect.x = 100
    message_rect.y = 310
    sprites.draw(screen)

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backBtn.rect.collidepoint(event.pos):
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
        screen.blit(background, background_rect)
        screen.blit(message, message_rect)
        sprites.draw(screen)
        pygame.display.flip()
    scene(pars[0], pars[1], 'lesson')


def not_late(scene, pars):
    global minute, second, time1
    exit = True
    screen = pygame.display.set_mode((1000, 625))
    screen.fill((255, 255, 255))

    sprites = pygame.sprite.Group()

    mainfont = pygame.font.SysFont('MyriadPro', 50)
    backBtn = pygame.sprite.Sprite()
    backBtn.image = pygame.image.load("sprites/menuback.png")
    backBtn.rect = backBtn.image.get_rect()
    backBtn.rect.x = WIDTH / 2 - 100
    backBtn.rect.y = HEIGHT / 2 + 100
    sprites.add(backBtn)

    background = pygame.image.load('sprites/minigamebg.png').convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    message = mainfont.render('Молодец! Не опоздал на пару! Оценка - 10', True, (166, 67, 181))
    message_rect = message.get_rect()
    message_rect.x = 100
    message_rect.y = 310
    sprites.draw(screen)

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backBtn.rect.collidepoint(event.pos):
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
        screen.blit(background, background_rect)
        screen.blit(message, message_rect)
        sprites.draw(screen)
        pygame.display.flip()
    scene(pars[0], pars[1], 'lesson')


def studying(scene, pars, curroom):
    global minute, second, current_day, lessonsattended
    if output_string == '09:30':
        if curroom == dict_rooms[dict_classes['09:30-10:50']]:
            if dict_classes['09:30-10:50'] != 'Фонетика' and dict_classes['09:30-10:50'] != 'Введение в лингвистику':
                grades[dict_classes['09:30-10:50']].append(10)
                lessonsattended.append('09:30-10:50')
                not_late(scene, pars)
            elif dict_classes['09:30-10:50'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['09:30-10:50'] == 'Введение в лингвистику':
                dictantgame.main()
    elif minute == 9 and second > 30 or (minute == 10 and second < 50):
        if curroom == dict_rooms[dict_classes['09:30-10:50']]:
            if dict_classes['09:30-10:50'] != 'Фонетика' and dict_classes['09:30-10:50'] != 'Введение в лингвистику':
                grades[dict_classes['09:30-10:50']].append(6)
                lessonsattended.append('09:30-10:50')
                bit_late(scene, pars)
            elif dict_classes['09:30-10:50'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['09:30-10:50'] == 'Введение в лингвистику':
                dictantgame.main()

    elif output_string == '11:10':
        if curroom == dict_rooms[dict_classes['11:10-12:30']]:
            if dict_classes['11:10-12:30'] != 'Фонетика' and dict_classes['11:10-12:30'] != 'Введение в лингвистику':
                grades[dict_classes['11:10-12:30']].append(10)
                lessonsattended.append('11:10-12:30')
                not_late(scene, pars)
            elif dict_classes['11:10-12:30'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['11:10-12:30'] == 'Введение в лингвистику':
                dictantgame.main()
    elif minute == 11 and second > 10 or (minute == 12 and second < 30):
        if curroom == dict_rooms[dict_classes['11:10-12:30']]:
            if dict_classes['11:10-12:30'] != 'Фонетика' and dict_classes['11:10-12:30'] != 'Введение в лингвистику':
                grades[dict_classes['11:10-12:30']].append(6)
                lessonsattended.append('11:10-12:30')
                bit_late(scene, pars)
            elif dict_classes['11:10-12:30'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['11:10-12:30'] == 'Введение в лингвистику':
                dictantgame.main()

    elif output_string == '13:00':
        if curroom == dict_rooms[dict_classes['13:00-14:20']]:
            if dict_classes['13:00-14:20'] != 'Фонетика' and dict_classes['13:00-14:20'] != 'Введение в лингвистику':
                grades[dict_classes['13:00-14:20']].append(10)
                lessonsattended.append('13:00-14:20')
                not_late(scene, pars)
            elif dict_classes['13:00-14:20'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['13:00-14:20'] == 'Введение в лингвистику':
                dictantgame.main()
    elif minute == 13 and second > 0 or (minute == 14 and second < 20):
        if curroom == dict_rooms[dict_classes['13:00-14:20']]:
            if dict_classes['13:00-14:20'] != 'Фонетика' and dict_classes['13:00-14:20'] != 'Введение в лингвистику':
                grades[dict_classes['13:00-14:20']].append(6)
                lessonsattended.append('13:00-14:20')
                bit_late(scene, pars)
            elif dict_classes['13:00-14:20'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['13:00-14:20'] == 'Введение в лингвистику':
                dictantgame.main()

    elif output_string == '14:40':
        if curroom == dict_rooms[dict_classes['14:40-16:00']]:
            if dict_classes['14:40-16:00'] != 'Фонетика' and dict_classes['14:40-16:00'] != 'Введение в лингвистику':
                grades[dict_classes['14:40-16:00']].append(10)
                lessonsattended.append('14:40-16:00')
                not_late(scene, pars)
            elif dict_classes['14:40-16:00'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['14:40-16:00'] == 'Введение в лингвистику':
                dictantgame.main()
    elif minute == 14 and second > 40 or (minute == 16 and second < 0):
        if curroom == dict_rooms[dict_classes['14:40-16:00']]:
            if dict_classes['14:40-16:00'] != 'Фонетика' and dict_classes['14:40-16:00'] != 'Введение в лингвистику':
                grades[dict_classes['14:40-16:00']].append(6)
                lessonsattended.append('14:40-16:00')
                bit_late(scene, pars)
            elif dict_classes['14:40-16:00'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['14:40-16:00'] == 'Введение в лингвистику':
                dictantgame.main()

    elif output_string == '16:20':
        if curroom == dict_rooms[dict_classes['16:20-17:40']]:
            if dict_classes['16:20-17:40'] != 'Фонетика' and dict_classes['16:20-17:40'] != 'Введение в лингвистику':
                grades[dict_classes['16:20-17:40']].append(10)
                lessonsattended.append('16:20-17:40')
                not_late(scene, pars)
            elif dict_classes['16:20-17:40'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['16:20-17:40'] == 'Введение в лингвистику':
                dictantgame.main()
    elif minute == 16 and second > 20 or (minute == 17 and second < 40):
        if curroom == dict_rooms[dict_classes['16:20-17:40']]:
            if dict_classes['16:20-17:40'] != 'Фонетика' and dict_classes['16:20-17:40'] != 'Введение в лингвистику':
                grades[dict_classes['16:20-17:40']].append(6)
                lessonsattended.append('16:20-17:40')
                bit_late(scene, pars)
            elif dict_classes['16:20-17:40'] == 'Фонетика':
                transcriptgame.main()
            elif dict_classes['16:20-17:40'] == 'Введение в лингвистику':
                dictantgame.main()

    if current_day == 6 and output_string == '23:59':  # подсчёт оценок в конце модуля
        grades['Морфология'] = sum(grades['Морфология']) / len(grades['Морфология'])
        grades['Введение в лингвистику'] = sum(grades['Введение в лингвистику']) / len(grades['Введение в лингвистику'])
        grades['Иностранный язык'] = sum(grades['Иностранный язык']) / len(grades['Иностранный язык'])
        grades['Латинский язык'] = sum(grades['Латинский язык']) / len(grades['Латинский язык'])
        grades['Программирование'] = sum(grades['Программирование']) / len(grades['Программирование'])
        grades['Фонетика'] = sum(grades['Фонетика']) / len(grades['Фонетика'])
        sch = str(grades)
        sch1 = sch.replace("'", '')
        sch2 = sch1.replace('{', '')
        sch3 = sch2.replace('}', '')
        sch4 = sch3.split(', ')
        exit = True
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
        head = mainfont.render('Оценки за модуль', True, (166, 67, 181))
        head_rect = head.get_rect()
        head_rect.x = 540
        head_rect.y = 70
        button = pygame.sprite.Group()
        backbutton = pygame.sprite.Sprite()  # кнопка возвращения в игру
        backbutton.image = pygame.image.load("sprites/back.png")
        backbutton.rect = backbutton.image.get_rect()
        backbutton.rect.x = 50
        backbutton.rect.y = 570
        button.add(backbutton)
        while exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backbutton.rect.collidepoint(event.pos):  # если нажимается кнопка открытия/закрытия инструкции
                        exit = False
                        scene(pars[0], pars[1], 'pause')
                        minute = 0
                        second = 0
                        current_day = 0
                        current_module += 1
                        home()
            screen.blit(background, background_rect)
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)
            screen.blit(text4, text4_rect)
            screen.blit(text5, text5_rect)
            screen.blit(head, head_rect)
            button.draw(screen)
            pygame.display.flip()


main_menu()  # сначала включается сцена главного меню

pygame.quit()
