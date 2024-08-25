import os
import sqlalchemy as db
from sqlalchemy import String, REAL, ForeignKey, Boolean, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db_path = os.path.join(os.getcwd(), 'main.db')
db_uri = 'sqlite:///{}'.format(db_path)
engine = db.create_engine(db_uri)
metadata = db.MetaData()
Base = DeclarativeBase

class Base(DeclarativeBase):
    pass

class FilamentRoll(Base):
    __tablename__ = 'filament_roll'
    filament_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    brand: Mapped[str] = mapped_column(String(40), nullable=False)
    color: Mapped[str] = mapped_column(String(40))
    cost: Mapped[REAL] = mapped_column(REAL)
    roll_weight: Mapped[REAL] = mapped_column(REAL, nullable=False)
    diameter: Mapped[REAL] = mapped_column(REAL, nullable=False)
    spool_material: Mapped[str] = mapped_column(String(40), nullable=False)
    roll_finished = Column(Boolean, unique=False, default=False)
    fill_roll_to_prints: Mapped["FilamentRollPrints"] = relationship(back_populates="prints_to_fill_roll")
    def __repr__(self):
        return f'ID: {self.filament_id}, Filament Name: {self.name}, Filament Brand: {self.brand}, Filament Color: {self.color}, Filament Cost: {self.cost}, Roll Weight: {self.roll_weight}, Filament Diameter: {self.diameter}, Spool Material: {self.spool_material}, Roll Finished: {self.roll_finished}'

class FilamentRollPrints(Base):
    __tablename__ = 'filament_roll_prints'
    print_id: Mapped[int] = mapped_column(primary_key=True)
    print_name: Mapped[str] = mapped_column(String(40), nullable=False)
    print_length: Mapped[REAL] = mapped_column(REAL, nullable=False)
    filament_id: Mapped[str] = mapped_column(String(40), ForeignKey("filament_roll.filament_id"), nullable=False)
    prints_to_fill_roll: Mapped["FilamentRoll"] = relationship(back_populates="fill_roll_to_prints")
    def __repr__(self):
        return f'ID: {self.print_id}, Print Name: {self.print_name}, Print Filament Length: {self.print_length}, Filament ID: {self.filament_id}'
    
class FilamentSpool(Base):
    __tablename__ = 'spool'
    spool_id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(40), ForeignKey("filament_roll.brand"), nullable=False)
    spool_material: Mapped[str] = mapped_column(String(40), ForeignKey("filament_roll.spool_material"), nullable=False)
    weight: Mapped[REAL] = mapped_column(REAL, nullable=False)
    def __repr__(self):
        return f'ID: {self.spool_id}, Brand Name: {self.brand}, Spool Material: {self.spool_material}, Spool Weight: {self.weight}'


Base.metadata.create_all(engine)