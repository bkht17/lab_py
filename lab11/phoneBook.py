import psycopg2
import csv
from configparser import ConfigParser

def read_csv(path):
    with open(path, 'r') as file:
        return [row for row in csv.DictReader(file)]

def load_config(filename='database.ini', section='postgresql'):
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
cur.execute("""CREATE TABLE IF NOT EXISTS PhoneBook(
    user_name VARCHAR(255),
    phone_number VARCHAR(255)
);
""")

def upload_csv_to_postgres(connection,csv_file, table_name):
    cursor = connection.cursor()
    columns = ', '.join(csv_file[0].keys())
    placeholders = ', '.join(['%s'] * len(csv_file[0]))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Execute the INSERT statement for each row of data
    for row in csv_file:
        cursor.execute(insert_query, list(row.values()))

    connection.commit()
    cursor.close()


def insert_phonebook_entry(user_name, phone_number):
    """ Insert a new entry into the phonebook table """
    sql = """INSERT INTO phonebook(user_name, phone_number)
             VALUES(%s, %s);"""
    
    try:
        # execute the INSERT statement
        cur.execute(sql, (user_name, phone_number))

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update(phone_number, user_name):
    """ Update  phone number based on the user_name """
    
    updated_row_count = 0

    sql = """ UPDATE Phonebook
                SET phone_number = %s
                WHERE user_name = %s"""
    
    try:
                
        # execute the UPDATE statement
        cur.execute(sql, (phone_number, user_name))
        updated_row_count = cur.rowcount

        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return updated_row_count

def get_data():
    """ Retrieve data from the Phonebook table """
    try:
        
        cur.execute("SELECT user_name, phone_number FROM Phonebook ORDER BY user_name")
        rows = cur.fetchall()

        print("The number of phonenumbers: ", cur.rowcount)
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_number(user_name):
    """ Delete part by user_name """

    rows_deleted  = 0
    sql = 'DELETE FROM Phonebook WHERE user_name = %s'

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

def get_data_part_of_name_and_lastname(partofname_pattern, lastname_pattern):
    """ Retrieve data from the Phonebook table based on part of name or lastname """
    try:
        
        cur.execute("SELECT user_name, phone_number FROM Phonebook WHERE user_name LIKE %s OR user_name LIKE %s ORDER BY user_name",
        (f'%{partofname_pattern}%', f'% {lastname_pattern}'))#1st seeks rows that have users  that contain part of name,2nd seeks for the rows that ends with some string
        rows = cur.fetchall()

        print("The number of phonenumbers: ", cur.rowcount)
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_data_phonenum(phone_number_pattern):
    """ Retrieve data from the Phonebook table based on phonenumber"""
    try:
        
        cur.execute("SELECT user_name, phone_number FROM Phonebook WHERE phone_number LIKE %s ORDER BY user_name",
                    (f'%{phone_number_pattern}%',))#contains some digits in phonenum
        rows = cur.fetchall()

        print("The number of phonenumbers: ", cur.rowcount)
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_data_by_exact_phonenumber(phone_number):
    """ Retrieve data from the Phonebook table based on exact phone number match """
    try:

        cur.execute("SELECT user_name, phone_number FROM Phonebook WHERE phone_number = %s ORDER BY user_name",
                    (phone_number,))
        
        rows = cur.fetchall()

        print("The number of phonenumbers: ", cur.rowcount)
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
"""
CREATE OR REPLACE PROCEDURE insert_or_update_user(IN p_user_name VARCHAR, IN p_phone_number VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE user_name = p_user_name) THEN
        UPDATE phonebook SET phone_number = p_phone_number WHERE user_name = p_user_name;
        RAISE NOTICE 'User %s updated with phone number %s', p_user_name, p_phone_number;
    ELSE

        INSERT INTO phonebook(user_name, phone_number) VALUES (p_user_name, p_phone_number);
        RAISE NOTICE 'New user %s inserted with phone number %s', p_user_name, p_phone_number;
    END IF;
END;
$$;
"""
def insert_or_update(user_name, phone_number):
    """ Inserting new user and phone, updating if it exists"""
    
    try:
        # call a stored procedure
        cur.execute('CALL insert_or_update_user(%s,%s)', (user_name, phone_number))

        # commit the transaction
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

