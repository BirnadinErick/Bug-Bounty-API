#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.
#
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_CONN_STR = os.environ.get('MONGODB_CONN_STR')  # mongo URI from env. var.(s)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Base dir constant for navigation
