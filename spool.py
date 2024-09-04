import time
import sqlalchemy
from sqlalchemy.orm import session, sessionmaker
from models import FilamentSpool, db_uri
from other import spool_inventory_all

engine = sqlalchemy.create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

def add_spool(*args):
    entry = FilamentSpool(
        brand=args[0],
        spool_material=args[1],
        weight=args[2],
        )
    session.add(entry)
    session.commit()

def update_spool(id, col, val):
    session.query(FilamentSpool).filter(FilamentSpool.id == id).update({col: val})
    session.commit()

def delete_spool(id):
    session.query(FilamentSpool).filter(FilamentSpool.id == id).delete()
    session.commit()

def add_spool_menu():
    print("Press Q if you need to cancel and return to previous menu.\n")
    while True:
        spool_brand = input("Please enter spool brand: ")
        if not spool_brand:
            continue
        elif spool_brand.lower().startswith("q"):
            return
        else:
            break
    while True:
        spool_material = input("Please enter spool material: ")
        if not spool_material:
            continue
        elif spool_material.lower().startswith("q"):
            return
        else:
            break
    while True:
        spool_weight = input("Please enter empty spool weight in grams: ")
        if not spool_weight:
            continue
        elif spool_weight.lower().startswith("q"):
            return
        else:
            break
    add_spool(spool_brand, spool_material, spool_weight)
    print("Spool has been added! Taking you back to Add Spool Menu.\n")
    time.sleep(1)

def update_spool_menu_selection():
    user_input = input("""
Update Menu:
    1) Brand
    2) Material
    3) Weight
    Q) Return to previous menu
                      

Please select an option: """)
    return user_input

def update_spool_menu():
    id_list = [id for (id,) in session.query(FilamentSpool.id).order_by(FilamentSpool.id)]
    while True:
        spool_inventory_all()
        spool_update_choice = input("\n\nPlease enter an ID to update, or Q to return to previous menu: ")
        if not spool_update_choice:
            continue
        elif spool_update_choice.lower().startswith("q"):
            break
        elif spool_update_choice in str(id_list):
            while True:
                spool_inventory_all()
                spo_input = update_spool_menu_selection()
                if spo_input.startswith("q"):
                    break
                elif spo_input == "1":
                    while True:
                        spo_update = input("Please enter new brand for the spool or Q to cancel: ")
                        if not spo_update:
                            continue
                        elif spo_update.lower().startswith("q"):
                            break
                        else:
                            update_spool(spool_update_choice, "brand", spo_update)
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif spo_input == "2":
                    while True:
                        spo_update = input("Please enter new material type or Q to cancel: ")
                        if not spo_update:
                            continue
                        elif spo_update.lower().startswith("q"):
                            break
                        else:
                            update_spool(spool_update_choice, "spool_material", spo_update)
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                elif spo_input == "3":
                    while True:
                        spo_update = input("Please enter new weight in grams or Q to cancel: ")
                        if not spo_update:
                            continue
                        elif spo_update.lower().startswith("q"):
                            break
                        else:
                            update_spool(spool_update_choice, "weight", (spo_update))
                            print("Entry has been update.")
                            time.sleep(0.5)
                            break
                else:
                    print("Please select one of the three options or (Q)uit:\n")
                    continue
            break

def delete_spool_menu():
    id_list = [id for (id,) in session.query(FilamentSpool.id).order_by(FilamentSpool.id)]
    spool_inventory_all()
    while True:
        spool_delete_choice = input("\n\nPlease enter an ID to delete, or Q to return to previous menu: ")
        if not spool_delete_choice:
            continue
        elif spool_delete_choice.lower().startswith("q"):
            break
        else:
            delete_spool(spool_delete_choice)
            print("Entry has been deleted.")
            time.sleep(0.5)
            break


def spool_questions():
    while True:
        spool_inventory_all()
        spool_choices = input("""

Spool Menu:

    1) Add Spool.
    2) Update Spool.
    3) Delete Spool.
    Q) Return to Main Menu.


Please select an option: """)

        if not spool_choices:
            time.sleep(0.5)
            continue
        elif spool_choices.lower().startswith("q"):
            break
        elif spool_choices == "1":
            add_spool_menu()
        elif spool_choices == "2":
            update_spool_menu()
        elif spool_choices == "3":
            delete_spool_menu()

