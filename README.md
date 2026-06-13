# Cobrinha

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

## Integrantes do grupo

- Gabriel Henrique de Souza Rodrigues
- Gabriel Mota Valério
- Pedro Afonso Marquetotti
- Isaque Eduardo Gonçalves de Paiva

## Descrição do jogo

O jogo consiste em controlar uma cobrinha pela tela. O jogador deve coletar comidas, fazendo a cobrinha crescer e aumentando a pontuação. A partida termina com vitória ao coletar 30 comidas ou com derrota se a cobrinha bater na parede ou no próprio corpo.

## Objetivo do jogador

Coletar 30 comidas sem bater nas paredes da tela e sem colidir com o próprio corpo da cobrinha.

## Regras do jogo

- A cobrinha se movimenta continuamente.
- O jogador muda a direção usando as setas do teclado.
- Cada comida coletada vale 10 pontos.
- A cobrinha cresce a cada comida coletada.
- O jogador vence ao coletar 30 comidas.
- O jogador perde ao bater na parede ou no próprio corpo.
- O recorde é salvo em `data/recorde.txt`.

## Controles

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- ESC: sair do jogo

## Como executar o projeto

```bash
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```
