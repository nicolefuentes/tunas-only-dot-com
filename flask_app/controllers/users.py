from ast import Delete
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.testimonial import Testimonial
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.testimonial import Testimonial

from datetime import date

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    all_testimonials=Testimonial.get_testimonials()
    return render_template('index.html', all_testimonials=all_testimonials)

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "confirm": request.form['confirm'],
        "birthdate": request.form['birthdate'],
        "user_type": request.form['user_type'],
        "looking_for": request.form['looking_for'],
        "bio": request.form['bio']
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    all_users=User.get_by_id_except(data)
    return render_template("dashboard.html",user=user, all_users=all_users)

@app.route('/edit-profile')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("edit-profile.html",user=User.get_by_id(data))

@app.route('/user/update',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_user_update(request.form):
        return redirect('/edit-profile')
    data ={
        'id': session['user_id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "birthdate": request.form['birthdate'],
        "user_type": request.form['user_type'],
        "looking_for": request.form['looking_for'],
        "bio": request.form['bio']
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/testimonial', methods=['POST'])
def testimonial():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "testimonial": request.form['testimonial'],
        "share": request.form['share'],
        "user_id": request.form['user_id']
    }
    Testimonial.save(data)
    return redirect('/dashboard')

@app.route('/view-profile/<int:user_profile_id>')
def view_profile(user_profile_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': user_profile_id
    }
    user_profile=User.get_by_id(data)
    user=User.get_by_id(data)
    return render_template("view-profile.html", user_profile=user_profile, user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete-profile/<int:user_id>')
def delete(user_id):
    data ={
        'user_id': user_id
    }
    User.delete(data)
    return redirect('/logout')