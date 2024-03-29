import pygame
import random
import time
import sys

all_images = {}
TILE_SIZE = 18
DUNGEON_SIZE = 40

## HI DEVIN <3 <3<3<3

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
#       self.heal = False
#       full properties of an item here

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

        self.players = []
        self.monsters = []


    def generate(self):

        # step one: fill the entire dungeon with bricks
        for y in range(self.height):
            self.grid += [[]]
            for x in range(self.width):
                self.grid[-1] += [Tile("bricks.png", x, y)]

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
                    self.players += [player]
                    return True
        return False


    def add_monster(self, monster):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].name == "empty.png":
                    self.grid[y][x] = monster
                    monster.x = x
                    monster.y = y
                    return True
        return False

    def move_player(self, dx, dy):

        current_y = self.players[0].y
        current_x = self.players[0].x
        if self.grid[current_y+dy][current_x+dx].name =="empty.png":
            self.players[0].x += dx
            self.players[0].y += dy
            self.grid[current_y][current_x] = Tile("empty.png", current_x, current_y)
            self.grid[current_y + dy][current_x + dx] = self.players[0]


class Player(Tile):
    """docstring for Player"""
    def __init__(self, x, y):
        super(Player, self).__init__("player.png", x, y)




class Monster(Tile):
    """docstring for Monster"""
    def __init__(self, x, y):
        super(Monster, self).__init__("monster.png", x, y)

    def minDistance(self, dist, sptSet):
        min = sys.maxint
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstras(self, src):
        dist = [sys.maxint] * self.V
        disr[src] = 0;
        sptSet = [False] * self.V

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]

    #def chasePlayer(self):


pygame.init()
screen = pygame.display.set_mode((DUNGEON_SIZE*TILE_SIZE, DUNGEON_SIZE*TILE_SIZE))
done = False
my_dungeon = Dungeon(DUNGEON_SIZE, DUNGEON_SIZE)

my_dungeon.add_player(Player(1,1))
my_dungeon.add_monster(Monster(0,200))

dx, dy = 0, 0
last_moved = 0


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -1
            if event.key == pygame.K_DOWN:
                dy = 1
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_UP:
                dy = 0
            if event.key == pygame.K_DOWN:
                dy = 0
            if event.key == pygame.K_LEFT:
                dx = 0
            if event.key == pygame.K_RIGHT:
                dx = 0
    if (dx != 0 or dy != 0) and time.time() > last_moved + 0.1:
        my_dungeon.move_player(dx, dy)
        last_moved = time.time()

    my_dungeon.display(screen)

    pygame.display.flip()
