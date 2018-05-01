class Session:
    """A Session Object"""
    def __init__(self, number, code, teacher, time, room):
        self.number = number
        self.code = code
        self.teacher = teacher
        self.room = room
        self.time = time
    def return_html(self):
        return ("<code>{}</code>".format(self.code))
    def return_all_html(self):
        return ("<code>{}</code><teacher>{}</teacher><room>{}</room><time>{}<time>"
                .format(self.code, self.teacher, self.room, self.time))
    
