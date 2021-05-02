import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_CONN_STR = os.environ.get('MONGODB_CONN_STR')  # mongo URI from env. var.(s)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Base dir constant for navigation
