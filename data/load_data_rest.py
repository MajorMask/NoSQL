import requests
import csv
import json

HBASE_REST_URL = "http://hbase:8085"
TABLE_NAME = "customers"
COLUMN_FAMILY = "info"

def create_table_if_not_exists():
    # This is a simplified example. You might need a more robust check.
    try:
        response = requests.get(f"{HBASE_REST_URL}/{TABLE_NAME}/exists")
        response.raise_for_status()
        if response.status_code == 404:
            # Table doesn't exist, create it
            headers = {'Content-Type': 'application/xml'}
            data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <TableSchema name="{TABLE_NAME}">
              <ColumnSchema name="{COLUMN_FAMILY}"/>
            </TableSchema>"""
            response = requests.post(f"{HBASE_REST_URL}/{TABLE_NAME}/schema", headers=headers, data=data)
            response.raise_for_status()
            print(f"✅ Table '{TABLE_NAME}' created.")
        else:
            print(f"✅ Table '{TABLE_NAME}' already exists.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking/creating table: {e}")

def load_customers(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customer_id = row['customer_id']
            city = row['customer_city']
            state = row['customer_state']

            data = {
                "Row": [
                    {
                        "key": customer_id.encode('utf-8').hex(),
                        "Cell": [
                            {"column": f"{COLUMN_FAMILY}:city".encode('utf-8').hex(), "$": city.encode('utf-8').hex()},
                            {"column": f"{COLUMN_FAMILY}:state".encode('utf-8').hex(), "$": state.encode('utf-8').hex()}
                        ]
                    }
                ]
            }
            headers = {'Content-Type': 'application/json'}
            url = f"{HBASE_REST_URL}/{TABLE_NAME}/{customer_id}"
            try:
                response = requests.put(url, headers=headers, data=json.dumps(data))
                response.raise_for_status()
                print(f"✅ Put customer: {customer_id}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Error putting customer {customer_id}: {e}")
                if response is not None:
                    print(f"   Response status code: {response.status_code}")
                    print(f"   Response text: {response.text}")

if __name__ == "__main__":
    create_table_if_not_exists()
    load_customers("customers.csv")
    print("✅ Customer data loading complete (using REST API).")
