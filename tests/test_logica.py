from pathlib import Path
from tempfile import TemporaryDirectory

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


def test_mover_posicao():
    assert mover_posicao((20, 20), (20, 0)) == (40, 20)


def test_calcular_pontuacao():
    assert calcular_pontuacao(3, 10) == 30


def test_mover_cobrinha_mantem_tamanho():
    cobrinha = [(40, 20), (20, 20), (0, 20)]
    assert mover_cobrinha(cobrinha, (20, 0)) == [(60, 20), (40, 20), (20, 20)]


def test_mover_cobrinha_cresce():
    cobrinha = [(40, 20), (20, 20), (0, 20)]
    assert mover_cobrinha(cobrinha, (20, 0), crescer=True) == [
        (60, 20),
        (40, 20),
        (20, 20),
        (0, 20),
    ]


def test_derrota_parede_lado_direito():
    assert verificar_derrota_parede((800, 100), 800, 600) is True


def test_derrota_parede_lado_esquerdo():
    assert verificar_derrota_parede((-20, 100), 800, 600) is True


def test_sem_derrota_dentro_da_tela():
    assert verificar_derrota_parede((400, 300), 800, 600) is False


def test_derrota_no_proprio_corpo():
    cobrinha = [(40, 20), (20, 20), (40, 20)]
    assert verificar_derrota_corpo(cobrinha) is True


def test_sem_derrota_no_proprio_corpo():
    cobrinha = [(40, 20), (20, 20), (0, 20)]
    assert verificar_derrota_corpo(cobrinha) is False


def test_posicoes_iguais():
    assert posicoes_iguais((40, 80), (40, 80)) is True


def test_posicoes_diferentes():
    assert posicoes_iguais((40, 80), (80, 40)) is False


def test_vitoria_com_30_comidas():
    assert verificar_vitoria(30, 30) is True


def test_sem_vitoria_antes_de_30_comidas():
    assert verificar_vitoria(29, 30) is False


def test_direcao_oposta():
    assert direcao_oposta((20, 0), (-20, 0)) is True


def test_salvar_e_carregar_recorde():
    with TemporaryDirectory() as pasta_temporaria:
        caminho = Path(pasta_temporaria) / "recorde.txt"

        salvar_recorde(caminho, 120)

        assert carregar_recorde(caminho) == 120
