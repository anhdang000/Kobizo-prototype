class Error_Handler(Exception):
    def __init__(self):
        pass

class NoDataReturn(Error_Handler):
    pass

class NoDataPassThroughFilter(Error_Handler):
    pass