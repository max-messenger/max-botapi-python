

from aiohttp import ClientTimeout


class DefaultConnectionProperties:
    
    def __init__(self, timeout: int = 5 * 30, sock_connect: int = 30, **kwargs):
        self.timeout = ClientTimeout(total=timeout, sock_connect=sock_connect)
        self.kwargs = kwargs