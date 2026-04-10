# 16_task_management.py
# Task Management System — 4-layer architecture
# Classes: Task, Project, ITaskRepository (ABC), TaskRepository,
#          TaskService, TaskController, DatabaseConnection

from abc import ABC, abstractmethod
from typing import List, Optional


# ── Models ─────────────────────────────────────────────────────────────────

class Task:
    def __init__(self, task_id: str, title: str, project_id: str, priority: str):
        self.task_id    = task_id
        self.title      = title
        self.project_id = project_id
        self.priority   = priority
        self.status     = "TODO"
        self.assignee   = None

    def get_task_id(self) -> str:
        return self.task_id

    def get_title(self) -> str:
        return self.title

    def get_project_id(self) -> str:
        return self.project_id

    def get_priority(self) -> str:
        return self.priority

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str):
        self.status = status

    def set_assignee(self, assignee: str):
        self.assignee = assignee


class Project:
    def __init__(self, project_id: str, name: str, owner: str):
        self.project_id = project_id
        self.name       = name
        self.owner      = owner
        self.active     = True

    def get_project_id(self) -> str:
        return self.project_id

    def get_name(self) -> str:
        return self.name

    def get_owner(self) -> str:
        return self.owner

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        self.active = active


# ── Repository Interface ───────────────────────────────────────────────────

class ITaskRepository(ABC):

    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    def find_all(self) -> List[Task]:
        pass

    @abstractmethod
    def find_by_project(self, project_id: str) -> List[Task]:
        pass

    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def delete(self, task_id: str):
        pass

    @abstractmethod
    def exists_by_id(self, task_id: str) -> bool:
        pass


# ── Database Layer ─────────────────────────────────────────────────────────

class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self.host      = host
        self.port      = port
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def get_host(self) -> str:
        return self.host


# ── Repository Implementation ──────────────────────────────────────────────

class TaskRepository(ITaskRepository):
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def find_by_id(self, task_id: str) -> Optional[Task]:
        self.connection.connect()
        return None  # stub

    def find_all(self) -> List[Task]:
        self.connection.connect()
        return []

    def find_by_project(self, project_id: str) -> List[Task]:
        self.connection.connect()
        return []

    def save(self, task: Task):
        self.connection.connect()

    def delete(self, task_id: str):
        self.connection.connect()

    def exists_by_id(self, task_id: str) -> bool:
        self.connection.connect()
        return False


# ── Service Layer ──────────────────────────────────────────────────────────

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.repository.find_by_id(task_id)

    def get_all_tasks(self) -> List[Task]:
        return self.repository.find_all()

    def get_project_tasks(self, project_id: str) -> List[Task]:
        return self.repository.find_by_project(project_id)

    def create_task(self, task: Task):
        self._validate_task(task)
        self.repository.save(task)

    def update_status(self, task_id: str, status: str):
        task = self.repository.find_by_id(task_id)
        task.set_status(status)
        self.repository.save(task)

    def assign_task(self, task_id: str, assignee: str):
        task = self.repository.find_by_id(task_id)
        task.set_assignee(assignee)
        self.repository.save(task)

    def delete_task(self, task_id: str):
        self.repository.delete(task_id)

    def _validate_task(self, task: Task):
        if not task.get_title():
            raise ValueError("Task title cannot be empty")


# ── Controller Layer ───────────────────────────────────────────────────────

class TaskController:
    def __init__(self, service: TaskService):
        self.service = service

    def handle_get_task(self, task_id: str) -> Optional[Task]:
        return self.service.get_task(task_id)

    def handle_get_all(self) -> List[Task]:
        return self.service.get_all_tasks()

    def handle_get_project_tasks(self, project_id: str) -> List[Task]:
        return self.service.get_project_tasks(project_id)

    def handle_create_task(self, task: Task):
        self.service.create_task(task)

    def handle_update_status(self, task_id: str, status: str):
        self.service.update_status(task_id, status)

    def handle_assign_task(self, task_id: str, assignee: str):
        self.service.assign_task(task_id, assignee)

    def handle_delete_task(self, task_id: str):
        self.service.delete_task(task_id)