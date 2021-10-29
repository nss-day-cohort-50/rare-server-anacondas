import sqlite3
import json
from models import Post, post
import posts


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.content
        FROM Posts a
        """)

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['content'])
            posts.append(post.__dict__)

    return json.dumps(posts)

def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.content
        FROM Posts a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['content'])

        return json.dumps(post.__dict__)


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, content )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_post['user_id'],
              new_post['category_id'], new_post['title'],
              new_post['publication_date'], new_post['content'] ))

        id = db_cursor.lastrowid

        new_post['id'] = id


    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))


def update_post(id, new_Post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
            id = ?,
            user_id = ?,
            category_id = ?,
            title = ?,
            publication_date = ?,
            content = ?

        WHERE id = ?
        """, (new_Post['user_id'], new_Post['category_id'],
              new_Post['title'], new_Post['publication_date'],
              new_Post['content'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def get_post_by_user(id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.content
        FROM Posts a
        WHERE a.user_id = ?
        """, (id,))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'] , row['publication_date'], row['content'])
            posts.append(post.__dict__)

    return json.dumps(posts)


