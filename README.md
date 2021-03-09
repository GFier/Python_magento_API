# Python_magento_API
Python app to use Magento 2.0 Admin APIRest.
Secrets keys are encrypted with simmetric encryptation in a SQLite database.

## Install:
1. clone the repository.
2. Fill keys.json in app/data/keys.json with your integration keys found in the magento backend ->system ->integration.
3. Navigate to your directory and Run in your terminal: bash install.sh (First install pipenv if is not already installed).
4. Now you can delete the keys.json.

## Import:
1. On your script located at the root directory, import as --> from __init__ import APIREST

## Run:
Follow the examples in request_examples.py

## Documentation:
[Magento docs](https://magento.redoc.ly/2.4.2-admin/) 
### Methods:
- get: fetch data*\
    - return: Dictionary with following keys:\
      -results -> api response\
      -response:\
        *status_code: response status
        *content: response content
   \
*post: create*\
    *return: Dictionary with following keys:\
      a. admin_token -> admin token
      b. response:\
        1. status_code: response status
        2. content: response content    
   \
*put: update*\
    *return: Dictionary with following keys:\
      a. admin_token -> admin token
      b. response:\
        1. status_code: response status
        2. content: response content    
   \  
*delete: erase*\
    *return: Dictionary with following keys:\
      a. admin_token -> admin token
      b. response:\
        1. status_code: response status
        2. content: response content    


### Parameters:
*query_to: Select API endpoint*
  *options:
    1. orders
    2. products
    3. customer
    4. stockItems
    5. categories

### Options:
filter: get options
  1. by_create_date: get orders since certain create-date.
    parameter: filter field: date, string format %Y-%m-%d %H:%M:%S.
  2. by_create_and_update_date: get orders since certain update-date and create date 14 days before.
    parameter: filter field: date, string format %Y-%m-%d %H:%M:%S.
  3. prod_by_sku: get product by sku.
    parameter: sku, string.
  4. by_id: get product by id.
    parameter: id, string.
  5. all_products: fetch all products.
    parameter: None.
  6. prod_stock: get product quantity.
    parameter: sku, string.
  7. by_customer_id: get customer by id.
    parameter: customer id, string.
  8. by_address_id: get customer by address id.
    parameter: address id, string.
  9. by_shipping_id: get customer shipping address by id.
    parameter: shipping id, string.
  10. by_billing_id: get customer billing address by id.
    parameter: billing id, string.

save_json: save results to json file.
pagesize: pagesize for pagination.
data: only for post and put, data in dictionary as stated in magento docs
