import os
import psycopg2.extras
from psycopg2 import sql

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_DATABASE", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "K94dka")
)

# toto se nazývá dynamická query
student_id = "2"

# Příklady kde nám může někdo do url adresy zadat tyto typy a smazal by nám například data nebo je ukradl
# student_id="1 OR 1=1" # toto je příklad nebezpečného SQL injection
# student_id="1; DROP TABLE student" # toto je příklad ještě nebezpečnějšího SQL injection

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Ukázka nebezpečného použití execute
# ŠPATNĚ!!!!!
# cursor.execute(
#     "SELECT * FROM student WHERE student_id=" + student_id
# )

# Jiné nebezpečné zápisy query
# TAKÉ NEPOUŽÍVAT
# cursor.execute("SELECT * FROM student WHERE student_id=%s" %student_id)
# cursor.execute(f"SELECT * FROM student WHERE student_id={student_id}")
# cursor.execute("SELECT * FROM student WHERE student_id={}".format(student_id))

# Správné zápisy query
# Tuple ošetřuje že nám zde nejde vložit další hodnota, takže třeba OR NĚCO tam nepůjde atp.
cursor.execute("SELECT * FROM student WHERE student_id=%s", (student_id, ))

# Jiný styl tohoto zápisu
# Tvoří literal student_id a následně dictionary který se skládá z literalu,
# takže student_id a následně hodnoty takže proměnné student_id
cursor.execute("SELECT * FROM student WHERE student_id=%(student_id)s", {"student_id": student_id})


# Co když chceme poskytnut jako parametr název tabulky nebo sloupce (použití identifikátoru a literalu)
table = "student"
# cursor.execute(
#     "SELECT * FROM %s WHERE student_id=1", (table,)
# )  # toto nebude fungovat

# Správné použití konstruktoru SQL
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


table = "Test"
select_sql = sql.SQL(
    """
    SELECT * 
    FROM {table}
    """
).format(
    table=sql.Identifier(table),
)
# print(select_sql)
# cursor.execute(select_sql)

students = cursor.fetchall()
print(students)
cursor.close()
conn.close()
