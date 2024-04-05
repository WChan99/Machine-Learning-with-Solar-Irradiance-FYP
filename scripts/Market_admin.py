import time
import threading
import json
import pathlib as pl
import os
import pandas as pd
from web3.auto.gethdev import Web3
from web3.middleware import geth_poa_middleware
import random
with open(pl.Path("./config/password.txt"), "r") as file: 
 nodePassword = file.read() 
with open(pl.Path("./config/httpport.txt"), "r") as httpportFile: 
 httpport = httpportFile.read() 
# setup blockchain connection
web3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:{httpport}")) 
web3.middleware_onion.inject(geth_poa_middleware, layer=0) 
with open(pl.Path("./config/contractAddress.txt"), "r") as addressFile: 
 address = web3.toChecksumAddress(addressFile.read()) 

with open(pl.Path("./config/contractAbi.json"), "r") as abiFile: 
    abi = json.load(abiFile) 
    startmarket = web3.eth.contract(address=address, abi=abi) 
    print("Own address: " + web3.eth.accounts[0]) 

with open(pl.Path("./config/pubkey.txt"), "r") as f: 
 admin_address = web3.toChecksumAddress(f.read()) 

def whilel(): 
 for x in range(0, 40): 
    tx = startmarket.functions.getBuy().call() 
    ttx = startmarket.functions.getbuyerCount().call() 
    print(f"Buyer count: {ttx}") 
    print(f"Buyers: {tx}") 
    time.sleep(1) 
    fx = startmarket.functions.getSell().call() 
    ffx = startmarket.functions.getsellerCount().call() 
    print(f"Seller count: {ffx}") 
    print(f"Sellers: {fx}") 
    time.sleep(1) 
def start(): 
 global state 
 global startmarket
 global web3
 global admin_address
 global starttime 
 global endtime 
 startmarket.functions.OPENmarket().transact({ # Start Market
 "from": admin_address, 
 "gasPrice": 0, 
 } 
 ) 
 print("market is open") 
 whilel() 
 startmarket.functions.CLOSEmarket().transact( 
 { # Start Market
 "from": admin_address, 
 "gasPrice": 0, 
 } 
 ) 
 print("The market is now closed") 
 startmarket.functions.PROCESSINGmarket().transact( 
 { # Start Market
 "from": admin_address, 
 "gasPrice": 0, 
 } 
 ) 
 startmarket.functions.marketClearing().transact( 
 { # Start Market
 "from": admin_address, 
 "gasPrice": 0, 
 } 
 ) 
 time.sleep(8) 
 transx = startmarket.functions.gettrans().call() 
 print( 
 "-------------------SELL-------------------|pri|amt|---time---|---------------------BUY------------------"
 ) 
 for i in transx: 
    for j in i: 
        print(j, end=" ") 
 print() 
 startmarket.functions.marketClear().transact( 
        { # Make all to 0
        "from": admin_address, 
        "gasPrice": 0, 
        } 
 ) 
start() 