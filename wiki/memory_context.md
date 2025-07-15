# MemoryContext

Контекст данных пользователя с поддержкой асинхронных блокировок. Используется для хранения и управления состоянием пользователя в рамках сессии.

## Класс: `MemoryContext`

```python
MemoryContext(chat_id: int, user_id: int)
````

### Аргументы:

* `chat_id` (`int`): Идентификатор чата.
* `user_id` (`int`): Идентификатор пользователя.


## Методы

### `async def get_data() -> dict[str, Any]`

Возвращает текущие данные контекста.

#### Возвращает:

* `dict[str, Any]`: Словарь с текущими данными пользователя.

---

### `async def set_data(data: dict[str, Any])`

Полностью заменяет контекст данных.

#### Аргументы:

* `data` (`dict[str, Any]`): Новый словарь данных, заменяющий текущий.

---

### `async def update_data(**kwargs)`

Обновляет текущий контекст, добавляя или изменяя переданные пары ключ-значение.

#### Аргументы:

* `**kwargs`: Ключи и значения для обновления контекста.

---

### `async def set_state(state: State | str = None)`

Устанавливает новое состояние пользователя или сбрасывает его.

#### Аргументы:

* `state` (`State | str | None`): Новое состояние. Если `None` — состояние будет сброшено.

---

### `async def get_state() -> State | None`

Возвращает текущее состояние пользователя.

#### Возвращает:

* `State | None`: Текущее состояние или `None`, если не установлено.

---

### `async def clear()`

Очищает все данные контекста и сбрасывает состояние.

---

## Пример использования

[Полный пример](https://github.com/love-apples/maxapi/tree/main/examples/router_with_input_media)

```python
@dp.message_created(Command('clear'))
async def hello(event: MessageCreated, context: MemoryContext):
    await context.clear()
    await event.message.answer(f"Ваш контекст был очищен!")


@dp.message_created(Command('data'))
async def hello(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    await event.message.answer(f"Ваша контекстная память: {str(data)}")


@dp.message_created(Command('context'))
@dp.message_created(Command('state'))
async def hello(event: MessageCreated, context: MemoryContext):
    data = await context.get_state()
    await event.message.answer(f"Ваше контекстное состояние: {str(data)}")
```