from flask import Flask, request, jsonify, redirect, url_for
from jsonable import Jsonable
from CustomerAccessor.customer_accessor import item_accessor

app = Flask(__name__)

@app.route('/accounts/<username>/items')
def getItems(username):
    accessor = item_accessor(username)
    print(username)
    items = accessor.get_item_selections()
    
    return jsonify([(item.get_item().get_name(), item.get_item().get_source()) for item in items])

@app.route('/accounts/<username>/items/add/<name>/<source>', methods=['POST'])
def add(username, name, source):
    accessor = item_accessor(username)
    item = accessor.create_item(name, source)

    if item:
        accessor.add_item_to_cart(item, 1)
        print("Added")
        
    return jsonify(Jsonable(item))

@app.route('/accounts/<username>/items/remove/<name>/<source>', methods=['POST'])
def remove(username, name, source):
    accessor = item_accessor(username)
    item = accessor.create_item(name, source)

    if item:
        print("Removed")
        accessor.remove_item_from_cart(item)
        
    return jsonify(Jsonable(item))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)