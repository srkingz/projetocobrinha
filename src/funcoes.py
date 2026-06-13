def mover_posicao(posicao, direcao):
    """Move uma posicao usando a direcao informada."""
    x, y = posicao
    direcao_x, direcao_y = direcao
    return (x + direcao_x, y + direcao_y)


def mover_cobrinha(cobrinha, direcao, crescer=False):
    """Move a cobrinha e aumenta o corpo quando necessario."""
    nova_cabeca = mover_posicao(cobrinha[0], direcao)

    if crescer:
        return [nova_cabeca] + cobrinha

    return [nova_cabeca] + cobrinha[:-1]


def posicoes_iguais(posicao_1, posicao_2):
    """Verifica se duas posicoes sao iguais."""
    return posicao_1 == posicao_2


def calcular_pontuacao(comidas_coletadas, pontos_por_comida):
    """Calcula a pontuacao com base nas comidas coletadas."""
    return comidas_coletadas * pontos_por_comida


def direcao_oposta(direcao_atual, nova_direcao):
    """Verifica se a nova direcao e oposta a direcao atual."""
    return (
        direcao_atual[0] + nova_direcao[0] == 0
        and direcao_atual[1] + nova_direcao[1] == 0
    )


def verificar_derrota_parede(posicao, largura_tela, altura_tela):
    """Verifica se a cobrinha saiu dos limites da tela."""
    x, y = posicao

    if x < 0 or x >= largura_tela:
        return True
    if y < 0 or y >= altura_tela:
        return True

    return False


def verificar_derrota_corpo(cobrinha):
    """Verifica se a cabeca encostou no proprio corpo."""
    cabeca = cobrinha[0]
    corpo = cobrinha[1:]
    return cabeca in corpo


def verificar_vitoria(comidas_coletadas, meta_comidas):
    """Verifica se o jogador coletou a quantidade necessaria de comidas."""
    return comidas_coletadas >= meta_comidas
