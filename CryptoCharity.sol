pragma solidity 0.6.3;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol';
import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Counters.sol';

contract CharityMaker {
    
    using Counters for Counters.Counter;
    using SafeMath for uint;
    
    mapping(address => bool) public admins;
    
    Counters.Counter private CharityEventIDs;
    
    struct CharityEvent {
        address payable charityEventAddress;
        uint startDate;
        uint endDate;
        bool isApproved;
        string URI;
    }

    mapping(uint => CharityEvent) public charityBook;
        
    constructor() public {
        admins[msg.sender] = true;
    }
    
    event charityEventRegistration(
        uint _charityEventID,
        uint _startDate,
        uint _endDate,
        string _URI
    );    
    
    function registerCharityEvent(
        address payable _charityEventAddress,
        uint _startDate,
        uint _endDate,
        string memory _URI
        ) public returns (uint)
    {
        require(now >= _startDate  && now <= _endDate, "Start date must be after current date.");
        CharityEventIDs.increment();
        uint cID = CharityEventIDs.current();
        charityBook[cID] = CharityEvent(_charityEventAddress, _startDate, _endDate, false, _URI);
        emit charityEventRegistration(cID, _startDate, _endDate, _URI);
        return cID;
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
        uint startD = charityBook[_charityEventID].startDate;
        uint endD = charityBook[_charityEventID].endDate;
        require(now >= startD  && now <= endD, "Donation must be made within the start and end date parameters.");        
        require(charityBook[_charityEventID].isApproved == true, "This charity is currently unable to recieve funds.");
        address payable charityAddress = charityBook[_charityEventID].charityEventAddress;
        charityAddress.transfer(msg.value);
        emit Donate(_donorName, msg.value, _charityEventID);
    }      
}