SAMPLE   = "15_inventory_management.java"
LANGUAGE = "java"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Product", "Supplier", "IProductRepository",
        "ProductRepository", "InventoryService", "InventoryController",
        "DatabaseConnection", "ProductCategory"
    },
    "fields": {
        "Product.productId", "Product.name", "Product.price",
        "Product.quantity", "Product.category",
        "Supplier.supplierId", "Supplier.name", "Supplier.email", "Supplier.phone",
        "ProductRepository.connection",
        "InventoryService.repository", "InventoryService.supplier",
        "InventoryController.service",
        "DatabaseConnection.host", "DatabaseConnection.port",
        "DatabaseConnection.connected",
    },
    "methods": {
        "Product.getProductId", "Product.getName", "Product.getPrice",
        "Product.getQuantity", "Product.getCategory",
        "Product.setPrice", "Product.setQuantity",
        "Supplier.getSupplierId", "Supplier.getName", "Supplier.getEmail",
        "Supplier.getPhone", "Supplier.setEmail",
        "IProductRepository.findById", "IProductRepository.findAll",
        "IProductRepository.findByCategory", "IProductRepository.save",
        "IProductRepository.delete", "IProductRepository.existsById",
        "IProductRepository.findLowStock",
        "ProductRepository.findById", "ProductRepository.findAll",
        "ProductRepository.findByCategory", "ProductRepository.save",
        "ProductRepository.delete", "ProductRepository.existsById",
        "ProductRepository.findLowStock",
        "InventoryService.getProduct", "InventoryService.getAllProducts",
        "InventoryService.addProduct", "InventoryService.updatePrice",
        "InventoryService.restockProduct", "InventoryService.removeProduct",
        "InventoryService.checkLowStock", "InventoryService.getSupplier",
        "InventoryService.validateProduct",
        "InventoryController.handleGetProduct", "InventoryController.handleGetAllProducts",
        "InventoryController.handleAddProduct", "InventoryController.handleUpdatePrice",
        "InventoryController.handleRestock", "InventoryController.handleRemoveProduct",
        "InventoryController.handleLowStockAlert",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.isConnected", "DatabaseConnection.getHost",
        "DatabaseConnection.getPort",
    },
    "relationships": {
        ("implements", "ProductRepository",  "IProductRepository"),
        ("associates", "ProductRepository",  "DatabaseConnection"),
        ("associates", "InventoryService",   "IProductRepository"),
        ("associates", "InventoryService",   "Supplier"),
        ("associates", "InventoryController","InventoryService"),
        ("depends_on", "IProductRepository", "Product"),
        ("depends_on", "ProductRepository",  "Product"),
        ("depends_on", "InventoryService",   "Product"),
        ("depends_on", "InventoryController","Product"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Product", "Supplier", "IProductRepository",
        "ProductRepository", "InventoryService", "InventoryController",
        "DatabaseConnection", "ProductCategory"
    },
    "dependencies": {
        "ProductRepository->IProductRepository",
        "ProductRepository->DatabaseConnection",
        "InventoryService->IProductRepository",
        "InventoryService->Supplier",
        "InventoryController->InventoryService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "InventoryController",
        "InventoryService",
        "ProductRepository",
    },
    "key_messages": {
        "InventoryController->InventoryService:getProduct",
        "InventoryController->InventoryService:addProduct",
        "InventoryController->InventoryService:updatePrice",
        "InventoryService->ProductRepository:findById",
        "InventoryService->ProductRepository:save",
        "InventoryService->ProductRepository:delete",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Product", "Supplier", "IProductRepository",
        "ProductRepository", "InventoryService", "InventoryController", "DatabaseConnection"
    },
    "interfaces": {
        "IProductRepository", "InventoryService", "DatabaseConnection"
    },
    "connections": {
        "ProductRepository->DatabaseConnection",
        "InventoryService->IProductRepository",
        "InventoryController->InventoryService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "getProduct", "getAllProducts", "addProduct",
        "updatePrice", "restockProduct", "removeProduct", "checkLowStock",
        "findById", "save", "delete",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True