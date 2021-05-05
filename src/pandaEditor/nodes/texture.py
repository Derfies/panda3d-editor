class Texture:

    default_values = {
        'name': 'foobar'
    }

    def set_default_values(self):
        super().set_default_values()
        self.data.set_filename('fdsa')