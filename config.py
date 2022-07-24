from pyliteconf.config import Config


class SQLAlchemyConfig(Config):
    _dialect = "sqlite+aiosqlite"

    _username = ""
    _password = ""
    _need_dog = "@" if _username or _password else ""

    _database = "database1"

    url = f"{_dialect}://{_username}{_need_dog}{_password}/{_database}"


class PersonConfig(Config):
    cookie = None
    schoolid = "6bfe3c56-0211-4fe1-9e59-51616caac4dd"
    userrole ="STUDENT"
