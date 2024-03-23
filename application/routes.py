#from application import app
#from flask import render_template, request, json, Response

from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session
from application.models import User, Contact
from application.forms import LoginForm, RegisterForm, ContactForm
classes = {
    "Battery": "images/batteries.jpg",
    "Biological": "images/biological.jpg",
    "Brown Glass": "images/brown-glass.jpg",
    "Cardboard": "images/cardboard.jpg",
    "White Glass": "images/white-glass.jpg",
    "Clothes": "images/clothes.jpg",
    "Green Glass": "images/green-glass.jpg",
    "Metal": "images/metal-scrap.jpg",
    "Paper": "images/paper.jpg",
    "Plastic": "images/plastic.jpg",
    "Shoes": "images/shoes.jpg",
    "Trash": "images/trash.jpg"
    
}
carousel = {
    "images/logo1.png",
    "images/logo2.png",
    "images/logo3.png",
    "images/logo4.png",
    "images/logo.jpg"
}

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", classes = classes, carousel= carousel, index=True )

@app.route("/image_upload")
def image_upload():
    return render_template("image_upload.html", login=True )

@app.route("/video_upload")
def video_upload():
    return render_template("video_upload.html", login=True )

@app.route("/live_camera")
def live_camera():
    return render_template("live_camera.html", login=True )

@app.route("/about_us")
def about_us():
    return render_template("about_us.html", login=True )

#@app.route("/contact_us")
#def contact_us():
#   return render_template("contact_us.html", login=True )

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for('index'))
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )


@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/contact_us", methods=['POST', 'GET'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        email       = form.email.data
        first    = form.first.data
        subject  = form.subject.data
        message   = form.message.data

        contact = Contact( email=email, first=first, subject=subject, message = message)
        contact.save()
        flash("Message Sent  Successfully!","success")
        return redirect(url_for('index'))
    return render_template("contact_us.html", title="contact us", form=form)

        

