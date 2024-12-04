class Config(object):
    HOST = '7a6.h.filess.io'
    DATABASE = 'CS440ShoppingCart_industrial'
    USER = 'CS440ShoppingCart_industrial'
    PASSWORD = 'a42ff5253a411662e184a51da2693e7bdf6c93a1'
    PORT = 3307

    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True

    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
            'port': cls.PORT,
        }