// 22_food_delivery.js
// Food Delivery System — association-heavy
// Classes: Restaurant, MenuItem, Order, OrderItem, DeliveryAgent, Customer
// Features: Customer -> Order -> OrderItem -> MenuItem, Order -> DeliveryAgent

// ── Models ─────────────────────────────────────────────────────────────────

class MenuItem {
    constructor(itemId, restaurantId, name, price, category) {
        this.itemId       = itemId;
        this.restaurantId = restaurantId;
        this.name         = name;
        this.price        = price;
        this.category     = category;
        this.available    = true;
    }

    getItemId()       { return this.itemId; }
    getRestaurantId() { return this.restaurantId; }
    getName()         { return this.name; }
    getPrice()        { return this.price; }
    getCategory()     { return this.category; }
    isAvailable()     { return this.available; }

    setPrice(price)          { this.price = price; }
    setAvailable(available)  { this.available = available; }
}

class OrderItem {
    constructor(orderItemId, menuItem, quantity) {
        this.orderItemId = orderItemId;
        this.menuItem    = menuItem;
        this.quantity    = quantity;
    }

    getOrderItemId() { return this.orderItemId; }
    getMenuItem()    { return this.menuItem; }
    getQuantity()    { return this.quantity; }
    getSubtotal()    { return this.menuItem.getPrice() * this.quantity; }

    setQuantity(qty) { this.quantity = qty; }
}

class Customer {
    constructor(customerId, name, email, address) {
        this.customerId = customerId;
        this.name       = name;
        this.email      = email;
        this.address    = address;
        this.orders     = [];
    }

    getCustomerId() { return this.customerId; }
    getName()       { return this.name; }
    getEmail()      { return this.email; }
    getAddress()    { return this.address; }
    getOrders()     { return this.orders; }

    setAddress(address) { this.address = address; }
    addOrder(order)     { this.orders.push(order); }
}

class DeliveryAgent {
    constructor(agentId, name, phone) {
        this.agentId   = agentId;
        this.name      = name;
        this.phone     = phone;
        this.available = true;
        this.location  = null;
    }

    getAgentId()   { return this.agentId; }
    getName()      { return this.name; }
    getPhone()     { return this.phone; }
    isAvailable()  { return this.available; }
    getLocation()  { return this.location; }

    setAvailable(available) { this.available = available; }
    setLocation(location)   { this.location = location; }
}

class Order {
    constructor(orderId, customer, restaurant) {
        this.orderId    = orderId;
        this.customer   = customer;
        this.restaurant = restaurant;
        this.items      = [];
        this.agent      = null;
        this.status     = "PLACED";
        this.total      = 0;
    }

    getOrderId()    { return this.orderId; }
    getCustomer()   { return this.customer; }
    getRestaurant() { return this.restaurant; }
    getItems()      { return this.items; }
    getAgent()      { return this.agent; }
    getStatus()     { return this.status; }
    getTotal()      { return this.total; }

    setStatus(status) { this.status = status; }
    setAgent(agent)   { this.agent = agent; }

    addItem(orderItem) {
        this.items.push(orderItem);
        this.total += orderItem.getSubtotal();
    }
}

class Restaurant {
    constructor(restaurantId, name, address, cuisine) {
        this.restaurantId = restaurantId;
        this.name         = name;
        this.address      = address;
        this.cuisine      = cuisine;
        this.menu         = [];
        this.open         = true;
    }

    getRestaurantId() { return this.restaurantId; }
    getName()         { return this.name; }
    getAddress()      { return this.address; }
    getCuisine()      { return this.cuisine; }
    getMenu()         { return this.menu; }
    isOpen()          { return this.open; }

    setOpen(open)       { this.open = open; }
    addMenuItem(item)   { this.menu.push(item); }

    getAvailableItems() {
        return this.menu.filter(item => item.isAvailable());
    }
}

module.exports = { MenuItem, OrderItem, Customer, DeliveryAgent, Order, Restaurant };