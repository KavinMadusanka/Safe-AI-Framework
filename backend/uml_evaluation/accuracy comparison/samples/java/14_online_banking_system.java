// 14_online_banking_system.java

import java.util.List;

class Account {
    private String accountId;
    private String ownerId;
    private double balance;
    private String accountType;
    private boolean active;

    public Account(String accountId, String ownerId, String accountType) {
        this.accountId   = accountId;
        this.ownerId     = ownerId;
        this.accountType = accountType;
        this.balance     = 0.0;
        this.active      = true;
    }

    public String getAccountId()   { return accountId; }
    public String getOwnerId()     { return ownerId; }
    public double getBalance()     { return balance; }
    public String getAccountType() { return accountType; }
    public boolean isActive()      { return active; }
    public void setBalance(double balance) { this.balance = balance; }
    public void setActive(boolean active)  { this.active = active; }
}

class Transaction {
    private String transactionId;
    private String fromAccountId;
    private String toAccountId;
    private double amount;
    private String status;

    public Transaction(String transactionId, String fromAccountId, String toAccountId, double amount) {
        this.transactionId  = transactionId;
        this.fromAccountId  = fromAccountId;
        this.toAccountId    = toAccountId;
        this.amount         = amount;
        this.status         = "PENDING";
    }

    public String getTransactionId()  { return transactionId; }
    public String getFromAccountId()  { return fromAccountId; }
    public String getToAccountId()    { return toAccountId; }
    public double getAmount()         { return amount; }
    public String getStatus()         { return status; }
    public void setStatus(String status) { this.status = status; }
}


interface IBankRepository {
    Account findAccountById(String accountId);
    List<Account> findAllAccounts();
    void saveAccount(Account account);
    void deleteAccount(String accountId);
    void saveTransaction(Transaction transaction);
    Transaction findTransactionById(String transactionId);
    List<Transaction> findTransactionsByAccount(String accountId);
}


class DatabaseManager {
    private String connectionString;
    private String username;
    private boolean connected;

    public DatabaseManager(String connectionString, String username) {
        this.connectionString = connectionString;
        this.username         = username;
        this.connected        = false;
    }

    public void connect()    { this.connected = true; }
    public void disconnect() { this.connected = false; }
    public boolean isConnected() { return connected; }
    public String getConnectionString() { return connectionString; }
}


class BankRepository implements IBankRepository {
    private DatabaseManager dbManager;

    public BankRepository(DatabaseManager dbManager) {
        this.dbManager = dbManager;
    }

    @Override
    public Account findAccountById(String accountId) {
        dbManager.connect();
        return null; // stub
    }

    @Override
    public List<Account> findAllAccounts() {
        dbManager.connect();
        return List.of();
    }

    @Override
    public void saveAccount(Account account) {
        dbManager.connect();
    }

    @Override
    public void deleteAccount(String accountId) {
        dbManager.connect();
    }

    @Override
    public void saveTransaction(Transaction transaction) {
        dbManager.connect();
    }

    @Override
    public Transaction findTransactionById(String transactionId) {
        dbManager.connect();
        return null;
    }

    @Override
    public List<Transaction> findTransactionsByAccount(String accountId) {
        dbManager.connect();
        return List.of();
    }
}

class TransactionService {
    private IBankRepository repository;

    public TransactionService(IBankRepository repository) {
        this.repository = repository;
    }

    public Account getAccount(String accountId) {
        return repository.findAccountById(accountId);
    }

    public List<Account> getAllAccounts() {
        return repository.findAllAccounts();
    }

    public void createAccount(Account account) {
        validateAccount(account);
        repository.saveAccount(account);
    }

    public void closeAccount(String accountId) {
        Account account = repository.findAccountById(accountId);
        account.setActive(false);
        repository.saveAccount(account);
    }

    public void transfer(Transaction transaction) {
        validateTransaction(transaction);
        Account from = repository.findAccountById(transaction.getFromAccountId());
        Account to   = repository.findAccountById(transaction.getToAccountId());
        from.setBalance(from.getBalance() - transaction.getAmount());
        to.setBalance(to.getBalance() + transaction.getAmount());
        transaction.setStatus("COMPLETED");
        repository.saveTransaction(transaction);
        repository.saveAccount(from);
        repository.saveAccount(to);
    }

    public List<Transaction> getAccountHistory(String accountId) {
        return repository.findTransactionsByAccount(accountId);
    }

    private void validateAccount(Account account) {
        if (account == null) throw new IllegalArgumentException("Account cannot be null");
    }

    private void validateTransaction(Transaction transaction) {
        if (transaction.getAmount() <= 0) throw new IllegalArgumentException("Amount must be positive");
    }
}

class AccountController {
    private TransactionService service;

    public AccountController(TransactionService service) {
        this.service = service;
    }

    public Account handleGetAccount(String accountId) {
        return service.getAccount(accountId);
    }

    public List<Account> handleGetAllAccounts() {
        return service.getAllAccounts();
    }

    public void handleCreateAccount(Account account) {
        service.createAccount(account);
    }

    public void handleCloseAccount(String accountId) {
        service.closeAccount(accountId);
    }

    public void handleTransfer(Transaction transaction) {
        service.transfer(transaction);
    }

    public List<Transaction> handleGetHistory(String accountId) {
        return service.getAccountHistory(accountId);
    }
}