import random
import pygame

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 1000
HEIGHT = 625  # размер экрана


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.sheet = pygame.transform.scale(pygame.image.load("sprites/spritesheet.png"), (240, 900))  # лист спрайтов
        self.image = self.sheet.subsurface(pygame.Rect((0, 0), (60, 180)))  # вырезаем кадр из листа спрайтов
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dirs = {'r': [2, 2, 0], 'l': [2, 2, 0], 'u': [4, 1, 0], 'd': [4, 0, 0], 'ru': [2, 4, 0],
                     'rd': [2, 3, 0], 'lu': [2, 4, 0], 'ld': [2, 3, 0]}
        # аргументы в списках: 1 - сколько кадров у анимации, 2 - какую строчку листа занимает, 3 - какой текущий кадр
        self.dir = ''  # текущее направление игрока

        pygame.draw.rect(self.image, color, self.rect)
        self.rect = self.image.get_rect()

    def animate(self, dir, stop=False):  # функция, обновляющая анимацию игрока. стоп - анимация стояния (не ходьбы)
        self.image = self.sheet.subsurface(pygame.Rect((self.dirs[dir][2] * 60, self.dirs[dir][1] * 180), (60, 180)))
        if stop:  # если персонаж стоит, выбирается первый кадр анимации ходьбы соответствующего направления
            self.image = self.sheet.subsurface(pygame.Rect((0, self.dirs[dir][1] * 180), (60, 180)))
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


def mapupdate(id, neighbours):  # смена отображаемых комнат, когда заходишь в другую комнату
    neighwalls = neighbours.copy()  # это просто технический момент, чтобы работал алгоритм
    for room in map:  # удаляем те комнаты, которые больше не соседние
        if room.id not in neighbours and room.id != id:
            room.kill()
        elif room.id in neighbours:
            neighbours.remove(room.id)
    walls.empty()  # удаляем все стены
    for obj in objects:  # удаляем объекты в соседних комнатах
        if obj.id not in neighwalls:
            obj.kill()
    for roomid in neighbours:  # добавляем новые соседние комнаты
        room = RoomElement(roomid, id, rooms[roomid][id], rooms[roomid].keys())
        map.add(room)
    for roomid in neighwalls:  # добавляем стены соседних комнат
        if roomid in wallist.keys():
            for wallid in wallist[roomid]['out'][id]:
                wall = RoomElement(roomid, roomid, wallist[roomid][wallid], rtype='wall', typen=wallid)
                walls.add(wall)
    if id in wallist.keys():  # добавляем стены текущей комнаты
        for wallid in wallist[id]['in']:
            wall = RoomElement(id, id, wallist[id][wallid], rtype='wall', typen=wallid)
            walls.add(wall)
    if id in objlist.keys():  # добавляем объекты текущей комнаты
        for objid in objlist[id].keys():
            obj = RoomElement(id, id, objlist[id][objid], rtype='obj', typen=objid)
            objects.add(obj)


pygame.init()


size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")



all_sprites_list = pygame.sprite.Group()
map = pygame.sprite.Group()  # полы комнат
walls = pygame.sprite.Group()  # стены
objects = pygame.sprite.Group()  # объекты
playergroup = pygame.sprite.Group()  # игрок
collision = pygame.sprite.Group()  # неотображаемые рамки для столкновения со стенами

