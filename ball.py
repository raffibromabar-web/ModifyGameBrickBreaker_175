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

# Kelas Block (blok)
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100
        self.isBonus = False
        self.isExtraBall = False

        # Blok putih memiliki nyawa 200, jadi
        # bola harus mengenainya dua kali agar pecah
        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        # Variabel rect dipakai untuk mengatur posisi
        # dan tabrakan objek
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(screen, self.color,
                                      self.blockRect)

    # Digunakan untuk menggambar objek di layar hanya jika
    # nyawanya masih lebih dari 0
    def display(self):
        if self.health > 0:
            self.brick = pygame.draw.rect(screen,
                                          self.color, self.blockRect)

    # Mengubah blok ini menjadi blok bonus oranye
    # (pecah dengan sekali pukul dan memberi poin tambahan)
    def makeBonus(self):
        self.isBonus = True
        self.color = ORANGE
        self.health = 100

    # Mengubah blok ini menjadi blok merah pembawa bola tambahan
    # (pecah dengan sekali pukul dan memunculkan satu bola lagi)
    def makeExtraBall(self):
        self.isExtraBall = True
        self.color = RED
        self.health = 100

    # Digunakan untuk mengurangi nyawa blok
    def hit(self):
        self.health -= self.damage

    # Digunakan untuk mendapatkan rect dari objek
    def getRect(self):
        return self.blockRect

    # Digunakan untuk mendapatkan nyawa dari objek
    def getHealth(self):
        return self.health

# Kelas Ball (bola)
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,
                                 self.posy), self.radius)

    # Digunakan untuk menampilkan objek di layar
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,
                                 self.posy), self.radius)

    # Digunakan untuk memperbarui keadaan objek
    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Memantulkan bola jika menyentuh
        # salah satu tepi vertikal (kiri/kanan)
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        # Pantulan dari tepi paling atas layar
        if self.posy <= 0:
            self.yFac *= -1

        # Jika bola menyentuh tepi paling bawah layar,
        # nilai True dikembalikan
        if self.posy >= HEIGHT:
            return True

        return False

    # Mengatur ulang posisi bola
    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1

    # Digunakan untuk mengubah arah pada sumbu Y
    def hit(self):
        self.yFac *= -1

    # Mengembalikan rect dari bola. Dalam hal ini,
    # rect-nya adalah bola itu sendiri
    def getRect(self):
        return self.ball


# Fungsi Bantuan

# Fungsi untuk memeriksa tabrakan antara dua objek
def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True

    return False


# Fungsi untuk membuat dan menyusun blok
def populateBlocks(blockWidth, blockHeight,
                   horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth + horizontalGap):
        for j in range(0, HEIGHT // 2, blockHeight + verticalGap):
            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight,
                      random.choice([WHITE, GREEN])))

    # Pilih beberapa blok secara acak menjadi blok bonus oranye
    bonusCount = min(BONUS_BLOCK_COUNT, len(listOfBlocks))
    for block in random.sample(listOfBlocks, bonusCount):
        block.makeBonus()

    # Pilih beberapa blok lain secara acak menjadi blok merah (bola tambahan)
    candidates = [b for b in listOfBlocks if not b.isBonus]
    extraCount = min(EXTRA_BALL_BLOCK_COUNT, len(candidates))
    for block in random.sample(candidates, extraCount):
        block.makeExtraBall()

    return listOfBlocks


# Membuat bola di posisi awal
def createBall():
    return Ball(BALL_SPAWN_X, BALL_SPAWN_Y, 7, 5, WHITE)


# Setelah semua nyawa habis, fungsi ini menunggu sampai
# pemain menutup game atau menekan spasi, lalu menjalankan aksi yang sesuai
def gameOver():
    waiting = True

    while waiting:
        # Penanganan event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        # Hindari pemakaian CPU 100% saat menunggu
        clock.tick(FPS)


# Pengelola Game
def main():
    running = True
    lives = 3
    score = 0

    scoreText = font.render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT - 10)

    livesText = font.render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (120, HEIGHT - 10)

    striker = Striker(0, HEIGHT - 50, 100, 20, 10, WHITE)
    strikerXFac = 0

    # Daftar bola, karena blok merah bisa menambah jumlah bola
    balls = [createBall()]

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Perulangan utama game
    while running:
        screen.fill(BLACK)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        scoreText = font.render("Score : " + str(score), True, WHITE)
        livesText = font.render("Lives : " + str(lives), True, WHITE)

        # Jika semua blok sudah hancur, blok dibuat ulang
        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # Semua nyawa habis, sehingga fungsi gameOver() dipanggil
        if lives <= 0:
            running = gameOver()

            lives = 3
            score = 0
            balls = [createBall()]
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight, horizontalGap, verticalGap)

        # Penanganan event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                # PERBAIKAN: kondisi dibungkus tanda kurung
                # agar tidak berakhir dengan "or" di ujung baris
                if (event.key == pygame.K_LEFT or
                        event.key == pygame.K_RIGHT):
                    strikerXFac = 0

        # Pemeriksaan tabrakan (untuk setiap bola di layar)
        for ball in balls[:]:
            if collisionChecker(striker.getRect(), ball.getRect()):
                ball.hit()

            # Looping pada salinan list agar penghapusan blok aman
            for block in listOfBlocks[:]:
                if collisionChecker(block.getRect(), ball.getRect()):
                    ball.hit()
                    block.hit()

                    if block.getHealth() <= 0:
                        listOfBlocks.remove(block)
                        score += 5
                        if block.isBonus:
                            score += BONUS_POINTS
                        if block.isExtraBall:
                            # Bola baru muncul di posisi awal
                            balls.append(createBall())

        # Perbarui
        striker.update(strikerXFac)

        for ball in balls[:]:
            if ball.update():
                if len(balls) > 1:
                    # Masih ada bola lain yang bermain: hapus bola ini saja
                    balls.remove(ball)
                else:
                    # Bola terakhir jatuh: nyawa berkurang dan bola direset
                    lives -= 1
                    ball.reset()
                    print(lives)

        # Tampilkan
        striker.display()
        for ball in balls:
            ball.display()

        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()