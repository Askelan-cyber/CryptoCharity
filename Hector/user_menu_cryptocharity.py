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

    return crypto_charity.py.donate(event_id, amount, donor_private_key, donor_name)


# Is this going to be front end or mid level?

def view_all_donations():
    charity_event_id = input("Please enter charity event id:")
    view_options = input("Would you like to view all donations for this event or just the top donations?")
    if view_options == "view all":
        return crypto_charity.py.get_total_donations(charity_event_id)

    elif view_options == "view top 5 donations":
        top_donations = charity_contract.events.Donate.createFilter(fromBlock="0x0",
                                                                argument_filters={"charityEventID": charity_event_id})
        top_donations_filter = top_donations.get_all_entries()

        # loop through solidity returned list of objects and convert to list of dicts
        top_donations_list = []
        for top_donation in top_donations_filter:
            top_donations_list.append(toDict(top_donation))

        # loop through donations_list and add up donorAmount from each donation
        top_total_donations = 0
        for top_donation in top_donations_list:
            top_total_donations += top_donation['args']['donorAmount']
            sorted_top_total_donations = sorted(top_total_donations)
        return sorted_top_total_donations[5:]

# Is the private_key going to be the filter?

# def view_own_donations(donor_private_key):
#    personal_donations = charity_contract.events.Donate.createFilter(fromBlock="0x0",
                                                                     # argument_filters={"charityEventID": charity_event_id})
 #   personal_donations_filter = personal_donations.get_all_entries()

    # loop through solidity returned list of objects and convert to list of dicts

#    personal_donations_list = []
 #   for personal_donation in personal_donations_filter:
 #       personal_donations_list.append(toDict(personal_donation))

    # loop through donations_list and add up donorAmount from each donation

#    total_personal_donations = 0
#    for personal_donation in personal_donations_list:
#       total_personal_donations += personal_donation['args']['donorAmount']

#    return total_personal_donations

def view_list_charity_events():
    view_options = input("Would you like to see all currently active charity events or all past events?")
    if view_options == "See all active charity events":
        # search blockchain for all distinct charity event where end date > now and isApproved = True

    elif view_options == "See past charity events that have passed":
        #  search blockchain for all distinct charity event where end date < now and isApproved = True

def view_charity_event_info():
    charity_event_id = input("Please enter the charity event id that you would like information on?")
    return crypto_charity.py.get_charity_event(charity_event_id)

def cancel_charity_event():
    charity_event_id = input("Please enter the event id of the charity event you wish to cancel:")
    confirmation = input("Are you sure you wish to cancel this event?")
    if confirmation == "yes" or "y" or "Y" or "Yes":
        return crypto_charity.py.update_charity_event_approval(charity_event_id, False)

    elif confirmation == "no" or "n" or "N" or "No":
        return main_menu

donor_wallet = input("Please enter your wallet address:")
donor_private_key = input("Please enter your private key:")

main_menu = input(
    "What would you like to do? Options are: Register Charity Event, Update Approval Status, Donate, View Donations, View Charity Events, Cancel Charity Event")

if main_menu == "Register Charity Event":
    register_charity_event()

elif main_menu == "Update Approval Status":
    update_charity_event_approval()

elif main_menu == "Donate":
    donate()

elif main_menu == "View Donations":
    view_all_donations()

elif main_menu == "View Charity Event info":
    view_charity_event_info()

elif main_menu == "Cancel Charity Event":
    cancel_charity_event()
