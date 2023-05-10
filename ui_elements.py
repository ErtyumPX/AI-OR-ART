import pygame
import re

empty_function = lambda: 0
BLANK_WHITE_IMAGE = pygame.image.load('data/white.jpg')
DEFAULT_FONT = 'data/munro.ttf'

class InterfaceElement:
	def __init__(self, status):
		self.status = status # 0: visible/interactable   1: visible/uninteractable  2: invisible
		self.image = None
		self.x = 0
		self.y = 0

	def change_status(self, new_status):
		if -1 < new_status < 3:
			self.status = new_status
		else:
			raise Exception("Improper status")

def ElementCollide(button:InterfaceElement, mouse):
	x = button.x
	y = button.y
	return x < mouse[0] < x + button.image.get_width() and y < mouse[1] < y + button.image.get_height()

class ImageButton(pygame.sprite.Sprite, InterfaceElement):
	def __init__(self, surface, image, x, y, image_percentage=100, func=empty_function, args=(), kwargs={}, upper_surface=(0,0), selected_change=(0,0), highlight_color = None, highlight_offset = (0, 0), status=0):
		pygame.sprite.Sprite.__init__(self)
		InterfaceElement.__init__(self, status)
		self.surface = surface
		fraction = image_percentage/100
		self.image = pygame.transform.scale(image, (int(image.get_width()*fraction), int(image.get_height()*fraction)))

		self.x = x
		self.y = y
		self.upper_surface = upper_surface
		self.selected_change = selected_change
		self.selected = False
		self.clicked = False

		self.func = func
		self.args = args
		self.kwargs = kwargs

		self.highlight_color = highlight_color
		self.highlight_offset = highlight_offset
		if highlight_color:
			image_size = image.get_size()
			self.effect = pygame.Surface((image_size[0]+highlight_offset[0], image_size[1]+highlight_offset[1]), pygame.SRCALPHA)
			self.effect.fill(highlight_color)

	def update(self):
		if self.status != 2:
			if self.selected:
				self.surface.blit(self.image, (self.x+self.selected_change[0], self.y+self.selected_change[1]))
				if self.highlight_color: self.surface.blit(self.effect, (self.x+self.selected_change[0]-self.highlight_offset[0]/2, self.y+self.selected_change[1]-self.highlight_offset[1]/2))
			else:
				self.surface.blit(self.image, (self.x, self.y))



class TextButton(pygame.sprite.Sprite, InterfaceElement):
	def __init__(self, surface, x, y, width, height, func=empty_function, args=(), kwargs={}, font_size=24, text="Default Text", color=(0,0,0), image=BLANK_WHITE_IMAGE, selected_change=(0,0), highlight_color = None, highlight_offset = (0, 0), status=0):
		pygame.sprite.Sprite.__init__(self)
		InterfaceElement.__init__(self, status)
		self.surface = surface
		self.image = pygame.transform.scale(image, (width, height))

		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.selected_change = selected_change
		self.selected = False
		self.clicked = False

		self.func = func
		self.args = args
		self.kwargs = kwargs

		self.highlight_color = highlight_color
		self.highlight_offset = highlight_offset
		if highlight_color:
			self.effect = pygame.Surface((width+highlight_offset[0], height+highlight_offset[1]), pygame.SRCALPHA)
			self.effect.fill(highlight_color)

		self.text = text
		self.color = color
		self.font = pygame.font.Font(DEFAULT_FONT, font_size)
		self.text_box = self.font.render(self.text, True, color)
		text_size = self.text_box.get_size()
		self.textRect = pygame.Rect(0,0,0,0)
		self.textRect.center = (x+int(width/2)-int(text_size[0]/2), y+int(height/2)-int(text_size[1]/2))

	def update(self):
		if self.status != 2:
			self.surface.blit(self.image, (self.x, self.y))
			self.surface.blit(self.text_box, self.textRect)

			if self.selected and self.highlight_color:
				self.surface.blit(self.effect, (self.x-self.highlight_offset[0]/2, self.y-self.highlight_offset[1]/2))

