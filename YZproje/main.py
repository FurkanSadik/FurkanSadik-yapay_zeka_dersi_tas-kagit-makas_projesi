import pygame
import random
import sys
from collections import defaultdict

pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 1300, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))  # Pygame penceresini oluştur
pygame.display.set_caption("Taş-Kağıt-Makas")  # Pencere başlığı

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
BLUE = (50, 100, 255)
GREEN = (0, 200, 100)
RED = (200, 50, 50)

# Yazı fontu
FONT = pygame.font.Font("fonts/PIXELADE.TTF", 32)

# Arka plan resmi
background_img = pygame.image.load("images/background1.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Seçenekler
choices = ["rock", "paper", "scissors"]

# Skorlar
player_score = 0
ai_score = 0

# Oyuncu geçmişi ve geçiş sayımları
player_history = []
transition_counts = defaultdict(lambda: defaultdict(int))

# Zorluk seviyeleri ve seçilen zorluk
difficulty_levels = {
    "Easy": 45.5,
    "Medium": 8.5,
    "Hard": 0.5,
    "Impossible": 0.1
}
selected_difficulty = "Medium"

# Taş, Kağıt, Makas görselleri
rock_img = pygame.image.load("images/tas.png")
paper_img = pygame.image.load("images/kagit.png")
scissors_img = pygame.image.load("images/makas.png")

rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))

# Küçük boyutlardaki görseller
rock_small_img = pygame.transform.scale(rock_img, (100, 100))
paper_small_img = pygame.transform.scale(paper_img, (100, 100))
scissors_small_img = pygame.transform.scale(scissors_img, (100, 100))

# Seçenek sınırları
choice_limits = {"rock": 5, "paper": 5, "scissors": 5}
limited_mode = False  # Sınırlı mod başlangıçta kapalı

# Yazı çizme fonksiyonu
def draw_text(text, x, y, color=BLACK):
    img = FONT.render(text, True, color)
    win.blit(img, (x, y))

# Kazananı belirleyen fonksiyon
def get_winner(player, ai):
    if player == ai:
        return "draw"
    elif (player == "rock" and ai == "scissors") or \
         (player == "scissors" and ai == "paper") or \
         (player == "paper" and ai == "rock"):
        return "player"
    else:
        return "ai"

# Markov AI seçimi
def markov_ai_choice(history, transitions, mistake_chance):
    # Eğer yeterli geçmiş yoksa veya rastgele hata yapma durumu varsa, rastgele seçim yap
    if len(history) < 2 or random.random() < mistake_chance:
        return random.choice(choices)
    last_move = history[-1]
    next_moves = transitions[last_move]
    if not next_moves:
        return random.choice(choices)
    predicted_move = max(next_moves, key=next_moves.get)  # En yüksek olasılıklı hamleyi seç
    counter = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return counter[predicted_move]  # Rakibin seçimine karşı gelen hamleyi döndür

# Seçim butonlarını çizen fonksiyon
def draw_buttons():
    spacing = 250
    start_x = (WIDTH - (spacing * 2 + 150)) // 2
    positions = [start_x, start_x + spacing, start_x + 2 * spacing]
    images = [rock_img, paper_img, scissors_img]
    names = ["rock", "paper", "scissors"]

    for pos, img, name in zip(positions, images, names):
        win.blit(img, (pos, 600))  # Görseli ekrana yerleştir
        if limited_mode:  # Eğer sınırlı mod aktifse
            remaining = choice_limits[name]  # Kalan seçim sayısı
            color = RED if remaining == 0 else BLACK  # Seçim kalmadıysa kırmızı renkte yaz
            draw_text(f"x{remaining}", pos + 55, 760, color)

    # Zorluk değiştir ve skorlari sıfırla butonları
    pygame.draw.rect(win, GRAY, (1050, 30, 220, 50))
    draw_text("Zorluk Degistir", 1060, 40)

    pygame.draw.rect(win, GRAY, (1050, 100, 220, 50))
    draw_text("Skorlari Sifirla", 1065, 110)

# Zorluk seçme butonlarını çizen fonksiyon
def draw_difficulty_buttons():
    win.blit(background_img, (0, 0))  # Arka planı çiz
    draw_text("Zorluk Sec:", 585, 150)
    levels = list(difficulty_levels.keys())  # Zorluk seviyelerini listele
    for i, level in enumerate(levels):
        pygame.draw.rect(win, GRAY, (500, 250 + i * 100, 300, 80))  # Zorluk seviyesinin kutusunu çiz
        draw_text(level, 590, 275 + i * 100)
    pygame.draw.rect(win, GRAY, (500, 250 + len(levels) * 100, 300, 80))
    draw_text("Modlar", 590, 275 + len(levels) * 100)
    pygame.display.update()

