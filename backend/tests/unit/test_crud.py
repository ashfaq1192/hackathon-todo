"""
Unit tests for CRUD operations.

This module tests the Create, Read, Update, and Delete operations
for the Task model.
"""

from sqlmodel import Session

from src.database.crud import create_task, get_task_by_id, get_tasks_by_user
from src.models.task import Task


def test_create_task_saves_to_db(test_session: Session):
    """
    T043: Verify create_task() saves a task and returns the created task object with an ID.
    """
    task = create_task(
        test_session, user_id="user1", title="Test Task", description="Test Description"
    )

    assert task.id is not None

    retrieved_task = test_session.get(Task, task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.user_id == "user1"


def test_get_task_by_id(test_session: Session):
    """
    T044: Verify get_task_by_id() retrieves the correct task.
    """
    task = Task(user_id="user1", title="Test Task")
    test_session.add(task)
    test_session.commit()
    test_session.refresh(task)

    retrieved_task = get_task_by_id(test_session, task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == "Test Task"


def test_get_tasks_by_user(test_session: Session):
    """
    T045: Verify get_tasks_by_user() filters by user_id correctly.
    """
    # Tasks for user1
    test_session.add(Task(user_id="user1", title="Task 1 for user1"))
    test_session.add(Task(user_id="user1", title="Task 2 for user1"))

    # Task for user2
    test_session.add(Task(user_id="user2", title="Task 1 for user2"))

    test_session.commit()

    user1_tasks = get_tasks_by_user(test_session, "user1")

    assert len(user1_tasks) == 2
    assert all(task.user_id == "user1" for task in user1_tasks)


def test_multi_user_isolation(test_session: Session):
    """
    T046: Verify that one user cannot see another user's tasks.
    """
    # Task for user1
    test_session.add(Task(user_id="user1", title="user1's private task"))
    test_session.commit()

    # Attempt to retrieve tasks for user2
    user2_tasks = get_tasks_by_user(test_session, "user2")

    assert len(user2_tasks) == 0
