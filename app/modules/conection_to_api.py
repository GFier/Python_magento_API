from .decorators import correct_server_response, timer
from requests_oauthlib import OAuth1
from abc import ABC, abstractmethod
import datetime, requests, json, math

class Oauth_Strategy( ABC):
    """
    This class declares the different interfaces common for all api servers to get, post or put data.
    """

    access_token = None
    store_id = None
    user_id = None
    client_url = None
    consumer_key = None
    consumer_secret = None
    access_token_secret = None
    auth = None
    admin_token = None
    user_pass = None

    def __init__(self, client_url, access_token, store_id, user_id, consumer_key, consumer_secret, access_token_secret, user_pass, admin_token):
        self.client_url = client_url
        self.access_token = access_token
        self.store_id = store_id
        self.user_id = user_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_secret = access_token_secret
        self.admin_token = admin_token
        self.user_pass = user_pass
        if self.consumer_secret != '':
            self.auth = OAuth1(self.consumer_key,self.consumer_secret, self.access_token, self.access_token_secret,signature_type='auth_header')

    @abstractmethod
    def search_method(self):
        pass

    @abstractmethod
    def save_json( self):
        pass

    @abstractmethod
    def execute_get(self):
        pass

    @abstractmethod
    def execute_post(self):
        pass

    @abstractmethod
    def execute_put(self):
        pass

