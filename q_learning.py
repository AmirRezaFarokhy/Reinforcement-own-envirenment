import cv2
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import time
import pickle
from Envirenment import Blob

SIZE = 10
HM_EPISODES = 25000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300 
start_q_table = None
FOOD_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 5
LEARNING_RATE = 0.1
DISCOUNT = 0.95
PLAYER_N = 1
FOOD_N = 2
ENEMY_N = 3

d = {1: (255, 175, 0),
	 2: (0, 255, 0),
	 3: (0, 0, 255)}

if start_q_table is None:
	q_table = {}
	for x1 in range(-SIZE+1, SIZE):
		for y1 in range(-SIZE+1, SIZE):
			for x2 in range(-SIZE+1, SIZE):
				for y2 in range(-SIZE+1, SIZE):
					q_table[((x1, y1),(x2, y2))] = [np.random.uniform(-5, 0) for i in range(4)]


else:
	with open(start_q_table, "rb") as f:
		q_table = puckle.load(f)


ep_rewards = []
for episode in range(HM_EPISODES):
	player = Blob()
	food = Blob()
	enemy = Blob()

	if episode%SHOW_EVERY==0:
		#print(f"on # {episode}, epsilon: {epsilon}")
		#print(f"{SHOW_EVERY} ep mean {np.mean(ep_rewards[-SHOW_EVERY:])}")
		show = True
	else:
		show = False

	ep_reward = 0
	for i in range(200):
		obs = (player-food, player-enemy)
		if np.random.random()>epsilon:
			action = np.argmax(q_table[obs])
		else:
			action = np.random.randint(0, 4)

		player.action(action)

		food.move()
		enemy.move()

		if player.x==enemy.x and player.y==enemy.y:
			reward = -ENEMY_PENALTY
		elif player.x==food.x and player.y==food.y:
			reward = FOOD_REWARD
		else:
			reward = -MOVE_PENALTY

		new_obs = (player-food, player-enemy)
		max_future_q = np.max(q_table[new_obs])
		current_q = q_table[obs][action]	
		print(f"future q {max_future_q}")
		print(f"currect q {current_q}")

		if reward==FOOD_REWARD:
			new_q = FOOD_REWARD
		elif reward==-ENEMY_PENALTY:
			new_q = -ENEMY_PENALTY
		else:
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

		q_table[obs][action] = new_q

		if show:
			env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
			env[food.y][food.x] = d[FOOD_N]
			env[player.y][player.x] = d[PLAYER_N]
			env[enemy.y][enemy.x] = d[ENEMY_N]

			img = Image.fromarray(env, "RGB")
			img = img.resize((300, 300))
			cv2.imshow("RainForcement LR", np.array(img))
			if reward==FOOD_REWARD or reward==-ENEMY_PENALTY:
				if cv2.waitKey(500) & 0xFF == ord("q"):
					break
			else:
				if cv2.waitKey(1) & 0xFF == ord("q"):
					break

		ep_reward += reward
		if reward==FOOD_REWARD or reward==-ENEMY_PENALTY:
			break     

	ep_rewards.append(ep_reward)
	epsilon *= EPS_DECAY


moving_avg = np.convolve(ep_rewards, np.ones((SHOW_EVERY, ))/SHOW_EVERY, mode="valid")

plt.figure(figsize=(10,10))
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable {time.time()}.pickle") as f:
	pickle.dump(q_table, f)