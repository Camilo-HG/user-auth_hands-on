import os
import logging
import falcon
from falcon_cors import CORS
from falcon_cors.middleware import CORSMiddleware

# Resources
from .controllers.base_controller import BaseController

# Middleware
from .middlewares.json_middleware import JSONTranslator

def prepare_log(logs_path=Config.LOGS_PATH, log_file=Config.FALCON_MONGO_API_LOG):
    """
    Prepare the logging for the Websockets Middleware
    """
    if not os.path.exists(logs_path):
        try:
            os.mkdir(logs_path)
        except:
            print("Couldn't create log path {}".format(logs_path))
    log_file = os.path.join(logs_path, log_file)
    logging.basicConfig(filename=log_file, format=Config.LOG_FORMAT, level=logging.DEBUG)

# Prepare the logger
prepare_log()

logger = logging.getLogger("Falcon-Mongo APP")

# CORS
logger.info("Starting the CORS connection for Falcon")
cors = CORS(logger=logging.getLogger("CorsMiddleware"),
            expose_headers_list=['token'],
            allow_all_origins=True,
            allow_all_methods=True,
            allow_all_headers=True,
            allow_credentials_all_origins=True)

CORSMiddleware(cors)

# Init falcon app
logger.info("Setting middlewares: cors, JSONTranslator, ProjectMiddleware, SiteMiddleware")

app = application = falcon.API(middleware=[ cors.middleware,
                                            JSONTranslator()])

# DB
logger.info("Connecting with MongoDB {} at {}:{}".format(Config.MONGO_DB_DATABASE,
                                                         Config.MONGO_DB_HOST,
                                                         Config.MONGO_DB_PORT))
mongo.connect(Config.MONGO_DB_DATABASE,
              host=Config.MONGO_DB_HOST,
              port=Config.MONGO_DB_PORT)

# API definitions
logger.info("Loading API definitions")
UserController(app)
