from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from typing import Optional
import sqlite3
from task import startup_db
app=FastAPI()
@app.on_event("startup")
def starting_task():
    startup_db()
@app.get("/")
def read_route():
    return {"name":"Task API","version":1.1,"endpoint":["/tasks"]}
@app.get("/health")
def health_route():
    return {"status":"ok"}
@app.get("/tasks")
def all_tasks():
    conn=sqlite3.connect("tasks.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks" )
    rows=cursor.fetchall()
    all_task=[dict(row) for row in rows]
    conn.close()
    return all_task
@app.get("/tasks/{task_id}")
def single_task(task_id: int):
    conn=sqlite3.connect("tasks.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    single=cursor.fetchone()
    if single is None:
        conn.close()
        raise HTTPException(status_code=404,detail="task not found")    
    conn.close()
    return dict(single)    
class taskcreate(BaseModel):
    title:str
@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task_title(task_title:taskcreate):
    if not task_title.title.strip():
        raise HTTPException(status_code=400,detail="Title cannot be empty...")
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)",(task_title.title.strip(),False))
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    return {"id":new_id, "title":task_title.title.strip(), "done":False}
class Update_task(BaseModel):
    title:Optional[str]=None
    done:Optional[bool]=None
@app.put("/tasks/{task_id}")
def update_task(task_id:int,task_data:Update_task):
    conn=sqlite3.connect("tasks.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    check=cursor.fetchone()
    if check is None:
        conn.close()
        raise HTTPException(status_code=404,detail="Task not found..")
    current_task=dict(check)
    update_title=current_task["title"]
    update_done=current_task["done"]
    if task_data.title is not None:
            if not task_data.title.strip():
                conn.close()
                raise HTTPException(status_code=400,detail="Title cannot be empty..")
            update_title=task_data.title.strip()
    if task_data.done is not None:
            update_done=task_data.done
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",(update_title, update_done,task_id))        
    conn.commit()
    conn.close()
    return {"id":task_id, "title":update_title,"done":update_done}
@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int):
    conn=sqlite3.connect("tasks.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    delete=cursor.fetchone()
    if delete is None:
         conn.close()
         raise HTTPException(status_code=404,detail="Task not found..")
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    conn.commit()
    conn.close()
    return     