import math, random, sys, os
import pygame
from pygame.locals import *

# import map/table image for generate .exe in pyinstaller
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# path for the map/table image
asset_url = resource_path('images/map4.png')
map_image = pygame.image.load(asset_url)

# ---

# exit the program
def events():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

# define display surface			
W, H = 1280, 720
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
pygame.font.init()
CLOCK = pygame.time.Clock()
FONT_SMALL = pygame.font.Font(None, 22)
FONT_LARGE = pygame.font.Font(None, 50)
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Template")
FPS = 1

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 128, 0, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (30,144,255, 255)

# define node class
class node:
	def __init__(self, x, y, obstacle):
		self.x = x
		self.y = y
		self.pos = (x, y)
		self.h = 0
		self.g = 0
		self.f = 0
		self.obstacle = obstacle
		self.other = None
		self.parent = None
	
	def neighbourPos(self, offset):
		return (self.x + offset[0], self.y + offset[1])
	
	def draw(self, size, color = None, id = None, surface = None):
		global text, FONT_SMALL, FONT_LARGE
		if not surface: surface = pygame.display.get_surface()
		pos = (self.x * size[0], self.y * size[1])
		if not color:
			if not self.obstacle:
				if not self.other: pygame.draw.rect(surface, BLACK, pos + size, 0)
				else: pygame.draw.rect(surface, BLUE, pos + size, 0)
			else:
				pygame.draw.rect(surface, WHITE, pos + size, 0)
		else:
			pygame.draw.rect(surface, color, pos + size, 0)
		pygame.draw.rect(surface, WHITE, pos + size, 1)
		if self.f:
			text(FONT_SMALL, "G:{0}".format(self.g), pos[0] + 5, pos[1] + 5, 0, 0, surface)
			text(FONT_SMALL, "H:{0}".format(self.h), pos[0] + size[0] - 5, pos[1] + 5, 1, 0, surface)
			text(FONT_LARGE, "F:{0}".format(self.f),  pos[0] + size[0] / 2, pos[1] + size[1] / 2 , 2, 2, surface)
			if not id == None:
				text(FONT_SMALL, "{0}".format(id), pos[0] + 5, pos[1] + size[1] - 5, 0, 1, surface)
				
			
def drawNodes(n, ms, cs):
	for x in range(ms[0]):
		for y in range(ms[1]):
			n[x][y].draw(cs)

def drawNodeList(node_list, cs, color):
	id = 0
	for n in node_list:
		n.draw(cs, color, id)
		id += 1
		
def heuristics(pos1, pos2):
	return int(math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]) * 10)

def text(font, string, x, y, xJustify = None, yJustify = None, surface = None):
	global WHITE
	if not surface: surface = pygame.display.get_surface()
	textSurface = font.render(string, 1, WHITE)
	textRect = textSurface.get_rect()
	if xJustify == 1:
		x -= textRect.width
	elif xJustify == 2:
		x -= textRect.center[0]
	if yJustify == 1:
		y -= textRect.height
	elif yJustify == 2:
		y -= textRect.center[1]
	surface.blit(textSurface, (x, y))
	
map = map_image.convert()
map_size = map_width, map_height = map.get_rect().size
cell_size = (W / map_width, H / map_height)

#create list of nodes
nodes = list([])
for x in range(map_width):
	nodes.append(list([]))
	for y in range(map_height):
		color = map.get_at((x, y))
		if color != WHITE:
			nodes[x].append(node(x, y, False))
			if color == BLUE:
				start = nodes[x][y]
				start.other = True
			elif color == RED:
				end = nodes[x][y]
				end.other = True
		else:
			nodes[x].append(node(x, y, True))


# This list contains relative x & y positions to reference a node's neighbour 
NEIGHBOURS = list([(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)])			




# the closed list contains all the nodes that have been considered economical viable.
# By that I mean a node that has been closer to the end node than any other in the open list at one time
closed = list([])

# The open list contains all the closed list's neighbours that haven't been identified as being economically sound node yet
open = list([])
open.append(start) # add the start node so that we can then add it's neighbours



# if the algorithm finds the end node then pathFound will be true otherwise it's false. 
# Once it becomes true there's no more calculations to do so the path finding script will be skipped over
pathFound = False
completedPath = list([]) # 

# main loop
while True:
	DS.fill(BLACK)	
	drawNodes(nodes, map_size, cell_size)
	drawNodeList(open, cell_size, GREEN)
	drawNodeList(closed, cell_size, RED)
	if pathFound: drawNodeList(completedPath, cell_size, PURPLE)
	pygame.display.update()
	
	# wait for user to press mouse button
	while not pygame.mouse.get_pressed()[0]:
		events()
	while pygame.mouse.get_pressed()[0]:
		events()
	
	# if we've found the quickest path from start node to end node then just draw, no need continue path finding
	if pathFound: continue
	if not open: continue
	
	
	# get lowest f from the open list, the node with the lowest f is the most economical in terms of the path towards the end node
	openNodeWithlowestF = open[0]
	for o in open:
		if  o.f < openNodeWithlowestF.f: openNodeWithlowestF = o

	mostEconomicalNodeSoFar = openNodeWithlowestF # let's make this more readable! Economical means the best path to the end given the choices but not definitive.
	
	# remove the mostEconomicalNodeSoFar from the open list
	open.remove(mostEconomicalNodeSoFar)
	# add mostEconomicalNodeSoFar to the closed list
	closed.append(mostEconomicalNodeSoFar)
	
	# if the mostEconomicalNodeSoFar is equal to the end node then we've reach our target
	if mostEconomicalNodeSoFar == end:
		temp = end
		while temp.parent:
			completedPath.append(temp)
			temp = temp.parent
		completedPath.append(start)
		pathFound = True
		# get the path etc
		
	# iterate through the list of neighbours belonging to the mostEconomicalNodeSoFar. Why?
	for neighbourOffset in NEIGHBOURS:
		nx, ny = mostEconomicalNodeSoFar.neighbourPos(neighbourOffset)

		if nx < 0 or nx >= map_width or ny < 0 or ny >= map_height: continue
		neighbour = nodes[nx][ny] # create a variable to represent the mostEconomicalNodeSoFar's neighbour
		if neighbour.obstacle: continue # if the mostEconomicalNodeSoFar's neighbouring node is an obstacle then we can't ...?
		if neighbour in closed: continue # if the mostEconomicalNodeSoFar's neighbouring node is in the closed list then we can't ...?

		# now we need to see if the mostEconomicalNodeSoFar's neighbour is more economical ...?
		hypotheticalFScore = mostEconomicalNodeSoFar.g + heuristics(neighbour.pos, mostEconomicalNodeSoFar.pos)
		NeighbourIsBetterThanMostEconomicalNodeSoFar = False # Yes it's a long variable name but it describes what it is so all is good!
		
		# is this neighbour already in open list? if it is then we don't want to be adding it again. to chec
		if not neighbour in open:
			NeighbourIsBetterThanMostEconomicalNodeSoFar = True
			neighbour.h = heuristics(neighbour.pos, end.pos)
			open.append(neighbour)
		elif hypotheticalFScore < neighbour.g:
			NeighbourIsBetterThanMostEconomicalNodeSoFar = True

		if NeighbourIsBetterThanMostEconomicalNodeSoFar:
			neighbour.parent = mostEconomicalNodeSoFar
			neighbour.g = hypotheticalFScore
			neighbour.f = neighbour.g + neighbour.h
	#sys.exit()