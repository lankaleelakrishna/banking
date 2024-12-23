// Modal functions for Bank Actions
function showDepositModal() {
    document.getElementById('deposit-modal').style.display = 'flex';
}

function showWithdrawModal() {
    document.getElementById('withdraw-modal').style.display = 'flex';
}

function showTransferModal() {
    document.getElementById('transfer-modal').style.display = 'flex';
}

function showTransactions() {
    document.getElementById('transactions-modal').style.display = 'flex';
    loadTransactions();
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Process Deposit
function processDeposit() {
    let amount = document.getElementById('deposit-amount').value;
    alert(`Deposited: $${amount}`);
    closeModal('deposit-modal');
}

// Process Withdraw
function processWithdraw() {
    let amount = document.getElementById('withdraw-amount').value;
    alert(`Withdrew: $${amount}`);
    closeModal('withdraw-modal');
}

// Process Transfer
function processTransfer() {
    let amount = document.getElementById('transfer-amount').value;
    let recipient = document.getElementById('transfer-to').value;
    alert(`Transferred: $${amount} to ${recipient}`);
    closeModal('transfer-modal');
}

// Load Transaction History
function loadTransactions() {
    const transactions = [
        "Deposit: $500 on 12/21/2024",
        "Withdraw: $200 on 12/20/2024",
        "Transfer: $150 to account 12345 on 12/18/2024",
    ];
    
    const transactionsList = document.getElementById('transactions-list');
    transactionsList.innerHTML = '';
    transactions.forEach(transaction => {
        const li = document.createElement('li');
        li.textContent = transaction;
        transactionsList.appendChild(li);
    });
}
