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

# Kelas Striker (papan pemukul)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # Variabel rect dipakai untuk mengatur posisi
        # dan tabrakan objek
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.striker = pygame.draw.rect(screen,
                                        self.color, self.strikerRect)

    # Digunakan untuk menggambar objek di layar
    def display(self):
        self.striker = pygame.draw.rect(screen,
                                        self.color, self.strikerRect)

    # Digunakan untuk memperbarui keadaan objek
    def update(self, xFac):
        self.posx += self.speed * xFac

        # Membatasi striker agar tetap berada di antara
        # tepi kiri dan kanan layar
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)

    # Mengembalikan rect dari objek
    def getRect(self):
        return self.strikerRect

