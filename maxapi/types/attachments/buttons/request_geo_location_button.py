from .button import Button


class RequestGeoLocationButton(Button):
    
    """Кнопка запроса геолокации пользователя.

    Attributes:
        quick: Если True, запрашивает геолокацию без дополнительного 
               подтверждения пользователя (по умолчанию False)
    """
    
    quick: bool = False