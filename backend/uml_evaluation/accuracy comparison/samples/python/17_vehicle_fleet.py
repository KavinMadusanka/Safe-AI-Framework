# 17_vehicle_fleet.py
# Vehicle Fleet Management System
# Classes: Vehicle, Driver, IFleetRepository (ABC), FleetRepository,
#          FleetService, FleetController, DatabaseConnection
# Features: association-heavy, Driver <-> Vehicle assignment

from abc import ABC, abstractmethod
from typing import List, Optional


# ── Models ─────────────────────────────────────────────────────────────────

class Vehicle:
    def __init__(self, vehicle_id: str, plate: str, model: str, vehicle_type: str):
        self.vehicle_id   = vehicle_id
        self.plate        = plate
        self.model        = model
        self.vehicle_type = vehicle_type
        self.mileage      = 0
        self.available    = True

    def get_vehicle_id(self) -> str:
        return self.vehicle_id

    def get_plate(self) -> str:
        return self.plate

    def get_model(self) -> str:
        return self.model

    def get_vehicle_type(self) -> str:
        return self.vehicle_type

    def get_mileage(self) -> int:
        return self.mileage

    def is_available(self) -> bool:
        return self.available

    def set_mileage(self, mileage: int):
        self.mileage = mileage

    def set_available(self, available: bool):
        self.available = available


class Driver:
    def __init__(self, driver_id: str, name: str, license_no: str):
        self.driver_id  = driver_id
        self.name       = name
        self.license_no = license_no
        self.active     = True
        self.vehicle    = None

    def get_driver_id(self) -> str:
        return self.driver_id

    def get_name(self) -> str:
        return self.name

    def get_license_no(self) -> str:
        return self.license_no

    def is_active(self) -> bool:
        return self.active

    def get_vehicle(self) -> Optional["Vehicle"]:
        return self.vehicle

    def set_vehicle(self, vehicle: Optional["Vehicle"]):
        self.vehicle = vehicle

    def set_active(self, active: bool):
        self.active = active


# ── Repository Interface ───────────────────────────────────────────────────

class IFleetRepository(ABC):

    @abstractmethod
    def find_vehicle_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        pass

    @abstractmethod
    def find_all_vehicles(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def save_vehicle(self, vehicle: Vehicle):
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: str):
        pass

    @abstractmethod
    def find_driver_by_id(self, driver_id: str) -> Optional[Driver]:
        pass

    @abstractmethod
    def find_all_drivers(self) -> List[Driver]:
        pass

    @abstractmethod
    def save_driver(self, driver: Driver):
        pass


# ── Database Layer ─────────────────────────────────────────────────────────

class DatabaseConnection:
    def __init__(self, url: str, username: str):
        self.url       = url
        self.username  = username
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def get_url(self) -> str:
        return self.url


# ── Repository Implementation ──────────────────────────────────────────────

class FleetRepository(IFleetRepository):
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def find_vehicle_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        self.connection.connect()
        return None

    def find_all_vehicles(self) -> List[Vehicle]:
        self.connection.connect()
        return []

    def save_vehicle(self, vehicle: Vehicle):
        self.connection.connect()

    def delete_vehicle(self, vehicle_id: str):
        self.connection.connect()

    def find_driver_by_id(self, driver_id: str) -> Optional[Driver]:
        self.connection.connect()
        return None

    def find_all_drivers(self) -> List[Driver]:
        self.connection.connect()
        return []

    def save_driver(self, driver: Driver):
        self.connection.connect()


# ── Service Layer ──────────────────────────────────────────────────────────

class FleetService:
    def __init__(self, repository: IFleetRepository):
        self.repository = repository

    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        return self.repository.find_vehicle_by_id(vehicle_id)

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.repository.find_all_vehicles()

    def add_vehicle(self, vehicle: Vehicle):
        self._validate_vehicle(vehicle)
        self.repository.save_vehicle(vehicle)

    def remove_vehicle(self, vehicle_id: str):
        self.repository.delete_vehicle(vehicle_id)

    def assign_driver(self, vehicle_id: str, driver_id: str):
        vehicle = self.repository.find_vehicle_by_id(vehicle_id)
        driver  = self.repository.find_driver_by_id(driver_id)
        driver.set_vehicle(vehicle)
        vehicle.set_available(False)
        self.repository.save_vehicle(vehicle)
        self.repository.save_driver(driver)

    def unassign_driver(self, driver_id: str):
        driver = self.repository.find_driver_by_id(driver_id)
        vehicle = driver.get_vehicle()
        vehicle.set_available(True)
        driver.set_vehicle(None)
        self.repository.save_vehicle(vehicle)
        self.repository.save_driver(driver)

    def update_mileage(self, vehicle_id: str, mileage: int):
        vehicle = self.repository.find_vehicle_by_id(vehicle_id)
        vehicle.set_mileage(mileage)
        self.repository.save_vehicle(vehicle)

    def _validate_vehicle(self, vehicle: Vehicle):
        if not vehicle.get_plate():
            raise ValueError("Vehicle plate cannot be empty")


# ── Controller Layer ───────────────────────────────────────────────────────

class FleetController:
    def __init__(self, service: FleetService):
        self.service = service

    def handle_get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        return self.service.get_vehicle(vehicle_id)

    def handle_get_all_vehicles(self) -> List[Vehicle]:
        return self.service.get_all_vehicles()

    def handle_add_vehicle(self, vehicle: Vehicle):
        self.service.add_vehicle(vehicle)

    def handle_remove_vehicle(self, vehicle_id: str):
        self.service.remove_vehicle(vehicle_id)

    def handle_assign_driver(self, vehicle_id: str, driver_id: str):
        self.service.assign_driver(vehicle_id, driver_id)

    def handle_unassign_driver(self, driver_id: str):
        self.service.unassign_driver(driver_id)

    def handle_update_mileage(self, vehicle_id: str, mileage: int):
        self.service.update_mileage(vehicle_id, mileage)