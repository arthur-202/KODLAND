# Adventure Coins

Adventure Coins é um jogo de plataforma simples desenvolvido em Python utilizando a biblioteca Pygame Zero. O jogador controla um herói que deve coletar moedas enquanto evita inimigos e salta entre plataformas. O jogo possui menu interativo, sistema de pontuação, efeitos sonoros e música de fundo.

---

## Sobre

Este projeto foi criado como parte de um processo seletivo para a KODLAND, com o objetivo de demonstrar habilidades em programação de jogos, lógica, organização de código e uso de bibliotecas gráficas em Python.

---

## Funcionalidades

- Menu inicial com botões para iniciar o jogo, ativar/desativar som e sair.
- Controle do herói com setas do teclado para mover e tecla espaço para pular.
- Plataformas para o herói andar e pular.
- Inimigos que se movem horizontalmente e causam game over ao colidir.
- Moedas animadas para coletar e aumentar a pontuação.
- Música de fundo e efeitos sonoros para ações como pular, coletar moedas e morrer.
- Tela de game over com pontuação final e opção para reiniciar.

---

## Como jogar

- Use as setas esquerda e direita para mover o herói.
- Pressione a tecla espaço para pular.
- Colete todas as moedas para ganhar pontos.
- Evite os inimigos para não perder o jogo.
- No menu, clique nos botões para iniciar, controlar o som ou sair.

---

## Requisitos

- Python 3.x
- Pygame Zero (instalável via `pip install pgzero`)

---

## Estrutura do código

- `Game`: classe principal que gerencia estados do jogo, atualizações, desenho e eventos.
- `Hero`, `Enemy`, `Coin`, `GameObject`: classes que representam os elementos do jogo.
- `Button`: classe para botões interativos no menu.
- Funções do Pygame Zero (`update`, `draw`, `on_key_down`, etc.) delegam para a instância do jogo.

---

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato

Este código foi desenvolvido para o processo seletivo da KODLAND. Para dúvidas ou sugestões, entre em contato.

---

**Divirta-se jogando Adventure Coins!**

