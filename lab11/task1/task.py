import psycopg2
import csv
from configparser import ConfigParser

def read_csv(path):
    with open(path, 'r') as file:
        return [row for row in csv.DictReader(file)]

def load_config(filename='lab11/task1/database.ini', section='postgresql'):
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
    
def delete_number_by_num(phone_number):
    """ Delete part by user_name """

    rows_deleted  = 0
    sql = 'DELETE FROM phonebook WHERE phone_number = %s'

    try:
        # execute the UPDATE statement
        cur.execute(sql, (phone_number,))
        rows_deleted = cur.rowcount

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return rows_deleted
    
    
def update_or_insert_user(user_name, phone_number):
    try:
        # Попытка вставить новую запись, при конфликте по номеру телефона происходит обновление имени
        sql = """
            INSERT INTO phonebook(user_name, phone_number)
            VALUES (%s, %s)
            ON CONFLICT (phone_number) DO UPDATE
            SET user_name = EXCLUDED.user_name
            RETURNING phone_number
        """
        cur.execute(sql, (user_name, phone_number))
        conn.commit()

        new_phone_number = cur.fetchone()[0]
        return new_phone_number

    except Exception as e:
        print(f"Error occurred while updating or inserting user: {e}")
        conn.rollback() 
        return None
    
def insert_many_users(user_data_list):
    sql = """
        INSERT INTO phonebook(user_name, phone_number)
        VALUES (%s, %s)
        ON CONFLICT (phone_number) DO UPDATE
        SET user_name = EXCLUDED.user_name
    """
    try:
        # Execute the insert for each user in the list
        with conn.cursor() as cur:
            cur.executemany(sql, user_data_list)
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(user_data_list)} users.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error occurred while inserting users: {error}")
    
def handle_user_update():
    username = input("Enter username: ")
    new_phone_number = input("Enter phone number: ")

    try:
        # Проверяем существует ли пользователь
        cur.execute("SELECT phone_number FROM phonebook WHERE user_name = %s", (username,))
        user_data = cur.fetchone()

        if user_data:
            # Если пользователь существует, обновляем его запись
            updated_phone_number = update_or_insert_user(username, new_phone_number)
            if updated_phone_number:
                print(f"User '{username}' updated with new phone number: {updated_phone_number}")
            else:
                print(f"Failed to update user '{username}' with new phone number.")
        else:
            # Если пользователь не существует, добавляем нового пользователя
            inserted_phone_number = update_or_insert_user(username, new_phone_number)
            if inserted_phone_number:
                print(f"New user '{username}' added with phone number: {inserted_phone_number}")
            else:
                print(f"Failed to add new user '{username}'.")

    except Exception as e:
        print(f"Error occurred: {e}")

def search(pattern):
        sql = """
        SELECT user_name, phone_number FROM phonebook
        WHERE LOWER(user_name) LIKE LOWER(%s)
        OR LOWER(phone_number) LIKE LOWER(%s)
        """
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    search_pattern = f"%{pattern}%"
                    cur.execute(sql, (search_pattern, search_pattern))
                    results = cur.fetchall()
                    return results
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error searching for contacts: {error}")
            return []

def get_by_limit_and_offset(limit, offset):
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook LIMIT %s OFFSET %s",(limit, offset))
                rows = cur.fetchall()

                for row in rows:
                    print(f'User: {row[0]} || Phone: {row[1]}')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    

csv = read_csv("lab11/task1/another_data.csv")
#upload_csv(csv)
#insert_data(str(input()), str(input()))
#update_data(str(input()), str(input()))
#get_by_alphabet()
#delete_number(str(input()))
#print(search(input()))
#handle_user_update()
#insert_many_users([('Daur', '87777777777'), ('Hello', '87777777778')])
#get_by_limit_and_offset(2, 1)
    
