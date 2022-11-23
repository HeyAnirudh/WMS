from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
install_solc("0.8.8")

with open("./Transaction.sol", "r") as file:
    storage_file = file.read()

# Complie solidity

compiledSol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.8",
)

with open("transaction.json", "w") as file:
    json.dump(compiledSol, file)