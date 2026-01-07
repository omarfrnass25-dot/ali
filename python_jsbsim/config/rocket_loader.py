import configparser

class RocketLoader:
    def load(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config