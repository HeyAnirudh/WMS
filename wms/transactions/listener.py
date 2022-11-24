from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
install_solc("0.8.8")

with open("./transactions/transaction.json", "r") as file:
    compiledSol = json.load(file)

bytecode = compiledSol["contracts"]["SimpleStorage.sol"]["Transaction"]["evm"][
    "bytecode"
]["object"]

abi = compiledSol["contracts"]["SimpleStorage.sol"]["Transaction"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chainId = 1337
myAddr = os.getenv("SENDER_ADDR")
privateKey = os.getenv("PRIVATE_KEY")

contract = w3.eth.contract(abi=abi, bytecode=bytecode)


def handle_event(event):
    print(event.args)


async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


def listen():
    event_filter = contract.events.TransactionSent.createFilter(fromBlock="latest")
    # block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
        # log_loop(block_filter, 2),
        # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()
