def mover_posicao(posicao, direcao):
    """Move uma posicao usando a direcao informada."""
    x, y = posicao
    direcao_x, direcao_y = direcao
    return (x + direcao_x, y + direcao_y)


def manter_na_tela(posicao, largura_tela, altura_tela):
    """Faz a posicao voltar pelo outro lado quando sai da tela."""
    x, y = posicao
    return (x % largura_tela, y % altura_tela)


def posicoes_iguais(posicao_1, posicao_2):
    """Verifica se duas posicoes sao iguais."""
    return posicao_1 == posicao_2
