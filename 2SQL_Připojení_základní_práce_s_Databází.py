import os
import psycopg2.extras

# Napojíme se přes proměnnou která je definovaná v počítači kde databáze běží,
# pokud neexistuje, tak to přeskočí a použije údaje za čárkou
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_DATABASE", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "K94dka")
)

# Druhý styl připojení
# conn=psycopg2.connect(
#     os.getenv("POSTGRES_CONNECTION_STRING", "dbname=postgres user=postgres password=K94dka host=localhost port=5432")
# )

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute(
    "SELECT * FROM student;"
)
students = cursor.fetchall()
target = students[0]
print(f"Jméno: {target['username']} a rok narození: {target['year_born']}")
cursor.close()
conn.close()
