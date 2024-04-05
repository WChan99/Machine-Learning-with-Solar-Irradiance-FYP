pragma solidity >0.8.0; 
// SPDX-License-Identifier: UNLICENSED
// reference: https://solidity.readthedocs.io/en/v0.5.3/styleguide.html
// @author: felix funk, felix.funk@faps.fau.de
// @title: sealed double auction contract
contract Marketsetting { 
    string public name = "Energy P2P"; 
    address owner; 
    uint256 openingTime; 
    uint256 closingTime; 
    uint256 currentTime; 
    uint256 public seller_number; //3
    uint256 seller_count; 
    uint256 public buyer_number; //3
    uint256 buyer_count; 
    uint256 max_number; 
    enum marketstate { 
        OPEN, 
        CLOSED, 
        PROCESSING
    } 
    marketstate public marketstatep; 
    event buyerInfo( 
        address indexed _nodeAddress, 
        uint256 difference, 
        uint256 price
    ); 
    event sellerInfo( 
        address indexed _nodeAddress, 
        uint256 difference, 
        uint256 price
    ); 
    event ClearedAmount(uint256 buy, uint256 sell); 
    event PriceCleared(uint256 price, uint256 quantity); 
    event clearedOffer( 
        address indexed agent, 
        uint256 price, 
        uint256 quantity, 
        uint256 timestamp, 
        string status
    ); 
    struct ClearedOffer { 
        address seller; 

        uint256 price; 
        uint256 energy; 
        uint256 timestamp; 
        address buyer; 
    } 
    struct SellOrders { 
        address seller; 
        uint256 price; 
        uint256 energy; 
        uint256 timestamp; 
    } 
    struct BuyOrders { 
        address buyer; 
        uint256 price; 
        uint256 energy; 
        uint256 timestamp; 
    } 
    SellOrders[] public sellOrders; 
    BuyOrders[] public buyOrders; 
    ClearedOffer[] public clearedoffer; 
    constructor(address timer) { 
        owner = timer; 
        marketstatep = marketstate.CLOSED; 
    } 
    modifier onlyOwner() { 
        require(msg.sender == owner, "Only the owner is authorized to do this"); 
        _; 
    }
    modifier onlyWhileOpen() { 
        require( 
            block.timestamp >= openingTime && block.timestamp <= 
            closingTime, 
            "Auction has closed, please wait for the next auction"
        ); 
        _; 
    } 
    function getsellerCount() public view returns (uint256) { 
        return (seller_count); 
    } 

    function getbuyerCount() public view returns (uint256) { 
        return (buyer_count); 
    } 
    function getBuy() public view returns (BuyOrders[] memory) { 
        return buyOrders; 
    } 
    function gettrans() public view returns (ClearedOffer[] memory) 
    { 
        return clearedoffer; 
    } 
    function getSell() public view returns (SellOrders[] memory) { 
        return sellOrders; 
    } 
    function OPENmarket() public onlyOwner { 
        require(marketstatep == marketstate.CLOSED, "Can't open market yet"); //if market not closed , cant open
        marketstatep = marketstate.OPEN; //market open, create time stamps and close market after 1 min
        openingTime = block.timestamp; 
        closingTime = block.timestamp + 1 minutes; 
    } 
    function CLOSEmarket() public onlyOwner { 
        //if market not open, cant close
        marketstatep = marketstate.CLOSED; // market is closed, proceed to process trades
    } 
    //if there is orders for both
    function PROCESSINGmarket() public onlyOwner { 
        uint256 i = 0; 
        uint256 j = 0; 
        uint256 buyeramount = 0; 
        uint256 selleramount = 0; 
        uint256 prevdiffbuyer = 0; 
        uint256 prevdiffseller = 0; 
        uint256 n = 0; 
        uint256 _timestamp = block.timestamp; 
        marketstatep = marketstate.PROCESSING; 
        if ( 
                buyOrders.length > 0 && 
                sellOrders.length > 0 && 
                buyOrders[0].price >= sellOrders[0].price 
            ) { 
                while (buyOrders[i].price >= sellOrders[j].price && n < 10) n++; 
                { 
                    buyeramount = buyOrders[(i)].energy - prevdiffbuyer; 
                    selleramount = sellOrders[(j)].energy - 
                    prevdiffseller; 
                    if (buyeramount > selleramount) { 
                        clearedoffer.push( 
                        ClearedOffer({ 
                            seller: sellOrders[(j)].seller, 
                            price: sellOrders[(i)].price, 
                            energy: selleramount, 
                            timestamp: _timestamp, 
                            buyer: buyOrders[(j)].buyer 
                            }) 
                        ); 
                        prevdiffbuyer = selleramount; 
                        prevdiffseller = 0; 
                        j += 1; 
                    } else if (selleramount > buyeramount) { 
                        clearedoffer.push( 
                        ClearedOffer({ 
                            seller: sellOrders[(i)].seller, 
                            price: sellOrders[(j)].price, 
                            energy: buyeramount, 
                            timestamp: _timestamp, 
                            buyer: buyOrders[(j)].buyer 
                            }) 
                        ); 
                        prevdiffseller = buyeramount; 
                        prevdiffbuyer = 0; 
                        i += 1; 
                    } else { 
                        clearedoffer.push( 
                        ClearedOffer({ 
                            seller: sellOrders[(j)].seller, 
                            price: sellOrders[(i)].price, 
                            energy: selleramount, 
                            timestamp: _timestamp, 
                            buyer: buyOrders[(j)].buyer 
                        }) 
                    ); 
                        clearedoffer.push( 
                        ClearedOffer({ 
                            seller: sellOrders[(i)].seller, 
                            price: sellOrders[(j)].price, 
                            energy: buyeramount, 
                            timestamp: _timestamp, 
                            buyer: buyOrders[(j)].buyer 
                        }) 
                    ); 
                    prevdiffbuyer = 0; 
                    prevdiffseller = 0; 
                    i += 1; 
                    j += 1; 
                } 
            } 
        } 
    } 
    function sellBuyEnergy(int256 price, int256 difference) 
        public
        returns (int256 moneyearn) 
    { 
        moneyearn = price * difference; 
        return moneyearn; 
    } 
    function sellbuy( 
        uint256 price, 
        uint256 difference, 
        uint256 buyer
    ) public onlyWhileOpen { 
        uint256 _timestamp = block.timestamp; 
        // 0 is Seller, 99 is Buyer
        if (buyer == 0) { 
            sellOrders.push( 
                SellOrders({ 
                    seller: msg.sender, 
                    price: price, 
                    energy: difference, 
                    timestamp: _timestamp 
                }) 
            ); 
            seller_count = seller_count + 1; 
            sortSellOrder(0, int256(sellOrders.length - 1)); 
        } else { 
            buyOrders.push( 
                BuyOrders({ 
                    buyer: msg.sender, 
                    price: price, 
                    energy: difference, 
                    timestamp: _timestamp 
                }) 
            ); 
            buyer_count = buyer_count + 1; 
            sortBuyOrder(0, int256(buyOrders.length - 1)); 
        } 
    } 
    function sortSellOrder(int256 start, int256 end) internal { 
        int256 i = start; 
        int256 j = end; 
        uint256 length = 0; 
        uint256 pivotIndex = uint256(start + (end - start) / 2); 
        uint256 pivot = sellOrders[pivotIndex].price; 
        while (i <= j) { 
            while (sellOrders[uint256(i)].price < pivot) i++; 
            while (sellOrders[uint256(j)].price > pivot) j--; 
            if (i <= j) { 
                sellOrders.push( 
                    SellOrders({ 
                        seller: sellOrders[uint256(i)].seller, 
                        price: sellOrders[uint256(i)].price, 
                        energy: sellOrders[uint256(i)].energy, 
                        timestamp: sellOrders[uint256(i)].timestamp 
                    }) 
                ); 
                length = uint256(sellOrders.length - 1); 
                sellOrders[uint256(i)] = sellOrders[uint256(j)]; 
                sellOrders[uint256(j)] = sellOrders[length]; 
                sellOrders.pop(); 
                i++; 
                j--; 
            } 
        } 
        if (start < j) sortSellOrder(start, j); 
        if (i < end) sortSellOrder(i, end); 
    } 
    function sortBuyOrder(int256 start, int256 end) internal { 
        int256 i = start; 
        int256 j = end; 
        uint256 length = 0; 
        uint256 pivotIndex = uint256(start + (end - start) / 2); 
        uint256 pivot = buyOrders[pivotIndex].price; 
        while (i <= j) { 
            while (buyOrders[uint256(i)].price > pivot) i++; 
            while (buyOrders[uint256(j)].price < pivot) j--; 
            if (i <= j) { 
                buyOrders.push( 
                    BuyOrders({ 
                        buyer: buyOrders[uint256(i)].buyer, 
                        price: buyOrders[uint256(i)].price, 
                        energy: buyOrders[uint256(i)].energy, 
                        timestamp: buyOrders[uint256(i)].timestamp 
                    }) 
                ); 
                length = uint256(buyOrders.length - 1); 
                buyOrders[uint256(i)] = buyOrders[uint256(j)]; 
                buyOrders[uint256(j)] = buyOrders[length]; 
                buyOrders.pop(); 
                i++; 
                j--; 
            } 
        } 
        if (start < j) sortBuyOrder(start, j); 
        if (i < end) sortBuyOrder(i, end); 
    } 
    function marketClear() public onlyOwner { 
        require( 
            marketstatep == marketstate.PROCESSING, 
            "Cant clear market yet"
        ); 
        delete sellOrders; 
        delete buyOrders; 
        buyer_count = 0; 
        seller_count = 0; 
        marketstatep = marketstate.CLOSED; 
    } 
    modifier marketCLOSED() { 
        require(marketstatep == marketstate.CLOSED, "Market s open"); 
        _; 
    } 
    modifier marketOPEN() { 
        require(marketstatep == marketstate.OPEN, "Market is not open "); 
        _; 
    } 
    modifier marketPROCESSING() { 
        require( marketstatep == marketstate.PROCESSING, "Market is not processing yet"
        ); 
        _; 
    } 
    function marketClearing() public onlyOwner { 
        require(block.timestamp > closingTime); 
        int256 i = 0; 
        int256 j = 0; 
        int256 feasible_i = 0; 
        int256 feasible_j = 0; 
        uint256 buy_sum = 0; 
        uint256 sell_sum = 0; 
        uint256 cumulated = 0; 
        uint256 price = 0; 
        uint256 quantity = 0; 
        marketstatep == marketstate.PROCESSING; 
        if ( 
            buyOrders.length > 0 && 
            sellOrders.length > 0 && 
            buyOrders[0].price >= sellOrders[0].price 
        ) { 
            while ( 
                buyOrders[uint256(i)].price >= sellOrders[uint256(j)].price 
            ) { 
                if (buy_sum == sell_sum) { 
                    buy_sum += buyOrders[uint256(i)].energy; 
                    sell_sum += sellOrders[uint256(j)].energy; 
                } else if (buy_sum > sell_sum) { 
                    sell_sum += sellOrders[uint256(j)].energy; 
                } else if (buy_sum < sell_sum) { 
                    buy_sum += buyOrders[uint256(i)].energy; 
                } 
                feasible_i = i; 
                feasible_j = j; 
                if (buy_sum > sell_sum) { 
                    j++; 
                } else if (buy_sum < sell_sum) { 
                    i++; 
                } else { 
                    i++; 
                    j++; 
                } 
                if ( 
                    (i >= int256(buyOrders.length)) || 
                    (j >= int256(sellOrders.length)) 
                ) { 
                    break; 
                } 
            } 
            price = uint256( 
                (sellOrders[uint256(feasible_j)].price + 
                    buyOrders[uint256(feasible_i)].price) / 2
            ); 
            if (buy_sum > sell_sum) { 
                quantity = sell_sum; 
            } else { 
                quantity = buy_sum; 
            } 
            emit ClearedAmount(buy_sum, sell_sum); 
            emit PriceCleared(price, quantity); 
            for (uint256 z = 0; z < uint256(sellOrders.length); z++) 
            { 
                if (cumulated < quantity) { 
                    if (cumulated + sellOrders[z].energy <= quantity) { 
                        // fully cleared
                        emit clearedOffer( 
                            sellOrders[z].seller, 
                            price, 
                            sellOrders[z].energy, 
                            block.timestamp, 
                            "Sold"
                        ); 
                    } else { 
                        //partially cleared
                        emit clearedOffer( 
                            sellOrders[z].seller, 
                            price, 
                            quantity - cumulated, 
                            block.timestamp, 
                            "Sold"
                        ); 
                    } 
                } else { 
                    //fully served by grid
                    emit clearedOffer( 
                        sellOrders[z].seller, 
                        0, 
                        0, 
                        block.timestamp, 
                        "Bid unsuccessful"
                    ); 
                } 
                cumulated += sellOrders[z].energy; 
            } 
            cumulated = 0; 
            for (uint256 y = 0; y < uint256(buyOrders.length); y++) 
            { 
                if (cumulated < quantity) { 
                    if (cumulated + buyOrders[y].energy <= quantity) 
                    { 
                        // fully cleared
                        emit clearedOffer( 
                            buyOrders[y].buyer, 
                            price, 
                            buyOrders[y].energy, 
                            block.timestamp, 
                            "Bought"
                        ); 
                    } else { 
                        //partially cleared
                        emit clearedOffer( 
                            buyOrders[y].buyer, 
                            price, 
                            quantity - cumulated, 
                            block.timestamp, 
                            "Bought"
                        ); 
                    } 
                } else { 
                    //fully served by grid
                    emit clearedOffer( 
                        buyOrders[y].buyer, 
                        0, 
                        0, 
                        block.timestamp, 
                        "Bid unsuccessful"
                    ); 
                } 
                cumulated += buyOrders[y].energy; 
            } 
            delete sellOrders; 
            delete buyOrders; 
        } else { 
            emit ClearedAmount(buy_sum, sell_sum); 
            emit PriceCleared(price, quantity); 
            delete sellOrders; 
            delete buyOrders; 
        } 
    } 
} 
