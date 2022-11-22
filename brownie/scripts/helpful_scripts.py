from brownie import (
    network,
    accounts,
    config,
)

LOCAL_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]


def getAcc(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_ENV) or (
        network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
