import json
import sqlite3
from models import Subscription, subscription


def get_all_subscriptions():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select 
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on 
        from tag as s
        """)

        dataset = db_cursor.fetchall()
        subscriptions = []

        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id,'], row['created_on'], row['ended_on'])
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
        from subscription s
        where s.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        subscription = Subscription(data['id'], data['follower_id'], data['author_id'], data['created_on'], data['ended_on'])
        subscription.id = data['id']

        return json.dumps(subscription.__dict__)

def create_subscription(tag):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Subscription
        (follower_id, author_id, created_on, ended_on)
        values (?, ?)
        """, (subscription['follower_id'], subscription['author_id'], subscription['created_on'], subscription['ended_on'] ))

        subscription_id = db_cursor.lastrowid

        subscription['id'] = subscription_id

    return json.dumps(subscription)

def delete_subscription(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            DELETE FROM subscription
            where id = ?
        """, (id, ))


def update_subscription(id, updated_subscription):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update Subscription
            Set
                follower_id = ?,
                author_id = ?,
                created_on = ?,
                ended_on = ?
            where id = ?
        """, (
            updated_subscription['follower_id'], ['author_id'], ['created_on'], ['ended_on'],
            id
        ))

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False
