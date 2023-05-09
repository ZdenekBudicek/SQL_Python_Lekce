import os
import psycopg2.extras

# Contextový manager nam umí zjednodušit práci s commitováním transakcí.
# Zabalením proměnné s connection do kontextového managera můžeme na konci managera forcnout commit
# POZOR na chyby v rámci těla contextového managera

if __name__ == '__main__':
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_DATABASE", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "K94dka")
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO student (name, surname) VALUES (%s, %s)", ('Zdeněk', 'Blablaf'))

    # Ukončení bloku contextového managera pro connection odpálí commit
    # Jeslti nastane chyba před ukončením bloku máme tu problém.

    # Zjednodušený zápis v jendom řádku toho nad tímto
    # Kdybych nedal pod zachycení erroru rollback, hodnota by se vložila i když tam je error.
    with conn, conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO student (name, surname) VALUES (%s, %s)", ('test_student', 'test_student'))
            raise Exception("Error")
        except Exception as e:
            print("Error during execution")
            conn.rollback()

    conn.close()  # Nezapomenout vždy ukončit connection
    print(conn.closed)  # Jestli si nejsme jistý pomocí parametru closed umíme zjistit jeslti je connection ukončený
