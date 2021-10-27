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
            t.first_name,
            t.last_name,
            t.email,
            t.username,
            t.password
        from Users as t
        """)

        dataset = db_cursor.fetchall()
        users = []

        for row in dataset:
            user = User(row['id'], row['bio'],row['created_on'], row['active'], row['first_name'],row['last_name'], row['email'], row['username'], row['password'])
            users.append(user.__dict__)
    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            t.id,
            t.bio,
            t.created_on,
            t.active,
            t.first_name,
            t.last_name,
            t.email,
            t.username,
            t.password
        from Users t
        where t.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['bio'], data['created_on'], data['active'], data['first_name'], data['last_name'], data['email'], data['username'], data['password'])

        return json.dumps(user.__dict__)

def create_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
        ( first_name, last_name, username )
        VALUES ( ?, ?, ? );
        """, ( new_user['first_name'],new_user['last_name'], new_user['username'], ))
        id = db_cursor.lastrowid
        new_user['id'] = id

    return json.dumps(new_user)

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
            UPDATE Users
            SET
                bio = ?,
                email = ?
            WHERE id = ?
        """, (updated_user['bio'], updated_user['email'],
            id, ))

        was_updated = db_cursor.rowcount

        if was_updated == 0:
            return False
        else:
            return True

def get_users_by_search(text):
    users = json.loads(get_all_users())
    users = [user for user in users if text.lower() in user['username'].lower()]
    return json.dumps(users)

def check_auth(email):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
        id,
        email
        FROM Users
        WHERE email = ?
        """, (email["email"], ))

        data = db_cursor.fetchone()
        if data: 
            response = {"valid": True, "token": data["id"]}
        else: 
            response = {"valid": False }
        
        return json.dumps(response)

def register_user(new_register):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
        ( first_name, last_name, email, password )
        VALUES ( ?, ?, ?, ? );
        """, ( new_register['first_name'],new_register['last_name'], new_register['email'], new_register['password'], ))
        id = db_cursor.lastrowid
        new_register["id"] = id

        if id:
            response = {"valid": True, "token": id}
        else:
            response = {"valid": False}

    return json.dumps(response)