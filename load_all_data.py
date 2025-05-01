import happybase
import csv

# Connect to HBase Thrift server running in Docker
conn = happybase.Connection('hbase', port=9090)

# Define HBase table bindings
tables = {
    'customers': conn.table('customers'),
    'orders': conn.table('orders'),
    'order_items': conn.table('order_items'),
    'products': conn.table('products'),
    'sellers': conn.table('sellers')
}

# Load customers.csv
with open('customers.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tables['customers'].put(row['customer_id'], {
            b'info:city': row['customer_city'].encode(),
            b'info:state': row['customer_state'].encode()
        })

# Load orders.csv
with open('orders.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tables['orders'].put(row['order_id'], {
            b'meta:customer_id': row['customer_id'].encode(),
            b'meta:status': row['order_status'].encode(),
            b'meta:purchase_date': row['order_purchase_timestamp'].encode()
        })

# Load order_items.csv
with open('order_items.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tables['order_items'].put(row['order_item_id'], {
            b'details:order_id': row['order_id'].encode(),
            b'details:product_id': row['product_id'].encode(),
            b'details:seller_id': row['seller_id'].encode(),
            b'details:price': row['price'].encode(),
            b'details:freight_value': row['freight_value'].encode()
        })

# Load products.csv
with open('products.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tables['products'].put(row['product_id'], {
            b'info:category': row['product_category_name'].encode(),
            b'info:length_cm': row['product_length_cm'].encode(),
            b'info:weight_g': row['product_weight_g'].encode()
        })

# Load sellers.csv
with open('sellers.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tables['sellers'].put(row['seller_id'], {
            b'info:city': row['seller_city'].encode(),
            b'info:state': row['seller_state'].encode()
        })

print(" All CSV files successfully imported into HBase.")

