from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
install_solc("0.8.8")


def deploy(sender, receiver, quantity, quality):
    with open("./transactions/transaction.json", "r") as file:
        compiledSol = json.load(file)

    # Get Bytecode

    bytecode = compiledSol["contracts"]["SimpleStorage.sol"]["Transaction"]["evm"][
        "bytecode"
    ]["object"]

    # Get ABI
    abi = compiledSol["contracts"]["SimpleStorage.sol"]["Transaction"]["abi"]

    # Connecting
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    chainId = 1337
    myAddr = os.getenv("SENDER_ADDR")
    privateKey = os.getenv("PRIVATE_KEY")

    # Create the contract
    SimpleTransaction = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get latest transaction
    nonce = w3.eth.getTransactionCount(myAddr)

    # 1. Build a transaction
    # 2. Sign a transaction
    # 3. Send a transaction

    # 1
    transaction = SimpleTransaction.constructor().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": myAddr,
            "nonce": nonce,
        }
    )

    # 2
    signedTxn = w3.eth.account.sign_transaction(transaction, private_key=privateKey)

    # 3
    txHash = w3.eth.send_raw_transaction(signedTxn.rawTransaction)
    txReceipt = w3.eth.wait_for_transaction_receipt(txHash)

    # Working with contract
    # Contract addr, ABI
    sTxn = w3.eth.contract(address=txReceipt.contractAddress, abi=abi)
    # Call -> Simulate making the call and getting a return value
    # Transact -> Actually make a state change

    # print(sTxn.functions.createTransaction().call())

    storeTxn = sTxn.functions.createTransaction(
        sender, receiver, quality, quantity
    ).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": myAddr,
            "nonce": nonce + 1,
        }
    )

    signStoreTxn = w3.eth.account.sign_transaction(storeTxn, private_key=privateKey)
    storeTxnHash = w3.eth.send_raw_transaction(signStoreTxn.rawTransaction)
    storeTxnReceipt = w3.eth.wait_for_transaction_receipt(storeTxnHash)

    return f"{storeTxnReceipt.transactionHash}"


# print(sTxn.functions.retrieve().call())