class Text(pygame.sprite.Sprite, InterfaceElement):
	def __init__(self, surface, x:int = 0, y:int = 0, text:str = "New Text", font_size:int = 12, color:tuple = (0,0,0), status:int = 0):
		pygame.sprite.Sprite.__init__(self)
		InterfaceElement.__init__(self, status)
		self.surface = surface
		self.x = x
		self.y = y
		self.text = text
		self.color = color
		self.font = pygame.font.Font(DEFAULT_FONT, font_size)
		self.text_box = self.font.render(self.text, True, color)

	def change_text_to(self, new_text:str):
		self.text = new_text
		self.text_box = self.font.render(self.text, True, self.color)

	def change_color_to(self, new_color:tuple):
		self.color = new_color
		self.text_box = self.font.render(self.text, True, self.color)

	def move_to(self, x, y):
		self.x = x
		self.y = y

	def center(self, x:int = None, y:int = None):
		text_size = self.text_box.get_size()
		text_rect = pygame.Rect(0, 0, 0, 0)
		if x and y:
			text_rect.center = (x - int(text_size[0] / 2), y - int(text_size[1] / 2))
			self.x = text_rect.x
			self.y = text_rect.y
		else:
			text_rect.center = (self.x - int(text_size[0] / 2), self.y - int(text_size[1] / 2))
			self.x = text_rect.x
			self.y = text_rect.y


	def update(self):
		if self.status != 2:
			self.surface.blit(self.text_box, (self.x, self.y))


valid = r'[^\.A-Za-z0-9 _]'
class InputBox(pygame.sprite.Sprite, InterfaceElement):
	def __init__(self, surface, x:int = 0, y:int = 0, width:int = 50, height:int = 20, font_size = 50, color=(0, 0, 0), default_text='', image=BLANK_WHITE_IMAGE, status:int = 0):
		pygame.sprite.Sprite.__init__(self)
		InterfaceElement.__init__(self, status)
		self.surface = surface
		self.image = pygame.transform.scale(image, (width, height))
		self.x, self.y, self.width, self.height = x, y, width, height
		self.selected = False

		self.text = ''
		self.default_text = default_text
		self.color = color
		self.font_size = min(height-10, font_size)
		self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)
		self.text_box = self.font.render(self.text, True, color)

	def add(self, char):
		if not re.search(valid, char) and self.image.get_width() - self.text_box.get_width() > 15 + self.font_size/2:
			self.text += char

	def remove(self):
		self.text = self.text[:-1]

	def clear(self):
		self.text = ''

	def update(self):
		self.surface.blit(self.image, (self.x, self.y))
		if self.text == '':
			self.text_box = self.font.render(self.default_text, True, (140,140,140))
		else:
			self.text_box = self.font.render(self.text, True, self.color)
		self.surface.blit(self.text_box, (self.x + 7.5, self.y + 4))


def ProcessElements(events, pressed_keys, mouse_pos, elements:list = [], inputs:list = []):
	for element_ in elements:
		element_.clicked = False
		if ElementCollide(element_, mouse_pos):
			element_.selected = True
		else:
			element_.selected = False
	for event in events:
		if event.type == pygame.MOUSEBUTTONUP:
			for element_ in elements:
				if element_.selected and element_.status == 0:
					element_.func(*element_.args, **element_.kwargs)
					element_.clicked = True
			for input_box in inputs:
				if ElementCollide(input_box, mouse_pos):
					input_box.selected = True
				else: 
					input_box.selected = False

		elif event.type == pygame.KEYDOWN:
			for input_box in inputs:
				if input_box.selected:
					if event.key == pygame.K_BACKSPACE:
						if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT] or pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]:
							input_box.clear()
						else: 
							input_box.remove()
					else: 
						input_box.add(event.unicode)


def UpdateElements(elements:list = [], inputs:list = [], texts:list = []):
	for element_ in elements:
		element_.update()
	for input_ in inputs:
		input_.update()
	for text_ in texts:
		text_.update()
