pragma solidity 0.6.3;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol';

contract CharityMaker {
    struct Token {
        bytes32 ticker;
        address tokenAddress;
    }
    
    struct CharityEvent {
        address payable recipient;
        string charityEventName;
        uint startDate;
        uint endDate;
        uint goalAmount;
        bool isApproved;
        string URI;
    }
    
    mapping(bytes32 => CharityEvent) public CharityEvents;

    event charityEventRegistration(
        uint charityEventID,
        string URI
    );
    
    event donation (
        string donorName,
        uint amount,
        uint charityEventID
    );
    
    constructor() public {
        donor = msg.sender;
    }

    function registerCharityEvent(
        string charityEventName,
        string recipient,
        uint goalAmount,
        uint startDate,
        uint endDate) public {return(str);
   
    }
    
    function updateCharityEventApproval(
        //check if admin
        uint charityEventID,
        bool _isApproved) 
        public 
        {return ();
        
    }
    
    function donate(
        uint charityEventID,
        string donorName) 
        public 
        {return ();
        
    }    
    
    function getCharityEvent(
        uint charityEventID) 
        public view
        {return ();
        
    } 
    
    function approveTransfer(uint id) external onlyApprover() {
        require(transfers[id].sent == false, 'transfer has already been sent');
        require(approvals[msg.sender][id] == false, 'cannot approve transfer twice');
        
        approvals[msg.sender][id] = true;
        transfers[id].approvals++;
        
        if(transfers[id].approvals >= quorum) {
            transfers[id].sent = true;
            address payable to = transfers[id].to;
            uint amount = transfers[id].amount;
            to.transfer(amount);
        }
    }    
    
    modifier onlyApprover() {
        bool allowed = false;
        for(uint i = 0; i < approvers.length; i++) {
            if(approvers[i] == msg.sender) {
                allowed = true;
            }
        }
        require(allowed == true, 'only approver allowed');
        _;
    }    
    
    
}