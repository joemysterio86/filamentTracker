import os, sqlalchemy
from sqlalchemy import func, text, event
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
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()

@app.route("/")
def index():
    if 'view_prints' in request.form and request.method == 'POST':
        session['fila_id'] = request.form.get('view_prints')
        return redirect("prints")

    view_gen_filament = sqlsession.query(FilamentRoll.roll_id, FilamentRoll.name, FilamentRoll.brand, FilamentRoll.filament_types, FilamentRoll.color, FilamentRoll.spool_material, FilamentRoll.roll_finished).order_by(FilamentRoll.roll_id).all()
    return render_template("index.html", fil_length_remaining_calc=fil_length_remaining_calc, view_gen_filament=view_gen_filament)

@app.route("/filaments", methods=["GET","POST"])
def filaments():
    view_all_filament = sqlsession.query(FilamentRoll.roll_id, FilamentRoll.name, FilamentRoll.brand, FilamentRoll.filament_types, FilamentRoll.color, FilamentRoll.cost, FilamentRoll.roll_weight, FilamentRoll.diameter, FilamentRoll.spool_material, FilamentRoll.roll_finished).order_by(FilamentRoll.roll_id).all()
    spool_mat_list = set(sqlsession.query(FilamentSpool.spool_material).all())
    spool_brand_list = set(sqlsession.query(FilamentSpool.brand).all())
    fil_types_list = sqlsession.query(FilamentType.filament_types).all()

    if 'new_fila' in request.form and request.method == 'POST':
        entry = FilamentRoll(
            name=request.form.get("name"),
            brand=request.form.get("brand"),
            filament_types=request.form.get("filament_types"),
            color=request.form.get("color"),
            cost=request.form.get("cost"),
            roll_weight=request.form.get("roll_weight"),
            diameter=request.form.get("diameter"),
            spool_material=request.form.get("spool_material")
        )
        try:
            sqlsession.add(entry)
            sqlsession.commit()
        except:
            sqlsession.rollback()
            return render_template("filaments.html", view_all_filament=view_all_filament, spool_mat_list=spool_mat_list, spool_brand_list=spool_brand_list, fil_types_list=fil_types_list)
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

    return render_template("filaments.html", view_all_filament=view_all_filament, spool_mat_list=spool_mat_list, spool_brand_list=spool_brand_list, fil_types_list=fil_types_list)

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
            print("somethign failed")
        else:
            return redirect("spools")

    
    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            sqlsession.execute(text(f'DELETE FROM filament_spool WHERE spool_id = {entry}'))
        sqlsession.commit()
        return redirect("spools")
    # if 'delete_checked' in request.form and request.method == 'POST':
    #     for entry in request.form.getlist('delete_checked'):
    #         sqlsession.query(FilamentSpool).filter(FilamentSpool.spool_id == entry).delete()
    #     sqlsession.commit()
    #     return redirect("spools")

    view_spools = sqlsession.query(FilamentSpool.spool_id, FilamentSpool.brand, FilamentSpool.spool_material, FilamentSpool.weight).order_by(FilamentSpool.spool_id).all()
    return render_template("spools.html", view_spools=view_spools)

def fil_length_remaining_calc(fil_type, id, spool_brand, material):
    density = sqlsession.query(FilamentType.density).filter(FilamentType.filament_types == fil_type).scalar()
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