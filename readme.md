# BLEM setup

The contents of this folder allow the easy setup of a BLEM, including blockchain nodes, contract deployment and agent distribution.


## Contents

- contracts: the Solidity smart contracts for a sealed double auction marketplace and an always accepting marketplace
- py: the scripts necessary to run the agents and coordinate interaction with the marketplace
- networkCreator.py: a script which creates PoA network with a desired number of nodes
- contractDeployer.py: a script which deploys the sealed double auction contract
- referenceGenesis.json: a blockchain configuration which serves as basis for every newly generated network

## Description

This project can be used to set up a Proof of Authority network using Geth's integrate Clique consensus mechanism.
For simplicity, only one node (node0) is designated as a signer initially. node0 is also designated as the so-called timer, being the only node allowed to change the marketplace's phase (commit/reveal) and start new trading periods. 
All other nodes merely import chain segments from node0, however, they can be added as signers using clique.propose(address, bool) in the Geth console. More information here: https://geth.ethereum.org/docs/rpc/ns-clique


## Setup guide

1. Run networkCreator.py in the main directory
2. Start node0 by executing startnode.cmd in /node0/
3. Run contractDeployer.py in the main directory
4. [Optional] Shut down node0 (ctrl-d)
5. [Optional] Distribute the node folders across devices as desired
6. Start the individual nodes by executing the respective startnode.cmd in their respective directories
7. Get the marketplace running by launching timing.py in /node0/py
8. Start the agents for nodes 1-n by launching threadedServer.py in the /py directories
9. Start an ibaLogic Simulation with the correctly configured IPs and ports (counting up from 48174)


## Required
### For Blockchain
Geth v1.10.15 (on pi: download, tar -xvf, cd, chmod +x geth, sudo mv geth /usr/local/bin/)
pip install web3
[Optional] py-solc-x on the machine which compiles the contract

### For Agents
pip install pulp==1.6.8
pip install pandas
[Optional] sudo apt-get install libatlas-base-dev (to make numpy work on raspi)
