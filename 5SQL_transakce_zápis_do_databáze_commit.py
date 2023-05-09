import psycopg2.extras
import os

# from utils import consts


# Pro přehlednost je lepší použít vyjmenování sloupců než hvězdičku pro jiné programátory
def get_cars(curr, conn):
    curr.execute("SELECT * FROM car;")
    results = curr.fetchall()
    return results


def insert_car(curr, conn, brand):
    curr.execute("INSERT INTO car (brand) VALUES (%s)", (brand,))


if __name__ == "__main__":
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_DATABASE", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "K94dka")
    )
    # conn.commit()    # toto ukončí jednu transakci, pak už by to dále zase nefungovalo, autocommit funguje stále dokud není False
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cars = get_cars(cursor, conn)
    print(cars)
    insert_car(cursor, conn, 'Audi')
    cars = get_cars(cursor, conn)
    print(cars)
    cursor.close()
    conn.close()  # automaticky udělá rollback pokud zde není commit

    # Ak nechceme stale commitovat vsetky query mozeme nastavit autocommit, teraz je kazdy execute jedna transakcia
    # conn.autocommit = True
