from utils import *

class Formas(StatesGroup):
    waiting_for_message = State() # modo espera atendente


def criar_menu() -> ReplyKeyboardMarkup:
    # Já testei: com one_time_keyboard=False o teclado não some
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Horário de funcionamento")],
            [KeyboardButton(text="Contato")],
            [KeyboardButton(text="Serviços disponíveis")],
            [KeyboardButton(text="Ajuda")],
            [KeyboardButton(text="Falar com atendente")],
        ],
        # ajustar o tamanho do teclado
        resize_keyboard=True,  
        # Evita que o teclado desapareça após cada interação
        one_time_keyboard=False,  
    )


def normalizar_texto(texto: str) -> str:
    # tira acentos e deixa minúsculo
    texto = texto.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


# Salva a mensagem do usuário em um arquivo - persistência de dados
def salvar_mensagem_log(user: types.User, message_text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nome_usuario = f"@{user.username}" if user.username else "sem_username"
    nome_completo = user.full_name or "Sem nome"

    log_line = (
        f"[{timestamp}] "
        f"ID: {user.id} | "
        f"Nome: {nome_completo} | "
        f"Usuário: {nome_usuario} | "
        f"Mensagem: {message_text}\n"
    )
    # Tratar possíveis erros na persistência dos dados
    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(log_line)
    except Exception:
        logging.exception("Erro ao salvar mensagem no arquivo.")


# Quando o usuário digita /start
@router.message(CommandStart())
async def comando_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Olá! Seja bem-vindo(a) ao atendimento virtual da <b>{COMPANY_NAME}</b>.\n\n"
        "Sou o seu assistente automático e estou pronto para ajudar.\n"
        "Escolha uma opção no menu abaixo:",
        reply_markup=criar_menu(),
    )


# Esse handler roda quando o usuário está no modo "falar com atendente"
@router.message(StateFilter(Formas.waiting_for_message), F.text)
async def mensagem_atendente(message: types.Message, state: FSMContext):
    # Salva a mensagem no arquivo
    salvar_mensagem_log(message.from_user, message.text)

    # Confirma pro usuário que foi enviado
    await message.answer(
    "Recebi! Vou repassar pro pessoal. Eles costumam responder em até 1 hora (em horário comercial).\n\n"
    "Enquanto isso, pode usar o menu abaixo:",
    reply_markup=criar_menu(),
)
    # Sai do modo atendente
    await state.clear()


# Handler principal pra mensagens normais
@router.message(F.text)
async def mensagens_de_texto(message: types.Message, state: FSMContext):
    text = message.text.strip()
    text_normalized = normalizar_texto(text)

    if text == "Horário de funcionamento":
        await message.answer(
            "<b>Horário de funcionamento</b>\n\n"
            "Segunda a sexta: 08h às 18h\n"
            "Sábado: 08h às 12h\n"
            "Domingo: fechado"
        )
        return

    if text == "Contato":
        await message.answer(
            "<b>Contato</b>\n\n"
            "E-mail: contato@auroraservicos.com.br\n"
            "Telefone: (83) 3210-4500\n"
            "WhatsApp: (83) 98888-4500"
        )
        return

    if text == "Serviços disponíveis":
        await message.answer(
            "<b>Serviços disponíveis</b>\n\n"
            "• Suporte técnico\n"
            "• Segunda via de documentos e boletos\n"
            "• Agendamento de atendimento\n"
            "• Consulta de protocolos\n"
            "• Informações gerais"
        )
        return

    if text == "Ajuda":
        await message.answer(
            "<b>Ajuda</b>\n\n"
            "Use os botões do menu para navegar.\n"
            "Se quiser falar com um atendente, clique em <b>Falar com atendente</b> "
            "e envie sua mensagem.\n\n"
            "Você também pode digitar palavras como <i>horário</i>, <i>contato</i> ou <i>serviços</i>."
        )
        return

    if text == "Falar com atendente":
        await message.answer(
            "Perfeito. Escreva sua mensagem agora que ela será encaminhada a um atendente.",
            reply_markup=ReplyKeyboardRemove(),
        )

        # Entra no modo de espera de mensagem
        await state.set_state(Formas.waiting_for_message)
        return

    # Aqui ele entende texto "livre", mesmo sem clicar nos botões

    if "horario" in text_normalized or "funcionamento" in text_normalized:
        await message.answer(
            "Nosso horário é de segunda a sexta, das 08h às 18h, e aos sábados, das 08h às 12h."
        )
        return

    if any(p in text_normalized for p in ["contato", "email", "telefone", "whatsapp"]):
        await message.answer(
            "Você pode falar conosco pelo e-mail contato@auroraservicos.com.br "
            "ou pelo telefone (83) 3210-4500."
        )
        return

    if any(p in text_normalized for p in ["servico", "servicos", "serviço", "serviços"]):
        await message.answer(
            "Oferecemos suporte técnico, segunda via, agendamento, consulta de protocolos e informações gerais."
        )
        return

    if "ajuda" in text_normalized:
        await message.answer(
            "Use o menu abaixo para navegar. Se precisar, escolha a opção de atendimento humano."
        )
        return

    # Se não entender nada;
    await message.answer(
        "Desculpe, não entendi sua mensagem.\n"
        "Use o menu abaixo para acessar as opções disponíveis.",
        reply_markup=criar_menu(),
    )


# Caso receba algo que não é texto (imagem, áudio, etc)
@router.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "Desculpe, ainda não consigo processar esse tipo de mensagem.\n"
        "Use o menu abaixo para continuar.",
        reply_markup=criar_menu(),
    )


# Função principal que inicia o bot
async def main():
    logging.info("Bot iniciado com sucesso.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
