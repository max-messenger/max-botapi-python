# Асинхронный MAX API

[![PyPI version](https://img.shields.io/pypi/v/maxapi.svg)](https://pypi.org/project/maxapi/)
[![Python Version](https://img.shields.io/pypi/pyversions/maxapi.svg)](https://pypi.org/project/maxapi/)
[![License](https://img.shields.io/github/license/love-apples/maxapi.svg)](https://love-apples/maxapi/blob/main/LICENSE.md)

---

## 📦 Установка

```bash
pip install maxapi
```

---

## 🚀 Быстрый старт

```python
import asyncio
import logging

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

logging.basicConfig(level=logging.INFO)

bot = Bot('тут_ваш_токен')
dp = Dispatcher()


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Привет! Отправь мне /start'
    )


@dp.message_created(Command('start'))
async def hello(event: MessageCreated):
    await event.message.answer(f"Пример чат-бота для MAX 💙")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
```

---

## 📚 Документация

В разработке...

---

## 🧩 Возможности

- ✅ Роутеры
- ✅ Билдер инлайн клавиатур
- ✅ Простая загрузка медиафайлов
- ✅ MagicFilter
- ✅ Внутренние функции моделей
- ✅ Контекстный менеджер
- ✅ Поллинг
- ✅ Вебхук
- ✅ Логгирование

---


## 💬 Обратная связь и поддержка

- MAX: [Чат](https://max.ru/join/IPAok63C3vFqbWTFdutMUtjmrAkGqO56YeAN7iyDfc8)
- Telegram: [@loveappless](https://t.me/loveappless)
---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.
