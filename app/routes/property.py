from flask import Blueprint, render_template,flash, redirect,request
from ..controllers.propertyController import getPropertyById,addImage,updateProperty,addProperty,deleteProperty,getImagesByPropertyId
from flask_login import login_required, current_user
from ..models.formProperty import PropertyForm

property_bp = Blueprint('property', __name__, url_prefix='/property')

@property_bp.route('/<int:id>')
def property(id):
    property=getPropertyById(id)
    propertyImages={}
    propertyImages=getImagesByPropertyId(id)
    return render_template('properties/property.html', property=property,propertyImages=propertyImages)

@property_bp.route('/add', methods=['GET', 'POST'])
@property_bp.route('/alter/<int:propertyId>', methods=['GET', 'POST'])
@login_required
def manageProperty(propertyId=None):
    if propertyId:
        property = getPropertyById(propertyId)
        if not property:
            flash('El producto no existe', 'error')
            return redirect('home')
    else:
        property = None
    
    form = PropertyForm(obj=property)

    if form.validate_on_submit():
        street = form.street.data
        streetNumber = form.streetNumber.data
        city = form.city.data
        description = form.description.data
        price = form.price.data
        images = request.files.getlist('image')
        user = current_user.id
        address = f"{streetNumber} {street}, {city}"
        rooms = form.rooms.data
        squareMeters = form.squareMeters.data
        
        try:
            if propertyId:
                updateProperty(propertyId, address, description, price,rooms,squareMeters)
                flash('Producto modificado exitosamente', 'success')
                for image in images:
                    if image:
                        addImage(propertyId, image)
                return redirect('/auth/profile')
            else:
                propertyId = addProperty(address, description, price, user,rooms,squareMeters)
                print(propertyId)
                flash('Producto agregado exitosamente', 'success')
                for image in images:
                    if image:
                        addImage(propertyId, image)
                return redirect('/auth/profile')
        except Exception as ex:
            print(f'Error al guardar el producto: {ex}', 'error')
    
    return render_template('properties/addProperty.html', form=form, property=property)

@property_bp.route('/delete/<int:propertyId>', methods=['GET', 'POST'])
@login_required
def propertyDelete(propertyId):
    deleteProperty(propertyId)
    return redirect('/auth/profile')

