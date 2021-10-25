import sqlite3
import json
from models import Category

def get_all_categories():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name
        FROM Category c
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            category = Category(row['id'], row['label'])
            
            categories.append(category.__dict__)

    return json.dumps(categories)



# Function with a single parameter
def get_single_category(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.name
        FROM Category c
        """, ( id, ))

        data = db_cursor.fetchone()
        
        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)



def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Category
            ( label )
        VALUES
            ( ? ); 
        """, (new_category['label'] ))

        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_category['id'] = id


    return json.dumps(new_category)


def update_category(id, new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Category
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))


        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_category(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM category
        WHERE id = ?
        """, (id, ))