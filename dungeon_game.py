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
		self.Spawnable #I want to make it possible to add a Spawnable iteam randomly, sometimes

		# initialize image
		self.surface = None
		if self.name not in all_images.keys():
			all_images[self.name] = pygame.image.load(self.name)
		self.surface = all_images[self.name]
		
	def step_on(player):
		self.Spawnable.activate(player)



# My for this is to have a spawnable class that works as an interface that all of 
# things on the board inheart from and then all of them can activate to do something
# once a condition is activate probably the player stands on them

class Spawnable(object):
	def __init__():
		
		
	# methiod that is called if a player steps on the tile
	def activate(player):
		print('This should never happen you have declared a Spawnable when you should only ever declare it\'s children')
		
	# methiod to supply the image for the tile
	def image():
		print('this is a methiod to return the image of the object for the tile to replace as it\'s owen \n this should never be called but be overidden by a child' )
	
#		super(Spawnable, self).__init__(image_name, x, y)
# 		self.heal = False
# 		full properties of an item here




class Car(Spawnable):
	def __init__(self, x, y):
		
	def activate(player):
		player.getHit(20)
		
	def image():
		return "item.png"
	

class Chest(Spawnable):
	def __init__(self, x, y):
		super(Spawnable, self).__init__("", x, y)
		print('the chest has no image ksbjfabkjakfkjafbjk')
		
	def activate(player):
		player.loot(random.randint(0,10))

		def image():
			print('Chest doesn\'t have a image LSDBlbhvdslsg')
			return ""
		
		


		
		
		

class Dungeon(object):
	"""docstring for Dungeon"""
	def __init__(self, width, height):
		super(Dungeon, self).__init__()
		self.width = width
		self.height = height

		self.grid = []
		self.generate()

		self.players = []
		

	def generate(self):

		# step one: fill the entire dungeon with bricks
		for y in range(self.height):
			self.grid += [[]]
			for x in range(self.width):
				self.grid[-1] += [Tile(x, y)]

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
		return False
		


class Player(Tile):
	"""docstring for Player"""
	def __init__(self, x, y):
		super(Player, self).__init__("player.png", x, y)
		self.gear = []
		self.health = 100
		self.power = 1
		self.armor = 0
		self.purse = 0
		
		
		
	#The following methods are created for interacting with spawnable ojects
	def equip(spawnable):
		self.gear += spawnable
		
	def gitHit(hit):
		self.health -= hit
		
	def powerUp(boost):
		self.power += boost
		
	def heal(amount):
		self.health += amount
		
	def loot(coin):
		self.purse += coin
	
	





pygame.init()
screen = pygame.display.set_mode((DUNGEON_SIZE*TILE_SIZE, DUNGEON_SIZE*TILE_SIZE))
done = False
my_dungeon = Dungeon(DUNGEON_SIZE, DUNGEON_SIZE)
my_dungeon.add_player(Player(1,1))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    my_dungeon.display(screen)

    pygame.display.flip()