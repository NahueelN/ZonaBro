from flask import Blueprint, render_template, request, redirect, flash,url_for
from ..controllers.userController import loginn,getUserByEmail, addUser,updateUser,getUserById,checkPassword
from ..controllers.propertyController import getPropertiesByUserId,getImagesByPropertyId,getAddressByPropertyId
from app.models.formUser import UserForm,RegisterForm
from flask_login import login_user, logout_user,login_required,current_user


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(include_nombre=False)
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        logged_user = loginn(email,password)
        if logged_user!=None:
            login_user(logged_user)
            return redirect('profile')
        else:
            form.email.errors.append('Usuario o contraseña incorrectos')

    return render_template('users/login.html', form=form)

'''@auth_bp.route('/register', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        if getUserByEmail(email) is not None:
            form.email.errors.append('El correo electrónico ya está registrado')
        else:
            addUser(email, password, name)
            login()
            return redirect('profile')
        
    return render_template('users/register.html', form=form)
'''

@auth_bp.route('/profile', methods=["GET"])
@login_required
def profile():
    properties = getPropertiesByUserId(current_user.id)
    profile = True
    
    context = {
        'properties': properties,
        'propertyImages': {},
        'propertyAddress': {},
        'profile': profile
    }
    
    for property in properties:
        property_id = property['id']
        context['propertyImages'][property_id] = getImagesByPropertyId(property_id)
        context['propertyAddress'][property_id] = getAddressByPropertyId(property_id)

    return render_template('users/profile.html', **context)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm() 

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data if form.password.data else None
            name = form.name.data

            try:
                addUser(email, password, name)
                flash('Usuario registrado correctamente', 'success')
                return redirect(url_for('auth.profile'))
            except ValueError as e:
                flash(str(e), 'error')

    return render_template('users/register.html', form=form, is_editing=False)

'''
@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    user=getUserById(current_user.id)
    form = RegisterForm()

    form.name.data = current_user.name
    form.email.data = current_user.email
    form.password.data = current_user.password

    if form.validate_on_submit():
        try:
            name = form.name.data
            email = form.email.data
            password = form.password.data

            updateUser(current_user.id, email, password, name)
           
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as ex:
            flash(f'Error al actualizar el perfil: {ex}', 'error')


    return render_template('users/edit_profile.html', )
'''


@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = getUserById(current_user.id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('home.index'))

    form = RegisterForm()
    form.name.data = user['name']

    form.email.data = user['email']

    if form.validate_on_submit():
        current_password = form.current_password.data
        name = form.name.data
        email = form.email.data
        password = form.password.data if form.password.data else current_user.password 
        print(checkPassword(current_user.id, current_password))
        if not checkPassword(current_user.id, current_password):
            flash('La contraseña actual es incorrecta', 'error')
        else:
            try:
                updateUser(current_user.id, email, password, name)
                flash('Perfil actualizado correctamente', 'success')
                return redirect(url_for('auth.profile'))
            except Exception as ex:
                flash(f'Error al actualizar el perfil: {ex}', 'error')

    return render_template('users/edit_profile.html', form=form)