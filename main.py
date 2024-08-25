import time
from other import view_inventory
from filament import filament_questions
from prints import prints_questions
from spool import spool_questions

def menu():
    while True:
        print(f"""What would you like to do?

    1) View Inventory Data (Overview)
    2) Filament (View/Add/Update/Delete)
    3) Prints (View/Add/Update/Delete)
    4) Spool Data (View/Add/Update/Delete)
    Q) Exit.

    """)
        choice = input("Please select an option: ")
        if choice.lower() == "q":
            print("You selected Q, exiting...")
            exit()
        elif choice == "1":
            view_inventory()
        elif choice == "2":
            filament_questions()
        elif choice == "3":
            prints_questions()
        elif choice == "4":
            spool_questions()
        else:
            print("\nPlease select an appropriate option!")
            time.sleep(.5)

menu()
