from .conection_to_api import Magento, Undefined
from app.database.session_generator import session_background
from .encrypter import decrypt_message, encrypt_message
from .model import Magento_Service
from .decorators import timer
import os

class APIREST(object):
    """
    This class may work as the interface from where different strategies are choosen through the
    authentication method. New strategies may be enumareted in strategy_dict.
    """
    strategy_dict = {'magento': Magento, 'undefined': Undefined}

    def __init__(self, **kwargs):
        self.session = session_background( 'session')
        self.key = open(os.getcwd() + '/app/data/secret.key').read()
        self.service= self.session.query(Magento_Service).first()
        # Must be a variable:
        self.query_to = kwargs['query_to']
        # Optional Variables:
        self.filter = kwargs.get('filter','no_filter')
        self.filter_field = kwargs.get('filter_field','')
        self.pagesize = kwargs.get('pagesize',100)
        self.save_json = kwargs.get('save_json', False)
        self.data = kwargs.get('data','')

     # Authentication where the particular strategy is choosen:
    def authentication(self):
        return self.strategy_dict.get(self.service.name.lower(),'undefined')( decrypt_message(self.key,self.service.service_url), decrypt_message(self.key,self.service.access_token),
            decrypt_message(self.key,self.service.store_id), decrypt_message(self.key,self.service.user_id),decrypt_message(self.key,self.service.consumer_key),
            decrypt_message(self.key,self.service.consumer_secret), decrypt_message(self.key,self.service.access_token_secret), decrypt_message(self.key,self.service.user_pass),
            decrypt_message(self.key,self.service.admin_token))

    # Search:
    @timer
    def get(self):
        resp = self.authentication().execute_get( type = self.query_to, filter = self.filter, filter_field = self.filter_field, pagesize = self.pagesize, savejson = self.save_json)
        return resp

    # Update:
    @timer
    def put(self):
        resp = None
        resp = self.authentication().execute_put( type = self.query_to, data = self.data)
        if resp.get('admin_token') is not None: self.admin_token = encrypt_message(self.key, resp.get('admin_token'))
        return resp

    # Create:
    @timer
    def post(self):
        resp = None
        resp = self.authentication().execute_post( type = self.query_to, data = self.data)
        if resp.get('admin_token') is not None: self.admin_token = encrypt_message(self.key, resp.get('admin_token'))
        return resp

    # Delete:
    @timer
    def delete(self):
        resp = None
        resp = self.authentication().execute_delete( type = self.query_to)
        if resp.get('admin_token') is not None: self.admin_token = encrypt_message(self.key, resp)
        return resp
