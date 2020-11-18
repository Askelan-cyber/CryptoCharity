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

load_dotenv()



def init_contract(abi_path: str, contract_address: str):
    """ Initialize a contract given the abi and address """
    with open(abi_path) as json_file:
        abi = json.load(json_file)
    return w3.eth.contract(address=contract_address, abi=abi)


charity_contract = init_contract("CharityMakerABI.json", os.getenv("CHARITY_MAKER_ADDRESS"))


def register_charity_event():
    # Need to have checks for each input

    event_name = input("Name of Charity Event: ")
    event_recipient = input("Name(s) of recipient(s): ")
    funding_goal = input("Goal amount for this event: ")
    start_date = input("Start date for this event(YYYY/MM/DD): ")
    end_date = input("End date for this event(YYYY/MM/DD): ")

    return crypto_charity.py.register_charity_event(event_name, event_recipient, funding_goal, start_date, end_date)


def update_charity_event_approval():
    # verification needs to be more sophisticated

    charity_event_id = input("What is the charity id?")
    verification = input("Does the event meet all the necessary requirements?")
    if verification == "Yes" or "yes" or "y" or "Y":
        is_approved = True
    elif verification == "No" or "no" or "N" or "n":
        is_approved = False

    return crypto_charity.py.update_charity_event_approval(charity_event_id, is_approved)

def donate(donor_private_key):
    # input donator name set to anon if none given
    # private key is global variable

    event_id = input("Please enter charity event id:")
    amount = input("Donation amount:")
    donor_name = input("Enter your name (Optional):")
    if donor_name == " ":
        return donor_name == "anonymous"

    return crypto_charity.py.donate(event_id, amount, donor_privatekey, donor_name)

# Is this going to be front end or mid level?

def view_all_donations():
    charity_event_id = ("Please enter event id:")
    view_options = "Would you like to view all donations for this event or just the top donations?"
    if view_options == "view all":
        return crypto_charity.py.get_total_donations(charity_event_id)
    
    elif view_options == "view top":

    # Is the private_key going to be the filter?

def view_own_donations(donor_private_key):
    personal_donations = charity_contract.events.Donate.createFilter(fromBlock="0x0",
                                                                #argument_filters={"charityEventID": charity_event_id})
    personal_donations_filter = personal_donations.get_all_entries()

    # loop through solidity returned list of objects and convert to list of dicts

    personal_donations_list = []
    for personal_donation in personal_donations_filter:
        personal_donations_list.append(toDict(personal_donation))

    # loop through donations_list and add up donorAmount from each donation
    
    total_personal_donations = 0
    for personal_donation in personal_donations_list:
        total_personal_donations += personal_donation['args']['donorAmount']

    return total_personal_donations_donations

    def view_list_charity_events():


def view_charity_event_info(event_id):

    return crypto_charity.py.get_charity_event(charity_event_id)

donor_wallet = input("Please enter your wallet address:")
donor_private_key = input("Please enter your private key:")

    option_menu = input(
        "What would you like to do? Options are: Register Charity Event, View Approval Status, Donate, View Donations, View Charity Events, Cancel Charity Events")

    if option_menu == "Register Charity Event":
        register_charity_event()

    elif option_menu == "Approve Charity event":
    # prompts for verification

    elif option_menu == "Update Approval Status":
       
        update_charity_event_approval(event_id)

    elif option_menu == "Donate":
        donate()

    elif option_menu == "View Donations":
        view_donations()

    elif option_menu == "View Charity Events":
        view_charity_events()

    elif option_menu == "Cancel Charity Event"
        cancel_charity_event()

    # options are register charity event, donate, see approval status, view donations, view active charities,

