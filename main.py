import pygame
import random

def dosya_oku_yaz(dosya_adı, mod, içerik=None):
    try:
        with open(dosya_adı, mod, encoding="utf-8") as dosya:
            if içerik is not None:
                dosya.write(str(içerik))
            else:
                return dosya.readline().strip()
    except FileNotFoundError:
        return 0

def oyun_kurulum():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()  # pygame.font'u başlat

    genislik, yukseklik = 600, 750
    pencere = pygame.display.set_mode((genislik, yukseklik))
    pygame.mixer.music.load("kaynaklar/oyun_muzik.wav")
    pygame.mixer.music.play(-1, 0.0)
    seviye_yukselme_sesi = pygame.mixer.Sound("kaynaklar/level_up.wav")
    altin_yeme = pygame.mixer.Sound("kaynaklar/jump.wav")
    hiz = 10
    saat = pygame.time.Clock()
    fps = 40
    yazi_font = pygame.font.SysFont("consolas", 25)
    return genislik, yukseklik, pencere, seviye_yukselme_sesi, altin_yeme, hiz, saat, fps, yazi_font

def ana_dongu():
    durum = True
    y, x = 0, 0
    scor = 0
    max_scor = 0

    genislik, yukseklik, pencere, seviye_yukselme_sesi, altin_yeme, hiz, saat, fps, yazi_font = oyun_kurulum()

    canavar = pygame.image.load("kaynaklar/monster.png")
    canavar_koordinat = canavar.get_rect()
    canavar_koordinat.topleft = (genislik / 2, yukseklik / 2)

    yem = pygame.image.load("kaynaklar/cent.png")
    yem_koordinat = yem.get_rect()
    yem_koordinat.topleft = (150, 150)

    arka_palan = pygame.image.load("kaynaklar/background.jpg")

    while durum:
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                if scor > max_scor:
                    dosya_oku_yaz("kaynaklar/max_scor.txt", "w", scor)
                durum = False

        if scor > 200:
            arka_palan = pygame.image.load("kaynaklar/background2.jpg")

        pencere.blit(arka_palan, (0, 0))
        pencere.blit(canavar, canavar_koordinat)
        pencere.blit(yem, yem_koordinat)

        yazi = yazi_font.render("Scor: " + str(scor), True, (0, 255, 0))
        yazi_koordinat = yazi.get_rect()
        yazi_koordinat.topleft = (8, 9)

        max_scor = int(dosya_oku_yaz("kaynaklar/max_scor.txt", "r"))

        yazi2 = yazi_font.render("Max Scor: " + str(max_scor), True, (0, 255, 0))
        yazi2_koordinat = yazi2.get_rect()
        yazi2_koordinat.topright = (genislik - 8, 9)

        pygame.draw.line(pencere, (255, 0, 255), (0, 50), (600, 50), 3)
        pencere.blit(yazi, yazi_koordinat)
        pencere.blit(yazi2, yazi2_koordinat)
        pygame.display.update()

        saat.tick(fps)
        tus = pygame.key.get_pressed()

        if tus[pygame.K_LEFT] and canavar_koordinat.left > 0:
            canavar_koordinat.x -= hiz
        elif tus[pygame.K_RIGHT] and canavar_koordinat.right < genislik:
            canavar_koordinat.x += hiz
        elif tus[pygame.K_UP] and canavar_koordinat.top > 55:
            canavar_koordinat.y -= hiz
        elif tus[pygame.K_DOWN] and canavar_koordinat.bottom < yukseklik:
            canavar_koordinat.y += hiz

        if canavar_koordinat.colliderect(yem_koordinat):
            altin_yeme.play()
            yem_koordinat.x = random.randint(0, genislik - 32)
            yem_koordinat.y = random.randint(55, yukseklik - 24)
            scor += 1

        if scor > 100:
            canavar = pygame.image.load("kaynaklar/monster2.png")
            if y == 0:
                seviye_yukselme_sesi.play()
                canavar_koordinat = canavar.get_rect()
                canavar_koordinat.topleft = (195, 195)
                y += 1
            fps = 25
            if tus[pygame.K_LEFT] and canavar_koordinat.left > 0 + 10:
                canavar_koordinat.x -= hiz
            elif tus[pygame.K_RIGHT] and canavar_koordinat.right < genislik + 10:
                canavar_koordinat.x += hiz
            elif tus[pygame.K_UP] and canavar_koordinat.top > 55 + 10:
                canavar_koordinat.y -= hiz
            elif tus[pygame.K_DOWN] and canavar_koordinat.bottom < yukseklik + 10:
                canavar_koordinat.y += hiz

            if canavar_koordinat.colliderect(yem_koordinat):
                altin_yeme.play()
                yem_koordinat.x = random.randint(0, genislik - 64)
                yem_koordinat.y = random.randint(55, yukseklik - 24)
                scor += 1

        elif scor > 150:
            canavar = pygame.image.load("kaynaklar/monster3.png")
            if x == 0:
                seviye_yukselme_sesi.play()
                canavar_koordinat = canavar.get_rect()
                canavar_koordinat.topleft = (195, 195)
                x += 1
            fps = 30
            if tus[pygame.K_LEFT] and canavar_koordinat.left > 0:
                canavar_koordinat.x -= hiz
            elif tus[pygame.K_RIGHT] and canavar_koordinat.right < genislik:
                canavar_koordinat.x += hiz
            elif tus[pygame.K_UP] and canavar_koordinat.top > 55:
                canavar_koordinat.y -= hiz
            elif tus[pygame.K_DOWN] and canavar_koordinat.bottom < yukseklik:
                canavar_koordinat.y += hiz

            if canavar_koordinat.colliderect(yem_koordinat):
                altin_yeme.play()
                yem_koordinat.x = random.randint(0, genislik - 32)
                yem_koordinat.y = random.randint(55, yukseklik - 24)
                scor += 1

    pygame.quit()

if __name__ == "__main__":
    ana_dongu()
