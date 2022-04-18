import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


class Segment:

	def __init__(self, x, y, length, i, parent=None):
		self.parent = parent
		self.length = length
		self.b = Vec2(0, 0)
		self.child = None
		self.angle = 0

		if self.parent == None:
			self.a = Vec2(x, y)
		else:
			self.a = self.parent.b.Copy()
		
		self.CalculateB()

	def SetA(self, pos):
		self.a = Vec2(pos[0], pos[1])

	def AttachA(self):
		self.SetA(self.parent.b)

	def Follow(self, t=None):
		if t == None:
			targetX = self.child.a.x
			targetY = self.child.a.y
			self.Follow((targetX, targetY))
		else:
			target = Vec2(t[0], t[1])
			direction = target - self.a
		
			self.angle = direction.Heading()

			direction = direction.SetMag(self.length)
			direction *= -1
			self.a = target + direction

	def CalculateB(self):
		dx = self.length * cos(self.angle)
		dy = self.length * sin(self.angle)
		self.b.Set(self.a.x + dx, self.a.y + dy)

	def Update(self):
		self.CalculateB()

	def Draw(self):
		pg.draw.aaline(screen, white, (self.a.x, self.a.y), (self.b.x, self.b.y))


length = 80
start = Segment(300, 200, length, 0)
current = start

numOfSegs = 4
for i in range(0, numOfSegs - 1):
	n = Segment(0, 0, length, i, current)
	current.child = n
	current = n

end = current
base = Vec2(width // 2, 1)


def DrawLoop():
	global pos
	screen.fill(darkGray)

	DrawAllGUIObjects()

	end.Follow(pg.mouse.get_pos())
	end.Update()

	n = end.parent
	while n != None:
		n.Follow()
		n.Update()
		n = n.parent

	start.SetA(base)
	start.CalculateB()
	n = start.child
	while n != None:
		n.AttachA()
		n.Update()
		n = n.child

	end.Draw()
	n = end.parent
	while n != None:
		n.Draw()
		n = n.parent

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)


while RUNNING:
	clock.tick_busy_loop(FPS)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			RUNNING = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				RUNNING = False

		HandleEvents(event)

	DrawLoop()
