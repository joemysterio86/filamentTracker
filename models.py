import os, csv
import sqlalchemy as db
from typing import List
from sqlalchemy import String, REAL, ForeignKey, Boolean, Column, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

db_path = os.path.join(os.getcwd(), 'main.db')
db_uri = 'sqlite:///{}'.format(db_path)
engine = db.create_engine(db_uri)
metadata = db.MetaData()
Session = sessionmaker(bind=engine)
sqlsession = Session()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()
    
class Base(DeclarativeBase):
    pass

class FilamentRoll(Base):
    __tablename__ = 'filament_roll'
    roll_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    brand: Mapped[str] = mapped_column(String(40), nullable=False)
    filament_types: Mapped[str] = mapped_column(String(40), nullable=False)
    color: Mapped[str] = mapped_column(String(40))
    cost: Mapped[REAL] = mapped_column(REAL)
    roll_weight: Mapped[REAL] = mapped_column(REAL, nullable=False)
    diameter: Mapped[REAL] = mapped_column(REAL, nullable=False)
    spool_material: Mapped[str] = mapped_column(String(40), nullable=False)
    roll_finished = Column(Boolean, unique=False, default=False)
    fil_roll_to_prints: Mapped[List["FilamentRollPrints"]] = relationship()
    def __repr__(self):
        return f'ID: {self.roll_id}, Filament Name: {self.name}, Filament Brand: {self.brand}, Filament Types: {self.filament_types}, Filament Color: {self.color}, Filament Cost: {self.cost}, Roll Weight: {self.roll_weight}, Filament Diameter: {self.diameter}, Spool Material: {self.spool_material}, Roll Finished: {self.roll_finished}'

class FilamentRollPrints(Base):
    __tablename__ = 'filament_roll_prints'
    print_id: Mapped[int] = mapped_column(primary_key=True)
    print_name: Mapped[str] = mapped_column(String(40), nullable=False)
    print_length: Mapped[REAL] = mapped_column(REAL, nullable=False)
    roll_id: Mapped[str] = mapped_column(String(40), ForeignKey("filament_roll.roll_id"), nullable=False)
    printsto_fil_roll: Mapped["FilamentRoll"] = relationship(back_populates="fil_roll_to_prints")
    def __repr__(self):
        return f'ID: {self.print_id}, Print Name: {self.print_name}, Print Filament Length: {self.print_length}, Filament ID: {self.roll_id}'
    
class FilamentSpool(Base):
    __tablename__ = 'filament_spool'
    spool_id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(40), nullable=False)
    spool_material: Mapped[str] = mapped_column(String(40), nullable=False)
    weight: Mapped[REAL] = mapped_column(REAL, nullable=False)
    def __repr__(self):
        return f'ID: {self.spool_id}, Brand Name: {self.brand}, Spool Material: {self.spool_material}, Spool Weight: {self.weight}'

class FilamentType(Base):
    __tablename__ = 'filament_type'
    filament_id: Mapped[int] = mapped_column(primary_key=True)
    filament_types: Mapped[str] = mapped_column(String(40), nullable=False)
    density: Mapped[REAL] = mapped_column(REAL, nullable=False)
    def __repr__(self):
        return f'ID: {self.filament_id}, Filament Types: {self.filament_types}, Filament Density: {self.density}'

def prepop_fil_type_table():
    if not sqlsession.query(FilamentType).first():
        try:
            with open('assets/prepop_filament_type.csv', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file, quotechar='"')
                clist = [row for row in csv_reader]
                entries = []
                for row in clist:
                    entries.append(FilamentType(filament_types=list(row.values())[0],density=list(row.values())[1]))

                sqlsession.add_all(entries)
                sqlsession.commit()
        except:
            print("Could not import data to Filament Type table!")

Base.metadata.create_all(engine)
prepop_fil_type_table()