from models import FilamentRoll, db_uri
from other import filament_inventory_all, filament_inventory_general
import time
import sqlalchemy as db
from sqlalchemy.orm import session, sessionmaker

engine = db.create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

def add_filament(*args):
    entry = FilamentRoll(
        name=args[0],
        brand=args[1],
        color=args[2],
        cost=args[3],
        roll_weight=args[4],
        diameter=args[5],
        spool_material=args[6],
        )
    session.add(entry)
    session.commit()

def update_filament(id, col, val):
    session.query(FilamentRoll).filter(FilamentRoll.filament_id == id).update({col: val})
    session.commit()

def delete_filament(id):
    session.query(FilamentRoll).filter(FilamentRoll.filament_id == id).delete()
    session.commit()

def add_filament_menu():
    print("Press Q if you need to cancel and return to previous menu.\n")
    while True:
        name = input("Please enter filament nickname (example: Inland PLA+ Black Roll #1): ")
        if not name:
            continue
        elif name.lower().startswith("q"):
            return
        else:
            break
    while True:
        brand = input("Please enter filament brand: ")
        if not brand:
            continue
        elif brand.lower().startswith("q"):
            return
        else:
            break
    while True:
        color = input("Please enter filament color: ")
        if not color:
            continue
        elif color.lower().startswith("q"):
            return
        else:
            break
    while True:
        cost = input("Please enter cost of filament roll: ")
        if not cost:
            continue
        elif cost.lower().startswith("q"):
            return
        else:
            break
    while True:
        weight = input("Please enter filament roll weight in grams : ")
        if not weight:
            continue
        elif weight.lower().startswith("q"):
            return
        else:
            break
    while True:
        diameter = input("Please enter cost filament diameter size (example: 1.75): ")
        if not diameter:
            continue
        elif diameter.lower().startswith("q"):
            return
        else:
            break
    while True:
        spool_material = input("Please enter filament spool material: ")
        if not spool_material.lower():
            continue
        elif spool_material.lower().startswith("q"):
            return
        else:
            break
        
    add_filament(name, brand, color, cost, weight, diameter, spool_material)
    print("Filament has been added! Taking you back to Add Filament Menu.\n")
    time.sleep(1)

def update_filament_menu_selection():
    user_input = input("""
Update Menu:
    1) Nickname
    2) Brand
    3) Color
    4) Cost
    5) Roll Weight
    6) Diameter
    7) Spool Material
    8) Finished Roll?
    Q) Return to previous menu
                      

Please select an option: """)
    return user_input

def update_filament_menu():
    id_list = [id for (id,) in session.query(FilamentRoll.filament_id).order_by(FilamentRoll.filament_id)]
    while True:
        filament_inventory_all()
        filament_update_choice = input("\n\nPlease enter an ID to update, or Q to return to previous menu: ")
        if not filament_update_choice:
            continue
        elif filament_update_choice.lower().startswith("q"):
            break
        elif filament_update_choice in str(id_list):
            while True:
                filament_inventory_all()
                fil_input = update_filament_menu_selection()
                if fil_input.startswith("q"):
                    break
                elif fil_input == "1":
                    while True:
                        fil_update = input("Please enter new nickname or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(filament_update_choice, "name", fil_update)
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "2":
                    while True:
                        fil_update = input("Please enter new brand name or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(filament_update_choice, "brand", fil_update)
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "3":
                    while True:
                        fil_update = input("Please enter new color or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(filament_update_choice, "color", (fil_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "4":
                    while True:
                        fil_update = input("Please enter new cost or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(float(filament_update_choice), "cost", (fil_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "5":
                    while True:
                        fil_update = input("Please enter new roll weight or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(float(filament_update_choice), "roll_weight", (fil_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "6":
                    while True:
                        fil_update = input("Please enter new diameter size or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(float(filament_update_choice), "diameter", (fil_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "7":
                    while True:
                        fil_update = input("Please enter new spool material type or Q to cancel: ")
                        if not fil_update:
                            continue
                        elif fil_update.lower().startswith("q"):
                            break
                        else:
                            update_filament(filament_update_choice, "spool_material", (fil_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif fil_input == "8":
                    while True:
                        fil_update = input("Please enter if roll is finished (yes or no) or Q to cancel: ").lower()
                        if not fil_update.startswith(("y","n","q")):
                            continue
                        elif fil_update.startswith("q"):
                            break
                        else:
                            if fil_update.startswith("y"):
                                update_filament(float(filament_update_choice), "roll_finished", 1)
                                print("Entry has been update.")
                                break
                            elif fil_update.startswith("n"):
                                update_filament(float(filament_update_choice), "roll_finished", 0)
                                print("Entry has been update.")
                                break
                else:
                    print("Please select one of the four options or (Q)uit:\n")
                    continue
            break

def delete_filament_menu():
    id_list = [id for (id,) in session.query(FilamentRoll.filament_id).order_by(FilamentRoll.filament_id)]
    filament_inventory_all()
    while True:
        filament_delete_choice = input("\n\nPlease enter an ID to update, or Q to return to previous menu: ")
        if not filament_delete_choice:
            continue
        elif filament_delete_choice.lower().startswith("q"):
            break
        else:
            delete_filament(filament_delete_choice)
            print("Entry has been deleted.")
            time.sleep(0.5)
            break


def filament_questions():
    while True:
        filament_inventory_general()
        filament_choices = input("""

Filament Menu:

    1) Add Filament.
    2) Update Filament.
    3) Delete Filament.
    Q) Return to Main Menu.


Please select an option: """)

        if not filament_choices:
            time.sleep(0.5)
            continue
        elif filament_choices.lower().startswith("q"):
            break
        elif filament_choices == "1":
            add_filament_menu()
        elif filament_choices == "2":
            update_filament_menu()
        elif filament_choices == "3":
            delete_filament_menu()

