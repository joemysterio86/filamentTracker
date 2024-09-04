from models import FilamentRoll, FilamentRollPrints, db_uri
from other import filament_inventory_all, print_inventory_all
import time
import sqlalchemy as db
from sqlalchemy.orm import session, sessionmaker

engine = db.create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

def add_print(*args):
    entry = FilamentRollPrints(
        print_name=args[0],
        print_length=args[1],
        filament_id=args[2],
        )
    session.add(entry)
    session.commit()

def update_print(id, col, val):
    session.query(FilamentRollPrints).filter(FilamentRollPrints.print_id == id).update({col: val})
    session.commit()

def delete_print(id):
    session.query(FilamentRollPrints).filter(FilamentRollPrints.print_id == id).delete()
    session.commit()

def add_print_menu_selection():
    user_input = input("""
Update Menu:
    1) Brand
    2) Material
    3) Weight
    Q) Return to previous menu
                      

Please select an option: """)
    return user_input

def add_print_menu():
    filament_inventory_all()
    while True:
        filament_id = input("Please select which filament roll to add print to or Q to return to previous menu: ")
        if not filament_id:
            continue
        elif filament_id.lower().startswith("q"):
            return
        else:
            break
    while True:
        print_name = input("Please enter print name: ")
        if not print_name:
            continue
        elif print_name.lower().startswith("q"):
            return
        else:
            break
    while True:
        print_length = input("Please enter how many meters of filament was used (eg. 4.32): ")
        if not print_length:
            continue
        elif print_length.lower().startswith("q"):
            return
        else:
            break
    add_print(print_name, print_length, filament_id)
    print("Print has been added! Taking you back to Print Menu.\n")

def update_print_menu_selection(fila_roll_id):
    print_inventory_all(fila_roll_id)
    prints_list = [id for (id,) in session.query(FilamentRollPrints.filament_id == fila_roll_id)]
    print_selection = input("Please select the print you would like to update or Q to cancel: ")
    while True:
        if not print_selection:
            print("Please select one of the three options or  or Q to cancel:\n")
            continue
        elif print_selection.startswith("q"):
            break
        else:
            print_inventory_all(fila_roll_id)
            user_input = input("""
Update Menu:
1) Print Name
2) Print Length
Q) Return to previous menu
                    

Please select an option: """)
            if user_input.startswith("q"):
                break
            elif user_input == "1":
                while True:
                    print_update = input("Please enter new print name or Q to cancel: ")
                    if not print_update:
                        continue
                    elif print_update.lower().startswith("q"):
                        break
                    else:
                        update_print(print_selection, "print_name", print_update)
                        print("Entry has been update.")
                        time.sleep(0.5)
                        break
            elif user_input == "2":
                while True:
                    print_update = input("Please enter new print length or Q to cancel: ")
                    if not print_update:
                        continue
                    elif print_update.lower().startswith("q"):
                        break
                    else:
                        update_print(print_selection, "print_length", print_update)
                        print("Entry has been update.")
                        time.sleep(0.5)
                        break

def delete_print_menu_selection(fila_roll_id):
    print_inventory_all(fila_roll_id)
    prints_list = [id for (id,) in session.query(FilamentRollPrints.filament_id == fila_roll_id)]
    print_selection = input("Please select the print you would like to delete or Q to cancel: ")
    while True:
        if not prints_list:
            continue
        elif print_selection.startswith("q"):
            break
        else:
            delete_print(print_selection)
            print("Entry has been deleted.")
            time.sleep(0.5)
            break


def update_print_menu():
    filament_id_list = [id for (id,) in session.query(FilamentRoll.filament_id).order_by(FilamentRoll.filament_id)]
    while True:
        filament_inventory_all()
        filament_roll_choice = input("\n\nPlease enter Filament Roll ID to view/update associated prints, or Q to return to previous menu: ")
        if not filament_roll_choice:
            continue
        elif filament_roll_choice.lower().startswith("q"):
            break
        elif filament_roll_choice in str(filament_id_list):
            update_print_menu_selection(filament_roll_choice)


def delete_print_menu():
    filament_id_list = [id for (id,) in session.query(FilamentRoll.filament_id).order_by(FilamentRoll.filament_id)]
    while True:
        filament_inventory_all()
        filament_roll_choice = input("\n\nPlease enter Filament Roll ID to view/delete associated prints, or Q to return to previous menu: ")
        if not filament_roll_choice:
            continue
        elif filament_roll_choice.lower().startswith("q"):
            break
        elif filament_roll_choice in str(filament_id_list):
            delete_print_menu_selection(filament_roll_choice)


def prints_questions():
    while True:
        print_choices = input("""

Prints Menu:

    1) Add Prints.
    2) Update Prints.
    3) Delete Prints.
    Q) Return to Main Menu.


Please select an option: """)

        if not print_choices:
            time.sleep(0.5)
            continue
        elif print_choices.lower().startswith("q"):
            break
        elif print_choices == "1":
            add_print_menu()
        elif print_choices == "2":
            update_print_menu()
        elif print_choices == "3":
            delete_print_menu()

