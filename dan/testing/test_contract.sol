pragma solidity ^0.5.0;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol';

contract web3TransactTest {
    using Counters for Counters.Counter;

    Counters.Counter private testEventIDs;

    struct testEvent {
    // address payable charityEventAddress;
    uint createDate;
    // uint endDate;
    // bool isApproved;
    string URI;
    }

    mapping(uint => testEvent) public testEvents;

    event testEventRegistration(
        uint TestEventID
        uint createDate,
        string URI 
    );

    function registerTestEvent(uint _createDate, string memory _URI) public returns(uint) {
        testEventIDs.increment();
        uint _testEventID = testEventIDs.current();
        
        emit testEventRegistration(_testEventID, _createDate, _URI)
    }

}