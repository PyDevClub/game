import pygame
import random
import time

all_images = {}
TILE_SIZE = 18
DUNGEON_SIZE = 40

class Tile(object):
    """docstring for Tile"""
    def __init__(self, image_name, x, y):
        super(Tile, self).__init__()
        self.name = image_name
        self.x = x
        self.y = y

        # initialize image
        self.surface = None
        if self.name not in all_images.keys():
            all_images[self.name] = pygame.image.load(self.name)
        self.surface = all_images[self.name]


class Spawnable(Tile):
    def __init__(self, image_name, x, y):
        super(Spawnable, self).__init__(image_name, x, y)
# 		self.heal = False
# 		full properties of an item here

class Car(Spawnable):
    def __init__(self, x, y):
        super(Spawnable, self).__init__("item.png", x, y)

class Dungeon(object):
    """docstring for Dungeon"""
    def __init__(self, width, height):
        super(Dungeon, self).__init__()
        self.width = width
        self.height = height

        self.grid = []
        self.generate()

        self.player = None


    def generate(self):

        # step one: fill the entire dungeon with bricks
        for y in range(self.height):
            self.grid += [[]]
            for x in range(self.width):
                self.grid[-1] += [Car(x, y)]

        # step two: randomly pick some spots in the dungeon (randomly pick a random number of them, should be not near the edges)
        num_rooms = random.randrange(10,15)
        room_coords = []
        for x in range(num_rooms):
            room_coords += [[random.randrange(5,self.width-5),random.randrange(5, self.height-5)]]




        # set the first spot to air, then keep calling this method
        def tunnel(x1, y1, x2, y2):
            # print(x1, y1, x2, y2)
            # step one: find the closest position of air (just brute force this for now)
            closest = (-10000, -100000)
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y][x].name == "empty.png" and (abs(x2 - x)+abs(y2-y)) < (abs(x2 - closest[0])+abs(y2-closest[1])):
                        closest = (x, y)
            # step two: tunnel a but in the x direction, then y, then x... or vice versa, until you are there
            current_spot = closest

            for x in range(current_spot[0], x2, -1 if current_spot[0] > x2 else 1):
                self.grid[current_spot[1]][x] = Tile("empty.png", x, current_spot[1])
            for y in range(current_spot[1], y2, -1 if current_spot[1] > y2 else 1):
                self.grid[y][x2] = Tile("empty.png", x2, y)



        # step three: tunnel between them

        curent_room = room_coords[0]
        self.grid[curent_room[1]][curent_room[0]] = Tile("empty.png", curent_room[0], curent_room[1])
        for i in range(1, len(room_coords)):
            tunnel(curent_room[0], curent_room[1], room_coords[i][0], room_coords[i][1])
            curent_room = room_coords[i]

        # step four: randomly make rooms around some of those spots
        for room in random.sample(room_coords,10):
            for x in range(room[0]-3, room[0]+3):
                for y in range(room[1]-3, room[1]+3):
                    self.grid[y][x] = Tile("empty.png", x, y)


    def print_dungeon(self):
        for y in range(self.height):
            for x in range(self.width):
                print("#" if self.grid[y][x].name != "empty.png" else " ", end="")
            print("")

    def display(self, screen):
        screen.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(self.grid[y][x].surface, (x*TILE_SIZE,y*TILE_SIZE))

    def add_player(self, player):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].name == "empty.png":
                    self.grid[y][x] = player
                    player.x = x
                    player.y = y
                    return True
                    self.player = player
        return False

    def move_player(self):
        current_y = self.player.y
        current_x = self.player.x
        if self.grid[current_y][current_x+1].name == "empty.png":
            self.player.x += 1
            self.grid[current_y][current_x] = Tile("empty.png", current_x, current_y)
            self.grid[current_y][current_x+1] = player


class Player(Tile):
    """docstring for Player"""
    def __init__(self, x, y):
        super(Player, self).__init__("player.png", x, y)





pygame.init()
screen = pygame.display.set_mode((DUNGEON_SIZE*TILE_SIZE, DUNGEON_SIZE*TILE_SIZE))
done = False
my_dungeon = Dungeon(DUNGEON_SIZE, DUNGEON_SIZE)
my_dungeon.add_player(Player(1,1))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type ==pygame.KEYDOWN:
            my_dungeon.move_player()

    my_dungeon.display(screen)

    pygame.display.flip()