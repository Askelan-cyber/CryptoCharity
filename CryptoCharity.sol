pragma solidity 0.6.3;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol';

contract CharityMaker {
    
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
    
    address payable donor;
    
    constructor() public {
        donor = msg.sender;
    }

    function registerCharityEvent(
        string memory charityEventName,
        string memory recipient,
        uint goalAmount,
        uint startDate,
        uint endDate) public 
        
    {
   
    }
    
    function updateCharityEventApproval(
        //check if admin
        uint charityEventID,
        bool _isApproved) 
        public
    {
        
    }
    
    function donate(
        uint charityEventID,
        string memory donorName) 
        public 
    {
        
    }    
    
    function getCharityEvent(
        uint charityEventID) 
        public view
    {
        
    } 
    
    modifier onlyApprover() {
        bool allowed = false;
        require(allowed == true, 'only approver allowed');
        _;
    }    
    
    
}