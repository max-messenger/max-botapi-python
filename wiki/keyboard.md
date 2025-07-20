Есть два способа построения клавиатур для сообщений: через **InlineKeyboardBuilder** и через **pydantic-модели** (ButtonsPayload)

---

## Синтаксис создания клавиатуры

### Через InlineKeyboardBuilder

```python
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


@dp.message_created(Command('builder'))
async def builder_process(event: MessageCreated):

    builder = InlineKeyboardBuilder()
    builder.row(
        LinkButton(text="Сайт", url="https://example.com"),
        CallbackButton(text="Нажми меня", payload="some_data"),
    )
    # ... добавляйте новые ряды builder.row(...)
    await event.message.answer(
        text='Вот клавиатура',
        attachments=[builder.as_markup()]
    )
```

### Через pydantic-модели

```python
from maxapi.types import ButtonsPayload


@dp.message_created(Command('payload'))
async def builder_process(event: MessageCreated):

    buttons = [
        [LinkButton(text="Сайт", url="https://example.com")],
        [CallbackButton(text="Callback", payload="some_data")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.message.answer(
        text='Вот клавиатура',
        attachments=[payload]
    )
```

---

## Типы кнопок

Каждый тип кнопки подходит для разных сценариев. Вот основные из них:

### LinkButton

* **Назначение:** Переход по ссылке.
* **Пример:**

  ```python
  LinkButton(text="Открыть сайт", url="https://example.com")
  ```

### CallbackButton

* **Назначение:** Для обработки нажатий через callback.
* **Пример:**

  ```python
  CallbackButton(text="Нажми меня", payload="my_payload")
  ```

### ChatButton

* **Назначение:** Создание нового чата.
* **Пример:**

  ```python
  ChatButton(text="Создать чат", chat_title="Название", chat_description="Описание")
  ```

### RequestGeoLocationButton

* **Назначение:** Запрос геолокации у пользователя (на момент публикации этой документации не работает со стороны API MAX).
* **Пример:**

  ```python
  RequestGeoLocationButton(text="Геолокация")
  ```

### MessageButton

* **Назначение:** Быстрая отправка сообщения.
* **Пример:**

  ```python
  MessageButton(text="Сообщение")
  ```

### RequestContactButton

* **Назначение:** Запросить контакт у пользователя.
* **Пример:**

  ```python
  RequestContactButton(text="Контакт")
  ```

### OpenAppButton

* **Назначение:** Открыть встроенное приложение.
* **Пример:**

  ```python
  OpenAppButton(
      text="Приложение",
      web_app="username бота",
      contact_id="Идентификатор бота"
  )
  ```

---

## Пример [тут](https://github.com/love-apples/maxapi/blob/main/examples/keyboard/main.py)