# Modlar paneli, limited mod veya AI vs AI gibi seçenekler
def modlar_paneli():
    global limited_mode
    mod_panel_active = True
    while mod_panel_active:
        win.blit(background_img, (0, 0))
        draw_text("Modlar", 600, 200)

        pygame.draw.rect(win, GRAY, (500, 350, 300, 80))
        draw_text("Limited", 600, 375)

        pygame.draw.rect(win, GRAY, (500, 450, 300, 80))
        draw_text("AI vs AI", 590, 475)

        pygame.draw.rect(win, GRAY, (WIDTH - 220, 30, 180, 50))
        draw_text("Geri Dön", WIDTH - 185, 40)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Limited moda geçiş
                if 500 <= x <= 800 and 350 <= y <= 430:
                    limited_mode = True
                    mod_panel_active = False
                    return
                # AI vs AI moduna geçiş
                if 500 <= x <= 800 and 450 <= y <= 530:
                    ai_vs_ai_mode()
                    return
                # Geri dön butonuna tıklanması durumunda
                if WIDTH - 220 <= x <= WIDTH - 40 and 30 <= y <= 80:
                    choose_difficulty()
                    return

# Seçilen zorluk ile oyunun ayarlanması
def choose_difficulty():
    global selected_difficulty, limited_mode, choice_limits
    limited_mode = False
    choice_limits = {"rock": 5, "paper": 5, "scissors": 5}
    choosing = True
    while choosing:
        draw_difficulty_buttons()  # Zorluk seçme butonlarını çiz
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                levels = list(difficulty_levels.keys())
                for i, level in enumerate(levels):
                    # Zorluk seviyesine tıklama
                    if 500 <= x <= 800 and 250 + i * 100 <= y <= 330 + i * 100:
                        selected_difficulty = level
                        choosing = False
                        break
                # Modlar butonuna tıklama
                if 500 <= x <= 800 and 250 + len(levels) * 100 <= y <= 330 + len(levels) * 100:
                    modlar_paneli()
                    choosing = False

