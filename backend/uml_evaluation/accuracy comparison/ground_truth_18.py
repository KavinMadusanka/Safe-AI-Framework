# ground_truth_18.py
# Hand-verified ground truth for 18_hotel_booking.py
#
# Source has:
#   Classes: Room, Guest, Payment, Booking, Hotel
#   Features: association-heavy — Guest->Booking->Room, Booking->Payment
#             No layered architecture, no repository

SAMPLE   = "18_hotel_booking.py"
LANGUAGE = "python"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Room", "Guest", "Payment", "Booking", "Hotel"
    },
    "fields": {
        "Room.room_id", "Room.room_number", "Room.room_type",
        "Room.price_per_night", "Room.available", "Room.floor",
        "Guest.guest_id", "Guest.name", "Guest.email",
        "Guest.phone", "Guest.bookings",
        "Payment.payment_id", "Payment.amount",
        "Payment.method", "Payment.status",
        "Booking.booking_id", "Booking.guest", "Booking.room",
        "Booking.check_in", "Booking.check_out",
        "Booking.status", "Booking.payment",
        "Hotel.hotel_id", "Hotel.name", "Hotel.address",
        "Hotel.rooms", "Hotel.guests",
    },
    "methods": {
        "Room.get_room_id", "Room.get_room_number", "Room.get_room_type",
        "Room.get_price_per_night", "Room.is_available", "Room.get_floor",
        "Room.set_available", "Room.set_floor",
        "Guest.get_guest_id", "Guest.get_name", "Guest.get_email",
        "Guest.get_phone", "Guest.get_bookings",
        "Guest.add_booking", "Guest.set_email",
        "Payment.get_payment_id", "Payment.get_amount",
        "Payment.get_method", "Payment.get_status", "Payment.set_status",
        "Booking.get_booking_id", "Booking.get_guest", "Booking.get_room",
        "Booking.get_check_in", "Booking.get_check_out",
        "Booking.get_status", "Booking.get_payment",
        "Booking.set_status", "Booking.set_payment",
        "Hotel.get_hotel_id", "Hotel.get_name", "Hotel.get_address",
        "Hotel.get_rooms", "Hotel.get_guests",
        "Hotel.add_room", "Hotel.add_guest",
        "Hotel.find_available_rooms", "Hotel.make_booking",
        "Hotel.cancel_booking", "Hotel.process_payment",
    },
    "relationships": {
        ("associates", "Booking", "Guest"),
        ("associates", "Booking", "Room"),
        ("associates", "Booking", "Payment"),
        ("associates", "Guest",   "Booking"),
        ("associates", "Hotel",   "Room"),
        ("associates", "Hotel",   "Guest"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Room", "Guest", "Payment", "Booking", "Hotel"
    },
    "dependencies": {
        "Booking->Guest",
        "Booking->Room",
        "Booking->Payment",
        "Hotel->Room",
        "Hotel->Guest",
        "Hotel->Booking",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "Hotel",
        "Guest",
        "Booking",
        "Room",
    },
    "key_messages": {
        "Hotel->Guest:add_guest",
        "Hotel->Room:set_available",
        "Hotel->Booking:make_booking",
        "Hotel->Payment:process_payment",
        "Booking->Guest:add_booking",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Room", "Guest", "Payment", "Booking", "Hotel"
    },
    "interfaces": {
        "Room", "Guest", "Hotel"
    },
    "connections": {
        "Booking->Room",
        "Booking->Guest",
        "Hotel->Room",
        "Hotel->Guest",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "make_booking", "cancel_booking", "process_payment",
        "find_available_rooms", "add_guest", "add_room",
        "set_available", "add_booking",
    },
    "decisions": {
        "room available",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True