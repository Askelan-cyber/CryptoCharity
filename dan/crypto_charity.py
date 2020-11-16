from logging import error
from web3.auto import w3
import json
import requests
import os
from datetime import datetime as dt
from hexbytes import HexBytes

## Moved to front end / may not be needed
# from dotenv import load_dotenv

# # for ETH transactions
# from eth_account import Account

# # for obscuring STDIN input
# from getpass import getpass

# load_dotenv()


"""
Planned Functions:
    X- register_charity_event(charity_event_name: str, recipient: str, goal_amt: int, start_date: str, end_date: str)
    X- update_charity_event_approval(charity_event_id: uint, is_approved: bool)
    donate(charity_event_id: uint, amount: int, donor_name=None)
        Note: will need to accept “hidden” private key to submit payment
    X- get_charity_event(charity_event_id)
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
## Moved to front end
# def init_contract(abi_path:str, contract_address:str):
#     """ Initialize a contract given the abi and address """
#     with open(abi_path) as json_file:
#         abi = json.load(json_file)
#     return w3.eth.contract(address=contract_address, abi=abi)

# charity_contract = init_contract("CharityMakerABI.json", os.getenv("CHARITY_MAKER_ADDRESS"))

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
    # return f"ipfs://{ipfs_hash}"
    return ipfs_hash

def getJSONfromPinata(ipfs_hash):
    response = requests.get(f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
    return json.loads(response.text)

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

def get_charityEventID_from_URI(event_URI: str):
    charity_event_reg_filter = charity_contract.events.charityEventRegistration.createFilter(fromBlock="0x0", argument_filters={"URI": event_URI})
    charity_event_registrations = charity_event_reg_filter.get_all_entries()
    charity_event_registrations_dict = toDict(charity_event_registrations[0])
    return charity_event_registrations_dict['args']['charityEventID'])

def register_charity_event(event_name: str, event_recipient: str, funding_goal: int, start_date, end_date):

    # convert string start and end dates to datetime (if they aren't already datetime objects)
    if not isinstance(start_date, dt):
        start_date = dt.strptime(start_date, "%Y/%m/%d")  # 2020/01/26
    if not isinstance(end_date, dt):
        end_date = dt.strptime(end_date, "%Y/%m/%d")

    # check if start_date is in the past and if so make the start_date today instead
    today = dt.now()
    if start_date < today:
        start_date = today
    
    # check if end date is after start_date and return error if not
    if start_date > end_date:
        return error(f"Error: End Date {end_date} is before Start Date {start_date}")

    # convert start and end datetimes to to unix timestamps
    start_date = int(start_date.timestamp())
    end_date = int(end_date.timestamp())

    # create charity_info dict
    charity_info = {
        "charityEventName": event_name,
        # charityEventRecipient: event_recipient,
        "goalAmount": funding_goal
    }

    # convert charity_info to json_charity_info (json format) and pin to IPFS via pinata api function
    json_charity_info = convertDataToJSON(charity_info)
    ipfs_link = pinJSONtoIPFS(json_charity_info)

    # create charity event in the block chain
    tx_hash = charity_contract.functions.registerCharityEvent(event_recipient, start_date, end_date, ipfs_link).transact({"from": w3.eth.accounts[0]})
    receipt  = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # lookup registerCharityEvent events, filtering by the newly created ipfs_link (URI) to cross reference and return the newly generated charity event id
    charity_event_id = get_charityEventID_from_URI(ipfs_link)

    return charity_event_id

def update_charity_event_approval(charity_event_id: uint, is_approved: bool):
    # call contract funtion to update approval
    tx_hash = charity_contract.functions.updateCharityEventApproval(charity_event_id, is_approved)\
        .transact({"from": w3.eth.accounts[0]})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

def donate(charity_event_id: int, amount: int, donor_name='Anonymous'):
    donate_tx_hash = charity_contract.functions.donate(charity_event_id, donor_name).transact({"value": amount, "from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(donate_tx_hash)
    return receipt

def get_total_donations(charity_event_id):
    donations = charity_contract.events.Donate.createFilter(fromBlock="0x0", argument_filters={"charityEventID": charity_event_id})
    donations_filter = donations.get_all_entries()

    # loop through solidity returned list of objects and convert to list of dicts
    donations_list = []
    for donation in donations_filter:
        donations_list.append(toDict(donation))

    # loop through donations_list and add up donorAmount from each donation
    total_donations = 0
    for donation in donations_list:
        total_donations += donation['args']['donorAmount']
        
    return total_donations

def get_charity_event(charity_event_id):
    solidity_info = charity_contract.functions.getCharityEventInfo(charity_event_id).call()

    ipfs_hash = solidity_info[5]
    charity_ipfs_data = getJSONfromPinata(ipfs_hash)
    
    charity_event_info = {
        "charityEventName": charity_ipfs_data['charityEventName'],
        "charityEventID": charity_event_id,
        "charityEventAddress": solidity_info[1],
        "startDate": dt.utcfromtimestamp(solidity_info[2]).strftime('%Y/%m/%d'),
        "endDate": dt.utcfromtimestamp(solidity_info[3]).strftime('%Y/%m/%d'),
        "goalAmount": charity_ipfs_data['goalAmount'],
        "totalDonations": get_total_donations(charity_event_id),
        "isApproved": solidity_info[4],
        "ipfsHash": solidity_info[5],
        "ipfsLink": f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    }

    return charity_event_info

### May not be needed
# def create_raw_tx(account, recipient, amount):
#     gasEstimate = w3.eth.estimateGas(
#         {"from": account.address, "to": recipient, "value": amount}
#     )
#     return {
#         "from": account.address,
#         "to": recipient,
#         "value": amount,
#         "gasPrice": w3.eth.gasPrice,
#         "gas": gasEstimate,
#         "nonce": w3.eth.getTransactionCount(account.address),
#     }

# def send_tx(account, recipient, amount):
#     tx = create_raw_tx(account, recipient, amount)
#     signed_tx = account.sign_transaction(tx)
#     result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     print(result.hex())
#     return result.hex()

# THIS IS INCOMPLETE AND NOT YET FUNCTIONAL   
def donate(charity_event_id: uint, amount: int, donor_wallet, donor_private_key, donor_name)


    # tx_hash = charity_contract.functions.donate(charity_event_id, donor_name)\
    #     .transact({"from": w3.eth.accounts[0]})

    # receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    ### Reference: https://web3py.readthedocs.io/en/stable/examples.html#using-infura-rinkeby-node
    transaction = charity_contract.functions.donate(charity_event_id, donor_name).buildTransaction()
    transaction.update({ 'gas' : appropriate_gas_amount })
    transaction.update({ 'nonce' : w3.eth.getTransactionCount(donor_wallet) })
    signed_tx = w3.eth.account.signTransaction(transaction, donor_private_key)


    return receipt

# code snippets:
# updateCharityEventApproval
# contract.functions.test(52).call()




# user input : register 
# event_id
# 1. register
# 2. view past events