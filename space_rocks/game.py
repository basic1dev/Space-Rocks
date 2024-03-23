import pygame 

#from models import GameObject
from models import Asteroid, Spaceship
from utils import load_sprite, get_random_position, print_text

# The spacerocks class.
class SpaceRocks: 
    MIN_ASTEROID_DISTANCE = 250

    # any fucntion that should be initialized here
    def __init__(self):
        self._init_pygame()
        # a display surface is created. 
        self.screen = pygame.display.set_mode((800, 600))

        # for the background image
        self.background = load_sprite("space", False)


        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 64)
        self.message = ""

        # Creating 6 asteroids
        self.asteroids = []

        # Creating bullets
        self.bullets = []
        
        # Add the spaceship
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        # Creating a random number until the position is farther 250 px away from the spaceship
        for _ in range(6):
         while True:
            position = get_random_position(self.screen)
            if (
                position.distance_to(self.spaceship.position)
                > self.MIN_ASTEROID_DISTANCE
            ):
                break

         self.asteroids.append(Asteroid(position, self.asteroids.append))

    # A helper class which downloads everything
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
    

    def main_loop(self):
        while True: 
        
            # Three steps would occur at each frame. 
            self._handle_input()
            self._process_game_logic()
            self._draw()


    # One time initialization of pygame
    def _init_pygame(self):
        # Sets up the features of pygame
        pygame.init()
        #set up caption (The name of the game)
        pygame.display.set_caption("Space Rocks")


    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()


        is_key_pressed = pygame.key.get_pressed()

        # This fucntions only if the function is true. 
        if self.spaceship:

            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
             if asteroid.collides_with(self.spaceship):
                self.spaceship = None
                self.message = "Get Good"
                break
             
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    asteroid.split()
                    self.bullets.remove(bullet)
                    break
             
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"

    def _draw(self):
        # cover the game with the backgound, since the image is as the same size as the background then blit is (0,0)
        self.screen.blit(self.background, (0,0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        # Updates contents
        pygame.display.flip()
        
        # to make the game function in 60 fps
        self.clock.tick(60)



    # Look at class definitions