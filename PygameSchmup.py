import os
import pygame
import random

# Dimensions of game window + FPS
WIDTH = 600
HEIGHT = 1050
FPS = 30

# image directory
img_dir = os.path.join(os.path.dirname(__file__), 'img')

# RGB values for drawing colors easily
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nick's Schmup Project")
clock = pygame.time.Clock()
# Sprite groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# function to draw text to screen
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

# Player class
class Player(pygame.sprite.Sprite):
	# Neccessary function to run the "Sprite" class initializer
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# Every sprite must have an image and a rect
		self.image = pygame.transform.scale(player_img, (50, 38))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		# Player sprite starts in center of pygame window
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0

	# FIXED: Player object not moving, as function was not indented properly
	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
			self.speedx = 8
		# FIXED: Allowed player to move up and down
		if keystate[pygame.K_UP] or keystate[pygame.K_w]:
			self.speedy = -8
		if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
			self.speedy = 8
		# Allows player to hold down spacebar to shoot
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		# FIXED: Stops player from leaving bounds of the top and bottom of the screen
		# Game window is drawn from top to bottom, inc/dec for y-axis movement is inverse
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT

	# lots of method overriding!
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

# Basic enemey class
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(enemy_img, (45, 45))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pygame.time.get_ticks()

	# Unused animation function to rotate the enemy sprites.
	# TODO: Fix animation so sprites are not destroyed when rotated
	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		#self.rotate() unused rotation animation. Sprites are destroyed when function is called
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if (self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20):
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(bullet_img, (12, 50))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -55

	def update(self):
		self.rect.y += self.speedy
		# Kill when it moves beyond the top of the screen
		if self.rect.bottom < 0:
			self.kill()

# Load game graphics
background = pygame.image.load(os.path.join(img_dir, 'IMG_1144.png')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_green.png")).convert()
enemy_img = pygame.image.load(os.path.join(img_dir, "ufoRed.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, "laserRed01.png")).convert()

# Creates object of type "Player()" and adds it to the all_sprites group
player = Player()
all_sprites.add(player)

# Creates 10 objects of type "Mob()" and adds them to our sprite group
for int in range(20):
	enemy = Mob()
	all_sprites.add(enemy)
	mobs.add(enemy)

score = 0
# Main game loop. Quits if "X" is pressed to exit
running = True
while (running):
	# Loop runs at specified speed:
	clock.tick(FPS)

	# Handles event "QUIT," closes game window
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
		# If you add an event.type of keystate then you have to press the space bar for each player.shoot()

	all_sprites.update()

	mobHit = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in mobHit:
		# increments score on hit
		score += 50
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)

	hits = pygame.sprite.spritecollide(player, mobs, False)
	if hits:
		running = False

	# drawing all screen elements
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	pygame.display.flip()

# IDLE friendly
pygame.quit()