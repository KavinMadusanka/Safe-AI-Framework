// 20_chat_application.js
// Chat Application — association-heavy
// Classes: User, Message, ChatRoom, Attachment, ChatManager
// Features: User <-> ChatRoom memberships, Message -> Attachment

// ── Models ─────────────────────────────────────────────────────────────────

class User {
    constructor(userId, username, email) {
        this.userId   = userId;
        this.username = username;
        this.email    = email;
        this.online   = false;
        this.rooms    = [];
    }

    getUserId()   { return this.userId; }
    getUsername() { return this.username; }
    getEmail()    { return this.email; }
    isOnline()    { return this.online; }
    getRooms()    { return this.rooms; }

    setOnline(online)   { this.online = online; }
    setEmail(email)     { this.email = email; }
    joinRoom(room)      { this.rooms.push(room); }
    leaveRoom(roomId)   { this.rooms = this.rooms.filter(r => r.getRoomId() !== roomId); }
}

class Attachment {
    constructor(attachmentId, filename, fileType, fileSize) {
        this.attachmentId = attachmentId;
        this.filename     = filename;
        this.fileType     = fileType;
        this.fileSize     = fileSize;
        this.url          = null;
    }

    getAttachmentId() { return this.attachmentId; }
    getFilename()     { return this.filename; }
    getFileType()     { return this.fileType; }
    getFileSize()     { return this.fileSize; }
    getUrl()          { return this.url; }
    setUrl(url)       { this.url = url; }
}

class Message {
    constructor(messageId, sender, roomId, text) {
        this.messageId  = messageId;
        this.sender     = sender;
        this.roomId     = roomId;
        this.text       = text;
        this.timestamp  = new Date().toISOString();
        this.attachment = null;
        this.deleted    = false;
    }

    getMessageId()   { return this.messageId; }
    getSender()      { return this.sender; }
    getRoomId()      { return this.roomId; }
    getText()        { return this.text; }
    getTimestamp()   { return this.timestamp; }
    getAttachment()  { return this.attachment; }
    isDeleted()      { return this.deleted; }

    setAttachment(attachment) { this.attachment = attachment; }
    setDeleted(deleted)       { this.deleted = deleted; }
    setText(text)             { this.text = text; }
}

class ChatRoom {
    constructor(roomId, name, createdBy) {
        this.roomId    = roomId;
        this.name      = name;
        this.createdBy = createdBy;
        this.members   = [];
        this.messages  = [];
        this.private   = false;
    }

    getRoomId()   { return this.roomId; }
    getName()     { return this.name; }
    getCreatedBy(){ return this.createdBy; }
    getMembers()  { return this.members; }
    getMessages() { return this.messages; }
    isPrivate()   { return this.private; }

    setPrivate(priv) { this.private = priv; }

    addMember(user) {
        this.members.push(user);
        user.joinRoom(this);
    }

    removeMember(userId) {
        const user = this.members.find(m => m.getUserId() === userId);
        if (user) user.leaveRoom(this.roomId);
        this.members = this.members.filter(m => m.getUserId() !== userId);
    }

    addMessage(message) {
        this.messages.push(message);
    }

    getLastMessages(count) {
        return this.messages.slice(-count);
    }
}

class ChatManager {
    constructor() {
        this.rooms = [];
        this.users = [];
    }

    getRooms()  { return this.rooms; }
    getUsers()  { return this.users; }

    registerUser(user) {
        this.users.push(user);
    }

    createRoom(room) {
        this.rooms.push(room);
    }

    findRoom(roomId) {
        return this.rooms.find(r => r.getRoomId() === roomId);
    }

    findUser(userId) {
        return this.users.find(u => u.getUserId() === userId);
    }

    sendMessage(message) {
        const room = this.findRoom(message.getRoomId());
        room.addMessage(message);
    }

    deleteMessage(roomId, messageId) {
        const room = this.findRoom(roomId);
        const msg  = room.getMessages().find(m => m.getMessageId() === messageId);
        if (msg) msg.setDeleted(true);
    }

    attachFile(message, attachment) {
        message.setAttachment(attachment);
    }
}

module.exports = { User, Attachment, Message, ChatRoom, ChatManager };