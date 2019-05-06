import psycopg2
from relational_database.config import DATABASE

conn = psycopg2.connect(**DATABASE)

with conn.cursor() as cursor:
    cursor.execute("SELECT supplierid FROM suppliers WHERE(country LIKE 'Sweden%');")
    supp_id_country = cursor.fetchall()

    print(supp_id_country)
    ids = [x[0] for x in supp_id_country]

    print(ids)
    cursor.execute("SELECT productname FROM products WHERE supplierid = ANY(%s);", (ids,))
    res = cursor.fetchall()
    print(res)
    re1 = [tuple((x[0])) for x in res]
    print(re1)


with conn.cursor() as cursor:

    cursor.execute("""SELECT customername, customers.address, customers.country as customercountry, suppliers.country, suppliername 
        FROM customers FULL JOIN suppliers ON customers.country = suppliers.country
        ORDER BY customers.country;
    """)

    print(cursor.fetchall())