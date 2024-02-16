from sqlalchemy.orm import Session

from . import models, schemas

http_options = {}


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**dict(task))

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    # Check for existance
    db.query(models.Task).filter_by(id=task_id).delete()
    db.commit()
    return


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    result = (
        db.query(models.Task).filter(models.Task.id == task_id).update(dict(task))
        # .returning(schemas.Task)
    )

    db.commit()
    return result


def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
