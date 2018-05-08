class Session:
    """A Session Object"""
    def __init__(self, number, code, teacher, time, room):
        self.number = number
        self.code = code
        self.teacher = teacher
        self.room = room
        self.time = time
    def return_html(self):
        return ("<item>{}</item>".format(self.code))
