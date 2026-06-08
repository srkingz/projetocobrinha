import random

import pygame

from src.config import (
    ALTURA_TELA,
    CINZA,
    FPS,
    LARGURA_TELA,
    PRETO,
    TAMANHO_BLOCO,
    TITULO_JOGO,
    VERDE,
    VERMELHO,
)
from src.funcoes import manter_na_tela, mover_posicao, posicoes_iguais


def criar_cobrinha():
    """Cria a cobrinha no centro da tela."""
    x = (LARGURA_TELA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = (ALTURA_TELA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return (x, y)


def sortear_comida(cobrinha):
    """Sorteia uma comida em uma posicao da grade."""
    colunas = LARGURA_TELA // TAMANHO_BLOCO
    linhas = ALTURA_TELA // TAMANHO_BLOCO

    while True:
        x = random.randrange(colunas) * TAMANHO_BLOCO
        y = random.randrange(linhas) * TAMANHO_BLOCO
        comida = (x, y)

        if comida != cobrinha:
            return comida


def direcao_por_tecla(tecla, direcao_atual):
    """Retorna a direcao escolhida pelo jogador."""
    if tecla == pygame.K_LEFT:
        return (-TAMANHO_BLOCO, 0)
    if tecla == pygame.K_RIGHT:
        return (TAMANHO_BLOCO, 0)
    if tecla == pygame.K_UP:
        return (0, -TAMANHO_BLOCO)
    if tecla == pygame.K_DOWN:
        return (0, TAMANHO_BLOCO)

    return direcao_atual


def atualizar_jogo(cobrinha, comida, direcao):
    """Move a cobrinha e atualiza a comida quando houver colisao."""
    cobrinha = mover_posicao(cobrinha, direcao)
    cobrinha = manter_na_tela(cobrinha, LARGURA_TELA, ALTURA_TELA)

    if posicoes_iguais(cobrinha, comida):
        comida = sortear_comida(cobrinha)

    return cobrinha, comida


def desenhar_bloco(tela, posicao, cor):
    """Desenha um bloco do jogo."""
    bloco = pygame.Rect(posicao[0], posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
    pygame.draw.rect(tela, cor, bloco)
    pygame.draw.rect(tela, PRETO, bloco, 1)


def desenhar_tela(tela, cobrinha, comida):
    """Desenha os elementos do prototipo."""
    tela.fill(CINZA)
    desenhar_bloco(tela, comida, VERMELHO)
    desenhar_bloco(tela, cobrinha, VERDE)
    pygame.display.flip()


def executar_jogo():
    """Executa a janela e o loop principal do jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    cobrinha = criar_cobrinha()
    comida = sortear_comida(cobrinha)
    direcao = (TAMANHO_BLOCO, 0)
    rodando = True

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                else:
                    direcao = direcao_por_tecla(evento.key, direcao)

        cobrinha, comida = atualizar_jogo(cobrinha, comida, direcao)
        desenhar_tela(tela, cobrinha, comida)

    pygame.quit()
