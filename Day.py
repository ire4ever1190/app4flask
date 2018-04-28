class Day(list):
    """A Day Object"""
    def __init__(self, list, day_name, day_id):
        self.day_name = day_name
        self.day_id = day_id
        self.week_id = 0 if day_id == 0 else 1 if day_id < 6 else 2
        self.extend(list)
    def return_html(self):
        html = "<h1>{}</h1><h3>Week {}</h3>".format(self.day_name, self.week_id)
        for session in self:
            html += "{}<br>".format(session.return_html())
        return html
