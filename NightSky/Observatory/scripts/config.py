from configparser import ConfigParser


class Config:
    _config_parser = ConfigParser()
    _config_parser.read('static/config.ini')

    @classmethod
    def get_section(cls, section):
        return Config._config_parser[section]

    @classmethod
    def get_property(cls, section, key):
        return Config._config_parser[section][key]