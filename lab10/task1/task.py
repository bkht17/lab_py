import psycopg2
import csv
from configparser import ConfigParser

def read_csv(path):
    with open(path, 'r') as file:
        return [row for row in csv.DictReader(file)]

def load_config(filename='lab10/task1/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

config = load_config()
conn = psycopg2.connect(**config)
cur = conn.cursor()

# Creating table
cur.execute("""CREATE TABLE IF NOT EXISTS phonebook(
    user_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(11) NOT NULL,
    UNIQUE(phone_number)
);
""")

def insert_data(user_name, phone_number):
    sql = """INSERT INTO phonebook(user_name, phone_number)
             VALUES(%s, %s);"""
    
    try:
        # execute the INSERT statement
        cur.execute(sql, (user_name, phone_number))

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def upload_csv(csv_file):
    columns = ', '.join(csv_file[0].keys())
    placeholders = ', '.join(['%s'] * len(csv_file[0]))
    insert_query = f"INSERT INTO phonebook ({columns}) VALUES ({placeholders})"

    # Execute the INSERT statement for each row of data
    for row in csv_file:
        cur.execute(insert_query, list(row.values()))

    conn.commit()
    cur.close()

def update_data(user_name, phone_number):
    sql = """ UPDATE phonebook
                SET user_name = %s
                WHERE phone_number = %s"""
    
    updated_row_count = 0
    
    try:        
            # execute the UPDATE statement
            cur.execute(sql, (user_name, phone_number))
            updated_row_count = cur.rowcount

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return updated_row_count
    
def get_by_alphabet():
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY LOWER(user_name)")
                rows = cur.fetchall()

                for row in rows:
                    print(f'User: {row[0]} || Phone: {row[1]}')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    

def delete_number(user_name):
    """ Delete part by user_name """

    rows_deleted  = 0
    sql = 'DELETE FROM phonebook WHERE user_name = %s'

    try:
        # execute the UPDATE statement
        cur.execute(sql, (user_name,))
        rows_deleted = cur.rowcount

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return rows_deleted
    

csv = read_csv("lab10_updated/task1/another_data.csv")
#upload_csv(csv)
#insert_data(str(input()), str(input()))
#update_data(str(input()), str(input()))
#get_by_alphabet()
delete_number(str(input()))
    
