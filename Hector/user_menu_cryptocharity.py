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

def register_charity_event():
    # charity_event_name: str, recipient: str, goal_amt: int,

    charity_event_name = input("Name of Charity Event: ")
    recipient_name = input("Name(s) of recipient(s): ")
    goal_amount = input("Goal amount for this event: ")
    start_date = input("Start date for this event: ")
    end_date = input("End date for this event: ")

    charity_event_object = {
        "charity_event_name": charity_event_name
        "recipient_name": recipient_name
        "goal_amount": goal_amount
        "start_date": start_date
        "end_date": end_date
    }

    return charity_event_object

def update_charity_event_approval(event_id):
    # charity_event_id: uint, is_approved: bool
    # where is_approved coming from

    if is_approved = True:
        print("Charity event has been approved.")
    elif is_approved = False:
        print("Charity event has not been approved.")

def donate():
    # event to donate to
    # amount to donate
    # Donators wallet address (I assume we need this)
    # Donators private key (using obscured input python function--can’t remember the name of it yet)
    # All above will feed to a donate python function, which will use web3 to pass back to the solidity contract function.

    identify_charity = input("Which charity event would you like to donate to?")
    donation = input("Donation amount:")
    # donator_wallet = input("What is your wallet address?")
    # donator_private_key = input("Please enter your private key")

def view_donations():

def view_charity_events():





option_menu= input("What would you like to do? Options are: Register Charity Event, View Approval Status, Donate, View Donations, View Charity Events, Cancel Charity Events")

if option_menu== "Register Charity Event":
    register_charity_event()

elif option_menu == "View Approval Status":
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
