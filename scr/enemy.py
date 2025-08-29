from pgzero.actor import Actor

class Enemy:

    def __init__(self, pos, left_bound, right_bound, speed=2):
        self.actor = Actor("enemy_idle1", pos)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = speed
        self.direction = 1
        self.frame = 0
        self.anim_timer = 0
			
    def update(self):
        self.actor.x += self.speed * self.direction
        if self.actor.x < self.left_bound or self.actor.x > self.right_bound:
        	self.direction *= -1
        	
        self.animate()
		
    def animate(self):
        self.anim_timer += 1
        if self.anim_timer % 10 == 0:
            self.frame = (self.frame + 1) % 2
            self.actor.image = f"enemy_walk{self.frame+1}"

    def draw(self):
        self.actor.draw()
	
    @property
    def rect(self):
        return self.actor._rect
