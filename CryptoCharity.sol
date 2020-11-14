pragma solidity 0.6.3;

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
    
    mapping(uint => charityEventID) public charityBook;
    
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
        require(now >= startD  && now <= endD, "Start date must be after current date.");
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
        require(admins[msg.sender], "You do not have permission to approve charity events.");
        charityBook[_charityEventID].isApproved = _isApproved;
    }
    
    function updateAdmins(
        address admin, bool isAdmin) public {
        require(admins[msg.sender], "We know who you are!!!");
        admins[admin] = isAdmin;
    }
    
//Donor section
    
    event Donate(
        string donorName,
        uint donorAmount,
        uint charityEventID
    );      
    
    function donate(
        uint _charityEventID,
        string memory _donorName
        ) 
        public payable
    {
        uint startD = charityBook[CharityEventID].startDate;
        uint endD = charityBook[CharityEventID].endDate;
        require(now >= startD  && now <= endD, "Donation must be made within the start and end date parameters.");
        //get charity address
        address payable charityAddress = charityBook[CharityEventID].charityEventAddress;
        //transfer to charity address
        charityAddress.transfer(msg.value);
        //log payment to contract using the event Donate
        emit Donate(_donorName, msg.value, _charityEventID);
    }      
}