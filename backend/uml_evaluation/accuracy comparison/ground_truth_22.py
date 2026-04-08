# ground_truth_22.py
# Hand-verified ground truth for 22_food_delivery.js
#
# Source has:
#   Classes: MenuItem, OrderItem, Customer, DeliveryAgent, Order, Restaurant
#   Features: association-heavy — Customer->Order->OrderItem->MenuItem,
#             Order->DeliveryAgent, Restaurant->MenuItem
#   No layered architecture, no repository

SAMPLE   = "22_food_delivery.js"
LANGUAGE = "javascript"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "MenuItem", "OrderItem", "Customer",
        "DeliveryAgent", "Order", "Restaurant"
    },
    "fields": {
        "MenuItem.itemId", "MenuItem.restaurantId", "MenuItem.name",
        "MenuItem.price", "MenuItem.category", "MenuItem.available",
        "OrderItem.orderItemId", "OrderItem.menuItem", "OrderItem.quantity",
        "Customer.customerId", "Customer.name", "Customer.email",
        "Customer.address", "Customer.orders",
        "DeliveryAgent.agentId", "DeliveryAgent.name", "DeliveryAgent.phone",
        "DeliveryAgent.available", "DeliveryAgent.location",
        "Order.orderId", "Order.customer", "Order.restaurant",
        "Order.items", "Order.agent", "Order.status", "Order.total",
        "Restaurant.restaurantId", "Restaurant.name", "Restaurant.address",
        "Restaurant.cuisine", "Restaurant.menu", "Restaurant.open",
    },
    "methods": {
        "MenuItem.getItemId", "MenuItem.getRestaurantId", "MenuItem.getName",
        "MenuItem.getPrice", "MenuItem.getCategory", "MenuItem.isAvailable",
        "MenuItem.setPrice", "MenuItem.setAvailable",
        "OrderItem.getOrderItemId", "OrderItem.getMenuItem",
        "OrderItem.getQuantity", "OrderItem.getSubtotal", "OrderItem.setQuantity",
        "Customer.getCustomerId", "Customer.getName", "Customer.getEmail",
        "Customer.getAddress", "Customer.getOrders",
        "Customer.setAddress", "Customer.addOrder",
        "DeliveryAgent.getAgentId", "DeliveryAgent.getName",
        "DeliveryAgent.getPhone", "DeliveryAgent.isAvailable",
        "DeliveryAgent.getLocation",
        "DeliveryAgent.setAvailable", "DeliveryAgent.setLocation",
        "Order.getOrderId", "Order.getCustomer", "Order.getRestaurant",
        "Order.getItems", "Order.getAgent", "Order.getStatus", "Order.getTotal",
        "Order.setStatus", "Order.setAgent", "Order.addItem",
        "Restaurant.getRestaurantId", "Restaurant.getName",
        "Restaurant.getAddress", "Restaurant.getCuisine",
        "Restaurant.getMenu", "Restaurant.isOpen",
        "Restaurant.setOpen", "Restaurant.addMenuItem",
        "Restaurant.getAvailableItems",
    },
    "relationships": {
        ("associates", "Order",      "Customer"),
        ("associates", "Order",      "Restaurant"),
        ("associates", "Order",      "DeliveryAgent"),
        ("associates", "Order",      "OrderItem"),
        ("associates", "OrderItem",  "MenuItem"),
        ("associates", "Customer",   "Order"),
        ("associates", "Restaurant", "MenuItem"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "MenuItem", "OrderItem", "Customer",
        "DeliveryAgent", "Order", "Restaurant"
    },
    "dependencies": {
        "Order->Customer",
        "Order->Restaurant",
        "Order->DeliveryAgent",
        "Order->OrderItem",
        "OrderItem->MenuItem",
        "Restaurant->MenuItem",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "Customer",
        "Order",
        "Restaurant",
        "DeliveryAgent",
    },
    "key_messages": {
        "Customer->Order:addOrder",
        "Order->Restaurant:getAvailableItems",
        "Order->OrderItem:addItem",
        "Order->DeliveryAgent:setAgent",
        "OrderItem->MenuItem:getSubtotal",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "MenuItem", "OrderItem", "Customer",
        "DeliveryAgent", "Order", "Restaurant"
    },
    "interfaces": {
        "Restaurant", "Customer", "Order"
    },
    "connections": {
        "Order->Customer",
        "Order->Restaurant",
        "Order->OrderItem",
        "OrderItem->MenuItem",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "addOrder", "addItem", "setAgent",
        "getAvailableItems", "addMenuItem",
        "setStatus", "setAvailable",
        "getSubtotal",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True