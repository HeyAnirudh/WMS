from scripts.helpful_scripts import getAcc
from brownie import Sender


def deploy_contracts():
    acc = getAcc()
    Sender.deploy({"from": acc})
    print("Deployed Sender!!")


def send_transaction():
    acc = getAcc()
    # rec_addr = str(input("enter rec address: "))
    rec_addr = "0xe54230F507eddd5dbF21E63D70eFdb5648D86154"
    # rec_addr = Receiver[-1].address
    sender = Sender[-1]
    sender.testCallFoo(rec_addr, {"from": acc, "value": 10000})


def main():
    deploy_contracts()
    send_transaction()
