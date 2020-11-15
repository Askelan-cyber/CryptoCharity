from logging import error
from web3.auto import w3
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from hexbytes import HexBytes

load_dotenv()

def init_contract(abi_path:str, contract_address:str):
    """ Initialize a contract given the abi and address """
    with open(abi_path) as json_file:
        abi = json.load(json_file)
    return w3.eth.contract(address=contract_address, abi=abi)

pinata_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def convertDataToJSON(content:dict):
    data = {
        "pinataOptions": {"cidVersion": 1},
        "pinataContent": content,
    }
    return json.dumps(data)

def pinJSONtoIPFS(json):
    req = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS", data=json, headers=pinata_headers
    )
    ipfs_hash = req.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"

# converts AttributeDict (including nested) to dict: reference and credit: vindard (https://github.com/vindard) https://github.com/ethereum/web3.py/issues/782
def toDict(dictToParse):
    # convert any 'AttributeDict' type found to 'dict'
    parsedDict = dict(dictToParse)
    for key, val in parsedDict.items():
        # check for nested dict structures to iterate through
        if  'dict' in str(type(val)).lower():
            parsedDict[key] = toDict(val)
        # convert 'HexBytes' type to 'str'
        elif 'HexBytes' in str(type(val)):
            parsedDict[key] = val.hex()
    return parsedDict

def get_testEventID_from_URI(event_URI: str):
    test_event_reg_filter = test_contract.events.testEventRegistration.createFilter(fromBlock="0x0", argument_filters={'URI': event_URI})
    test_event_registrations = test_event_reg_filter.get_all_entries()

    test_event_registrations_dict = toDict(test_event_registrations[0])

    return int(test_event_registrations_dict['args']['TestEventID'])

def register_test_event(event_name: str, event_recipient: str, funding_goal: int, create_date):

    # convert string start and end dates to datetime (if they aren't already datetime objects)
    if not isinstance(create_date, dt):
        create_date = dt.strptime(create_date, "%Y/%m/%d")

    # convert start and end datetimes to to unix timestamps
    create_date = create_date.timestamp()

    # create charity_info dict
    test_event_info = {
        "testEventName": event_name,
        # charityEventRecipient: event_recipient,
        "goalAmount": funding_goal
    }

    # convert charity_info to json_charity_info (json format) and pin to IPFS via pinata api function
    json_event_info = convertDataToJSON(test_event_info)
    ipfs_link = pinJSONtoIPFS(json_event_info)

    tx_hash = test_contract.functions.registerTestEvent(int(create_date), ipfs_link).transact({"from": w3.eth.accounts[0]})
    receipt  = w3.eth.waitForTransactionReceipt(tx_hash)

    test_event_id = get_testEventID_from_URI(ipfs_link)
    return test_event_id


abi='web3TransactTestABI.json'
# test_contract_address=""

test_contract = init_contract('web3TransactTestABI.json', os.getenv("TEST_CONTRACT_ADDRESS"))
# test_contract = init_contract(abi, test_contract_address)
# charity_contract = init_contract("CharityMakerABI.json", os.getenv("CHARITY_MAKER_ADDRESS"))

