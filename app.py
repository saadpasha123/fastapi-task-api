from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from typing import Optional
app=FastAPI()
tasks=[
    {"id":12,"title":"Python","done":True},
    {"id":1,"title":"Java","done":True},
    {"id":3,"title":"Machine Learning","done":False}
]
@app.get("/")
def read_route():
    return {"name":"Task API","version":1.1,"endpoint":["/tasks"]}
@app.get("/health")
def health_route():
    return {"status":"ok"}
@app.get("/tasks")
def get_all_task():
    return tasks
@app.get("/tasks/{task_id}")
def single_task(task_id:int):
    for task in tasks:
        if task["id"]==task_id:
            return task
    raise HTTPException(status_code=404,detail="task not found")
class taskcreate(BaseModel):
    title:str
@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task_title(task_title:taskcreate):
    if not task_title.title.strip():
        raise HTTPException(status_code=400,detail="Title cannot be empty...")
    new_id=max([t["id"] for t in tasks],default=0)+1
    new_task={
            "id":new_id,
            "title":task_title.title.strip(),
            "done":False
        }
    tasks.append(new_task)
    return new_task
class Update_task(BaseModel):
    title:Optional[str]=None
    done:Optional[bool]=None
@app.put("/tasks/{task_id}")
def update_task(task_id:int,task_data:Update_task):
    for task in tasks:
        if task["id"]==task_id:
            if task_data.title is not None:
                if not task_data.title.strip():
                    raise HTTPException(status_code=400,detail="Title cannot be empty..")
                task["title"]=task_data.title.strip()
            if task_data.done is not None:
                task["done"]=task_data.done
            return task
    raise HTTPException(status_code=404,detail="Task not found..")
@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int):
    for index,task in enumerate(tasks):
        if task["id"]==task_id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404,detail="No task...")           