import os
import psycopg2.extras
from psycopg2 import sql

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_DATABASE", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "K94dka")
)
student_id = "1"
table = "student"
# Z tuple listů mi udělá list listů, takže lze upravovat
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# Výběr tabulky, pokud jich je víc a chtěl bych to mít přes proměnnou
# Je to také save a zabezpečené proti injection
select_sql = sql.SQL(
    """
    SELECT * 
    FROM {table}
    WHERE student_id={student_id}
    """
).format(
    table=sql.Identifier(table),
    student_id=sql.Literal(student_id)
)
cursor.execute(select_sql)
# Uloží do proměnné vytažená data
vypis = cursor.fetchall()
print(vypis)
cursor.close()
conn.close()
