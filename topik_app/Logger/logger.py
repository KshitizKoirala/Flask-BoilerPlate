import os
import logging
from flask import current_app
from flask.logging import default_handler


logging.basicConfig(filename=f"{os.path.abspath(os.getcwd())}/topik_app/Logger/Logs.txt", level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


logger = logging.getLogger(__name__)
