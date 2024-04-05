import time
import json
import pathlib as pl
import os
import pandas as pd
from web3.auto.gethdev import Web3
from web3.middleware import geth_poa_middleware
import random
_PowerGenerated = 0
_EnergyComsumption = 0
excess = int(0) 
Powerneeded = int(0) 
buyer = int(0) 
def main(): 
 acquirestats() 
# setup logging and attempt time interval for attempting commit/reveal time delay every action
interval = 2
# get config info
with open(pl.Path("./config/password.txt"), "r") as file: 
 nodePassword = file.read() 
with open(pl.Path("./config/httpport.txt"), "r") as httpportFile: 
 httpport = httpportFile.read() 
# setup blockchain connection
w3 = Web3(Web3.HTTPProvider(f"HTTP://127.0.0.1:{httpport}")) 
w3.middleware_onion.inject(geth_poa_middleware, layer=0) 
with open(pl.Path("./config/contractAddress.txt"), "r") as addressFile: 
    address = w3.toChecksumAddress(addressFile.read()) 
with open(pl.Path("./config/contractAbi.json"), "r") as abiFile: 
    abi = json.load(abiFile) 
contract = w3.eth.contract(address=address, abi=abi) 

def acquirestats(): 
 global _PowerGenerated
 global _EnergyComsumption
 global buyer
 global excess
 global Powerneeded
 # time.sleep(interval)
 _PowerGenerated = random.randint(50, 100) 
 _EnergyComsumption = random.randint(0, 20) 
 print(  f"here1 address: {w3.eth.accounts[0]} Power generated is {_PowerGenerated} Energy Comsumption is {_EnergyComsumption}\n") 
 if _PowerGenerated > _EnergyComsumption: 
    difference = _PowerGenerated - _EnergyComsumption
    print("This node is a seller node") 
    buyer = 0
 else: 
    difference = _EnergyComsumption - _PowerGenerated
    print("This node is a buyer node") 
    buyer = 99
 if buyer == 99: 
    print(f"You need to buy {difference} of energy") 
    price = input("Input the price of energy you want to offer: ") 
    price = int(price) 
    moneyearned = contract.functions.sellBuyEnergy(price, 
difference).call() 
    print(f"The amount to be spent:{moneyearned}") 
    contract.functions.sellbuy(price, difference, buyer).transact( 
 {"from": w3.eth.accounts[0], "gasPrice": 0} 
 ) 
 if buyer == 0: 
    print(f"You can sell {difference} of energy") 
    price = input("Input the price of energy you want to sell: ") 
    price = int(price) 
    moneyearned = contract.functions.sellBuyEnergy(price, difference).call() 
 print(f"The amount to be earned:{moneyearned}") 
 contract.functions.sellbuy(price, difference, buyer).transact( 
 {"from": w3.eth.accounts[0], "gasPrice": 0} 
 ) 
 time.sleep(30) 
main()
