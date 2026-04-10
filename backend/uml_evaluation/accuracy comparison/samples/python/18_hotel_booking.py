# 18_hotel_booking.py
# Hotel Booking System — association-heavy, no layered architecture
# Classes: Room, Guest, Booking, Payment, Hotel
# Features: Guest -> Booking -> Room, Booking -> Payment associations

from typing import List, Optional


# ── Models ─────────────────────────────────────────────────────────────────

class Room:
    def __init__(self, room_id: str, room_number: str, room_type: str, price_per_night: float):
        self.room_id        = room_id
        self.room_number    = room_number
        self.room_type      = room_type
        self.price_per_night = price_per_night
        self.available      = True
        self.floor          = 1

    def get_room_id(self) -> str:
        return self.room_id

    def get_room_number(self) -> str:
        return self.room_number

    def get_room_type(self) -> str:
        return self.room_type

    def get_price_per_night(self) -> float:
        return self.price_per_night

    def is_available(self) -> bool:
        return self.available

    def get_floor(self) -> int:
        return self.floor

    def set_available(self, available: bool):
        self.available = available

    def set_floor(self, floor: int):
        self.floor = floor


class Guest:
    def __init__(self, guest_id: str, name: str, email: str, phone: str):
        self.guest_id = guest_id
        self.name     = name
        self.email    = email
        self.phone    = phone
        self.bookings: List["Booking"] = []

    def get_guest_id(self) -> str:
        return self.guest_id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_phone(self) -> str:
        return self.phone

    def get_bookings(self) -> List["Booking"]:
        return self.bookings

    def add_booking(self, booking: "Booking"):
        self.bookings.append(booking)

    def set_email(self, email: str):
        self.email = email


class Payment:
    def __init__(self, payment_id: str, amount: float, method: str):
        self.payment_id = payment_id
        self.amount     = amount
        self.method     = method
        self.status     = "PENDING"

    def get_payment_id(self) -> str:
        return self.payment_id

    def get_amount(self) -> float:
        return self.amount

    def get_method(self) -> str:
        return self.method

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str):
        self.status = status


class Booking:
    def __init__(self, booking_id: str, guest: Guest, room: Room, check_in: str, check_out: str):
        self.booking_id  = booking_id
        self.guest       = guest
        self.room        = room
        self.check_in    = check_in
        self.check_out   = check_out
        self.status      = "CONFIRMED"
        self.payment: Optional[Payment] = None

    def get_booking_id(self) -> str:
        return self.booking_id

    def get_guest(self) -> Guest:
        return self.guest

    def get_room(self) -> Room:
        return self.room

    def get_check_in(self) -> str:
        return self.check_in

    def get_check_out(self) -> str:
        return self.check_out

    def get_status(self) -> str:
        return self.status

    def get_payment(self) -> Optional[Payment]:
        return self.payment

    def set_status(self, status: str):
        self.status = status

    def set_payment(self, payment: Payment):
        self.payment = payment


class Hotel:
    def __init__(self, hotel_id: str, name: str, address: str):
        self.hotel_id = hotel_id
        self.name     = name
        self.address  = address
        self.rooms: List[Room] = []
        self.guests: List[Guest] = []

    def get_hotel_id(self) -> str:
        return self.hotel_id

    def get_name(self) -> str:
        return self.name

    def get_address(self) -> str:
        return self.address

    def get_rooms(self) -> List[Room]:
        return self.rooms

    def get_guests(self) -> List[Guest]:
        return self.guests

    def add_room(self, room: Room):
        self.rooms.append(room)

    def add_guest(self, guest: Guest):
        self.guests.append(guest)

    def find_available_rooms(self) -> List[Room]:
        return [r for r in self.rooms if r.is_available()]

    def make_booking(self, guest: Guest, room: Room, check_in: str, check_out: str) -> Booking:
        booking = Booking(f"BK{len(guest.get_bookings())+1}", guest, room, check_in, check_out)
        room.set_available(False)
        guest.add_booking(booking)
        return booking

    def cancel_booking(self, booking: Booking):
        booking.set_status("CANCELLED")
        booking.get_room().set_available(True)

    def process_payment(self, booking: Booking, payment: Payment):
        payment.set_status("PAID")
        booking.set_payment(payment)