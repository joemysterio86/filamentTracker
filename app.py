import json
import csv, os
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from collections import OrderedDict
from flask_pymongo import PyMongo
from wtforms import Form, BooleanField, StringField, FloatField, validators
from dotenv import load_dotenv

load_dotenv()
mongo_uri=os.environ.get('MONGO_DB_URI')
app_mongo = Flask(__name__)
app_mongo.config['MONGO_URI'] = mongo_uri
app_mongo.secret_key = os.urandom(24)
mongo = PyMongo(app_mongo)

class SpoolForm(Form):
    brand = StringField('brand', [validators.length(max=25),validators.input_required()])
    spool_material = StringField('spool_material', [validators.length(max=25),validators.input_required()])
    weight = FloatField('weight',[validators.input_required()])

filament_rolls = mongo.db.filament_rolls
filament_roll_prints = mongo.db.filament_roll_prints
filament_spools = mongo.db.filament_spools
filament_types = mongo.db.filament_types


def prepop_fil_type_table():
    if 'filament_types' not in mongo.db.list_collection_names():
        try:
            with open('assets/prepop_filament_type.csv', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file, quotechar='"')
                clist = [row for row in csv_reader]
                entries = []
                for row in clist:
                    entries.append({'filament_type':list(row.values())[0], 'density':float(list(row.values())[1])})
            filament_types.insert_many(entries)
        except:
            print('Could not import data to filament_types collection!')
    else:
        print('filament_types collection is there! moving on...')

def check_create_collections():
    collection_list = ['filament_rolls','filament_spools','filament_roll_prints']
    for collection in collection_list:
            if collection not in mongo.db.list_collection_names():
                try:
                    mongo.db.create_collection(collection)

                    with open(f'assets/{collection}_schema.json', 'r') as fss:
                        json_fss = json.loads(fss.read())

                    db_dict = OrderedDict([('collMod', 'filament_rolls'),
                                            ('validator', json_fss),
                                            ('validationLevel', 'strict')])
                    mongo.db.command(db_dict)
                except Exception:
                    print(f'Could not import data to {collection} collection!')
            else:
                print(f'{collection} collection is there! moving on...')

@app_mongo.route('/')
def index():
    view_gen_filament = filament_rolls.find({}, {'_id':1, 'name':1, 'brand':1, 'filament_type':1, 'color':1, 'spool_material':1, 'roll_finished':1})

    if 'view_prints' in request.form and request.method == 'POST':
        session['fila_id'] = request.form.get('view_prints')
        return redirect('prints')

    return render_template('index.html', view_gen_filament=view_gen_filament, fil_length_remaining_calc=fil_length_remaining_calc)


@app_mongo.route('/filaments', methods=['GET','POST'])
def filaments():
    view_all_filament = filament_rolls.find({}, {'_id':1, 'name':1, 'brand':1, 'filament_type':1, 'color':1, 'cost':1, 'roll_weight':1, 'diameter':1, 'spool_material':1, 'roll_finished':1})
    spool_mat_list = filament_spools.distinct('spool_material')
    fil_types_list = filament_types.distinct('filament_type')
    spool_brand_list = filament_spools.distinct('brand')

    if 'add_filament' in request.form and request.method == 'POST':
        try:
            spool_mat_list = filament_spools.distinct('spool_material', {'brand': f'{request.form.get("brand")}'})
            if request.form.get('spool_material') in spool_mat_list:
                filament_rolls.insert_one(
                    {
                        'name': request.form.get('name'),
                        'brand': request.form.get('brand'),
                        'filament_type': request.form.get('filament_type'),
                        'color': request.form.get('color'),
                        'cost': float(request.form.get('cost')),
                        'roll_weight': float(request.form.get('roll_weight')),
                        'diameter': float(request.form.get('diameter')),
                        'spool_material': request.form.get('spool_material'),
                        'roll_finished': False
                    }
                )
        except Exception:
            pass
        else:
            # return render_template('filaments.html', filament_spools=filament_spools,spool_brand_list=spool_brand_list,fil_types_list=fil_types_list,spool_mat_list=spool_mat_list, view_all_filament=view_all_filament)
            return redirect('filaments')

    if 'edit_selection' in request.form and request.method == 'POST':
        session['edit_fila_id'] = request.form.get('edit_selection')
        return redirect('edit_filaments')

    if 'view_prints' in request.form and request.method == 'POST':
        session['print_fila_id'] = request.form.get('view_prints')
        return redirect('prints')

    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            filament_rolls.delete_one({'_id':ObjectId(f'{entry}')})
        return redirect('filaments')

    return render_template('filaments.html', filament_spools=filament_spools,spool_brand_list=spool_brand_list,fil_types_list=fil_types_list,spool_mat_list=spool_mat_list, view_all_filament=view_all_filament)

