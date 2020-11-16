# User “menu” actions:
#   Register_charity_event
#   Update_charity_event_approval
#   Donate
#   View_donations
#       Support filter by event id or all event
#   Return Top X donations in last x days
#       Use view_donations
#   View_active_charity_events
#   View_charity_event_history
#   get_charity_event
#   Cancel event > call update_charity_event_approval (example)
from web3.auto import w3
import json
import os
from dotenv import load_dotenv

def init_contract(abi_path:str, contract_address:str):
    """ Initialize a contract given the abi and address """
    with open(abi_path) as json_file:
        abi = json.load(json_file)
    return w3.eth.contract(address=contract_address, abi=abi)

charity_contract = init_contract("CharityMakerABI.json", os.getenv("CharityMaker_CONTRACT_ADDRESS"))

def register_charity_event():
    # charity_event_name: str, recipient: str, goal_amt: int,

    event_name = input("Name of Charity Event: ")
    event_recipient = input("Name(s) of recipient(s): ")
    funding_goal = input("Goal amount for this event: ")
    start_date = input("Start date for this event: ")
    end_date = input("End date for this event: ")

    return crypto_charity.py.register_charity_event(event_name, event_recipient, funding_goal, start_date, end_date) 

def update_charity_event_approval():
    # user sees charity name: eventid
    # charity_event_id: uint, is_approved: bool
    # where is_approved coming from
    # verification

    # input(What charity?)
      
    if is_approved = True:
        print("Charity event has been approved.")
    elif is_approved = False:
        print("Charity event has not been approved.")

    return crypto_charity.py.update_charity_event_approval(charity_event_id, approval status)

def donate(donor_privatekey):
    # input donator name set to anon if none given
    # private key is global variable

    event_id = input("Please enter charity event id:")
    amount = input("Donation amount:")
    donor_name = input("Enter your name (Optional):")
    if donor_name = " ":
        return donor_name = "anonymous"
    
    # return filename.donate(event_id, amount, donor_privatekey, donor_name)

def view_donations():

def view_list_charity_events():
    # view their event id here for reference

    # charity_event_reg_filter = charity_contract.events.charityEventRegistration.createFilter(fromBlock="0x0", argument_filters={"URI": event_URI})
    # charity_event_registrations = charity_event_reg_filter.get_all_entries()

    
    
    #return charity_event_registrations[-1].charityEventID
def view_charity_event_info(event_id):
    # event_info = file.get_charity_event_info(event_id)
    # print(event_info)


# donator_wallet = input("What is your wallet address?")
# donator_private_key = input("Please enter your private key")

option_menu= input("What would you like to do? Options are: Register Charity Event, View Approval Status, Donate, View Donations, View Charity Events, Cancel Charity Events")

if option_menu== "Register Charity Event":
    register_charity_event()

elif option_menu == "Approve Charity event":
    # prompts for verification

elif option_menu == "Update Approval Status":
    # Does the user know their event_id?
    # event_approval = input("What charity event?")
    update_charity_event_approval(event_id)

elif option_menu == "Donate":
 
    donate():

elif option_menu == "View Donations":
    view_donations()

elif option_menu == "View Charity Events":
    view_charity_events()

elif option_menu == "Cancel Charity Event"
    cancel_charity_event()

# options are register charity event, donate, see approval status, view donations, view active charities,

