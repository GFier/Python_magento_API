from Support.logfile import save_in_log
from Support.pathfile import search_path
from APItoSQL.only_sql.session_generator import session_background
from APItoSQL.only_sql.table_class_sql import Transaction, User, Duna_Client, Product, Products_Variants, Mercadopago, Client_Services
from APItoSQL.only_api.main_api import APIREST
from Support.install_client import install_client
from datetime import date
import argparse, datetime, pytz, collections, time

if __name__ == "__main__":
    time.sleep(30)
###########################################################################################################################################################################
    my_parser = argparse.ArgumentParser(prog='harvest_data', description='Talk to Servers through APIRest connection and saves data in MySQL')
    my_parser.add_argument('MySQL', metavar='mysql',type=str, help='MySQL conecting info as //<user>:<password>@<host>[:<port>]/<dbname>')
    my_parser.add_argument('Key',metavar='key',type=str, help='Key for simetric encryption')
    args = my_parser.parse_args()
    creds = args.MySQL
    key = args.Key
###########################################################################################################################################################################
    today = datetime.datetime.today() - datetime.timedelta(days=5)
    hoy_dia = today.strftime("%Y-%m-%d")
    hoy_mes = today.strftime("%Y-%m")
    forever = True
    refresh_min = 25
    # # Delete Schema:
    # session = session_background( creds, 'delete')
    # session.close()
    # create = 'yes'
    # session = session_background( creds, create)
    # session.close()
    # install_client( creds)
    # # Add new client:
    # install_client( creds)
############################################################################################################################################################################
##----------------------------------------------------------------------- Harvest data -----------------------------------------------------------------------------##
############################################################################################################################################################################
    clients_active = {'Kiwano': True, 'MaggioRossetto': True, 'FaustoMilano': False, 'MonteCarlo': True, 'Paso': False, 'Turpin': False}
    while forever:
        create = 'no'
        session = session_background( creds, create)
        clients = session.query(Duna_Client).all()
        for client in clients:
            if clients_active.get(client.client_id):
                tiempo = datetime.datetime.now().time()
                save_in_log('Working on client', client.client_id)
                save_in_log('Initiating Base update at', tiempo)
                ksc = collections.namedtuple('ksc' ,'key session client')
                ksc = ksc(key = key, session = session, client = client)
                today_date = hoy_mes + '%'
                last_transactions = Transaction.get_by_paid_date( session, client, today_date)
                date = last_transactions[-1].paid_date.strftime('%Y-%m-%dT%H:%M:%S')
                save_in_log('LAST DATE:', date)
                for service in client.services:
                    if service.harvest_data == 'true':
                        if service.service_type == 'payment_method':
                            APIREST(ksc = ksc, query_to = 'payments', filter= 'since_date', filter_field = date, load_to_Sql = 'Yes', service = service).get()
                            save_in_log('Payments updated at', datetime.datetime.now().time())
                        elif service.service_type == 'ecomerce':
                            APIREST(ksc = ksc, query_to = 'orders', filter= 'by_both_date', filter_field = date, load_to_Sql = 'Yes', service = service).get()
                            save_in_log('Orders updated at', datetime.datetime.now().time())
                save_in_log('Base update Finished at', datetime.datetime.now().time())
                save_in_log('','')
        session.close()
        time.sleep(refresh_min*60)
##########################################################################################################################################################################
##########################################################################################################################################################################
##----------------------------------------------------------------------- Harvest data -----------------------------------------------------------------------------##
###########################################################################################################################################################################
