# -*- coding: utf-8 -*-

# script version 1.0
import os
from dotenv import load_dotenv

# telegram part
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "credentials/.env"))
path_to_creds = os.path.join(basedir, "credentials/credentials.json")


# this is list of users which have permissions for using this app
WHITE_LIST = [
    os.getenv("USER_1"),
    os.getenv("USER_2"),
    os.getenv("USER_3"),
    os.getenv("USER_4"),
    os.getenv("USER_5")
]

TOKEN = os.getenv("TOKEN")
URL_21 = os.getenv("URL_21")
URL_20 = os.getenv("URL_20")
URL_TO = os.getenv("URL_to")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if __name__ == '__main__':

    print(path_to_creds)
