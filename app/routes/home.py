from flask import Blueprint, render_template
from ..controllers.propertyController import getAllProperties,getImagesByPropertyId


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def home():
    properties=getAllProperties()
    propertyImages = {}
    for property in properties:
        images = getImagesByPropertyId(property['id'])
        propertyImages[property['id']] = images
    return render_template('home.html',properties=properties,propertyImages=propertyImages)