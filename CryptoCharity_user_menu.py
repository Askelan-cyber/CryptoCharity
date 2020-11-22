from web3.auto import w3
import json
import os
from dotenv import load_dotenv
import crypto_charity
from pprint import pprint

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
    event_recipient = input("Enter Recipient address: ")
    funding_goal = input("Goal amount for this event: ")
    start_date = input("Start date for this event(YYYY/MM/DD): ")
    end_date = input("End date for this event(YYYY/MM/DD): ")

    print(f"{event_name} has been registered successfully.")
    return crypto_charity.register_charity_event(event_name, event_recipient, funding_goal, start_date, end_date)

def add_admin():
    admin_address = input("Enter admin address: ")
    admin_verification = input("Does this address meet all the necessary criteria to have admin privileges? (y/n) ")
    if admin_verification == "y":
        return crypto_charity.update_admins(admin_address, True)
    
    elif admin_verification == "n":
        return crypto_charity.update_admins(admin_address, False)

def update_charity_event_approval():
    # verification needs to be more sophisticated

    charity_event_id = int(input("What is the charity id? "))
    verification = input("Does the event meet all the necessary requirements? (y/n) ")
    if verification == "y":
        is_approved = True
        print(f"Charity event {charity_event_id} has been approved")
    elif verification == "n":
        is_approved = False
        print(f"Charity event {charity_event_id} is currently not approved.")
    return crypto_charity.update_charity_event_approval(charity_event_id, is_approved)

def donate():
    event_id = int(input("Please enter charity event id: "))
    amount = input("Donation amount: ")
    donor_name = input("Enter your name (Optional): ")
    if donor_name == " ":
        return donor_name == "anonymous"
    print(f"Donation of {amount} to charity event {event_id} was successful.")
    return crypto_charity.donate(event_id, amount, donor_name)

def view_total_donations():
    charity_event_id = int(input("Please enter charity event id: "))
    view_all_donations = crypto_charity.get_total_donations(charity_event_id)
    pprint(view_all_donations)

def view_itemized_donations():
    charity_event_id = int(input("Please enter charity event id or 0 for all: "))
    if charity_event_id == 0:
        donations = charity_contract.events.Donate.createFilter(fromBlock="0x0")
        donations_filter = donations.get_all_entries()

    else:
        donations = charity_contract.events.Donate.createFilter(fromBlock="0x0", argument_filters={"charityEventID": charity_event_id})
        donations_filter = donations.get_all_entries()
        
    donations_list = []
    for donation in donations_filter:
        donations_list.append(crypto_charity.toDict(donation))
    
    
    for donation in donations_list:
        pprint(f"Charity Event ID: {donation['args']['charityEventID']}, Donor Amount: {crypto_charity.wei_to_eth(donation['args']['donorAmount'])}, Donor Name {donation['args']['donorName']}")
 
def view_charity_event_info():
    charity_event_id = int(input("Please enter the charity event id that you would like information on? "))
    view_event_info = crypto_charity.get_charity_event(charity_event_id)
    pprint(view_event_info)
    return view_event_info

def cancel_charity_event():
    charity_event_id = int(input("Please enter the event id of the charity event you wish to cancel: "))
    confirmation = input("Are you sure you wish to cancel this event? (y/n) ")
    if confirmation == "y":
        print("Charity Event has been cancelled successfully.")
        return crypto_charity.update_charity_event_approval(charity_event_id, False)

    elif confirmation == "n":
        print("Charity Event was not cancelled.")

def view_all_charity_events():
    all_charity_events = charity_contract.events.charityEventRegistration.createFilter(fromBlock="0x0")
    all_charity_events_filter = all_charity_events.get_all_entries()
    
    charity_event_list = []
    for charity_event in all_charity_events_filter:
        charity_event_list.append(crypto_charity.toDict(charity_event))

    for charity_event in charity_event_list:
        #pprint(charity_event['args'])
        event_info = crypto_charity.get_charity_event(int(charity_event['args']['charityEventID']))
        pprint(event_info)
        print()
        
def show_menu(menu, header=""):
    a = 0
    if menu[-1] != "Exit":
        menu.append("Exit")
    while a != len(menu): 
        counter = 0
        print(f"\n{header}\n")
        for i in menu:
            counter += 1
            print(f"{counter} {i}")
        n = int(input("\nMake selection: "))
        opt =  menu[n-1]
        print(f"\nYou selected option {n}, {opt}\n")
        if n-1 in range(len(menu)):
            return n, opt

main_menu = ["Donor", "Recipient", "Charity Event Admin"]
donor_menu = ["View All Charity Events", "View Charity Event Information", "Donate", "View Total Donations", "View Itemized Donations"]
charity_admin_menu = ["View All Charity Events", "Register Charity Event", "Approve Charity Event", "Add Administrator", "View Charity Event Information", "Cancel Charity Event"]
recipient_menu = ["View All Charity Events", "View Total Donations", "View Itemized Donations", "View Charity Event Info"]

a = 0 
while a != len(main_menu):
    
    a,text = show_menu(main_menu, "Main Menu") 
    
    if a == 1:
        
        donor_menu_options = 0
        
        while donor_menu_options != len(donor_menu):
            
            donor_menu_options, donor_opt =  show_menu(donor_menu, "Donor Menu")
            
            if donor_menu_options == 1:
                view_all_charity_events()
                input("\nPress Enter to Continue")

            elif donor_menu_options == 2:
                view_charity_event_info()
                input("\nPress Enter to Continue")

            elif donor_menu_options == 3:
                donate()
                input("\nPress Enter to Continue")

            elif donor_menu_options == 4:
                view_total_donations()
                input("\nPress Enter to Continue")

            elif donor_menu_options == 5:
                view_itemized_donations()
                input("\nPress Enter to Continue")
        
    elif a == 2:
        
        recipient_menu_options = 0
        while recipient_menu_options != len(recipient_menu):
            
            recipient_menu_options, recipient_opt =  show_menu(recipient_menu, "Recipient Menu")
            if recipient_menu_options == 1:
                view_all_charity_events()
                input("\nPress Enter to Continue")
            
            elif recipient_menu_options == 2:
                view_total_donations()
                input("\nPress Enter to Continue")

            elif recipient_menu_options == 3:
                view_itemized_donations()
                input("\nPress Enter to Continue")

            elif recipient_menu_options == 4:
                view_charity_event_info()
                input("\nPress Enter to Continue")

    elif a == 3:
        charity_admin_menu_options = 0
        while charity_admin_menu_options != len(charity_admin_menu):
            charity_admin_menu_options, charity_admin_opt = show_menu(charity_admin_menu, "Charity Administrator Menu")
            
            if charity_admin_menu_options == 1:
                view_all_charity_events()
                input("\nPress Enter to Continue")

            if charity_admin_menu_options == 2:
                register_charity_event()
                input("\nPress Enter to Continue")

            elif charity_admin_menu_options == 3:
                update_charity_event_approval()
                input("\nPress Enter to Continue")

            elif charity_admin_menu_options == 4:
                add_admin()
                input("\nPress Enter to Continue")

            elif charity_admin_menu_options == 5:
                view_charity_event_info()
                input("\nPress Enter to Continue")

            elif charity_admin_menu_options == 6:
                cancel_charity_event()
                input("\nPress Enter to Continue")

