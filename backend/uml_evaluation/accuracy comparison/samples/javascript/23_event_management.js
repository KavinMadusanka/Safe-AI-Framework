// 23_event_management.js
// Event Management System — 4-layer architecture
// Classes: Event, Ticket, IEventRepository, EventRepository,
//          EventService, EventController, DatabaseConnection

// ── Models ─────────────────────────────────────────────────────────────────

class Ticket {
    constructor(ticketId, eventId, attendeeId, ticketType) {
        this.ticketId   = ticketId;
        this.eventId    = eventId;
        this.attendeeId = attendeeId;
        this.ticketType = ticketType;
        this.price      = 0;
        this.used       = false;
    }

    getTicketId()   { return this.ticketId; }
    getEventId()    { return this.eventId; }
    getAttendeeId() { return this.attendeeId; }
    getTicketType() { return this.ticketType; }
    getPrice()      { return this.price; }
    isUsed()        { return this.used; }

    setPrice(price) { this.price = price; }
    setUsed(used)   { this.used = used; }
}

class Event {
    constructor(eventId, title, organizerId, venue, date) {
        this.eventId     = eventId;
        this.title       = title;
        this.organizerId = organizerId;
        this.venue       = venue;
        this.date        = date;
        this.capacity    = 0;
        this.cancelled   = false;
    }

    getEventId()      { return this.eventId; }
    getTitle()        { return this.title; }
    getOrganizerId()  { return this.organizerId; }
    getVenue()        { return this.venue; }
    getDate()         { return this.date; }
    getCapacity()     { return this.capacity; }
    isCancelled()     { return this.cancelled; }

    setCapacity(capacity)    { this.capacity = capacity; }
    setCancelled(cancelled)  { this.cancelled = cancelled; }
    setVenue(venue)          { this.venue = venue; }
}

// ── Repository Interface ───────────────────────────────────────────────────

class IEventRepository {
    findEventById(eventId)          { throw new Error("Not implemented"); }
    findAllEvents()                 { throw new Error("Not implemented"); }
    findEventsByOrganizer(orgId)    { throw new Error("Not implemented"); }
    saveEvent(event)                { throw new Error("Not implemented"); }
    deleteEvent(eventId)            { throw new Error("Not implemented"); }
    saveTicket(ticket)              { throw new Error("Not implemented"); }
    findTicketsByEvent(eventId)     { throw new Error("Not implemented"); }
    findTicketById(ticketId)        { throw new Error("Not implemented"); }
}

// ── Database Layer ─────────────────────────────────────────────────────────

class DatabaseConnection {
    constructor(host, dbName) {
        this.host      = host;
        this.dbName    = dbName;
        this.connected = false;
    }

    connect()    { this.connected = true; }
    disconnect() { this.connected = false; }
    isConnected() { return this.connected; }
    getHost()    { return this.host; }
    getDbName()  { return this.dbName; }
}

// ── Repository Implementation ──────────────────────────────────────────────

class EventRepository extends IEventRepository {
    constructor(connection) {
        super();
        this.connection = connection;
    }

    findEventById(eventId) {
        this.connection.connect();
        return null;
    }

    findAllEvents() {
        this.connection.connect();
        return [];
    }

    findEventsByOrganizer(orgId) {
        this.connection.connect();
        return [];
    }

    saveEvent(event) {
        this.connection.connect();
    }

    deleteEvent(eventId) {
        this.connection.connect();
    }

    saveTicket(ticket) {
        this.connection.connect();
    }

    findTicketsByEvent(eventId) {
        this.connection.connect();
        return [];
    }

    findTicketById(ticketId) {
        this.connection.connect();
        return null;
    }
}

// ── Service Layer ──────────────────────────────────────────────────────────

class EventService {
    constructor(repository) {
        this.repository = repository;
    }

    getEvent(eventId) {
        return this.repository.findEventById(eventId);
    }

    getAllEvents() {
        return this.repository.findAllEvents();
    }

    getEventsByOrganizer(orgId) {
        return this.repository.findEventsByOrganizer(orgId);
    }

    createEvent(event) {
        this._validateEvent(event);
        this.repository.saveEvent(event);
    }

    cancelEvent(eventId) {
        const event = this.repository.findEventById(eventId);
        event.setCancelled(true);
        this.repository.saveEvent(event);
    }

    deleteEvent(eventId) {
        this.repository.deleteEvent(eventId);
    }

    issueTicket(ticket) {
        this.repository.saveTicket(ticket);
    }

    useTicket(ticketId) {
        const ticket = this.repository.findTicketById(ticketId);
        ticket.setUsed(true);
        this.repository.saveTicket(ticket);
    }

    getEventTickets(eventId) {
        return this.repository.findTicketsByEvent(eventId);
    }

    _validateEvent(event) {
        if (!event.getTitle()) throw new Error("Event title cannot be empty");
        if (event.getCapacity() < 0) throw new Error("Capacity cannot be negative");
    }
}

// ── Controller Layer ───────────────────────────────────────────────────────

class EventController {
    constructor(service) {
        this.service = service;
    }

    handleGetEvent(eventId)          { return this.service.getEvent(eventId); }
    handleGetAllEvents()             { return this.service.getAllEvents(); }
    handleGetByOrganizer(orgId)      { return this.service.getEventsByOrganizer(orgId); }
    handleCreateEvent(event)         { this.service.createEvent(event); }
    handleCancelEvent(eventId)       { this.service.cancelEvent(eventId); }
    handleDeleteEvent(eventId)       { this.service.deleteEvent(eventId); }
    handleIssueTicket(ticket)        { this.service.issueTicket(ticket); }
    handleUseTicket(ticketId)        { this.service.useTicket(ticketId); }
    handleGetTickets(eventId)        { return this.service.getEventTickets(eventId); }
}

module.exports = {
    Ticket, Event, IEventRepository, EventRepository,
    EventService, EventController, DatabaseConnection
};