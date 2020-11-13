# from logging import error
from web3.auto import w3
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

"""
Planned Functions:
    register_charity_event(charity_event_name: str, recipient: str, goal_amt: int, start_date: str, end_date: str)
    update_charity_event_approval(charity_event_id: uint, is_approved: bool)
    donate(charityEventId: uint, donorName: str, amount: int)
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

crypto_charity = init_contract("CryptoCharityABI.json", os.getenv("CRYPTO_CHARITY_ADDRESS"))

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


# DO NOT USE
# def register_owner(contact_info: dict, owner_address:str):

#     # use contact_info to create URI using pinata API
#     data = convertDataToJSON(contact_info)
#     ipfs_link = pinJSONtoIPFS(data)

#     # call contract to create new owner
#     tx_hash = AssetContract.functions.registerOwner(owner_address, ipfs_link)\
#         .transact({"from": w3.eth.accounts[0]})

#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     return receipt

def register_charity_event(event_name: str, event_recipient: str, funding_goal: int, start_date, end_date)
    
    # Backend parameters:
    # charityEvent (uint > struct)
    # recipient payable address
    # uint startDate
    # uint endDate
    # isApproved: bool
    # URI (link to IPFS): json format
    # chartiyEventName: str
    # Recipient address
    # uint GoalAmount

    
    # convert string start and end dates to datetime (if they aren't already datetime objects)
    if not isinstance(start_date, dt):
        start_date = dt.strptime(start_date, "%Y/%m/%d") # 1996/08/30
    if not isinstance(end_date, dt):
        end_date = dt.strptime(end_date, "%Y/%m/%d")

    # convert start and end datetimes to to unix timestamps
    start_date = start_date.timestamp()
    end_date = end_date.timestamp()

    # create URI for storing in pinata


    # create charity event with default isApproved: FALSE

    # return charity_event_id int
    return charity_event_id