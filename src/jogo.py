import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.sprites import pegar_sprite
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()
    

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    # 1. Carregando as imagens recortadas do Spritesheet


    # Jogador: usando tamanho 110x110 para capturar o quadrado perfeitamente
    player_image = pegar_sprite(CAMINHO_SPRITES, x=110, y=120, width=190, height=190, scale=0.5)

    # Gema pequena: usando tamanho 64x64
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.5)

    # Morcego: usando tamanho 180x120 por causa das asas abertas
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=905, y=1060, width=200, height=130, scale=0.5)
    
    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(350, 250))
    }

    gema = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=(500, 300))
    }
    

    segmentos = [] 

    velocidade = 5
    pontos = 0
    vidas = 1
    recorde = carregar_recorde(CAMINHO_RECORDE)
    historico = []
    
    direcao_x = 0
    direcao_y = 0
    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        jogador["rect"].x += direcao_x * velocidade
        jogador["rect"].y += direcao_y * velocidade
        

        historico.append((jogador["rect"].x, jogador["rect"].y))
        if len(historico) > 1000:
            historico.pop(0)
        # Movimentação alterando direto os eixos X e Y do retângulo do jogador
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT and direcao_x != 1:
                direcao_x = -1
                direcao_y = 0

            elif evento.key == pygame.K_RIGHT and direcao_x != -1:
                direcao_x = 1
                direcao_y = 0

            elif evento.key == pygame.K_UP and direcao_y != 1:
                direcao_x = 0
                direcao_y = -1

            elif evento.key == pygame.K_DOWN and direcao_y != -1:
                direcao_x = 0
                direcao_y = 1

        # Limitando o jogador dentro das bordas da tela usando as propriedades do Rect
        if (
            jogador["rect"].left < 0
            or jogador["rect"].right > LARGURA_TELA
            or jogador["rect"].top < 0
            or jogador["rect"].bottom > ALTURA_TELA
        ):
            vidas = tomar_dano(vidas, 1)

        espaco = 30
        for i, seg in enumerate(segmentos):
            indice = len(historico) - 1 - (espaco * (i + 1))
            if indice >= 0:
                seg["rect"].topleft = historico[indice]
        for seg in segmentos[2:]:
            if verificar_colisao(
                jogador["rect"],
                seg["rect"]
            ):
                vidas = tomar_dano(vidas, 1)
                break

        # Verificação de colisão com a Gema (antigo 'item')
        if verificar_colisao(jogador["rect"], gema["rect"]):
            pontos = calcular_pontos(pontos, 10)

            gema["rect"].x = random.randint(0, LARGURA_TELA - gema["rect"].width)
            gema["rect"].y = random.randint(0, ALTURA_TELA - gema["rect"].height)

            novo_segmento = {
                "imagem": player_image,
                "rect": player_image.get_rect(topleft=(-200, -200))
            }
            segmentos.append(novo_segmento)

        
        # Regras de fim de jogo e recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        tela.fill(CINZA)

        # Desenhando os elementos na tela passando a imagem e o rect de cada dicionário
        tela.blit(gema["imagem"], gema["rect"])
        for seg in segmentos: 
            tela.blit(seg["imagem"], seg["rect"])

        tela.blit(jogador["imagem"], jogador["rect"])
        pygame.display.flip()

    pygame.quit()