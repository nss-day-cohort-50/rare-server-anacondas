import sqlite3
import json
from models import Post


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id
            a.category_id,
            a.title,
            a.publication_date,
            a.content,
            a.approved
        FROM Post a
        """)

        # Initialize an empty list to hold all Post representations
        Posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an Post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            Post = Post(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])

            location = Location(row['l_id'], row['location_name'], row['location_address'])
            customer = Customer(row['c_id'], row['customer_name'], row['customer_address'])

            Post.location = location.__dict__
            Post.customer = customer.__dict__
            Posts.append(Post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(Posts)

def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id
            a.category_id,
            a.title,
            a.publication_date,
            a.content,
            a.approved
        FROM Post a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an Post instance from the current row
        Post = Post(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(Post.__dict__)


def create_post(new_Post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Post
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_Post['name'], new_Post['breed'],
              new_Post['status'], new_Post['location_id'],
              new_Post['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the Post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_Post['id'] = id


    return json.dumps(new_Post)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Post
        WHERE id = ?
        """, (id, ))


def update_post(id, new_Post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Post
            SET
            id = ?,
            user_id = ?,
            category_id = ?,
            title = ?,
            publication_date = ?,
            content = ?,
            approved = ?
        WHERE id = ?
        """, (new_Post['user_id'], new_Post['category_id'],
              new_Post['title'], new_Post['publication_date'],
              new_Post['content'], new_Post['approved'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
