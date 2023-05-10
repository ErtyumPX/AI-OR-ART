import pygame

class RenderManager:
	def __init__(self, surface:pygame.Surface, background_color=None):
		self.surface = surface
		self.background_color = background_color
		self.objects = {}

	def add(self, obj, layer=0):
		if layer in self.objects.keys():
			self.objects[layer].append(obj)
		else:
			self.objects[layer] = [obj,]
		self.objects = dict(sorted(self.objects.items()))

	def add_all(self, objects:list, layer=0):
		if layer in self.objects.keys():
			self.objects[layer].extend(objects)
		else:
			self.objects[layer] = objects
		self.objects = dict(sorted(self.objects.items()))

	def remove(self, obj):
		for layer in self.objects.values():
			for obj_ in layer:
				if obj == obj_:
					layer.remove(obj)
			

	def reset(self):
		self.objects = []

	def render(self):
		if self.background_color is not None:
			self.surface.fill(self.background_color)
		for layer in self.objects.values():
			for obj in layer:
				obj.update()
