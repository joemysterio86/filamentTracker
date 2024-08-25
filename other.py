from models import FilamentRoll, FilamentRollPrints, FilamentSpool, db_uri
import sqlalchemy as db
from sqlalchemy.orm import session, sessionmaker

engine = db.create_engine(db_uri)
metadata = db.MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# this provides a general overview of your filament inventory
def filament_inventory_general():
    view_your_filament = session.execute(db.select(FilamentRoll.name, FilamentRoll.brand, FilamentRoll.color, db.case((FilamentRoll.roll_finished == '0','No'),(FilamentRoll.roll_finished == '1','Yes'))).order_by(FilamentRoll.filament_id)).all()
    formatted_result = [f'{name:<35}{brand:<15}{color:<15}{roll_finished:<15}' for name, brand, color, roll_finished in view_your_filament]
    name, brand, color, roll_finished = 'Name','Brand','Color','Roll Finished'
    print(f'\n\nAll entries:\n{name:<35}{brand:<15}{color:<15}{roll_finished:<15}')
    print('\n'.join(formatted_result))
    print('\n\n')

# this is an expanded view of your filament inventory
def filament_inventory_all():
    view_your_filament = session.execute(db.select(FilamentRoll.filament_id, FilamentRoll.name, FilamentRoll.brand, FilamentRoll.color, FilamentRoll.cost, FilamentRoll.roll_weight, FilamentRoll.diameter, FilamentRoll.spool_material, db.case((FilamentRoll.roll_finished == '0','No'),(FilamentRoll.roll_finished == '1','Yes'))).order_by(FilamentRoll.filament_id)).all()
    formatted_result = [f"{filament_id:<6}{name:<35}{brand:<15}{color:<15}{cost:<8}{roll_weight:<15}{diameter:<10}{spool_material:<15}{roll_finished:<10}" for filament_id, name, brand, color, cost, roll_weight, diameter, spool_material, roll_finished in view_your_filament]
    filament_id, name, brand, color, cost, roll_weight, diameter, spool_material, roll_finished = 'ID','Name','Brand','Color','Cost','Roll Weight','Diameter','Spool Material','Roll Finished'
    print(f'\n\nYour Filament(s):\n{filament_id:<6}{name:<35}{brand:<15}{color:<15}{cost:<8}{roll_weight:<15}{diameter:<10}{spool_material:<15}{roll_finished:<10}')
    print('\n'.join(formatted_result))    
    print('\n\n')
    
# this is an expanded view of your spool inventory
def spool_inventory_all():
    view_your_spools = session.query(FilamentSpool.spool_id, FilamentSpool.brand, FilamentSpool.spool_material, FilamentSpool.weight).order_by(FilamentSpool.spool_id).all()
    formatted_result = [f"{spool_id:<6}{brand:<15}{spool_material:<15}{weight:<15}" for spool_id, brand, spool_material, weight in view_your_spools]
    spool_id, brand, spool_material, weight = 'ID','Brand','Spool Material','Weight'
    print(f'\n\nYour Filament Spools(s):\n{spool_id:<6}{brand:<15}{spool_material:<15}{weight:<15}')
    print('\n'.join(formatted_result))    
    print('\n\n')
    
# this is a view of your spool inventory
def print_inventory_all(fila_id):
    view_your_prints = session.query(FilamentRollPrints.print_id, FilamentRollPrints.print_name, FilamentRollPrints.print_length).filter(FilamentRollPrints.filament_id == fila_id).order_by(FilamentRollPrints.print_id).all()
    formatted_result = [f"{print_id:<6}{print_name:<15}{print_length:<15}" for print_id, print_name, print_length in view_your_prints]
    print_id, print_name, print_length = 'ID','Brand','Spool Material'
    print(f'\n\nYour Filament Spools(s):\n{print_id:<6}{print_name:<15}{print_length:<15}')
    print('\n'.join(formatted_result))    
    print('\n\n')
    
def view_inventory():
    filament_inventory_general()
    input('\n\nPress ENTER key to continue to main menu.')
