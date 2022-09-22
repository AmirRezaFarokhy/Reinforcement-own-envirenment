import cv2
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import time
import pickle

plt.style.use("ggplot")

SIZE = 10
PLAYER_N = 1
FOOD_N = 2
ENEMY_N = 3

d = {1: (255, 175, 0),
	 2: (0, 255, 0),
	 3: (0, 0, 255)}

class Blob:
	def __init__(self):
		self.x = np.random.randint(0, SIZE)
		self.y = np.random.randint(0, SIZE)

	def __str__(self):
		return f"{self.x}, {self.y}"

	def __sub__(self, other):
		return (self.x-other.x, self.y-other.y)

	def action(self, choices):
		if choices==0:
			self.move(x=1, y=1)
		elif choices==1:
			self.move(x=-1, y=-1)
		elif choices==2:
			self.move(x=-1, y=1)
		elif choices==3:
			self.move(x=1, y=-1)

	def move(self, x=False, y=False):
		if not x:
			self.x += np.random.randint(-1, 2)
		else:
			self.x += x

		if not y:
			self.y += np.random.randint(-1, 2)
		else:
			self.y+= y

		if self.x < 0:
			self.x = 0 
		elif self.x > SIZE-1:
			self.x = SIZE-1

		if self.y < 0: 
			self.y = 0 
		elif self.y > SIZE-1:
			self.y = SIZE-1




