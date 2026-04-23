# ground_truth_17.py
# Hand-verified ground truth for 17_vehicle_fleet.py
#
# Source has:
#   Classes: Vehicle, Driver, IFleetRepository (ABC), FleetRepository,
#            FleetService, FleetController, DatabaseConnection
#   Features: Driver <-> Vehicle cross association

SAMPLE   = "17_vehicle_fleet.py"
LANGUAGE = "python"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Vehicle", "Driver", "IFleetRepository",
        "FleetRepository", "FleetService", "FleetController", "DatabaseConnection"
    },
    "fields": {
        "Vehicle.vehicle_id", "Vehicle.plate", "Vehicle.model",
        "Vehicle.vehicle_type", "Vehicle.mileage", "Vehicle.available",
        "Driver.driver_id", "Driver.name", "Driver.license_no",
        "Driver.active", "Driver.vehicle",
        "FleetRepository.connection",
        "FleetService.repository",
        "FleetController.service",
        "DatabaseConnection.url", "DatabaseConnection.username",
        "DatabaseConnection.connected",
    },
    "methods": {
        "Vehicle.get_vehicle_id", "Vehicle.get_plate", "Vehicle.get_model",
        "Vehicle.get_vehicle_type", "Vehicle.get_mileage", "Vehicle.is_available",
        "Vehicle.set_mileage", "Vehicle.set_available",
        "Driver.get_driver_id", "Driver.get_name", "Driver.get_license_no",
        "Driver.is_active", "Driver.get_vehicle",
        "Driver.set_vehicle", "Driver.set_active",
        "IFleetRepository.find_vehicle_by_id", "IFleetRepository.find_all_vehicles",
        "IFleetRepository.save_vehicle", "IFleetRepository.delete_vehicle",
        "IFleetRepository.find_driver_by_id", "IFleetRepository.find_all_drivers",
        "IFleetRepository.save_driver",
        "FleetRepository.find_vehicle_by_id", "FleetRepository.find_all_vehicles",
        "FleetRepository.save_vehicle", "FleetRepository.delete_vehicle",
        "FleetRepository.find_driver_by_id", "FleetRepository.find_all_drivers",
        "FleetRepository.save_driver",
        "FleetService.get_vehicle", "FleetService.get_all_vehicles",
        "FleetService.add_vehicle", "FleetService.remove_vehicle",
        "FleetService.assign_driver", "FleetService.unassign_driver",
        "FleetService.update_mileage", "FleetService._validate_vehicle",
        "FleetController.handle_get_vehicle", "FleetController.handle_get_all_vehicles",
        "FleetController.handle_add_vehicle", "FleetController.handle_remove_vehicle",
        "FleetController.handle_assign_driver", "FleetController.handle_unassign_driver",
        "FleetController.handle_update_mileage",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.is_connected", "DatabaseConnection.get_url",
    },
    "relationships": {
        ("implements", "FleetRepository",  "IFleetRepository"),
        ("associates", "FleetRepository",  "DatabaseConnection"),
        ("associates", "FleetService",     "IFleetRepository"),
        ("associates", "FleetController",  "FleetService"),
        ("associates", "Driver",           "Vehicle"),
        ("depends_on", "IFleetRepository", "Vehicle"),
        ("depends_on", "IFleetRepository", "Driver"),
        ("depends_on", "FleetRepository",  "Vehicle"),
        ("depends_on", "FleetRepository",  "Driver"),
        ("depends_on", "FleetService",     "Vehicle"),
        ("depends_on", "FleetService",     "Driver"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Vehicle", "Driver", "IFleetRepository",
        "FleetRepository", "FleetService", "FleetController", "DatabaseConnection"
    },
    "dependencies": {
        "FleetRepository->IFleetRepository",
        "FleetRepository->DatabaseConnection",
        "FleetService->IFleetRepository",
        "FleetController->FleetService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "FleetController",
        "FleetService",
        "FleetRepository",
    },
    "key_messages": {
        "FleetController->FleetService:get_vehicle",
        "FleetController->FleetService:add_vehicle",
        "FleetController->FleetService:assign_driver",
        "FleetService->FleetRepository:find_vehicle_by_id",
        "FleetService->FleetRepository:save_vehicle",
        "FleetService->FleetRepository:save_driver",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Vehicle", "Driver", "IFleetRepository",
        "FleetRepository", "FleetService", "FleetController", "DatabaseConnection"
    },
    "interfaces": {
        "IFleetRepository", "FleetService", "DatabaseConnection"
    },
    "connections": {
        "FleetRepository->DatabaseConnection",
        "FleetService->IFleetRepository",
        "FleetController->FleetService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "get_vehicle", "get_all_vehicles", "add_vehicle",
        "remove_vehicle", "assign_driver", "unassign_driver", "update_mileage",
        "find_vehicle_by_id", "save_vehicle", "save_driver",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True