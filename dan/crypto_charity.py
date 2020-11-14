# from logging import error
from web3.auto import w3
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime as dt

# for ETH transactions
from eth_account import Account

# for obscuring STDIN input
from getpass import getpass


load_dotenv()

"""
Planned Functions:
    register_charity_event(charity_event_name: str, recipient: str, goal_amt: int, start_date: str, end_date: str)
    update_charity_event_approval(charity_event_id: uint, is_approved: bool)
    donate(charity_event_id: uint, amount: int, donor_name=None)
    Note: will need to accept “hidden” private key to submit payment
    get_charity_event(charity_event_id)
    view_active_charity_events()
    Note: return loop of get_charity_event
    view_charity_event_history()
    Note: return loop of get_charity_event
    View_donations(event_id=0, donor_id=0)

Planned User interface actions:
    Register_charity_event 	
    Update_charity_event_approval
    Donate
    View_donations
    Support filter by event id or all event
    Return Top X donations in last x days
    Use view_donations
    View_active_charity_events
    View_charity_event_history
    get_charity_event
    Cancel event > call update_charity_event_approval (example)

"""

def init_contract(abi_path:str, contract_address:str):
    """ Initialize a contract given the abi and address """
    with open(abi_path) as json_file:
        abi = json.load(json_file)
    return w3.eth.contract(address=contract_address, abi=abi)

charity_contract = init_contract("CharityMakerABI.json", os.getenv("CHARITY_MAKER_ADDRESS"))

headers = {
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
        "https://api.pinata.cloud/pinning/pinJSONToIPFS", data=json, headers=headers
    )
    ipfs_hash = req.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"


def get_charityEventID_from_URI(event_URI: str):
    
    charity_event_reg_filter = charity_contract.events.charityEventRegistration.createFilter(fromBlock="0x0", argument_filters={"URI": event_URI})
    charity_event_registrations = charity_event_reg_filter.get_all_entries()

    
    
    return charity_event_registrations[-1].charityEventID

# THIS IS INCOMPLETE AND NOT YET FUNCTIONAL
def register_charity_event(event_name: str, event_recipient: str, funding_goal: int, start_date, end_date)

    # convert string start and end dates to datetime (if they aren't already datetime objects)
    if not isinstance(start_date, dt):
        start_date = dt.strptime(start_date, "%Y/%m/%d") # 2020/01/26
    if not isinstance(end_date, dt):
        end_date = dt.strptime(end_date, "%Y/%m/%d")

    # convert start and end datetimes to to unix timestamps
    start_date = start_date.timestamp()
    end_date = end_date.timestamp()

    # create charity_info dict
    charity_info = {
        charityEventName: event_name,
        # charityEventRecipient: event_recipient,
        goalAmount: funding_goal
    }

    # convert charity_info to json_charity_info (json format) and pin to IPFS via pinata api function
    json_charity_info = convertDataToJSON(charity_info)
    ipfs_link = pinJSONtoIPFS(json_charity_info)

    # create charity event in the block chain
    # registryCharityEvent(payable address recipient, uint startDate, uint endDatestr memory eventURI) public 
    tx_hash = charity_contract.functions.registryCharityEvent(event_recipient, start_date, end_date, ipfs_link).transact({"from": w3.eth.accounts[0]})
    receipt  = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # obtain charity_event_id from block chain event
        # ??how do we return the charity event id from the solidity contract when we've used web3 .transact to call the function that would logically return the charity event id?? 
        # We know the solidity registerCharityEvent will also emit an event on the block chain--perhaps we retrieve the charity event id from that, but how do we isolate the correct
        # event without already knowing the charity id?  Does it make sense to try to use the URI to do an event lookup to then return the charity event id?
    charity_event_id = get_charityEventID_from_URI(ipfs_link)

    return charity_event_id

def update_charity_event_approval(charity_event_id: uint, is_approved: bool)
    # call contract funtion to update approval
    tx_hash = charity_contract.functions.updateCharityEventApproval(charity_event_id, is_approved)\
        .transact({"from": w3.eth.accounts[0]})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


def create_raw_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }


def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

# THIS IS INCOMPLETE AND NOT YET FUNCTIONAL   
def donate(charity_event_id: uint, amount: int, donor_name=None)


    # tx_hash = charity_contract.functions.donate(charity_event_id, donor_name)\
    #     .transact({"from": w3.eth.accounts[0]})

    # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

# code snippets:
# updateCharityEventApproval
# contract.functions.test(52).call()




user input : register 
event_id
1. register
2. view past events