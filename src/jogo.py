import random

import pygame

from src.config import (
    ALTURA_TELA,
    BRANCO,
    CAMINHO_RECORDE,
    CINZA,
    FPS,
    LARGURA_TELA,
    META_COMIDAS,
    PONTOS_POR_COMIDA,
    PRETO,
    TAMANHO_BLOCO,
    TITULO_JOGO,
    VERDE,
    VERMELHO,
)
from src.dados import carregar_recorde, salvar_recorde
from src.funcoes import (
    calcular_pontuacao,
    direcao_oposta,
    mover_cobrinha,
    mover_posicao,
    posicoes_iguais,
    verificar_derrota_corpo,
    verificar_derrota_parede,
    verificar_vitoria,
)


def criar_cobrinha():
    """Cria a cobrinha no centro da tela."""
    x = (LARGURA_TELA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = (ALTURA_TELA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return [
        (x, y),
        (x - TAMANHO_BLOCO, y),
        (x - TAMANHO_BLOCO * 2, y),
    ]


def sortear_comida(cobrinha):
    """Sorteia uma comida em uma posicao da grade."""
    colunas = LARGURA_TELA // TAMANHO_BLOCO
    linhas = ALTURA_TELA // TAMANHO_BLOCO

    while True:
        x = random.randrange(colunas) * TAMANHO_BLOCO
        y = random.randrange(linhas) * TAMANHO_BLOCO
        comida = (x, y)

        if comida not in cobrinha:
            return comida


def criar_partida():
    """Cria os dados iniciais de uma partida."""
    cobrinha = criar_cobrinha()
    comida = sortear_comida(cobrinha)
    direcao = (TAMANHO_BLOCO, 0)
    comidas_coletadas = 0
    return cobrinha, comida, direcao, comidas_coletadas


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


def atualizar_jogo(cobrinha, comida, direcao, comidas_coletadas):
    """Move a cobrinha e atualiza a comida quando houver colisao."""
    nova_cabeca = mover_posicao(cobrinha[0], direcao)

    if posicoes_iguais(nova_cabeca, comida):
        comidas_coletadas += 1
        cobrinha = mover_cobrinha(cobrinha, direcao, crescer=True)
        comida = sortear_comida(cobrinha)
    else:
        cobrinha = mover_cobrinha(cobrinha, direcao)

    return cobrinha, comida, comidas_coletadas


def desenhar_bloco(tela, posicao, cor):
    """Desenha um bloco do jogo."""
    bloco = pygame.Rect(posicao[0], posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
    pygame.draw.rect(tela, cor, bloco)
    pygame.draw.rect(tela, PRETO, bloco, 1)


def desenhar_texto(tela, fonte, texto, cor, x, y):
    """Desenha um texto na tela."""
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, (x, y))


def desenhar_texto_centralizado(tela, fonte, texto, cor, y):
    """Desenha um texto centralizado horizontalmente."""
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(LARGURA_TELA // 2, y))
    tela.blit(superficie, retangulo)


def desenhar_tela_inicial(tela, fonte, fonte_grande, recorde):
    """Desenha a tela inicial do jogo."""
    tela.fill(PRETO)
    desenhar_texto_centralizado(tela, fonte_grande, TITULO_JOGO, VERDE, 170)
    desenhar_texto_centralizado(
        tela,
        fonte,
        f"Colete {META_COMIDAS} comidas sem bater nas paredes ou no proprio corpo.",
        BRANCO,
        250,
    )
    desenhar_texto_centralizado(tela, fonte, f"Recorde: {recorde}", BRANCO, 295)
    desenhar_texto_centralizado(tela, fonte, "Pressione Enter ou Espaco para iniciar", BRANCO, 365)
    desenhar_texto_centralizado(tela, fonte, "Use as setas para controlar a cobrinha", BRANCO, 405)
    pygame.display.flip()


def desenhar_tela(
    tela,
    fonte,
    cobrinha,
    comida,
    comidas_coletadas,
    pontuacao,
    recorde,
    resultado,
):
    """Desenha os elementos do prototipo."""
    tela.fill(CINZA)
    desenhar_bloco(tela, comida, VERMELHO)
    for parte in cobrinha:
        desenhar_bloco(tela, parte, VERDE)
    desenhar_texto(tela, fonte, f"Comidas: {comidas_coletadas}/{META_COMIDAS}", PRETO, 10, 10)
    desenhar_texto(tela, fonte, f"Pontos: {pontuacao}", PRETO, 10, 40)
    desenhar_texto(tela, fonte, f"Recorde: {recorde}", PRETO, 10, 70)

    if resultado == "vitoria":
        desenhar_texto(tela, fonte, f"Vitoria! Voce comeu {META_COMIDAS} comidas.", BRANCO, 250, 280)
    elif resultado == "derrota":
        desenhar_texto(tela, fonte, "Derrota! A cobrinha bateu.", BRANCO, 280, 280)

    pygame.display.flip()


def desenhar_tela_derrota(tela, fonte, fonte_grande, comidas_coletadas, pontuacao, recorde):
    """Desenha a tela de derrota."""
    tela.fill(PRETO)
    desenhar_texto_centralizado(tela, fonte_grande, "Derrota", VERMELHO, 170)
    desenhar_texto_centralizado(tela, fonte, "A cobrinha bateu na parede ou no proprio corpo.", BRANCO, 245)
    desenhar_texto_centralizado(tela, fonte, f"Comidas coletadas: {comidas_coletadas}", BRANCO, 295)
    desenhar_texto_centralizado(tela, fonte, f"Pontuacao: {pontuacao}", BRANCO, 335)
    desenhar_texto_centralizado(tela, fonte, f"Recorde: {recorde}", BRANCO, 375)
    desenhar_texto_centralizado(tela, fonte, "Enter ou Espaco para jogar novamente", BRANCO, 445)
    desenhar_texto_centralizado(tela, fonte, "ESC para sair", BRANCO, 485)
    pygame.display.flip()


def executar_jogo():
    """Executa a janela e o loop principal do jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    fonte = pygame.font.SysFont("arial", 24)
    fonte_grande = pygame.font.SysFont("arial", 58)
    relogio = pygame.time.Clock()
    cobrinha, comida, direcao, comidas_coletadas = criar_partida()
    recorde = carregar_recorde(CAMINHO_RECORDE)
    resultado = "inicio"
    rodando = True

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif resultado in ("inicio", "vitoria", "derrota") and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    cobrinha, comida, direcao, comidas_coletadas = criar_partida()
                    resultado = "jogando"
                elif resultado == "jogando":
                    nova_direcao = direcao_por_tecla(evento.key, direcao)
                    if not direcao_oposta(direcao, nova_direcao):
                        direcao = nova_direcao

        if resultado == "jogando":
            cobrinha, comida, comidas_coletadas = atualizar_jogo(
                cobrinha,
                comida,
                direcao,
                comidas_coletadas,
            )
            pontuacao = calcular_pontuacao(comidas_coletadas, PONTOS_POR_COMIDA)

            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(CAMINHO_RECORDE, recorde)

            if verificar_derrota_parede(cobrinha[0], LARGURA_TELA, ALTURA_TELA):
                resultado = "derrota"
            elif verificar_derrota_corpo(cobrinha):
                resultado = "derrota"
            elif verificar_vitoria(comidas_coletadas, META_COMIDAS):
                resultado = "vitoria"

        pontuacao = calcular_pontuacao(comidas_coletadas, PONTOS_POR_COMIDA)

        if resultado == "inicio":
            desenhar_tela_inicial(tela, fonte, fonte_grande, recorde)
        elif resultado == "derrota":
            desenhar_tela_derrota(tela, fonte, fonte_grande, comidas_coletadas, pontuacao, recorde)
        else:
            desenhar_tela(
                tela,
                fonte,
                cobrinha,
                comida,
                comidas_coletadas,
                pontuacao,
                recorde,
                resultado,
            )

    pygame.quit()
