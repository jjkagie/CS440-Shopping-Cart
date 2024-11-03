from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask import session
import backend_code.customer_accessor
accessor = backend_code.customer_accessor.customer_accessor()
app = Flask(__name__)

@app.route("/")
def home(username="Michael",password="my_password"):
    redirect("/login")
    return render_template("login.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))

        if accessor.login(username,password):
            return render_template("main.html",items=accessor.get_item_selections())
        else:
            accessor.create_account(username,password)
            return render_template("main.html",items=accessor.get_item_selections())
        
    return render_template("login.html")

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = str(request.form.get('name'))
        source = str(request.form.get('source'))
        print(name, source)
        item = accessor.create_item(name,source,1)
        #if item:
        #   accessor.add_item_to_cart(item, 1)
    
    return render_template("main.html",items=accessor.get_item_selections())

@app.route("/remove", methods=['GET','POST'])
def remove():
    item = 0
    if request.method == 'POST':
        name = str(request.form.get("removeName"))
        source = str(request.form.get("removeSource"))
        print(name, source)
        items = accessor.get_item_selections()
        for i in items:
            if i.get_item().get_name() == name and i.get_item().get_source() == source:
                item = i.get_item()
        if item:
            accessor.remove_item_from_cart(item)

    return render_template("main.html",items=accessor.get_item_selections())