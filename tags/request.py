import json
import sqlite3
from models import Tag


def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select 
            t.id,
            t.label
        from tag as t
        """)

        dataset = db_cursor.fetchall()
        tags = []

        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)
    return json.dumps(tags)

def get_single_tag(id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            t.id,
            t.label
        from tag t
        where t.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['label'])
        tag.id = data['id']

        return json.dumps(tag.__dict__)

def create_tag(tag):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Tag
        (name, label)
        values (?, ?)
        """, (tag['name'], tag['label']))

        tag_id = db_cursor.lastrowid

        tag['id'] = tag_id

    return json.dumps(tag)

def delete_tag(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            DELETE FROM tag
            where id = ?
        """, (id, ))


def update_tag(id, updated_tag):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update Tag
            Set
                label = ?,
            where id = ?
        """, (
            updated_tag['label'],
            id
        ))

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False

def get_tags_by_search(text):
    tags = json.loads(get_all_tags())
    tags = [tag for tag in tags if text.lower() in tag['label'].lower()]
    return json.dumps(tags)