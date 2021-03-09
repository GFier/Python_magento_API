from sqlalchemy import Column, Integer, String, Sequence
from app.database.session_generator import session_background
from app.database.base import Base
from .encrypter import encrypt_message
from .decorators import timer
import json, os

class Magento_Service(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    service_url = Column(String(250))
    store_id = Column(String(250))
    user_id = Column(String(250))
    user_pass = Column(String(250))
    access_token = Column(String(250))
    consumer_key = Column(String(250))
    consumer_secret = Column(String(250))
    access_token_secret = Column(String(250))
    admin_token = Column(String(250))

    def __init__(self, session):
        self.key = open(os.getcwd() + '/app/data/secret.key').read()
        self.session = session
        with open(os.getcwd() + '/app/data/keys.json') as json_file:
            self.json_data = json.load(json_file)

        def not_none( var):
            if var != "None": ret = encrypt_message(self.key,var)
            else: ret = ''
            return ret

        self.name = 'magento'
        self.service_url = not_none(self.json_data["url"]+'/rest/default/V1/')
        self.access_token= not_none(self.json_data["access_token"])
        self.store_id = not_none(self.json_data["store_id"])
        self.user_id = not_none(self.json_data["user_id"])
        self.user_pass= not_none(self.json_data["user_pass"])
        self.admin_token= not_none(self.json_data["admin_token"])
        self.consumer_key= not_none(self.json_data["consumer_key"])
        self.consumer_secret = not_none(self.json_data["consumer_secret"])
        self.access_token_secret = not_none(self.json_data["access_token_secret"])
