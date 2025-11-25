##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 1024, 536   # tamanho da tela
FPS = 60                    # taxa de atualização
pygame.display.set_caption("🚀 Space Escape")  # título da janela

# ----------------------------------------------------------
# 🧩 ASSETS DO JOGO
# ----------------------------------------------------------
ASSETS = {
    "background": "PlanoDeFundoTerror.png",  # imagem do fundo
    "player": "nave001.png",                 # imagem da nave
    "meteor": "meteoro001.png",              # imagem (não usada agora)
    "sound_point": "classic-game-action-positive-5-224402.mp3",  # som ao ganhar ponto
    "sound_hit": "harcore-terror-kick-74920.mp3",                # som ao perder vida
    "music": "Terror8bits_song.mp3"          # música de fundo
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
WHITE = (255, 255, 255)
RED   = (255, 60, 60)
BLUE  = (60, 100, 255)

# Cria a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Função para carregar imagens com fallback (caso não exista o arquivo)
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Cria um quadrado colorido se a imagem não existir
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# Carrega o fundo e o jogador
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))

# Frames do meteoro animado (2 imagens)
meteor_frames = [
    load_image("Terror_eye-1.png", RED, (80, 80)),
    load_image("Terror_eye-2.png", RED, (80, 80))
]

# Variáveis de animação do meteoro
meteor_animation_index = 0     # qual frame está exibindo
meteor_animation_timer = 0     # controla a troca de frame
meteor_animation_speed = 50    # quanto menor o valor, mais rápida a animação

# Função para carregar som com segurança
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# Música de fundo (loop)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DO JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))  # posição inicial da nave
player_speed = 7  # velocidade do jogador

# Cria 5 meteoros em posições aleatórias
meteor_list = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))

meteor_speed = 3  # velocidade dos meteoros

score = 0    # pontuação
lives = 3    # vidas do jogador
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

control_mode = "keyboard"  # modo de controle (teclado ou mouse)

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL DO JOGO
# ----------------------------------------------------------
while running:
    clock.tick(FPS)  # controla o FPS
    screen.blit(background, (0, 0))  # desenha o fundo

    # --- Tratamento de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Troca entre teclado e mouse com SHIFT direito
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                if control_mode == "keyboard":
                    control_mode = "mouse"
                else:
                    control_mode = "keyboard"

    # --- Movimento do jogador ---
    if control_mode == "keyboard":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed

        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed

        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

    elif control_mode == "mouse":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_rect.centerx = mouse_x
        player_rect.centery = mouse_y

    # --- Movimento e lógica dos meteoros ---
    for meteor in meteor_list:
        meteor.y += meteor_speed  # meteoros caem

        # Se saiu da tela → reposiciona e soma ponto
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            score += 1
            if sound_point:
                sound_point.play()

        # Se colidiu com o jogador
        if meteor.colliderect(player_rect):
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

        # Controle da animação (troca de frame)
        meteor_animation_timer += 1
        if meteor_animation_timer >= meteor_animation_speed:
            meteor_animation_timer = 0
            meteor_animation_index = (meteor_animation_index + 1) % 2

    # --- Desenho dos elementos na tela ---
    screen.blit(player_img, player_rect)  # desenha a nave

    # desenha todos os meteoros animados
    for meteor in meteor_list:
        screen.blit(meteor_frames[meteor_animation_index], meteor)

    # Exibe HUD (pontos e vidas)
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()  # atualiza a tela

# ----------------------------------------------------------
# 🏁 TELA FINAL
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))

end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)

screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

# Espera o jogador pressionar tecla ou fechar
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
