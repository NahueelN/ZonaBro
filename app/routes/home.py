from flask import Blueprint, render_template,request    
from ..controllers.propertyController import getAllProperties,getImagesByPropertyId,getAddressByPropertyId,SearchPropertyByAddress


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def home():
    properties = getAllProperties()
    
    context = {
        'properties': properties,
        'propertyImages': {},
        'propertyAddress': {}
    }
    
    for property in properties:
        property_id = property['id']
        context['propertyImages'][property_id] = getImagesByPropertyId(property_id)
        context['propertyAddress'][property_id] = SearchPropertyByAddress(property_id)

    return render_template('home.html', **context)



@home_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    properties = SearchPropertyByAddress(query)
    
    context = {
        'properties': properties,
        'propertyImages': {},
        'propertyAddress': {}
    }
    
    for property in properties:
        property_id = property['id']
        context['propertyImages'][property_id] = getImagesByPropertyId(property_id)
        context['propertyAddress'][property_id] = SearchPropertyByAddress(property_id)

    return render_template('home.html', **context)