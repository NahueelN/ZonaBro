from flask import Blueprint, render_template
from ..controllers.propertyController import getAllProperties,getImagesByPropertyId,getAddressByPropertyId


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def home():
    properties=getAllProperties()
    
    propertyImages = {}
    for property in properties:
        images = getImagesByPropertyId(property['id'])
        propertyImages[property['id']] = images

    propertyAddress={}
    for property in properties:
        address = getAddressByPropertyId(property['id'])
        propertyAddress[property['id']] = address

    return render_template('home.html',properties=properties,propertyImages=propertyImages,propertyAddress=propertyAddress)     