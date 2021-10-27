import sqlite3
import json
from models import Reaction

def get_all_reactions():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM Reactions r
        """)

        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            reaction = Reaction(row['id'], row['label'], row['image_url'])
            reactions.append(reaction.__dict__)

    return json.dumps(reactions)



# Function with a single parameter
def get_single_reaction(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM Reactions r
        WHERE r.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        
        reaction = Reaction(data['id'], data['label'], data['image_url'])

        return json.dumps(reaction.__dict__)



def create_reaction(new_reaction):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Reactions
            ( label, image_url )
        VALUES
            ( ?, ? ); 
        """, (new_reaction['label'], new_reaction['image_url'], ))

        id = db_cursor.lastrowid

        new_reaction['id'] = id


    return json.dumps(new_reaction)


def update_reaction(id, new_reaction):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Category
            SET
                label = ?,
                image_url = ?
        WHERE id = ?
        """, (new_reaction['label'], new_reaction['image_url'], id, ))


        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_reaction(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM reaction
        WHERE id = ?
        """, (id, ))