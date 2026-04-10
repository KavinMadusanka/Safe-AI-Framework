# ground_truth_23.py
# Hand-verified ground truth for 23_event_management.js
#
# Source has:
#   Classes: Ticket, Event, IEventRepository, EventRepository,
#            EventService, EventController, DatabaseConnection
#   Architecture: 4-layer Controller -> Service -> Repository -> DB
#   Language: JavaScript (ES6 classes, extends)

SAMPLE   = "23_event_management.js"
LANGUAGE = "javascript"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Ticket", "Event", "IEventRepository",
        "EventRepository", "EventService", "EventController", "DatabaseConnection"
    },
    "fields": {
        "Ticket.ticketId", "Ticket.eventId", "Ticket.attendeeId",
        "Ticket.ticketType", "Ticket.price", "Ticket.used",
        "Event.eventId", "Event.title", "Event.organizerId",
        "Event.venue", "Event.date", "Event.capacity", "Event.cancelled",
        "EventRepository.connection",
        "EventService.repository",
        "EventController.service",
        "DatabaseConnection.host", "DatabaseConnection.dbName",
        "DatabaseConnection.connected",
    },
    "methods": {
        "Ticket.getTicketId", "Ticket.getEventId", "Ticket.getAttendeeId",
        "Ticket.getTicketType", "Ticket.getPrice", "Ticket.isUsed",
        "Ticket.setPrice", "Ticket.setUsed",
        "Event.getEventId", "Event.getTitle", "Event.getOrganizerId",
        "Event.getVenue", "Event.getDate", "Event.getCapacity",
        "Event.isCancelled",
        "Event.setCapacity", "Event.setCancelled", "Event.setVenue",
        "IEventRepository.findEventById", "IEventRepository.findAllEvents",
        "IEventRepository.findEventsByOrganizer", "IEventRepository.saveEvent",
        "IEventRepository.deleteEvent", "IEventRepository.saveTicket",
        "IEventRepository.findTicketsByEvent", "IEventRepository.findTicketById",
        "EventRepository.findEventById", "EventRepository.findAllEvents",
        "EventRepository.findEventsByOrganizer", "EventRepository.saveEvent",
        "EventRepository.deleteEvent", "EventRepository.saveTicket",
        "EventRepository.findTicketsByEvent", "EventRepository.findTicketById",
        "EventService.getEvent", "EventService.getAllEvents",
        "EventService.getEventsByOrganizer", "EventService.createEvent",
        "EventService.cancelEvent", "EventService.deleteEvent",
        "EventService.issueTicket", "EventService.useTicket",
        "EventService.getEventTickets", "EventService._validateEvent",
        "EventController.handleGetEvent", "EventController.handleGetAllEvents",
        "EventController.handleGetByOrganizer", "EventController.handleCreateEvent",
        "EventController.handleCancelEvent", "EventController.handleDeleteEvent",
        "EventController.handleIssueTicket", "EventController.handleUseTicket",
        "EventController.handleGetTickets",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.isConnected", "DatabaseConnection.getHost",
        "DatabaseConnection.getDbName",
    },
    "relationships": {
        ("implements", "EventRepository",  "IEventRepository"),
        ("associates", "EventRepository",  "DatabaseConnection"),
        ("associates", "EventService",     "IEventRepository"),
        ("associates", "EventController",  "EventService"),
        ("depends_on", "IEventRepository", "Event"),
        ("depends_on", "IEventRepository", "Ticket"),
        ("depends_on", "EventRepository",  "Event"),
        ("depends_on", "EventRepository",  "Ticket"),
        ("depends_on", "EventService",     "Event"),
        ("depends_on", "EventService",     "Ticket"),
        ("depends_on", "EventController",  "Event"),
        ("depends_on", "EventController",  "Ticket"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Ticket", "Event", "IEventRepository",
        "EventRepository", "EventService", "EventController", "DatabaseConnection"
    },
    "dependencies": {
        "EventRepository->IEventRepository",
        "EventRepository->DatabaseConnection",
        "EventService->IEventRepository",
        "EventController->EventService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "EventController",
        "EventService",
        "EventRepository",
    },
    "key_messages": {
        "EventController->EventService:getEvent",
        "EventController->EventService:createEvent",
        "EventController->EventService:issueTicket",
        "EventService->EventRepository:findEventById",
        "EventService->EventRepository:saveEvent",
        "EventService->EventRepository:saveTicket",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Ticket", "Event", "IEventRepository",
        "EventRepository", "EventService", "EventController", "DatabaseConnection"
    },
    "interfaces": {
        "IEventRepository", "EventService", "DatabaseConnection"
    },
    "connections": {
        "EventRepository->DatabaseConnection",
        "EventService->IEventRepository",
        "EventController->EventService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "getEvent", "getAllEvents", "getEventsByOrganizer",
        "createEvent", "cancelEvent", "deleteEvent",
        "issueTicket", "useTicket", "getEventTickets",
        "findEventById", "saveEvent",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True