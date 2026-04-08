# ground_truth_16.py
# Hand-verified ground truth for 16_task_management.py
#
# Source has:
#   Classes: Task, Project, ITaskRepository (ABC), TaskRepository,
#            TaskService, TaskController, DatabaseConnection
#   Architecture: 4-layer Controller -> Service -> Repository -> DB

SAMPLE   = "16_task_management.py"
LANGUAGE = "python"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Task", "Project", "ITaskRepository",
        "TaskRepository", "TaskService", "TaskController", "DatabaseConnection"
    },
    "fields": {
        "Task.task_id", "Task.title", "Task.project_id",
        "Task.priority", "Task.status", "Task.assignee",
        "Project.project_id", "Project.name", "Project.owner", "Project.active",
        "TaskRepository.connection",
        "TaskService.repository",
        "TaskController.service",
        "DatabaseConnection.host", "DatabaseConnection.port",
        "DatabaseConnection.connected",
    },
    "methods": {
        "Task.get_task_id", "Task.get_title", "Task.get_project_id",
        "Task.get_priority", "Task.get_status",
        "Task.set_status", "Task.set_assignee",
        "Project.get_project_id", "Project.get_name", "Project.get_owner",
        "Project.is_active", "Project.set_active",
        "ITaskRepository.find_by_id", "ITaskRepository.find_all",
        "ITaskRepository.find_by_project", "ITaskRepository.save",
        "ITaskRepository.delete", "ITaskRepository.exists_by_id",
        "TaskRepository.find_by_id", "TaskRepository.find_all",
        "TaskRepository.find_by_project", "TaskRepository.save",
        "TaskRepository.delete", "TaskRepository.exists_by_id",
        "TaskService.get_task", "TaskService.get_all_tasks",
        "TaskService.get_project_tasks", "TaskService.create_task",
        "TaskService.update_status", "TaskService.assign_task",
        "TaskService.delete_task", "TaskService._validate_task",
        "TaskController.handle_get_task", "TaskController.handle_get_all",
        "TaskController.handle_get_project_tasks", "TaskController.handle_create_task",
        "TaskController.handle_update_status", "TaskController.handle_assign_task",
        "TaskController.handle_delete_task",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.is_connected", "DatabaseConnection.get_host",
    },
    "relationships": {
        ("implements", "TaskRepository",  "ITaskRepository"),
        ("associates", "TaskRepository",  "DatabaseConnection"),
        ("associates", "TaskService",     "ITaskRepository"),
        ("associates", "TaskController",  "TaskService"),
        ("depends_on", "ITaskRepository", "Task"),
        ("depends_on", "TaskRepository",  "Task"),
        ("depends_on", "TaskService",     "Task"),
        ("depends_on", "TaskController",  "Task"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Task", "Project", "ITaskRepository",
        "TaskRepository", "TaskService", "TaskController", "DatabaseConnection"
    },
    "dependencies": {
        "TaskRepository->ITaskRepository",
        "TaskRepository->DatabaseConnection",
        "TaskService->ITaskRepository",
        "TaskController->TaskService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "TaskController",
        "TaskService",
        "TaskRepository",
    },
    "key_messages": {
        "TaskController->TaskService:get_task",
        "TaskController->TaskService:create_task",
        "TaskController->TaskService:update_status",
        "TaskService->TaskRepository:find_by_id",
        "TaskService->TaskRepository:save",
        "TaskService->TaskRepository:delete",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Task", "Project", "ITaskRepository",
        "TaskRepository", "TaskService", "TaskController", "DatabaseConnection"
    },
    "interfaces": {
        "ITaskRepository", "TaskService", "DatabaseConnection"
    },
    "connections": {
        "TaskRepository->DatabaseConnection",
        "TaskService->ITaskRepository",
        "TaskController->TaskService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "get_task", "get_all_tasks", "get_project_tasks",
        "create_task", "update_status", "assign_task", "delete_task",
        "find_by_id", "save", "delete",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True