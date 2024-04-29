from flask import Flask, render_template, request
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

def create_connection():
    try:
        connection = psycopg2.connect(
            user="admin",
            password="admin",
            host="postgres",
            port="5432",
            database="db"
        )
        if connection:
            print("db connected")
            return connection
        else:
            print("Error: Unable to establish connection to PostgreSQL")
            return None
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS public.test (
                id SERIAL PRIMARY KEY,
                A INTEGER NOT NULL,
                B INTEGER NOT NULL,
                Sum INTEGER
            )
        '''
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error while creating table: {e}")

def insert_data(connection, a, b, total):
    try:
        cursor = connection.cursor()
        insert_query = '''
            INSERT INTO public.test (A, B, Sum)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(insert_query, (a, b, total))
    except Error as e:
        print(f"Error while inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a = int(request.form['a'])
        b = int(request.form['b'])
        total = a + b

        connection = create_connection()
        if connection:
            insert_data(connection, a, b, total)
            connection.close()

        return f"Data inserted successfully. Sum: {total}"
    return render_template('index.html')

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_table(connection)
        connection.close()
    app.run(debug=True, host='0.0.0.0', port=9000)