class Magento( Oauth_Strategy):
    __url = None
    __page_size = 100

    def __init__(self, url, access_token, store_id, user_id, consumer_key, consumer_secret, access_token_secret, user_pass, admin_token):
        super().__init__(url, access_token, store_id, user_id, consumer_key, consumer_secret, access_token_secret, user_pass, admin_token)

    def save_json(self, response):
        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = 'MAGENTO-' + date + '-response.json'
        with open(filename, 'w') as outf:
            json.dump(response, outf, sort_keys=True, indent=4)

    def search_method(self, type, filter, filter_field, **kwargs):
        self.__url = ''.join([self.client_url,type])
        def field(lg_and,lg_or): # AND is 0 & OR is 1
            return "searchCriteria[filter_groups][" + str(lg_and) +  "][filters][" +  str(lg_or) + "][field]="
        def value(lg_and,lg_or):
            return "&searchCriteria[filter_groups][" + str(lg_and) +  "][filters][" +  str(lg_or) + "][value]="
        def condition(lg_and,lg_or):
            return "&searchCriteria[filter_groups][" + str(lg_and) +  "][filters][" +  str(lg_or) + "][condition_type]="

        pagesize = "&searchCriteria[pageSize]=" + str(self.__page_size)
        current_page = "&searchCriteria[currentPage]=" + kwargs.get('new_page','1')
        only = "&fields=items[sku,id,type_id,extension_attributes[stock_item[item_id,qty]]]"
        end_url = ''.join(["&searchCriteria[filter_groups][1][filters][0][field]=status","&searchCriteria[filter_groups][1][filters][0][value]=processing"])

        def by_create_date():
            self.__url = ''.join([self.__url,'?',field(0,0),'created_at',value(0,0),filter_field,condition(0,0),'gt'])
            self.__url = self.__url + pagesize + current_page

        def by_create_and_update_date():
            dt = datetime.datetime.strptime(filter_field, '%Y-%m-%d %H:%M:%S')
            dtc = dt - datetime.timedelta(days=14)
            created_at = dtc.strftime('%Y-%m-%d %H:%M:%S')
            self.__url = ''.join([self.__url,'?',field(0,0),'created_at',value(0,0),created_at,condition(0,0),'gt','&',
                            field(1,0),'updated_at',value(1,0),filter_field,condition(1,0),'gt'])
            self.__url = self.__url + pagesize + current_page

        def prod_by_sku():
            self.__url = ''.join([self.__url,'?',field(0,0),'sku',value(0,0),filter_field,condition(0,0),'eq'])

        def by_id():
            self.__url = ''.join([self.__url,'?',field(0,0),'entity_id',value(0,0),filter_field,condition(0,0),'eq'])
            self.__url = self.__url + pagesize + current_page

        def all_products():
            self.__url = ''.join([self.__url,'?',field(0,0),'entity_id',value(0,0),filter_field,condition(0,0),'neq'])
            self.__url = self.__url + pagesize + current_page

        def prod_stock():
            self.__url = ''.join([self.__url, '/',filter_field])

        def by_customer_id():
            self.__url = ''.join([self.__url,'/',filter_field])

        def by_address_id():
            self.__url = ''.join([self.__url,'/addresses/',filter_field])

        def by_shipping_id():
            self.__url = ''.join([self.__url,'/',filter_field,'/shippingAddress'])

        def by_billing_id():
            self.__url = ''.join([self.__url,'/',filter_field,'/billingAddress'])

        def no_filter():
            pass

        def not_found():
            print('404: Search method not found')
            exit()

        filter_options = {'by_create_date': by_create_date, 'by_create_and_update_date':by_create_and_update_date, 'prod_by_sku':prod_by_sku, 'by_id':by_id, 'all_products':all_products,
        'prod_stock': prod_stock, 'by_address_id':by_address_id, 'by_shipping_id':by_shipping_id, 'by_customer_id': by_customer_id,'no_filter':no_filter}
        filter_options.get(filter, not_found)()

    @correct_server_response
    def execute_get(self, type, filter, filter_field, pagesize, savejson):
        self.__page_size = pagesize
        headers = {'accept': 'application/json', 'Authentication': 'bearer ' + self.access_token}
        self.search_method( type, filter, filter_field)
        results = []
        r = requests.get( self.__url, auth=self.auth, headers = headers)
        if r.json() != []:
            max_page = math.ceil(int(r.json().get('total_count', 0))/self.__page_size)
            page = 0
            while int(page) <= max_page:
                if r.status_code == 200:
                    r.encoding = 'utf-8'
                    raw = r.json()
                    results.extend( raw.get('items',[raw]))
                    try:
                        page = str(raw.get('search_criteria').get('current_page')+1)
                        self.search_method( type, filter, filter_field, new_page = page)
                        r = requests.get( self.__url, auth=self.auth, headers = headers)
                    except: break
                else:
                    print('GET:',r.status_code,flush=True)
                    print('GET:',r.content,flush=True)
                    break
        if savejson: self.save_json(results)
        return {'results': results, 'response': {'status': r.status_code, 'content': r.content}}

    @correct_server_response
    def get_admin_token(self): #  For refresh admin token:
        headers = {'Content-Type':'application/json'}
        self.__url = ''.join([self.client_url,'integration/admin/token'])
        input = {"username": self.user_id, "password": self.user_pass}
        r = requests.post( self.__url, json = input, headers = headers)
        r.encoding = 'utf-8'
        ad_tok = r.json()
        return ad_tok

    @correct_server_response
    def execute_post(self, type, data):
        admin_token = None
        headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + self.admin_token}
        self.__url = ''.join([self.client_url,type])
        r = requests.post( self.__url, json = data, headers = headers)
        if r.status_code == 401:
            admin_token = self.get_admin_token()
            headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + admin_token}
            self.__url = ''.join([self.client_url,type])
            r = requests.post( self.__url, json = data, headers = headers)
        else:
            admin_token = self.admin_token
        if r.status_code != 200:
            print('POST: ', r.status_code, flush = True)
            print('ERROR: ', r.content, flush = True)
        return {'admin_token': admin_token, 'response': {'status': r.status_code, 'content': r.content}}

    @correct_server_response
    def execute_put(self, type, data):
        admin_token = None
        headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + self.admin_token}
        self.__url = ''.join([self.client_url,type])
        r = requests.put( self.__url, json = data, headers = headers)
        if r.status_code == 401:
            admin_token = self.get_admin_token()
            headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + admin_token}
            self.__url = ''.join([self.client_url,type])
            r = requests.put( self.__url, json = data, headers = headers)
        else:
            admin_token = self.admin_token
        if r.status_code != 200:
             print('PUT: ', r.status_code, flush = True)
             print('ERROR: ', r.content, flush = True)
        return {'admin_token': admin_token, 'response': {'status': r.status_code, 'content': r.content}}

    @correct_server_response
    def execute_delete(self, type, filter):
        admin_token = None
        headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + self.admin_token}
        self.__url = ''.join([self.client_url,type])
        r = requests.delete( self.__url, headers = headers)
        if r.status_code == 401:
            admin_token = self.get_admin_token()
            headers = {'Accept': 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer ' + admin_token}
            self.__url = ''.join([self.client_url,type])
            r = requests.delete( self.__url, headers = headers)
        else:
            admin_token = self.admin_token
        if r.status_code != 200:
            print('DELETE:',r.status_code,flush=True)
            print('ERROR:',r.content,flush=True)
        return {'admin_token': admin_token, 'response': {'status': r.status_code, 'content': r.content}}

class Undefined:

    def __init__(self, **kwargs):
        print('404: Strategy Not Found')
        exit()
