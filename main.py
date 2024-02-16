from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine
from src.schemas import TaskBase, TaskUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all tasks
    """
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return JSONResponse(content=jsonable_encoder(tasks))


@app.post("/tasks")
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    """
    Create a task
    """
    return crud.create_task(db=db, task=task)


@app.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)

    if not db_task:
        raise HTTPException(status_code=404, detail="Task id not found")

    return crud.delete_task(db=db, task_id=db_task.id)


@app.put("/tasks/{task_id}")
def update_task_reminder(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)

    if not db_task:
        raise HTTPException(status_code=404, detail="Task id not found")

    updated_task = crud.update_task(db=db, task_id=db_task.id, task=task)

    return updated_task
