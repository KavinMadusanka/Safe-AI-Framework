// 15_inventory_management.java
// Inventory Management System
// Classes: Product, Supplier, IProductRepository, ProductRepository,
//          InventoryService, InventoryController, DatabaseConnection
// Features: enum for ProductCategory, cross-cutting supplier dependency

import java.util.List;

// ── Enum ───────────────────────────────────────────────────────────────────

enum ProductCategory {
    ELECTRONICS, CLOTHING, FOOD, FURNITURE, SPORTS
}

// ── Models ─────────────────────────────────────────────────────────────────

class Product {
    private String productId;
    private String name;
    private double price;
    private int quantity;
    private ProductCategory category;

    public Product(String productId, String name, double price, int quantity, ProductCategory category) {
        this.productId = productId;
        this.name      = name;
        this.price     = price;
        this.quantity  = quantity;
        this.category  = category;
    }

    public String getProductId()         { return productId; }
    public String getName()              { return name; }
    public double getPrice()             { return price; }
    public int getQuantity()             { return quantity; }
    public ProductCategory getCategory() { return category; }
    public void setPrice(double price)   { this.price = price; }
    public void setQuantity(int quantity){ this.quantity = quantity; }
}

class Supplier {
    private String supplierId;
    private String name;
    private String email;
    private String phone;

    public Supplier(String supplierId, String name, String email, String phone) {
        this.supplierId = supplierId;
        this.name       = name;
        this.email      = email;
        this.phone      = phone;
    }

    public String getSupplierId() { return supplierId; }
    public String getName()       { return name; }
    public String getEmail()      { return email; }
    public String getPhone()      { return phone; }
    public void setEmail(String email) { this.email = email; }
}

// ── Repository Interface ───────────────────────────────────────────────────

interface IProductRepository {
    Product findById(String productId);
    List<Product> findAll();
    List<Product> findByCategory(ProductCategory category);
    void save(Product product);
    void delete(String productId);
    boolean existsById(String productId);
    List<Product> findLowStock(int threshold);
}

// ── Database Connection ────────────────────────────────────────────────────

class DatabaseConnection {
    private String host;
    private int port;
    private boolean connected;

    public DatabaseConnection(String host, int port) {
        this.host      = host;
        this.port      = port;
        this.connected = false;
    }

    public void connect()    { this.connected = true; }
    public void disconnect() { this.connected = false; }
    public boolean isConnected() { return connected; }
    public String getHost()      { return host; }
    public int getPort()         { return port; }
}

// ── Repository Implementation ──────────────────────────────────────────────

class ProductRepository implements IProductRepository {
    private DatabaseConnection connection;

    public ProductRepository(DatabaseConnection connection) {
        this.connection = connection;
    }

    @Override
    public Product findById(String productId) {
        connection.connect();
        return null;
    }

    @Override
    public List<Product> findAll() {
        connection.connect();
        return List.of();
    }

    @Override
    public List<Product> findByCategory(ProductCategory category) {
        connection.connect();
        return List.of();
    }

    @Override
    public void save(Product product) {
        connection.connect();
    }

    @Override
    public void delete(String productId) {
        connection.connect();
    }

    @Override
    public boolean existsById(String productId) {
        connection.connect();
        return false;
    }

    @Override
    public List<Product> findLowStock(int threshold) {
        connection.connect();
        return List.of();
    }
}

// ── Service Layer ──────────────────────────────────────────────────────────

class InventoryService {
    private IProductRepository repository;
    private Supplier supplier;

    public InventoryService(IProductRepository repository, Supplier supplier) {
        this.repository = repository;
        this.supplier   = supplier;
    }

    public Product getProduct(String productId) {
        return repository.findById(productId);
    }

    public List<Product> getAllProducts() {
        return repository.findAll();
    }

    public void addProduct(Product product) {
        validateProduct(product);
        repository.save(product);
    }

    public void updatePrice(String productId, double newPrice) {
        Product product = repository.findById(productId);
        product.setPrice(newPrice);
        repository.save(product);
    }

    public void restockProduct(String productId, int quantity) {
        Product product = repository.findById(productId);
        product.setQuantity(product.getQuantity() + quantity);
        repository.save(product);
    }

    public void removeProduct(String productId) {
        repository.delete(productId);
    }

    public List<Product> checkLowStock(int threshold) {
        return repository.findLowStock(threshold);
    }

    public Supplier getSupplier() {
        return supplier;
    }

    private void validateProduct(Product product) {
        if (product.getPrice() < 0) throw new IllegalArgumentException("Price cannot be negative");
        if (product.getQuantity() < 0) throw new IllegalArgumentException("Quantity cannot be negative");
    }
}

// ── Controller Layer ───────────────────────────────────────────────────────

class InventoryController {
    private InventoryService service;

    public InventoryController(InventoryService service) {
        this.service = service;
    }

    public Product handleGetProduct(String productId) {
        return service.getProduct(productId);
    }

    public List<Product> handleGetAllProducts() {
        return service.getAllProducts();
    }

    public void handleAddProduct(Product product) {
        service.addProduct(product);
    }

    public void handleUpdatePrice(String productId, double price) {
        service.updatePrice(productId, price);
    }

    public void handleRestock(String productId, int quantity) {
        service.restockProduct(productId, quantity);
    }

    public void handleRemoveProduct(String productId) {
        service.removeProduct(productId);
    }

    public List<Product> handleLowStockAlert(int threshold) {
        return service.checkLowStock(threshold);
    }
}