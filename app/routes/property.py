from flask import Blueprint, render_template,flash, redirect,request
from ..controllers.propertyController import getPropertyById,addImage,updateProperty,addProperty,deleteProperty,getImagesByPropertyId,addAddress,getAddressByPropertyId,sendSellerInquiry
from flask_login import login_required, current_user
from ..models.formProperty import PropertyForm

property_bp = Blueprint('property', __name__, url_prefix='/property')

@property_bp.route('/<int:id>')
def property(id):
    property = getPropertyById(id)
    context = {
        'property': property,
        'propertyImages': getImagesByPropertyId(id),
        'propertyAddress': getAddressByPropertyId(id)
    }
    
    return render_template('properties/property.html', **context)

@property_bp.route('/add', methods=['GET', 'POST'])
@property_bp.route('/alter/<int:propertyId>', methods=['GET', 'POST'])
@login_required
def manageProperty(propertyId=None):
    if propertyId:
        property = getPropertyById(propertyId)
        if not property:
            flash('El producto no existe', 'error')
            return redirect('/home')
        address = getAddressByPropertyId(propertyId)
    else:
        property = None
        address = None

    form = PropertyForm()

    if property:
        form.street.data = address['street_name']
        form.streetNumber.data = address['street_number']
        form.city.data = address['city']
        form.description.data = property['description']
        form.price.data = property['price']
        form.rooms.data = property['rooms']
        form.squareMeters.data = property['squareMeters']

    if form.validate_on_submit():
        street_name = form.street.data
        street_number = form.streetNumber.data
        city = form.city.data
        description = form.description.data
        price = form.price.data
        images = request.files.getlist('image')
        user = current_user.id
        rooms = form.rooms.data
        squareMeters = form.squareMeters.data
        
        try:
            if propertyId:
                updateProperty(propertyId, description, price, rooms, squareMeters)
                addAddress(propertyId, street_name, street_number, city)
                flash('Producto modificado exitosamente', 'success')
                for image in images:
                    if image:
                        addImage(propertyId, image)
                return redirect('/auth/profile')
            else:
                propertyId = addProperty(description, price, user, rooms, squareMeters)
                addAddress(propertyId, street_name, street_number, city)
                flash('Producto agregado exitosamente', 'success')
                for image in images:
                    if image:
                        addImage(propertyId, image)
                return redirect('/auth/profile')
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

@property_bp.route('/contact/<int:property_id>', methods=['GET', 'POST'])
def sendSellerEmail(property_id):
    property = getPropertyById(property_id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        pregunta = request.form.get('question')
        
        sendSellerInquiry(email, pregunta, property)
        flash('Consulta enviada exitosamente', 'success')
        
        context = {
            'property': property,
            'propertyImages': getImagesByPropertyId(property_id),
            'propertyAddress': getAddressByPropertyId(property_id)
        }
        return render_template('properties/property.html', **context)
    
    context = {
        'property': property
    }
    return render_template('properties/contact.html', **context)