import os
from dotenv import load_dotenv

config = {
          'apikey': os.getenv('api_key'),
          'apisec': os.getenv('api_secret'),
          'acctok': os.getenv('access_token'),
          'accsec': os.getenv('access_secret'),
}
