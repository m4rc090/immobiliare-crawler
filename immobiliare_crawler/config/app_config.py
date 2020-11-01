from immobiliare_crawler.config import default_config, local_config


class AppConfig:

    def __init__(self):
        self.__read_default()
        self.__read_local()

    def get(self, key: str):
        value = self.config.get(key)

        return value

    def __read_default(self):
        '''load default variables'''
        self.config = {k: v for k, v in default_config.__dict__.items() if
                       not k.startswith("__")}  # **Requirement create and import module default_config

    def __read_local(self):
        '''load local variables'''
        self.config = {k: v for k, v in local_config.__dict__.items() if
                       not k.startswith("__")}  # **Requirement create and import module default_config

    def __str__(self):
        return str(self.config)


## APP CONFIG INIT ##
SETTINGS = AppConfig()

GMAIL_SENDER = SETTINGS.get("GMAIL_SENDER")
GMAIL_RECEIVERS = SETTINGS.get("GMAIL_RECEIVERS")
GMAIL_PASS = SETTINGS.get("GMAIL_PASS")

MONGO_HOST = SETTINGS.get("MONGO_HOST")
MONGO_PORT = SETTINGS.get("MONGO_PORT")
MONGO_DB = SETTINGS.get("MONGO_DB")