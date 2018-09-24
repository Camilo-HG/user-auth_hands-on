import os

def _get_env(env_var, default):
    """
    Retrieve environmental variable
    or fallback to a default value.
    Input:
      - env_var(string): name of the variable to retrieve
      - default(string): default value to fall back to
    Output:
      - Value of the environmental variable or default
        value in case the variable is not defined in the enviroment.
        The return always has the same type as the default value
    """
    try:
        tp = type(default)
        return tp(os.environ[env_var])
    except:
        return default


class Config:
    """
    Config is a class with the general
    geoserver configurations
    """

    ## General configurations

    # LOG FORMATTING
    LOG_FORMAT = _get_env("LOG_FORMAT", "%(asctime)s - %(levelname)s: %(message)s")

    # PATHS
    LOGS_PATH = _get_env("LOGS_PATH", "./logs")

    # HOST
    HOST = _get_env("HOST", "localhost")

    ## MONGO DB
    MONGO_DB_PORT = _get_env("MONGO_DB_PORT", 27017)
    MONGO_DB_URL = _get_env("MONGO_DB_URL", "mongodb://localhost/falcon-mongo")
    MONGO_DB_HOST = _get_env("MONGO_DB_HOST", "localhost")
    MONGO_DB_DATABASE = _get_env("MONGO_DB_DATABASE", "falcon-mongo")

    ## FALCON MONGO API
    FALCON_MONGO_API_LOG = _get_env("FALCON_MONGO_API_LOG", "mongo_api.log")
    MONGO_DB_API_PORT = _get_env("MONGO_DB_API_PORT", 3011)
    MONGO_DB_API_URL = _get_env("MONGO_DB_API_URL", "http://{}:{}".format(HOST, MONGO_DB_API_PORT))
