from pgzero.actor import Actor

class Hero:

	def __init__(self, pos):
		self.actor = Actor("hero_idle1", pos)
		self.speed = 3
		self.frame = 0
		self.direction = "right"
		self.anim_timer = 0
	
	def update(self, keys):
		dx = 0
		if keys.left:
			dx = -self.speed
			self.direction = "left"
		elif keys.right:
			dx = self.speed
			self.direction = "right"
		
		self.actor.x += dx
		self.animate(dx)
	
	def animate(self, dx):
		self.anim_timer += 1
		if self.anim_timer % 8 == 0:
			self.frame = (self.frame + 1) % 2
			if dx == 0:
				self.actor.image = f"hero_idle{self.frame+1}"
			else:
				self.actor.image = f"hero_walk{self.frame+1}"
	
	def draw(self):
		self.actor.draw()
	
	@property
	def rect(self):
		return self.actor._rect
