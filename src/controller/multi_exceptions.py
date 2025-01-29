class NoDataReturn(Exception):
    def __init__(self):
        pass

class NoDataPassThroughFilter(Exception):
    def __init__(self):
        pass

class NoLiveTicketPassThroughFilter(Exception):
    def __init__(self):
        pass

class NoNonLiveTicketPassThroughFilter(Exception):
    def __init__(self):
        pass
