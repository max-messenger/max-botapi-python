from typing import Callable

from magic_filter import F, MagicFilter

from ..types.command import Command
from ..context.state_machine import State
from ..enums.update import UpdateType
from ..loggers import logger_dp


class Handler:

    def __init__(
            self,
            *args,
            func_event: Callable,
            update_type: UpdateType,
            **kwargs
        ):
        
        self.func_event = func_event
        self.update_type = update_type
        self.filters = []
        self.state = None

        for arg in args:
            if isinstance(arg, MagicFilter):
                self.filters.append(arg)
            elif isinstance(arg, State):
                self.state = arg
            elif isinstance(arg, Command):
                self.filters.insert(0, F.message.body.text == arg.command)
            else:
                logger_dp.info(f'Обнаружен неизвестный фильтр `{arg}` при ' 
                               f'регистрации функции `{func_event.__name__}`')