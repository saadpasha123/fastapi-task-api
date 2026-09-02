import sqlite3
def startup_db():
    conn=sqlite3.connect("tasks.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0 
)
""")
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count=cursor.fetchone()[0]
    if count==0:
       initial_task=[
          ("Python",1),
          ("Java",1),
          ("Machine Learning",0)
       ]
       cursor.executemany("INSERT INTO tasks (title,done) VALUES (?,?)",initial_task)
       print("Initial tasks inserted into the database.")
    else:
       print("Database already has tasks. No initial data inserted.")
    conn.commit()    
    conn.close()