import json
import sqlite3
from models import User


def get_all_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select 
            t.id,
            t.bio,
            t.created_on,
            t.active,
            t.user_id,
            t.first_name,
            t.last_name,
            t.email,
            t.username,
            t.password
        from user as t
        """)

        dataset = db_cursor.fetchall()
        users = []

        for row in dataset:
            user = User(row['id'], row['bio'],row['created_on'], row['active'],row['user_id'], row['first_name'],row['last_name'], row['email'], row['username'], row['password'])
            users.append(user.__dict__)
    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            t.id,
            t.username
        from user t
        where t.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['bio'],data['created_on'], data['active'],data['user_id'], data['first_name'],data['last_name'], data['email'], data['username'], data['password'])

        return json.dumps(user.__dict__)

def create_user(user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into user
        (username, first_name, last_name)
        values (?, ?, ?)
        """, (user['username'], user['first_name'], user[last_name]))

        user_id = db_cursor.lastrowid

        user['id'] = user_id

    return json.dumps(user)

def delete_user(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            DELETE FROM user
            where id = ?
        """, (id, ))


def update_user(id, updated_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update User
            Set
                username = ?,
            where id = ?
        """, (
            updated_user['username'],
            id
        ))

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False

def get_users_by_search(text):
    users = json.loads(get_all_users())
    users = [user for user in users if text.lower() in user['username'].lower()]
    return json.dumps(users)