# ground_truth_20.py
# Hand-verified ground truth for 20_chat_application.js
#
# Source has:
#   Classes: User, Attachment, Message, ChatRoom, ChatManager
#   Features: association-heavy — User<->ChatRoom memberships,
#             Message->Attachment, ChatManager orchestrates all
#   No layered architecture, no repository

SAMPLE   = "20_chat_application.js"
LANGUAGE = "javascript"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "User", "Attachment", "Message", "ChatRoom", "ChatManager"
    },
    "fields": {
        "User.userId", "User.username", "User.email",
        "User.online", "User.rooms",
        "Attachment.attachmentId", "Attachment.filename",
        "Attachment.fileType", "Attachment.fileSize", "Attachment.url",
        "Message.messageId", "Message.sender", "Message.roomId",
        "Message.text", "Message.timestamp",
        "Message.attachment", "Message.deleted",
        "ChatRoom.roomId", "ChatRoom.name", "ChatRoom.createdBy",
        "ChatRoom.members", "ChatRoom.messages", "ChatRoom.private",
        "ChatManager.rooms", "ChatManager.users",
    },
    "methods": {
        "User.getUserId", "User.getUsername", "User.getEmail",
        "User.isOnline", "User.getRooms",
        "User.setOnline", "User.setEmail", "User.joinRoom", "User.leaveRoom",
        "Attachment.getAttachmentId", "Attachment.getFilename",
        "Attachment.getFileType", "Attachment.getFileSize",
        "Attachment.getUrl", "Attachment.setUrl",
        "Message.getMessageId", "Message.getSender", "Message.getRoomId",
        "Message.getText", "Message.getTimestamp",
        "Message.getAttachment", "Message.isDeleted",
        "Message.setAttachment", "Message.setDeleted", "Message.setText",
        "ChatRoom.getRoomId", "ChatRoom.getName", "ChatRoom.getCreatedBy",
        "ChatRoom.getMembers", "ChatRoom.getMessages", "ChatRoom.isPrivate",
        "ChatRoom.setPrivate", "ChatRoom.addMember", "ChatRoom.removeMember",
        "ChatRoom.addMessage", "ChatRoom.getLastMessages",
        "ChatManager.getRooms", "ChatManager.getUsers",
        "ChatManager.registerUser", "ChatManager.createRoom",
        "ChatManager.findRoom", "ChatManager.findUser",
        "ChatManager.sendMessage", "ChatManager.deleteMessage",
        "ChatManager.attachFile",
    },
    "relationships": {
        ("associates", "User",        "ChatRoom"),
        ("associates", "Message",     "User"),
        ("associates", "Message",     "Attachment"),
        ("associates", "ChatRoom",    "User"),
        ("associates", "ChatRoom",    "Message"),
        ("associates", "ChatManager", "ChatRoom"),
        ("associates", "ChatManager", "User"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "User", "Attachment", "Message", "ChatRoom", "ChatManager"
    },
    "dependencies": {
        "Message->User",
        "Message->Attachment",
        "ChatRoom->User",
        "ChatRoom->Message",
        "ChatManager->ChatRoom",
        "ChatManager->User",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "ChatManager",
        "ChatRoom",
        "User",
        "Message",
    },
    "key_messages": {
        "ChatManager->ChatRoom:addMessage",
        "ChatManager->ChatRoom:addMember",
        "ChatManager->User:registerUser",
        "ChatRoom->User:joinRoom",
        "ChatManager->Message:sendMessage",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "User", "Attachment", "Message", "ChatRoom", "ChatManager"
    },
    "interfaces": {
        "User", "ChatRoom", "ChatManager"
    },
    "connections": {
        "Message->User",
        "Message->Attachment",
        "ChatRoom->Message",
        "ChatManager->ChatRoom",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "registerUser", "createRoom", "sendMessage",
        "deleteMessage", "attachFile",
        "addMember", "removeMember",
        "findRoom", "findUser",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True