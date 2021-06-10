import pygame
from random import randint
pygame.init()
dx, dy = 1, 1


def move(blocks, width, height, dx, dy):
	moving = None
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
		elif i.type == pygame.KEYDOWN:
			
			if i.key == pygame.K_LEFT:
				for i in range(len(blocks)):
					if blocks[i][0] == 0:
						moving = True
				if moving != True:
					for i in range(len(blocks)):
						blocks[i][1]-=dx
						
			elif i.key == pygame.K_RIGHT:
				for i in range(len(blocks)):
					if blocks[i][0] == width:
						moving = True
				if moving != True:
					for i in range(len(blocks)):
						blocks[i][1]+=dx
						
			elif i.key == pygame.K_DOWN:
				for i in range(len(blocks)):
					if blocks[i][1] == height:
						moving=True
				if moving!=True:
					for i in range(len(blocks)):
						blocks[i][1]+=dy
	return blocks	


def rotate(blocks, width, height):
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
		elif i.type == pygame.KEYDOWN:
			if i.key == pygame.K_SPACE:
				pass


def down(blocks, width, height, store, dy):
	for i in range(len(blocks)):
		if [blocks[i][0], blocks[i][1]+dy] in store:
			for k in range(len(blocks)):
				store.append(blocks[k])
				blocks = None
			break
		if blocks[i][1]+dy == height:
			for k in range(len(blocks)):
				store.append(blocks[k])
				blocks = None
			break
	return blocks


def create_new(blocks, width, height, types):
	types = [[[0,0],[dx,0],[2*dx,0],[dx,dy]], [[0,0],[dx,0],[2*dx,0],[3*dx,0]], [[0,0],[dx,0],[dx,dy],[2*dx,dy]], [[0,0],[dx,0],[2*dx,0],[2*dx,dy]]]
	if blocks == None:
		blocks = types[randint(0,3)]	
	return blocks	

print(create_new())