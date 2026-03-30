import asyncio
import logging
import os
import unicodedata
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

load_dotenv()

# Token do bot
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN não encontrado no .env (verifique se o token realmente está no arquivo .env)")
 

# Nome de uma empresa
COMPANY_NAME = "Aurora chatbot"

# Local onde será adicionado as mensagens para os atendentes
LOG_FILE = Path("mensagens.txt")


# Configuração de log
logging.basicConfig(level=logging.INFO)

# Criando o bot usando o token do telegram 
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher gerencia os eventos do bot
dp = Dispatcher()

# Router organiza os tipo rotas
router = Router()
dp.include_router(router)
