class User:
    def __init__(self, name, chatId, mal=None):
        self.name = name
        self.mal = mal
        self.id = chatId

    def form_json(self):
        data = {}
        data['name'] = self.name
        data['mal'] = self.mal
        return data

    def __str__(self):
        return str(self.id)