from pgzero.actor import Actor

class Hero:
	# Constructor
	def __init__(self, pos):
		self.actor = Actor("hero_idle1", pos)
		self.speed = 3
		self.frame = 0
		self.direction = "right"
		self.anim_timer = 0
	
	def update(self, keys):
		
