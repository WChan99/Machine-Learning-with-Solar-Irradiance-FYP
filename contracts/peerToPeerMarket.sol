pragma solidity >0.8.0;
// SPDX-License-Identifier: UNLICENSED
// reference: https://solidity.readthedocs.io/en/v0.5.3/style-guide.html
// @author: felix funk, felix.funk@faps.fau.de
// @title: sealed double auction contract

contract PeerToPeerMarket {

    struct offer{
        uint id;
        uint price;
        uint quantity;
    }

    address public owner;
    uint public executedCount;
    mapping(address => offer) public asks;
    mapping(address => offer) public bids;
    address[] public askers;
    address[] public bidders;

    // if isBid == true, offer is a bid, else its an ask
    event receivedOffer(address indexed agent, bool indexed isBid, uint price, uint quantity);
    event retractedOffer(address indexed agent, bool indexed isBid, uint price, uint quantity);
    event offerFulfilled(address indexed agent, bool indexed isBid);
    event executedTrade(uint indexed number, address indexed seller, address indexed buyer, uint price, uint quantity);

    constructor(address _owner){
        owner = _owner;
        executedCount = 0;
    }

    modifier onlyOwner(){
        require(msg.sender == owner, "Only the owner is authorized to do this");
        _;
    }

    function publishOffer(bool isBid, uint quantity, uint price)
    public{
        require(quantity>0, "No empty offers allowed");
        require(price>0, "No gifts allowed");
        if (isBid){
            if (bids[msg.sender].price>0){ // if bid already exists
                emit retractedOffer(msg.sender, quantity<0, price, quantity);
                bids[msg.sender]=offer(bidders.length, price, quantity);
            }else{
                bids[msg.sender]=offer(bidders.length, price, quantity);
                bidders.push(msg.sender); //create new entry if not
            }
        }else{
            if (asks[msg.sender].price>0){ // if ask already exists
                emit retractedOffer(msg.sender, quantity<0, price, quantity);
                asks[msg.sender]=offer(askers.length, price, quantity);
            }else{
                asks[msg.sender]=offer(askers.length, price, quantity);
                askers.push(msg.sender);
            }
        }
        emit receivedOffer(msg.sender, quantity<0, price, quantity);
    }

    function acceptOffer(bool isBid, address offerer, uint quantity)
    public{
        require(quantity>0, "No empty accepts allowed");    //not accepting nothing
        if (isBid){
            offer memory bid = bids[offerer]; //store locally for repeated checks and emits
            require(bid.quantity>0, "Offer does not exist");  //check if offer exists
            require(quantity<=bid.quantity, "Offer smaller than requested value"); //check if offer covers
            bids[offerer].quantity -= quantity; //update permanent storage value
            executedCount++; //increase the trades count
            emit executedTrade(executedCount, msg.sender, offerer, bid.price, quantity);
            if(bid.quantity == 0){
                emit offerFulfilled(offerer, isBid); // emit that this is now an empty offer
            }
        }else{
            offer memory ask = asks[offerer];
            require(ask.quantity>0, "Offer does not exist");
            require(quantity<=ask.quantity, "Offer smaller than requested value");
            asks[offerer].quantity -= quantity;
            executedCount++;
            emit executedTrade(executedCount, offerer, msg.sender, ask.price, quantity);
            if(ask.quantity == 0){
                emit offerFulfilled(offerer, isBid); // emit that this is now an empty offer
            }
        }
    }

    function retractOffer(bool isBid)
    public{
        if (isBid){
            emit retractedOffer(msg.sender, isBid, bids[msg.sender].price, bids[msg.sender].quantity);
            bids[msg.sender].quantity = 0;
        }else{
            emit retractedOffer(msg.sender, isBid, asks[msg.sender].price, asks[msg.sender].quantity);
            asks[msg.sender].quantity = 0;
        }
    }

    /*##############################################
    #########AUXILLIARY FUNCTIONS###################
    ##############################################*/

    function getAskerLength()
    public view 
    returns(uint){
        return askers.length;
    }

    function getBidderLength()
    public view 
    returns(uint){
        return bidders.length;
    }
}