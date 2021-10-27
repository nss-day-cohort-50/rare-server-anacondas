import json
import sqlite3
from models import Subscription


def get_all_subscriptions():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on 
        FROM Subscriptions s
        """)
 
        subscriptions = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id,'], row['created_on'], row['ended_on'] )
            subscriptions.append(subscription.__dict__)
    return json.dumps(subscriptions)

def get_single_subscription(id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        from Subscriptions s
        where s.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        subscription = Subscription(data['id'], data['follower_id'], data['author_id'], data['created_on'], data['ended_on'])
        subscription.id = data['id']

        return json.dumps(subscription.__dict__)

def create_subscription(new_subscription):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Subscriptions
        (follower_id, author_id, created_on, ended_on)
        values (?, ?, ?, ?)
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on'], new_subscription['ended_on'] ))

        subscription_id = db_cursor.lastrowid

        new_subscription['id'] = subscription_id

    return json.dumps(new_subscription)

def delete_subscription(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            DELETE FROM Subscriptions
            where id = ?
        """, (id, ))


def update_subscription(id, updated_subscription):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update Subscriptions
            Set
                follower_id = ?,
                author_id = ?,
                created_on = ?,
                ended_on = ?
            where id = ?
        """, (
            updated_subscription['follower_id'], updated_subscription['author_id'], updated_subscription['created_on'], updated_subscription['ended_on'],
            id
        ))

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False
