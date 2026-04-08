SAMPLE   = "14_online_banking_system.java"
LANGUAGE = "java"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Account", "Transaction", "IBankRepository",
        "BankRepository", "TransactionService", "AccountController", "DatabaseManager"
    },
    "fields": {
        "Account.accountId", "Account.ownerId", "Account.balance",
        "Account.accountType", "Account.active",
        "Transaction.transactionId", "Transaction.fromAccountId",
        "Transaction.toAccountId", "Transaction.amount", "Transaction.status",
        "BankRepository.dbManager",
        "TransactionService.repository",
        "AccountController.service",
        "DatabaseManager.connectionString", "DatabaseManager.username",
        "DatabaseManager.connected",
    },
    "methods": {
        "Account.getAccountId", "Account.getOwnerId", "Account.getBalance",
        "Account.getAccountType", "Account.isActive",
        "Account.setBalance", "Account.setActive",
        "Transaction.getTransactionId", "Transaction.getFromAccountId",
        "Transaction.getToAccountId", "Transaction.getAmount",
        "Transaction.getStatus", "Transaction.setStatus",
        "IBankRepository.findAccountById", "IBankRepository.findAllAccounts",
        "IBankRepository.saveAccount", "IBankRepository.deleteAccount",
        "IBankRepository.saveTransaction", "IBankRepository.findTransactionById",
        "IBankRepository.findTransactionsByAccount",
        "BankRepository.findAccountById", "BankRepository.findAllAccounts",
        "BankRepository.saveAccount", "BankRepository.deleteAccount",
        "BankRepository.saveTransaction", "BankRepository.findTransactionById",
        "BankRepository.findTransactionsByAccount",
        "TransactionService.getAccount", "TransactionService.getAllAccounts",
        "TransactionService.createAccount", "TransactionService.closeAccount",
        "TransactionService.transfer", "TransactionService.getAccountHistory",
        "TransactionService.validateAccount", "TransactionService.validateTransaction",
        "AccountController.handleGetAccount", "AccountController.handleGetAllAccounts",
        "AccountController.handleCreateAccount", "AccountController.handleCloseAccount",
        "AccountController.handleTransfer", "AccountController.handleGetHistory",
        "DatabaseManager.connect", "DatabaseManager.disconnect",
        "DatabaseManager.isConnected", "DatabaseManager.getConnectionString",
    },
    "relationships": {
        ("implements", "BankRepository",      "IBankRepository"),
        ("associates", "BankRepository",      "DatabaseManager"),
        ("associates", "TransactionService",  "IBankRepository"),
        ("associates", "AccountController",   "TransactionService"),
        ("depends_on", "IBankRepository",     "Account"),
        ("depends_on", "IBankRepository",     "Transaction"),
        ("depends_on", "BankRepository",      "Account"),
        ("depends_on", "BankRepository",      "Transaction"),
        ("depends_on", "TransactionService",  "Account"),
        ("depends_on", "TransactionService",  "Transaction"),
        ("depends_on", "AccountController",   "Account"),
        ("depends_on", "AccountController",   "Transaction"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Account", "Transaction", "IBankRepository",
        "BankRepository", "TransactionService", "AccountController", "DatabaseManager"
    },
    "dependencies": {
        "BankRepository->IBankRepository",
        "BankRepository->DatabaseManager",
        "TransactionService->IBankRepository",
        "AccountController->TransactionService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "AccountController",
        "TransactionService",
        "BankRepository",
    },
    "key_messages": {
        "AccountController->TransactionService:getAccount",
        "AccountController->TransactionService:createAccount",
        "AccountController->TransactionService:transfer",
        "TransactionService->BankRepository:findAccountById",
        "TransactionService->BankRepository:saveAccount",
        "TransactionService->BankRepository:saveTransaction",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Account", "Transaction", "IBankRepository",
        "BankRepository", "TransactionService", "AccountController", "DatabaseManager"
    },
    "interfaces": {
        "IBankRepository", "TransactionService", "DatabaseManager", "Account"
    },
    "connections": {
        "BankRepository->DatabaseManager",
        "TransactionService->IBankRepository",
        "AccountController->TransactionService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "getAccount", "getAllAccounts", "createAccount",
        "closeAccount", "transfer", "getAccountHistory",
        "findAccountById", "saveAccount", "saveTransaction",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True