"""
CREATE OR REPLACE PROCEDURE insert_many_users(users_data TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    user_entry TEXT;
    u_user_name VARCHAR;
    u_phone_number VARCHAR;
BEGIN
    FOREACH user_entry IN ARRAY users_data
    LOOP
        -- split user entry into name and phone number
        u_user_name := split_part(user_entry, ',', 1);
        u_phone_number := split_part(user_entry, ',', 2);

        -- check if phone number is valid (e.g., correct length, numeric)
        IF LENGTH(u_phone_number) = 12 THEN
            -- check if the user already exists
            IF EXISTS (SELECT 1 FROM phonebook WHERE user_name = u_user_name) THEN
                -- if user exists, update the phone number
                UPDATE phonebook SET phone_number = u_phone_number WHERE user_name = u_user_name;
            ELSE
                -- if user does not exist, insert a new user
                INSERT INTO phonebook(user_name, phone_number) VALUES (u_user_name, u_phone_number);
            END IF;
        END IF;
    END LOOP;
END;
$$;
"""
#Inserting many users from list
def insert_many_users(users_data):
    try:
        users_data_tuple = tuple(users_data)
        # call the stored procedure
        cur.execute('CALL insert_many_users(%s)', (users_data,))

        # commit the transaction
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query_with_pagination(limit, offset):
    """ Retrieve data from the Phonebook table """
    try:
        
        cur.execute("SELECT user_name, phone_number FROM Phonebook ORDER BY user_name LIMIT %s OFFSET %s ", (limit, offset))
        rows = cur.fetchall()

        print("The number of phonenumbers: ", cur.rowcount)
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

"""
CREATE OR REPLACE PROCEDURE delete_user_phone(IN p_name_or_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    -- check if the entry matches the username pattern
    IF p_name_or_phone ~ '^[A-Za-z]+$' THEN
        DELETE FROM PhoneBook WHERE user_name = p_name_or_phone;
        RAISE NOTICE 'Data with username %s deleted successfully', p_name_or_phone;
    -- check if the entry matches the phone number pattern
    ELSIF p_name_or_phone ~ '^\+?[0-9]+$' THEN
        DELETE FROM PhoneBook WHERE phone_number = p_name_or_phone;
        RAISE NOTICE 'Data with phone number %s deleted successfully', p_name_or_phone;
    ELSE
        RAISE EXCEPTION 'Invalid entry provided';
    END IF;
END;
$$;
"""

def delete_data(name_or_phone):
    try:
        # call the stored procedure        
        cur.execute('CALL delete_user_phone(%s)', (name_or_phone,))

        # commit the transaction
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)




# Read data from CSV file
#datacsv = read_csv("pb.csv")

# Upload data to PostgreSQL
#upload_csv_to_postgres(datacsv, 'PhoneBook')

# Insert a new entry into the phonebook table
#insert_phonebook_entry(str(input()), str(input()))

# Update user name based on phone number
#update(str(input()), str(input()))


# Delete entry from the Phonebook table 
#deleted_rows = delete_number(str(input()))
#print('The number of deleted rows: ', deleted_rows)


# Retrieve data from the Phonebook table based on part of name or lastname 
#get_data_part_of_name_and_lastname(str(input()),str(input()))

# Retrieve data from the Phonebook table based on phone number
#get_data_phonenum(str(input()))

#get_data_by_exact_phonenumber(str(input()))

#Inserting or updating data using stored procedure
#insert_or_update(str(input()), str(input()))

# Inserting or updating many users using stored procedure
#users_data = ['John Boe,+77789563482', 'Fermen Clenchar,+77475963768', 'Char Gordon,+77071235326']
#insert_many_users(users_data)

#Querying data with limit and offset
#query_with_pagination(int(input()), int(input()))

#Deleting user based on username and phonebook
#delete_data(str(input()))

#get_data()