@app_mongo.route('/edit_filaments', methods=['GET','POST'])
def edit_filaments():
    fila_id = str(session.get('edit_fila_id'))
    view_filament_info = filament_rolls.find_one({'_id':ObjectId(f'{fila_id}')},{'_id':1, 'name':1, 'brand':1, 'filament_type':1, 'color':1, 'cost':1, 'roll_weight':1, 'diameter':1, 'spool_material':1, 'roll_finished':1})
    spool_mat_list = filament_spools.distinct('spool_material')
    fil_types_list = filament_types.distinct('filament_type')
    spool_brand_list = filament_spools.distinct('brand')
    diameter_list = [1.75,2.85,3]
    roll_finish_status = [True, False]

    if 'edit_filament' in request.form and request.method == 'POST':
        try:
            filament_rolls.update_one({'_id':ObjectId(f'{fila_id}')},
                {'$set': 
                    {
                        'name': request.form.get('name'),
                        'brand': request.form.get('brand'),
                        'filament_type': request.form.get('filament_type'),
                        'color': request.form.get('color'),
                        'cost': float(request.form.get('cost')),
                        'roll_weight': float(request.form.get('roll_weight')),
                        'diameter': float(request.form.get('diameter')),
                        'spool_material': request.form.get('spool_material'),
                        'roll_finished': request.form.get('roll_finished')
                    }
                }
            )
        except Exception:
            pass
        else:
            return redirect('edit_filaments')

    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            filament_rolls.delete_one({'_id':ObjectId(f'{entry}')})
        return redirect('edit_filaments')

    return render_template(
        'edit_filaments.html',
        view_filament_info=view_filament_info,
        spool_mat_list=spool_mat_list,
        fil_types_list=fil_types_list,
        spool_brand_list=spool_brand_list,
        diameter_list=diameter_list,
        roll_finish_status=roll_finish_status
        )

@app_mongo.route('/prints', methods=['GET','POST'])
def prints():
    fila_id = str(session.get('print_fila_id'))
    fila_name = filament_rolls.find_one({'_id':ObjectId(f'{fila_id}')},{'_id':0,'name':1})
    view_prints = filament_roll_prints.find({'roll_id': fila_id}, {'_id':1, 'print_name':1, 'print_length':1})

    if 'add_prints' in request.form and request.method == 'POST':
        try:
            filament_roll_prints.insert_one(
                {
                    'print_name': request.form.get('print_name'),
                    'print_length': float(request.form.get('print_length')),
                    'roll_id': fila_id
                }
            )
        except:
            pass
        else:
            return redirect('prints')
    
    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            filament_roll_prints.delete_one({'_id':ObjectId(f'{entry}')})
        return redirect('prints')

    return render_template('prints.html', view_prints=view_prints, fila_name=fila_name)

    
@app_mongo.route('/spools', methods=['GET','POST'])
def spools():
    view_spools = filament_spools.find({}, {'_id':1, 'brand':1, 'spool_material':1, 'weight':1})
 
    # if 'add_spools' in request.form and request.method == 'POST' and SpoolForm.validate(self=SpoolForm):
    #     brand = SpoolForm.brand
    #     spool_material = SpoolForm.spool_material
    #     weight = SpoolForm.weight

    if 'add_spools' in request.form and request.method == 'POST':
        try:
            filament_spools.insert_one(
                {
                    'brand': request.form.get('brand'),
                    'spool_material': request.form.get('spool_material'),
                    'weight': float(request.form.get('weight'))
                }            
            )
        except:
            return render_template('spools.html', view_spools=view_spools)
        else:
            return redirect('spools')

    if 'delete_checked' in request.form and request.method == 'POST':
        for entry in request.form.getlist('delete_checked'):
            filament_spools.delete_one({'_id':ObjectId(f'{entry}')})
        return redirect('spools')

    return render_template('spools.html', view_spools=view_spools)

def fil_length_remaining_calc(fil_type, id, spool_brand, spool_material):
    roll_weight = filament_rolls.find_one((ObjectId(f'{id}')),{'_id':0,'roll_weight':1}).get('roll_weight')
    spool_weight = filament_spools.find_one({'brand':f'{spool_brand}','spool_material':f'{spool_material}'},{'_id':0,'weight':1}).get('weight')

    density = filament_types.find_one({'filament_type': fil_type},{'_id':0,'density':1}).get('density')
    mass = roll_weight - spool_weight
    volume = mass / density * 1000
    diameter = filament_rolls.find_one((ObjectId(f'{id}')),{'_id':0,'diameter':1}).get('diameter')
    radius = diameter / 2
    area = radius * radius * 3.14
    length = volume / area
    length = length / 1000

    try:
        total_roll_prints = [i for i in filament_roll_prints.aggregate([
            {
                '$match': {
                    'roll_id': f'{id}'
                }
            },{
                '$group': {
                    '_id': 'null',
                    'total_length': {
                        '$sum': '$print_length'
                    }
                }
            }
        ])]

        remaining_length = length - total_roll_prints[0]['total_length']
        return '%.3f' % remaining_length
    except:
        return '%.3f' % length
    return render_template('spools.html')

prepop_fil_type_table()
check_create_collections()

if __name__ == '__main__':
    app_mongo.run(host='0.0.0.0', debug=True)