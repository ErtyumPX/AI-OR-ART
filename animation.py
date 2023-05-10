import pygame
import threading
from timeit import default_timer

on_action = []
empty_function = lambda: 0

class Timer:
	def __init__(self):
		self.counter = 0

	def __enter__(self):
		self.starting_time = default_timer()
		self.counter += 1
		return self.starting_time, self.counter

	def __exit__(self, type_, value, traceback):
		print(f'Time past on {self.counter} - {default_timer() - self.starting_time}')



def bySpeed(object_:object, target_position:tuple, speed:int, frame_rate:int = 120,
			after_function=empty_function, args=(), kwargs={}) -> bool:
	"""
	The object has to have an 'x' and 'y' property
	Speed is the "frequency", how many pixels to travel in one second.
	Function will return true after the animation is finished.
	"""
	if object_ in on_action:
		return

	path_x, path_y = target_position[0] - object_.x, target_position[1] - object_.y
	if not path_x and not path_y:
		print("No move given")
		return
	if path_y == 0:
		x_speed = speed*(path_x/abs(path_x))
		y_speed = 0
		total_frame = abs(path_x / (x_speed/frame_rate)) - 1
	elif path_x == 0:
		y_speed = speed*(path_y/abs(path_y))
		x_speed = 0
		total_frame = abs(path_y / (y_speed/frame_rate)) - 1
	else:
		ratio = path_x / path_y
		y_speed = speed / (ratio**2 + 1) ** .5
		x_speed = ratio * y_speed
		total_frame = abs(path_x / (x_speed/frame_rate)) - 1

	#print(f"x: {x_speed} -- y: {y_speed} -- frame: {total_frame}")

	on_action.append(object_)

	task = threading.Thread(target=act, args=(object_, target_position, (x_speed, y_speed), total_frame, frame_rate, after_function, args, kwargs))
	task.start()

	#return task.join()






def byDuration(object_:object, target_position:tuple, duration:int, frame_rate:int = 120) -> bool:
	"""
	The object has to have an 'x' and 'y' property
	Duration is the duration of the animation, how much time to use to reach the target position.
	Function will return true after the animation is finished.
	"""

	pass


def act(object_:object, target_position:tuple, speed:tuple, total_frame:int, frame_rate:int, after_func, args, kwargs) -> None:
	clock = pygame.time.Clock()
	frame = 0
	while frame < total_frame:
		object_.x += speed[0]/frame_rate
		object_.y += speed[1]/frame_rate
		clock.tick(frame_rate)
		frame += 1
	object_.x, object_.y = target_position[0], target_position[1]
	on_action.remove(object_)
	after_func(*args, **kwargs)
	#print("Animation finished.")


if __name__ == '__main__':
	class A:
		def __init__(self):
			self.x = 0
			self.y = 0

	timer = Timer()
	character = A()


	with timer:
		bySpeed(character, (100, 0), 100)

	with timer:
		bySpeed(character, (0, 0), 100)