"""
CRUD (Create, Read, Update, Delete) operations for the Task model.
"""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.models.task import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_task(session: Session, user_id: str, title: str, description: str | None = None) -> Task:
    """
    Create a new task and save it to the database.

    Args:
        session: The database session.
        user_id: The ID of the user creating the task.
        title: The title of the task.
        description: The description of the task (optional).

    Returns:
        The created task object.

    Raises:
        SQLAlchemyError: If a database error occurs.
    """
    try:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        logger.info(f"Task {task.id} created for user {user_id}.")
        return task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task for user {user_id}: {e}")
        session.rollback()
        raise


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    """
    Retrieve a single task by its ID.

    Args:
        session: The database session.
        task_id: The ID of the task to retrieve.

    Returns:
        The task object if found, otherwise None.

    Raises:
        SQLAlchemyError: If a database error occurs.
    """
    try:
        task = session.get(Task, task_id)
        return task
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving task {task_id}: {e}")
        raise


def get_tasks_by_user(session: Session, user_id: str) -> list[Task]:
    """
    Retrieve all tasks for a specific user.

    Args:
        session: The database session.
        user_id: The ID of the user whose tasks to retrieve.

    Returns:
        A list of task objects.

    Raises:
        SQLAlchemyError: If a database error occurs.
    """
    try:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {e}")
        raise
