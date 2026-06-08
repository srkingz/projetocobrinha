from src.funcoes import manter_na_tela, mover_posicao, posicoes_iguais


def test_mover_posicao():
    assert mover_posicao((20, 20), (20, 0)) == (40, 20)


def test_manter_na_tela_lado_direito():
    assert manter_na_tela((800, 100), 800, 600) == (0, 100)


def test_manter_na_tela_lado_esquerdo():
    assert manter_na_tela((-20, 100), 800, 600) == (780, 100)


def test_posicoes_iguais():
    assert posicoes_iguais((40, 80), (40, 80)) is True


def test_posicoes_diferentes():
    assert posicoes_iguais((40, 80), (80, 40)) is False
