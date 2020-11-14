pragma solidity 0.6.3;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol';

contract CharityMaker {
    
    using Counters for Counters.Counter;
    
    mapping(address => bool) public admins;
    admins[msg.sender] = true;
    
    Counters.Counter private CharityEventIDs;
    
    struct CharityEvent {
        address payable charityEventAddress;
        uint startDate;
        uint endDate;
        bool isApproved;
        string URI;
    }
    
    //need help deciding on above or below use
    mapping(uint => charityEventID) public charityBook;
    mapping(uint => recipientID) public donorBook;
    
    
    event charityEventRegistration(
        uint charityEventID,
        uint startDate,
        uint endDate        
    );    
    
    function registerCharityEvent(
        address payable _charityEventAddress,
        uint _startDate,
        uint _endDate,
        string memory _URI
        ) public return (uint)
    {
        CharityEventIDs.increment();
        uint CharityEventID = CharityEventIDs.current();
        charityBook[CharityEventID] = CharityEvent(_charityEventAddress, _startDate, _endDate, false, _URI);
        emit charityEventRegistration(CharityEventID, _startDate, _endDate);
        return CharityEventID;
    }
    
    function updateCharityEventApproval(
        //check if admin
        uint _charityEventID,
        bool _isApproved) 
        public
    {
        require(admins[msg.sender], "We know who you are!!!");
        charityBook[_charityEventID].isApproved = _isApproved;
    }
    
    function updateAdmins(
        address admin, bool isAdmin) public {
        require(admins[msg.sender], "We know who you are!!!");
        admins[admin] = isAdmin;
    }
    
    function getCharityEvent(
        uint charityEventID) 
        public view
    {    
    
    }
    
    function getCharityEvents(uint charityEventID) external view returns(bytes32) {
        return charityBook;
    }
    
    function getDonors(uint charityEventID) external view returns(bytes32) {
        return charityBook;
    }
    
    event donation (
        string donorName,
        uint amount,
        address payable charityEventID
    );
    
    
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
    
    
};
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
    
    modifier setApproval() {
        bool allowed = false;
        require(allowed == true, 'only approver allowed');
        _;
    }    
    
    
}