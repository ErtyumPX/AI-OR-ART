class Transform:
	def __init__(self, x=0, y=0, width=0, height=0, angle=0, color=(255,255,255)):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.angle = angle
		self.color = color

	@property
	def __repr__(self):
		return self.x, self.y, self.width, self.height

	@property
	def position(self):
		return self.x, self.y

	@property
	def int_position(self):
		return int(self.x), int(self.y)

	@property
	def size(self):
		return self.width, self.height

	@property
	def rect(self):
		return self.x, self.y, self.width, self.height
