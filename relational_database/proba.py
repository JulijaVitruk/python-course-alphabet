import psycopg2
from relational_database.config import DATABASE

conn = psycopg2.connect(**DATABASE)

with conn.cursor() as cursor:

    cursor.execute("""
        SELECT customername, customers.address, customers.country, suppliers.country, suppliername 
        FROM customers FULL JOIN suppliers ON customers.country = suppliers.country
        ORDER BY customers.country;
    """)
    print(len(cursor.fetchall()))
