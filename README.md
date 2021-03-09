# Python_magento_API
Python interface for using Magento 2.0 Admin APIRest. \
Secrets keys are encrypted with simmetric encryptation in a SQLite database. \
Developed at https://dunacore.cloud/

## Install:
1. clone the repository.
2. Fill `keys.json` in `app/data/keys.json` with your integration keys \
 found in the magento backend ->system ->integration.
4. Navigate to your directory and Run in your terminal: \
     `bash install.sh` (First install pipenv if is not already installed).
5. Now you can delete the keys.json.

## Import:
1. On your script located at the root directory \
      import as --> `from __init__ import APIREST`

## Run:
Follow the examples in request_examples.py \
`pipenv run python request_examples.py`

## Documentation:
[Magento docs](https://magento.redoc.ly/2.4.2-admin/) 
### Methods:
- `get:`
    - return: Dictionary with following keys:
      - results: api response
      - response:
        - status_code: response status
        - content: response content (use for error description)
- `post:`
    - return: Dictionary with following keys:
      - admin_token: admin token
      - response:
        - status_code: response status
        - content: response content (use for error description)   
- `put:`
    - return: Dictionary with following keys:
      - admin_token: admin token
      - response:
        - status_code: response status
        - content: response content (use for error description)   
- `delete:`
    - return: Dictionary with following keys:
      - admin_token: admin token
      - response:
        - status_code: response status
        - content: response content (use for error description)   
 
### Parameters:
- `query_to: Select API endpoint`
  - options:
    - orders
    - products
    - customer
    - stockItems
    - categories

### Options:
- `filter:`
  - by_create_date: get orders since certain create-date.
    - filter field: parameter -> date, string format %Y-%m-%d %H:%M:%S.
  - by_create_and_update_date: get orders since certain update-date and create date 14 days before.
    - filter field: parameter -> date, string format %Y-%m-%d %H:%M:%S.
  - prod_by_sku: get product by sku.
    - filter field: parameter -> sku, string.
  - by_id: get product by id.
    - filter field: parameter -> id, string.
  - all_products: fetch all products.
    - filter field:: None.
  - prod_stock: get product quantity.
    - filter field: parameter -> sku, string.
  - by_customer_id: get customer by id.
    - filter field: parameter -> customer id, string.
  - by_address_id: get customer by address id.
    - filter field: parameter -> address id, string.
  - by_shipping_id: get customer shipping address by id.
    - filter field: parameter -> shipping id, string.
  - by_billing_id: get customer billing address by id.
    - filter field: parameter -> billing id, string.

- `save_json`: optional, save results to json file.
- `pagesize`: optional, pagesize for pagination.
- `data`: only for post and put, data in dictionary as stated in magento docs