# AI vs AI modu (otomatik olarak oyun oynanır)
def ai_vs_ai_mode():
    clock = pygame.time.Clock()
    rounds = 10  # Oyun turları
    current_round = 0
    results = []
    ai1_score = 0
    ai2_score = 0
    draw_count = 0
    ai1_history = []
    ai2_history = []
    mistake_chance = difficulty_levels["Medium"]  # Zorluk seviyesine göre hata oranı

    replay_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)  # Tekrar oynama butonu
    back_button = pygame.Rect(WIDTH - 220, 30, 180, 50)  # Geri dön butonu

    while True:
        win.blit(background_img, (0, 0))
        draw_text("AI vs AI Modu", 575, 50)
        draw_text(f"AI 1 Skor: {ai1_score}", 100, 150, GREEN)
        draw_text(f"AI 2 Skor: {ai2_score}", 100, 200, RED)
        draw_text(f"Beraberlik: {draw_count}", 100, 250, BLUE)
        draw_text(f"Tur: {current_round} / {rounds}", 100, 300, BLACK)

        if current_round > 0:
            last_ai1, last_ai2, _ = results[-1]
            ai_images = {"rock": rock_img, "paper": paper_img, "scissors": scissors_img}
            win.blit(ai_images[last_ai1], (WIDTH // 2 - 300, HEIGHT // 2 - 75))
            draw_text(f"AI1: {last_ai1.capitalize()}", WIDTH // 2 - 300, HEIGHT // 2 + 90)
            win.blit(ai_images[last_ai2], (WIDTH // 2 + 150, HEIGHT // 2 - 75))
            draw_text(f"AI2: {last_ai2.capitalize()}", WIDTH // 2 + 150, HEIGHT // 2 + 90)

        if current_round >= rounds:
            pygame.draw.rect(win, GRAY, replay_button)
            draw_text("Tekrar Oyna", replay_button.x + 25, replay_button.y + 15)

        pygame.draw.rect(win, GRAY, back_button)
        draw_text("Geri Dön", back_button.x + 35, back_button.y + 10)

        pygame.display.update()
        clock.tick(2)

        if current_round < rounds:
            # AI seçimlerini yap ve kazananı belirle
            ai1 = markov_ai_choice(ai1_history, transition_counts, mistake_chance)
            ai2 = markov_ai_choice(ai2_history, transition_counts, mistake_chance)
            ai1_history.append(ai1)
            ai2_history.append(ai2)
            winner = get_winner(ai1, ai2)
            results.append((ai1, ai2, winner if winner != "draw" else "Berabere"))
            if winner == "player":
                ai1_score += 1
            elif winner == "ai":
                ai2_score += 1
            else:
                draw_count += 1
            if len(ai1_history) >= 2:
                transition_counts[ai1_history[-2]][ai1_history[-1]] += 1
            if len(ai2_history) >= 2:
                transition_counts[ai2_history[-2]][ai2_history[-1]] += 1
            current_round += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if current_round >= rounds and replay_button.collidepoint(x, y):
                    current_round = 0
                    ai1_score = 0
                    ai2_score = 0
                    draw_count = 0
                    ai1_history.clear()
                    ai2_history.clear()
                    results.clear()
                if back_button.collidepoint(x, y):
                    modlar_paneli()
                    return

# Ana oyun fonksiyonu
def main():
    global player_score, ai_score, player_choice, ai_choice
    player_choice = ""
    ai_choice = ""
    choose_difficulty()
    mistake_chance = difficulty_levels[selected_difficulty]  # Seçilen zorluk seviyesini al
    clock = pygame.time.Clock()
    run = True
    result = ""

    while run:
        clock.tick(60)
        win.blit(background_img, (0, 0))
        draw_buttons()  # Seçim butonlarını çiz
        draw_text(f"Zorluk: {selected_difficulty}", 100, 50, BLACK)
        draw_text(f"Player Score: {player_score}", 100, 250, GREEN)
        draw_text(f"AI Score: {ai_score}", 100, 300, RED)

        # Oyuncu seçimini ekrana çiz
        if player_choice:
            pos_x = WIDTH // 3 - 50
            if player_choice == "rock":
                win.blit(rock_small_img, (pos_x, HEIGHT // 2 - 50))
            elif player_choice == "paper":
                win.blit(paper_small_img, (pos_x, HEIGHT // 2 - 50))
            elif player_choice == "scissors":
                win.blit(scissors_small_img, (pos_x, HEIGHT // 2 - 50))
            draw_text("Player chose", pos_x, HEIGHT // 2 + 70)

        # AI seçimini ekrana çiz
        if ai_choice:
            pos_x = WIDTH * 2 // 3 - 50
            if ai_choice == "rock":
                win.blit(rock_small_img, (pos_x, HEIGHT // 2 - 50))
            elif ai_choice == "paper":
                win.blit(paper_small_img, (pos_x, HEIGHT // 2 - 50))
            elif ai_choice == "scissors":
                win.blit(scissors_small_img, (pos_x, HEIGHT // 2 - 50))
            draw_text("AI chose", pos_x, HEIGHT // 2 + 70)

        # Sonuç yazısı
        draw_text(f"Result: {result}", 100, 200, BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1050 <= x <= 1270 and 30 <= y <= 80:
                    choose_difficulty()  # Zorluk seçme
                    mistake_chance = difficulty_levels[selected_difficulty]
                    continue
                if 1050 <= x <= 1270 and 100 <= y <= 150:
                    player_score = 0  # Skorları sıfırla
                    ai_score = 0
                    player_choice = ""
                    ai_choice = ""
                    result = ""
                    choice_limits.update({"rock": 5, "paper": 5, "scissors": 5})
                    continue
                spacing = 250
                start_x = (WIDTH - (spacing * 2 + 150)) // 2
                for i, choice in enumerate(choices):
                    btn_x = start_x + i * spacing
                    if btn_x <= x <= btn_x + 150 and 600 <= y <= 750:
                        if limited_mode and choice_limits[choice] <= 0:  # Limited modda seçim yoksa devam etme
                            continue
                        player_choice = choice
                        player_history.append(choice)
                        if limited_mode:
                            choice_limits[choice] -= 1
                        ai_choice = markov_ai_choice(player_history, transition_counts, mistake_chance)
                        if len(player_history) >= 2:
                            prev = player_history[-2]
                            curr = player_history[-1]
                            transition_counts[prev][curr] += 1
                        winner = get_winner(player_choice, ai_choice)
                        if winner == "player":
                            player_score += 1
                            result = "Player Wins!"
                        elif winner == "ai":
                            ai_score += 1
                            result = "AI Wins!"
                        else:
                            result = "Draw"
        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
