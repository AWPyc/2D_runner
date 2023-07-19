from sys import exit
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # TODO: adapt player images
        player_walk_1 = pygame.image.load('graphics/player/movement/p3_walk01.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/movement/p3_walk02.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/player/movement/p3_walk03.png').convert_alpha()
        player_walk_4 = pygame.image.load('graphics/player/movement/p3_walk04.png').convert_alpha()
        player_walk_5 = pygame.image.load('graphics/player/movement/p3_walk05.png').convert_alpha()
        player_walk_6 = pygame.image.load('graphics/player/movement/p3_walk06.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/movement/p3_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 330))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump_08.wav')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 330:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 330:
            self.rect.bottom = 330

    def animation_state(self):
        if self.rect.bottom < 330:
            self.image = self.player_jump
        else:
            self.player_index += 0.3
            if self.player_index > len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        if enemy_type == 'fly':
            fly_1 = pygame.image.load('graphics/enemies/fly/flyFly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/enemies/fly/flyFly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 190
        else:
            snail_1 = pygame.image.load('graphics/enemies/snail/snailWalk1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/enemies/snail/snailWalk2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 330
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 4
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = round(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 0, 10)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10, 20)
    screen.blit(score_surface, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        enemies_group.empty()
        return False
    else:
        return True


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Game status
game_active = False

# Score
start_time = 0
score = 0

# Pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background music
bg_music = pygame.mixer.Sound('audio/background_audio.mp3')
bg_music.play(loops=-1).set_volume(0.2)

# Clocks
clock = pygame.time.Clock()

# Player Sprite Group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle Sprite Group
enemies_group = pygame.sprite.Group()

# Fonts
test_font = pygame.font.Font('fonts/font.ttf', 50)

# Background surfaces
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro text
greet_text = test_font.render('Welcome to Runner HD!', False, (255, 204, 229))
greet_rect = greet_text.get_rect(center=(400, 50))
info_text = test_font.render('Press space run ;)', False, (255, 204, 229))
info_rect = info_text.get_rect(center=(400, 350))

# Intro screen
player_stand = pygame.image.load('graphics/player/intro_stand_front/p3_front.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
enemies_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemies_timer, 1500)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pygame.display.set_caption('Runner')

    while True:
        for event in pygame.event.get():
            # Close the game window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                # Enemies
                if event.type == enemies_timer:
                    enemies_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
            else:
                # Restarting the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = round(pygame.time.get_ticks()/1000)

        # Game display
        if game_active:
            screen.blit(sky_surface, (0, -70))
            screen.blit(ground_surface, (0, 330))
            score = display_score()

            # Player update
            player.draw(screen)
            player.update()

            # Enemies update
            enemies_group.draw(screen)
            enemies_group.update()

            # Collisions
            game_active = collision_sprite()

        # Intro screen
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)

            score_message = test_font.render(f'Your score: {score}', False, (255, 204, 229))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(greet_text, greet_rect)

            if score == 0:
                screen.blit(info_text, info_rect)
            else:
                screen.blit(score_message, score_message_rect)

        pygame.display.update()
        clock.tick(60)
