from enum import IntEnum


class MessageAttribute(IntEnum):
    Flairs = 0 # list of flairs
    Upvotes = 1 # integer
    Date = 2


class Message:

    def __init__(self, flairs, upvotes, date):
        self.flairs = flairs
        self.upvotes = upvotes
        self.date = date
