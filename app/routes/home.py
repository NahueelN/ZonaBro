from flask import Blueprint, render_template,request    
from ..controllers.propertyController import getAllProperties,getImagesByPropertyId,getAddressByPropertyId,SearchPropertyByAddress,getPropertyByOrder


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
@home_bp.route('/home')
def home():
    order_by = request.args.get('order')
    print(order_by)
    if order_by is None:
        properties = getAllProperties()
    else:
        properties = getPropertyByOrder(order_by)
    context = {
        'properties': properties,
        'propertyImages': {},
        'propertyAddress': {}
    }

    for property in properties:
        property_id = property['id']
        context['propertyImages'][property_id] = getImagesByPropertyId(property_id)
        context['propertyAddress'][property_id] = getAddressByPropertyId(property_id)

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
        context['propertyAddress'][property_id] = getAddressByPropertyId(property_id)

    return render_template('home.html', **context)


@home_bp.route('/order', methods=['GET'])
def order():
    order_by = request.args.get('order', 'date_desc')
    properties=getPropertyByOrder(order_by)

    context = {
        'properties': properties,
        'propertyImages': {},
        'propertyAddress': {}
    }
    
    for property in properties:
        property_id = property['id']
        context['propertyImages'][property_id] = getImagesByPropertyId(property_id)
        context['propertyAddress'][property_id] = getAddressByPropertyId(property_id)

    return render_template('home.html', **context)



