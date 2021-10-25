import json
import sqlite3
from models import Animal
from models.location import Location

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers"
    },
    {
        "id": 2,
        "name": "Gypsy"
    }
]
# const animals = []

def get_all_animals():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from animal as a
        """)

        dataset = db_cursor.fetchall()
        animals = []

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'])
            animals.append(animal.__dict__)
    return json.dumps(animals)

def get_single_animal(id):
    with sqlite3.connect('./kennel.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address,
            c.name customer_name
        from animal a
        join location l on l.id = a.location_id
        join customer c on c.id = a.customer_id
        where a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        animal = Animal(data['id'], data['name'], data['breed'], data['status'], data['location_id'])
        location = Location(data['location_id'], data['location_name'], data['address'])
        animal.customer_name = data['customer_name']
        # animal.customer = {
        #     'name': data['customer_name']
        # }
        animal.location = location.__dict__
        return json.dumps(animal.__dict__)

def create_animal(animal):
    with sqlite3.connect('./kennel.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Animal
        (name, breed, status, location_id, customer_id)
        values (?, ?, ?, ?, ?)
        """, (animal['name'], animal['breed'], animal['status'], animal['location_id'], animal['customer_id']))

        animal_id = db_cursor.lastrowid

        animal['id'] = animal_id

    return json.dumps(animal)
def delete_animal(id):
    with sqlite3.connect('./kennel.db') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            DELETE FROM animal
            where id = ?
        """, (id, ))
    # conn = sqlite3.connect('./kennel.db')
    # # execute sql
    # conn.close()

def update_animal(id, updated_animal):
    with sqlite3.connect('./kennel.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            Update Animal
            Set
                name = ?,
                breed = ?,
                location_id = ?,
                status = ?,
                customer_id = ?
            where id = ?
        """, (
            updated_animal['name'],
            updated_animal['breed'],
            updated_animal['location_id'],
            updated_animal['status'],
            updated_animal['customer_id'],
            id
        ))

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False

def get_animals_by_search(text):
    animals = json.loads(get_all_animals())
    animals = [animal for animal in animals if text.lower() in animal['name'].lower()]
    return json.dumps(animals)