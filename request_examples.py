'''
How to import:
'''
from __init__ import APIREST

'''
Example get product by sku and print results and status code:
'''
fetch = APIREST(query_to = 'products', filter= 'prod_by_sku',filter_field = 'prod_sku', save_json= True).get()
fetch_status = fetch.get('response').get('status')
fetch_result = fetch.get('results')
print(fetch_status)
print(fetch_result)

'''
Products queries examples:
'''
# Get All products:
APIREST(query_to = 'products', filter= 'all_products', save_json= True, pagesize = 500).get()

#  Get Product by Id:
APIREST(query_to = 'products', filter= 'by_id',filter_field = 'prod_id', save_json= True).get()

#  Get Product by sku:
APIREST(query_to = 'products', filter= 'prod_by_sku',filter_field = 'prod_sku', save_json= True).get()

#  Get Product Stock Quantity:
APIREST(query_to = 'stockItems', filter= 'prod_stock',filter_field = 'prod_sku', save_json= True).get()

# Get all categories
APIREST(query_to = 'categories', save_json= True).get()

#  Get Prodcut Stock Quantity:
APIREST(query_to = 'stockItems', filter= 'prod_stock',filter_field = 'prod_sku', save_json= True).get()

# Post special price:
data ={ "prices": [
                    {
                     "price": price,
                     "store_id": 1,
                     "sku": product_sku,
                     "price_from": "2021-01-01 00:00:00",
                     "price_to": "2021-06-01 00:00:00",
                    }
                 ]
        }
APIREST(query_to = 'products/special-price', data = data).post()

# Update product Quantity and price:
data = {"product":
                {"sku" : product_sku,
                "price": price,
                "extension_attributes":{
                "stock_item": {
                            "qty": quantity,
                            "min_qty": 0,
                            "is_in_stock": 'true',
                            "manage_stock": 'true'
                            }
                    }
                }
        }
APIREST(ksc = self.ksc_out, query_to = 'products/'+ 'product_sku', data = data, service = self.service).put()

#   Update product images:
data = {"product": {"sku" : 'product_sku', "media_gallery_entries": images}}
APIREST( query_to = 'products/'+ 'product_sku', data = data).put()

# Delete product:
APIREST(query_to = 'products/'+ 'product_sku').delete()

'''
Customer queries examples:
'''
# By customer Id:
APIREST(query_to = 'customers', filter= 'by_customer_id',filter_field = '18', save_json= True).get()

#By customer address Id:
APIREST(query_to = 'customers', filter= 'by_address_id',filter_field = '10', save_json= True).get()

# By customer shipping address Id:
APIREST(query_to = 'customers', filter= 'by_shipping_id', filter_field = '16', save_json= True).get()

# By customer billing address Id:
APIREST(query_to = 'customers', filter= 'by_billing_id', filter_field = '6', save_json= True).get()

'''
Orders queries examples:
'''
# Get orders since created date:
APIREST(query_to = 'orders', filter= 'by_create_date', filter_field = '2021-03-08 00:00:00', save_json= True).get()

# Get orders since updated date and created 14 days before:
APIREST(query_to = 'orders', filter= 'by_create_and_update_date', filter_field = '2021-03-08 00:00:00', save_json= True).get()

# Post order:
data = {"entity": {}
        }
APIREST(query_to = 'orders', data = data, save_json= True).post()
