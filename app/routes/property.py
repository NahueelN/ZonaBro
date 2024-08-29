from flask import Blueprint, render_template,flash, redirect,request
from ..untils.geocoding import get_lat_long_osm
from ..controllers.propertyController import getPropertyById,addImage,updateProperty,addPropertyDB,deleteProperty,deleteImagesByPropertyId,getImagesByPropertyId,addAddress,getAddressByPropertyId,sendSellerInquiry,updateAddress

from flask_login import login_required, current_user
from ..models.formProperty import PropertyForm

property_bp = Blueprint('property', __name__, url_prefix='/property')

@property_bp.route('/<int:id>')
def propertyGET(id):
    property = getPropertyById(id)
    if not property:
        return render_template('errors/404.html'), 404
    address = getAddressByPropertyId(id)
    lat, lon = get_lat_long_osm(f"{address['street_name']} {address['street_number']}, {address['city']}")
    context = {
        'property': property,
        'propertyImages': getImagesByPropertyId(id),
        'propertyAddress': address,
        'latitude': lat,
        'longitude': lon
    }
    
    return render_template('properties/property.html', **context)

@property_bp.route('/add', methods=['GET', 'POST'])
@login_required
def addProperty():
    form = PropertyForm()
    if form.validate_on_submit():
        try:
            street_name = form.street.data
            street_number = int(form.streetNumber.data) 
            city = form.city.data
            description = form.description.data
            price = int(form.price.data)  
            rooms = int(form.rooms.data)
            squareMeters = int(form.squareMeters.data) 
            images = request.files.getlist('image')
            user = current_user.id

            propertyId = addPropertyDB(description,images, price, user, rooms, squareMeters)
            addAddress(propertyId, street_name, street_number, city)
            flash('Producto agregado exitosamente', 'success')

            return redirect('/auth/profile')
        except ValueError as ve:
            flash(f'Error en los datos ingresados: {ve}', 'error')
        except Exception as ex:
            flash(f'Error al guardar el producto: {ex}', 'error')

    return render_template('properties/addProperty.html', form=form)

@property_bp.route('/alter/<int:propertyId>', methods=['GET', 'POST'])
@login_required
def alterProperty(propertyId):
    property = getPropertyById(propertyId)
    if not property:
        flash('El producto no existe', 'error')
        return redirect('/home')
    address = getAddressByPropertyId(propertyId)

    form = PropertyForm()

    form.street.data = address['street_name']
    form.streetNumber.data = address['street_number']
    form.city.data = address['city']
    form.description.data = property['description']
    form.price.data = property['price']
    form.rooms.data = int(property['rooms'])
    form.squareMeters.data = property['squareMeters']
    
    if form.validate_on_submit():
        try:

            street_name = form.street.data
            street_number = int(form.streetNumber.data) 
            city = form.city.data
            description = form.description.data
            price = int(form.price.data)  
            rooms = int(form.rooms.data) 
            squareMeters = int(form.squareMeters.data)
            images = request.files.getlist('image')

            updateProperty(propertyId, description,images, price, rooms, squareMeters)
            updateAddress(propertyId, street_name, street_number, city)
            flash('Producto modificado exitosamente', 'success')
            
            return redirect('/auth/profile')
        except ValueError as ve:
            flash(f'Error en los datos ingresados: {ve}', 'error')
        except Exception as ex:
            flash(f'Error al guardar el producto: {ex}', 'error')

    context = {
        'form': form,
        'property': property,
        'address': address
    }
    
    return render_template('properties/addProperty.html', **context)

@property_bp.route('/delete/<int:propertyId>', methods=['GET', 'POST'])
@login_required
def propertyDelete(propertyId):
    deleteProperty(propertyId)
    return redirect('/auth/profile')

@property_bp.route('/contact/<int:property_id>', methods=[ 'POST'])
def sendSellerEmail(property_id):
    property = getPropertyById(property_id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        pregunta = request.form.get('question')
        
        sendSellerInquiry(email, pregunta, property)
        flash('Consulta enviada exitosamente', 'success')
        
        return propertyGET(property_id)
    
    return propertyGET(property_id)