import asyncio
import logging
import os
import unicodedata
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# =========================== CONFIGURAÇÕES ===========================
TOKEN = "7006587879:AAFtDeB3JT6lVQtcX-1UN_bvHOpIadkmxes"
COMPANY_NAME = "Aurora Serviços Inteligentes"
LOG_FILE = Path("mensagens.txt")

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# =========================== ESTADOS ===========================
class Form(StatesGroup):
    waiting_for_message = State()


# =========================== TECLADO ===========================
def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Horário de funcionamento")],
            [KeyboardButton(text="📞 Contato")],
            [KeyboardButton(text="🧾 Serviços disponíveis")],
            [KeyboardButton(text="❓ Ajuda")],
            [KeyboardButton(text="👤 Falar com atendente")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


# =========================== UTILITÁRIOS ===========================
def normalize_text(text: str) -> str:
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def save_message_to_file(user: types.User, message_text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = f"@{user.username}" if user.username else "sem_username"
    full_name = user.full_name or "Sem nome"
    log_line = (
        f"[{timestamp}] "
        f"ID: {user.id} | "
        f"Nome: {full_name} | "
        f"Usuário: {username} | "
        f"Mensagem: {message_text}\n"
    )

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(log_line)
    except Exception:
        logging.exception("Erro ao salvar mensagem no arquivo.")


# =========================== /start ===========================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"👋 Olá! Seja bem-vindo(a) ao atendimento virtual da <b>{COMPANY_NAME}</b>.\n\n"
        "Sou o seu assistente automático e estou pronto para ajudar.\n"
        "Escolha uma opção no menu abaixo:",
        reply_markup=get_main_keyboard(),
    )


# =========================== ATENDENTE ===========================
@router.message(StateFilter(Form.waiting_for_message), F.text)
async def handle_attendant_message(message: types.Message, state: FSMContext):
    save_message_to_file(message.from_user, message.text)

    await message.answer(
        "✅ Sua mensagem foi registrada com sucesso.\n"
        "Ela será encaminhada para um atendente humano em breve.\n\n"
        "Enquanto isso, você pode usar o menu abaixo:",
        reply_markup=get_main_keyboard(),
    )
    await state.clear()


@router.message(F.text)
async def handle_text_messages(message: types.Message, state: FSMContext):
    text = message.text.strip()
    text_normalized = normalize_text(text)

    # Respostas exatas dos botões
    if text == "📅 Horário de funcionamento":
        await message.answer(
            "<b>Horário de funcionamento</b>\n\n"
            "Segunda a sexta: 08h às 18h\n"
            "Sábado: 08h às 12h\n"
            "Domingo: fechado"
        )
        return

    if text == "📞 Contato":
        await message.answer(
            "<b>Contato</b>\n\n"
            "E-mail: contato@auroraservicos.com.br\n"
            "Telefone: (83) 3210-4500\n"
            "WhatsApp: (83) 98888-4500"
        )
        return

    if text == "🧾 Serviços disponíveis":
        await message.answer(
            "<b>Serviços disponíveis</b>\n\n"
            "• Suporte técnico\n"
            "• Segunda via de documentos e boletos\n"
            "• Agendamento de atendimento\n"
            "• Consulta de protocolos\n"
            "• Informações gerais"
        )
        return

    if text == "❓ Ajuda":
        await message.answer(
            "<b>Ajuda</b>\n\n"
            "Use os botões do menu para navegar.\n"
            "Se quiser falar com um atendente, clique em <b>👤 Falar com atendente</b> "
            "e envie sua mensagem.\n\n"
            "Você também pode digitar palavras como <i>horário</i>, <i>contato</i> ou <i>serviços</i>."
        )
        return

    if text == "👤 Falar com atendente":
        await message.answer(
            "Perfeito. Escreva sua mensagem agora que ela será encaminhada a um atendente.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Form.waiting_for_message)
        return

    # Respostas por palavras-chave
    if "horario" in text_normalized or "funcionamento" in text_normalized:
        await message.answer(
            "📅 Nosso horário é de segunda a sexta, das 08h às 18h, e aos sábados, das 08h às 12h."
        )
        return

    if any(p in text_normalized for p in ["contato", "email", "telefone", "whatsapp"]):
        await message.answer(
            "📞 Você pode falar conosco pelo e-mail contato@auroraservicos.com.br "
            "ou pelo telefone (83) 3210-4500."
        )
        return

    if any(p in text_normalized for p in ["servico", "servicos", "serviço", "serviços"]):
        await message.answer(
            "🧾 Oferecemos suporte técnico, segunda via, agendamento, consulta de protocolos e informações gerais."
        )
        return

    if "ajuda" in text_normalized:
        await message.answer(
            "❓ Use o menu abaixo para navegar. Se precisar, escolha a opção de atendimento humano."
        )
        return

    # Resposta padrão
    await message.answer(
        "Desculpe, não entendi sua mensagem. 😕\n"
        "Use o menu abaixo para acessar as opções disponíveis.",
        reply_markup=get_main_keyboard(),
    )


# =========================== FALHAS OU MENSAGENS NÃO-TEXTO ===========================
@router.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "Desculpe, ainda não consigo processar esse tipo de mensagem.\n"
        "Use o menu abaixo para continuar.",
        reply_markup=get_main_keyboard(),
    )


# =========================== EXECUÇÃO ===========================
async def main():
    logging.info("Bot iniciado com sucesso.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()

