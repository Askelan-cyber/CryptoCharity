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
        uint TestEventID,
        uint createDate,
        string URI 
    );
    
    event testEmit(
        uint TestEventID,
        string testText
    );
        

    function registerTestEvent(uint _createDate, string memory _URI) public returns(uint) {
        testEventIDs.increment();
        uint testEventID = testEventIDs.current();
        testEvents[testEventID] = testEvent(_createDate, _URI);
        
        emit testEventRegistration(testEventID, _createDate, _URI);
    }

    function testEmitEvent(string memory _testText) public {
        testEventIDs.increment();
        uint _testEventID = testEventIDs.current();
        emit testEmit(_testEventID, _testText);
    }

}