def scene_hse():
    # all_sprites_list = pygame.sprite.Group()
    for room in map:
        room.kill()
    # map = pygame.sprite.Group()  # полы комнат
    # walls = pygame.sprite.Group()  # стены
    # objects = pygame.sprite.Group()  # объекты
    playergroup = pygame.sprite.Group()  # очищает игрока, чтоб не двоился, остальное оставляет
    # collision = pygame.sprite.Group()

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
    global rooms
    rooms = {0: {1: (-38, 752), 6: (-1040, -90)}, 1: {0: (38, -752), 2: (440, 420)}, 2: {1: (-440, -420), 3: (-876, -85)},
            3: {2: (876, 85), 4: (-333, 420), 5: (-1569, 209)}, 4: {3: (333, -420)},
            5: {3: (1569, -209), 6: (1005, -1385)}, 6: {5: (-1005, 1385), 0: (1040, 90)}}
    #  для каждой комнаты здесь указано, на каком расстоянии от нее находятся соседние ей комнаты
    global wallist
    wallist = {2: {'out': {1: (2, 3), 3: (0, 2)}, 'in': (0, 1), 0: (4, -439), 1: (831, -439), 2: (4, -439), 3: (246, -20)}}
    """  для комнат, у которых есть стены, указывается, какие стены отображаются при нахождении в соседних комнатах и 
    непосредственно внутри данной, а также расстояние между левым верхним углом пола и верхним левым углом каждой стены """
    global objlist
    objlist = {5: {0: (1255, 1156)}}  # то же самое, что со стенами, но объекты видно только при нахождении в данной комнате

    playergroup.add(player)
    room0 = RoomElement(0, None, None, rooms[0].keys())
    map.add(room0)
    room1 = RoomElement(1, 0, rooms[1][0], rooms[1].keys())
    map.add(room1)
    room6 = RoomElement(6, 0, rooms[6][0], rooms[6].keys())
    map.add(room6)
    curroom = 0  # id текущей комнаты
    animatecount = -1

    exit = True
    clock = pygame.time.Clock()

    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exit = False
                elif event.key == pygame.K_m:
                    scene_home()
                    exit = False

        front = pygame.sprite.Group()  # объекты, находящиеся перед игроком, следовательно, рисующиеся поверх него
        animatecount = animatecount + 1  # счетчик, отвечающий за скорость анимации - она сменяется каждый третий кадр
        if animatecount == 3:
            animatecount = 0

        keys = pygame.key.get_pressed()
        direction = ''  # нажатые пользователем стрелки
        cango = set()  # множество направлений, в которые может двигаться игрок в данный кадр
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
        if keys[pygame.K_LEFT] and 'r' in cango:  # перемещение игрока в тех направлениях, в которых можно двигаться
            for sprite in map:
                sprite.moveRight(5)
            for sprite in walls:
                sprite.moveRight(5)
            for sprite in objects:
                sprite.moveRight(5)
            direction = 'r'
        if keys[pygame.K_RIGHT] and 'l' in cango:
            for sprite in map:
                sprite.moveLeft(5)
            for sprite in walls:
                sprite.moveLeft(5)
            for sprite in objects:
                sprite.moveLeft(5)
            direction = 'l'
        if keys[pygame.K_DOWN] and 'd' in cango:
            for sprite in map:
                sprite.moveBack(5)
            for sprite in walls:
                sprite.moveBack(5)
            for sprite in objects:
                sprite.moveBack(5)
            direction += 'd'
        if keys[pygame.K_UP] and 'u' in cango:
            for sprite in map:
                sprite.moveForward(5)
            for sprite in walls:
                sprite.moveForward(5)
            for sprite in objects:
                sprite.moveForward(5)
            direction += 'u'
        if len(direction) > 2:  # если нажато более 2 стрелок одновременно, учитываются только 2 из них
            direction = direction[:1]
        if 'du' in direction:  # если нажаты и вверх, и вниз, одно из этих направлений не учитывается
            direction = direction[:-2]
        if direction != '':  # смена анимации
            if animatecount == 0:
                player.animate(direction)
        elif player.dir != '':  # если игрок не перемещается, включается анимация стояния
            player.animate(player.dir, True)
        for obj in objects:  # если игрок оказывается за объектом, объект рисуется поверх него, иначе сверху рисуется игрок
            if obj.rect.bottom - 5 > player.rect.bottom:
                front.add(obj)

        all_sprites_list.update()
        screen.fill((0, 0, 0))
        screen.blit(background, background_rect)
        all_sprites_list.draw(screen)
        map.draw(screen)
        walls.draw(screen)
        objects.draw(screen)
        playergroup.draw(screen)
        front.draw(screen)
        pygame.display.flip()
        clock.tick(30)  # скорость перемещения


def scene_home():  # сцена дома
    exit = True
    while exit:
        screen.fill((255, 255, 255))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exit = False
                elif event.key == pygame.K_m:
                    scene_hse() # переключает сцену
                    exit = False
                    # scene_change(scene_hse)

scene_home() # сначала включается сцена дом

pygame.quit()
