import os, csv, sqlalchemy
from sqlalchemy import func
from models import FilamentRoll, FilamentRollPrints, FilamentSpool, FilamentType
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker


db_path = os.path.join(os.getcwd(), 'main.db')
db_uri = 'sqlite:///{}'.format(db_path)
engine = sqlalchemy.create_engine(db_uri)
Session = sessionmaker(bind=engine)
sqlsession = Session()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)


@app.route("/")
def index():
    if 'view_prints' in request.form and request.method == 'POST':
        session['fila_id'] = request.form.get('view_prints')
        return redirect("prints")

    view_gen_filament = sqlsession.query(FilamentRoll.roll_id, FilamentRoll.name, FilamentRoll.brand, FilamentRoll.filament_type, FilamentRoll.color, FilamentRoll.spool_material, FilamentRoll.roll_finished).order_by(FilamentRoll.roll_id).all()
    return render_template("index.html", fil_length_remaining_calc=fil_length_remaining_calc, view_gen_filament=view_gen_filament)

@app.route("/filaments", methods=["GET","POST"])
def filaments():
    if 'new_fila' in request.form and request.method == 'POST':
        try:
            entry = FilamentRoll(
                name=request.form.get("name"),
                brand=request.form.get("brand"),
                filament_type=request.form.get("filament_type"),
                color=request.form.get("color"),
                cost=request.form.get("cost"),
                roll_weight=request.form.get("roll_weight"),
                diameter=request.form.get("diameter"),
                spool_material=request.form.get("spool_material"),
                roll_finished=request.form.get("roll_finished"),
            )
            sqlsession.add(entry)
            sqlsession.commit()
        except:
            sqlsession.rollback()
        else:
            return redirect("filaments")

    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            sqlsession.query(FilamentRoll).filter(FilamentRoll.roll_id == entry).delete()
        sqlsession.commit()
        return redirect("filaments")

    if 'view_prints' in request.form and request.method == 'POST':
        session['fila_id'] = request.form.get('view_prints')
        return redirect("prints")

    view_all_filament = sqlsession.query(FilamentRoll.roll_id, FilamentRoll.name, FilamentRoll.brand, FilamentRoll.filament_type, FilamentRoll.color, FilamentRoll.cost, FilamentRoll.roll_weight, FilamentRoll.diameter, FilamentRoll.spool_material, FilamentRoll.roll_finished).order_by(FilamentRoll.roll_id).all()
    return render_template("filaments.html", view_all_filament=view_all_filament)

@app.route("/prints", methods=["GET","POST"])
def prints():
    fila_id = session.get('fila_id')
    if 'add_prints' in request.form and request.method == 'POST':
        try:
            entry = FilamentRollPrints(
                print_name=request.form.get("print_name"),
                print_length=request.form.get("print_length"),
                roll_id=fila_id,
                )
            sqlsession.add(entry)
            sqlsession.commit()
        except:
            sqlsession.rollback()
        else:
            return redirect("prints")
    
    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            sqlsession.query(FilamentRollPrints).filter(FilamentRollPrints.print_id == entry).delete()
        sqlsession.commit()
        return redirect("prints")

    view_prints = sqlsession.query(FilamentRollPrints.print_id, FilamentRollPrints.print_name, FilamentRollPrints.print_length).filter(FilamentRollPrints.roll_id == fila_id).order_by(FilamentRollPrints.print_id).all()
    return render_template("prints.html", view_prints=view_prints)

@app.route("/spools", methods=["GET","POST"])
def spools():
    if 'add_spools' in request.form and request.method == 'POST':
        try:
            entry = FilamentSpool(
                brand=request.form.get("brand"),
                spool_material=request.form.get("spool_material"),
                weight=request.form.get("weight")
            )
            sqlsession.add(entry)
            sqlsession.commit()
        except:
            sqlsession.rollback()
        else:
            return redirect("spools")

    
    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            sqlsession.query(FilamentSpool).filter(FilamentSpool.spool_id == entry).delete()
        sqlsession.commit()
        return redirect("spools")

    view_spools = sqlsession.query(FilamentSpool.spool_id, FilamentSpool.brand, FilamentSpool.spool_material, FilamentSpool.weight).order_by(FilamentSpool.spool_id).all()
    return render_template("spools.html", view_spools=view_spools)

def fil_length_remaining_calc(fil_type, id, spool_brand, material):
    density = sqlsession.query(FilamentType.density).filter(FilamentType.filament_type == fil_type).scalar()
    mass = (sqlsession.query(FilamentRoll.roll_weight).filter(FilamentRoll.roll_id == id).scalar()) - (sqlsession.query(FilamentSpool.weight).filter(FilamentSpool.brand == spool_brand).filter(FilamentSpool.spool_material == material).scalar())
    volume = mass / density * 1000
    diameter = sqlsession.query(FilamentRoll.diameter).filter(FilamentRoll.roll_id == id).scalar()
    radius = diameter / 2
    area = radius * radius * 3.14
    length = volume / area
    length = length / 1000

    try:
        total_roll_prints = sqlsession.query(func.sum(FilamentRollPrints.print_length).filter(FilamentRollPrints.roll_id == id))
        remaining_length = length - total_roll_prints.scalar()
        return "%.3f" % remaining_length
    except:
        return "%.3f" % length

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)