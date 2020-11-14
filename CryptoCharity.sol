pragma solidity 0.6.3;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol';

contract CharityMaker {
    
    struct CharityEvent {
        address payable charityEventID;
        string charityEventName;
        uint startDate;
        uint endDate;
        uint goalAmount;
        bool isApproved;
        string URI;
    }
    
    struct donor {
        address payable recipient;
        string donorName;
        string donorAmount;
    }
    //not sure whether to use a public array or a mapped byte array
    donor[] public donors;
    CharityEvent[] public CharityEvents;
    //need help deciding on above or below use
    mapping(bytes32 => mapping(uint => CharityEvent[])) public charityBook;
    mapping(bytes32 => mapping(uint => donor[])) public donorBook;
    
    function getCharityEvents() external view returns(CharityEvent[] memory) {
        return CharityEvents;
    }
    
    function getDonors() external view returns(donor[] memory) {
        return CharityEvents;
    }    

    event charityEventRegistration(
        uint charityEventID,
        string URI
    );
    
    event donation (
        string donorName,
        uint amount,
        address payable charityEventID
    );
    

    function registerCharityEvent(
        string memory _charityEventName,
        uint _goalAmount,
        uint _startDate,
        uint _endDate,
        string memory _URI,
        bool _isApproved) public 
    {
        if(_isApproved == true) {
            .charityEventName = _charityEventName;
            
        } else {

        }   
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
    
    modifier setApproval() {
        bool allowed = false;
        require(allowed == true, 'only approver allowed');
        _;
    }    
    
    
}