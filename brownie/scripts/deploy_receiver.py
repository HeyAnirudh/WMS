from scripts.helpful_scripts import getAcc
from brownie import network, config, Sender, Receiver
import asyncio
from web3 import Web3


def deploy_contracts():
    acc = getAcc()
    # sender_txn = Sender.deploy({"from": acc})
    rec_txn = Receiver.deploy({"from": acc})
    print("Deployed Sender and Receiver!!")
    event_filter = rec_txn.events.Received.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        loop.close()


def handle_event(event):
    print(Web3.toJSON(event))


def send_transaction():
    acc = getAcc()
    rec_addr = Receiver[-1].address
    sender = Sender[-1]
    sender.testCallFoo(rec_addr, {"from": acc, "value": 100000000000000})


async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


def main():
    deploy_contracts()
