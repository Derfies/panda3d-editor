class Texture:

    @property
    def label(self):
        return str(self.data.get_filename())
