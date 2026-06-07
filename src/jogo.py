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


def carregar_imagens():
    """Carrega e retorna as imagens do spritesheet."""
    player_image = pegar_sprite(CAMINHO_SPRITES, x=110, y=120, width=190, height=190, scale=0.5)
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.5)
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=905, y=1060, width=200, height=130, scale=0.5)
    return player_image, gem_image, bat_image


def criar_sprites(player_image, gem_image, bat_image):
    """Cria e retorna os dicionários de sprites."""
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }
    gema = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=(500, 300))
    }
    inimigo = {
        "imagem": bat_image,
        "rect": bat_image.get_rect(topleft=(200, 500))
    }
    return jogador, gema, inimigo


def mover_jogador(jogador, teclas, velocidade):
    """Move o jogador com base nas teclas pressionadas."""
    if teclas[pygame.K_LEFT]:
        jogador["rect"].x -= velocidade
    elif teclas[pygame.K_RIGHT]:
        jogador["rect"].x += velocidade
    elif teclas[pygame.K_UP]:
        jogador["rect"].y -= velocidade
    elif teclas[pygame.K_DOWN]:
        jogador["rect"].y += velocidade

    jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
    jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)


def atualizar_segmentos(segmentos, historico):
    """Move cada segmento para a posição correta no histórico."""
    espaco = 30
    for i, seg in enumerate(segmentos):
        indice = len(historico) - 1 - (espaco * (i + 1))
        if indice >= 0:
            seg["rect"].topleft = historico[indice]


def verificar_colisao_gema(jogador, gema, segmentos, pontos, player_image):
    """Verifica colisão com a gema e adiciona segmento se coletada."""
    if verificar_colisao(jogador["rect"], gema["rect"]):
        pontos = calcular_pontos(pontos, 10)

        gema["rect"].x = random.randint(0, LARGURA_TELA - gema["rect"].width)
        gema["rect"].y = random.randint(0, ALTURA_TELA - gema["rect"].height)

        novo_segmento = {
            "imagem": player_image,
            "rect": player_image.get_rect(topleft=(-200, -200))
        }
        segmentos.append(novo_segmento)

    return pontos


def verificar_colisao_inimigo(jogador, inimigo, vidas):
    """Verifica colisão com o inimigo e aplica dano."""
    if verificar_colisao(jogador["rect"], inimigo["rect"]):
        vidas = tomar_dano(vidas, 1)

        inimigo["rect"].x += 80
        inimigo["rect"].y += 50

        if inimigo["rect"].x > LARGURA_TELA - inimigo["rect"].width:
            inimigo["rect"].x = 50
        if inimigo["rect"].y > ALTURA_TELA - inimigo["rect"].height:
            inimigo["rect"].y = 50

    return vidas


def desenhar_tela(tela, gema, inimigo, segmentos, jogador):
    """Desenha todos os elementos na tela."""
    tela.fill(CINZA)
    tela.blit(gema["imagem"], gema["rect"])
    tela.blit(inimigo["imagem"], inimigo["rect"])
    for seg in segmentos:
        tela.blit(seg["imagem"], seg["rect"])
    tela.blit(jogador["imagem"], jogador["rect"])
    pygame.display.flip()


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    player_image, gem_image, bat_image = carregar_imagens()
    jogador, gema, inimigo = criar_sprites(player_image, gem_image, bat_image)

    segmentos = []
    historico = []
    velocidade = 5
    pontos = 0
    vidas = 1
    recorde = carregar_recorde(CAMINHO_RECORDE)

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()

        historico.append((jogador["rect"].x, jogador["rect"].y))
        if len(historico) > 500:
            historico.pop(0)

        mover_jogador(jogador, teclas, velocidade)
        atualizar_segmentos(segmentos, historico)

        pontos = verificar_colisao_gema(jogador, gema, segmentos, pontos, player_image)
        vidas = verificar_colisao_inimigo(jogador, inimigo, vidas)

        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        desenhar_tela(tela, gema, inimigo, segmentos, jogador)

    pygame.quit()