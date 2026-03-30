# Aurora Bot — Atendente Virtual para Telegram

Esse chatbot foi criado pra atender um cliente que precisa de um atendente virtual simples, mas com um potencial escalar. Ele responde perguntas comuns sobre horário, contato e serviços, e registra mensagens de quem clica em “Falar com atendente”. 

OBS: O chatbot presupõe que o cliente usa um celular. Nada foi feito para ser usado no Computador!

---

## Funcionalidades

- **Menu interativo** com botões:
  - Horário de funcionamento
  - Contato (e‑mail, telefone, WhatsApp)
  - Serviços disponíveis
  - Ajuda
  - Falar com atendente (modo que salva a mensagem num arquivo)

- **Reconhecimento de texto livre** 
  O bot também entende palavras como *horário*, *contato*, *serviços* ou *ajuda* se o usuário digitar sem usar os botões.

- **Persistência de mensagens** 
  Quando o usuário entra no modo “Falar com atendente”, a mensagem é salva em `mensagens.txt` com data, ID do usuário e nome.

- **Tratamento de erros básico** 
  Caso o bot não entenda o que foi digitado, ele sugere o uso do menu.

---

## Como rodar

1. **Clone o repositório** 
   ```bash
   git clone https://github.com/arthur-202/KODLAND
   cd chatbot

2. **Crie um ambiente virtual**
3. **Instale as dependências**
  ```bash
  pip install -r requirements.txt
4. **Crie um arquivo .env na raiz do projeto com o token do seu bot:**
  ```bash
  BOT_TOKEN=seu_token_aqui

# OBSERVAÇÃO:
 **O token você obtém com o @BotFather no Telegram.**
