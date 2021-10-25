import sqlite3
import json
from models import Category


def get_all_categories():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn: #this returns a connection

        # Just use these. It's a Black Box.
        #must run cursor before you can execute
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() #creates an environment to execute the code

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Category c
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            
            # Create a Location instance for the current row
            # Class name, parentheses, and then parameters being passed in
            location = Location(row['location_id'], row['location_name'], row['location_address'])

            customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])
            
            #Add the dictionary representation of the location to the animal since we are dumping into JSON
            animal.location = location.__dict__ #adding location to animal as a new property
            animal.customer = customer.__dict__
            
            # Add the dictrionary representation of the animal to the list
            animals.append(animal.__dict__) #making into a dictionary as appending

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)



# Function with a single parameter
def get_single_category(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address
        FROM animal a
        JOIN location l on l.id = a.location_id
        JOIN customer c on c.id = a.customer_id
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        location = Location(data['location_id'], data['location_name'], data['location_address'])
        customer = Customer(data['customer_id'], data['customer_name'], data['customer_address'])

        animal.location = location.__dict__
        animal.customer = customer.__dict__

        return json.dumps(animal.__dict__)



def create_category(new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?); 
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))
            # Dictionary so use [] notation
        # Need as many ? as properties that you are going to be passing
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)


def update_catgeory(id, new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_category(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))