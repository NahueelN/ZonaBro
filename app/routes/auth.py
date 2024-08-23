from flask import Blueprint, render_template, request, redirect, flash,url_for
from ..controllers.userController import loginn,getUserByEmail, addUser
from ..controllers.propertyController import getPropertiesByUserId,getImagesByPropertyId
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

@auth_bp.route('/register', methods=['GET', 'POST'])
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


@auth_bp.route('/profile', methods=["GET"])
@login_required
def perfil():
    properties = getPropertiesByUserId(current_user.id)
    profile=True
    propertyImages = {}
    for property in properties:
        images = getImagesByPropertyId(property['id'])
        propertyImages[property['id']] = images
    return render_template('users/profile.html',properties=properties,propertyImages=propertyImages,profile=profile)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))