import pygame
import random

pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 600, 500

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Pengaturan blok bonus (oranye)
BONUS_BLOCK_COUNT = 4   # jumlah blok oranye per ronde
BONUS_POINTS = 10       # poin tambahan saat blok oranye pecah

# Pengaturan blok bola tambahan (merah)
EXTRA_BALL_BLOCK_COUNT = 3   # jumlah blok merah per ronde

# Posisi awal bola (juga tempat bola tambahan muncul)
BALL_SPAWN_X, BALL_SPAWN_Y = 0, HEIGHT - 150

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# Untuk mengatur kecepatan frame (frame rate)
clock = pygame.time.Clock()
FPS = 30
