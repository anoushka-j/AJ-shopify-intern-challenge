from flask import Flask, render_template, request, session, Response
import sqlite3

app = Flask(__name__)
app.secret_key = "key"
conn = sqlite3.connect("inventory.db")
c = conn.cursor()

create_inventory_table = """CREATE TABLE IF NOT EXISTS inventory (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  item_name TEXT, 
  item_price REAL, 
  item_quantity INTEGER, 
  item_inventory_value REAL
)"""

# update_inventory = f"""UPDATE inventory SET item_name = "item 4",  item_price = 12.00, item_quantity = 4, item_inventory_value = 48.00
#     WHERE item_id = 2"""


def validateInput(inputs) : 
  for input in inputs :  
    if not len(input) : 
      return False 

  try : 
    float_item_price = float(inputs[1])
    int_item_quantity = int(inputs[2])
    float_item_inventory_price = float(inputs[3])
  except : 
    return False 
  
  return True 


def updateInventory(conn, query) : 
  conn = sqlite3.connect("inventory.db")
  c = conn.cursor()
  c.execute(query)
  conn.commit()
  result = c.fetchall()
  return result

#updateInventory(conn, update_inventory)

# add_item = """INSERT INTO inventory
#   (item_name, item_price, item_quantity, item_inventory_value) VALUES ("item 2", 1334.4, 3, 5284.12)
#   """


#check = """DROP table inventory"""
updateInventory(conn, create_inventory_table)
#updateInventory(conn, check)
#updateInventory(conn, select_item)


@app.route("/")
def home() : 
  return render_template('index.html')

@app.route("/edit", methods=["POST", "GET"])
def edit() : 
  items = updateInventory(conn, "SELECT item_id FROM inventory")
  numItems = len(items)
  print(numItems)
  itemNames = updateInventory(conn, "SELECT item_name FROM inventory")
  print(itemNames)
  itemQuantities = updateInventory(conn, "SELECT item_quantity FROM inventory")
  print(itemQuantities)
  itemPrices = updateInventory(conn, "SELECT item_price FROM inventory")
  print(itemPrices)
  inventoryItemValues = updateInventory(conn, "SELECT item_inventory_value FROM inventory")
  print(inventoryItemValues)
  return render_template("edit.html", items=items, numItems=numItems, itemNames=itemNames, itemQuantities=itemQuantities, itemPrices=itemPrices, inventoryItemValues=inventoryItemValues)

@app.route("/editItem", methods=["POST", "GET"])
def editItem() : 
  initialState = True
  inputIsValid = True
  editsSaved = False 
  current_item_id = request.args.get('itemId')
  current_item_name = request.args.get('itemName')
  current_item_price = request.args.get('itemPrice')
  current_item_quantity = request.args.get('itemQuantity')
  current_item_inventory = request.args.get('inventoryItemValue')
  if request.method == "POST" : 
    initialState = False 
    current_item_id = request.args.get('itemId')
    print(current_item_name)
    new_item_name = request.form['item_name']
    new_item_price = request.form['item_price']
    new_item_quantity = request.form['item_quantity']
    new_item_inventory = request.form['item_inventory_value']
    inputs = [new_item_name, new_item_price, new_item_quantity, new_item_inventory]
    inputIsValid = validateInput(inputs)
    print("inputIsValid", inputIsValid)
    if inputIsValid : 
      editsSaved = True 
      edit_row = f"""UPDATE inventory SET item_name = "{new_item_name}", item_price = {new_item_price}, item_quantity = {new_item_quantity}, item_inventory_value = {new_item_inventory} WHERE item_id = {current_item_id}"""

      updateInventory(conn, edit_row)
    else : 
      initialState = True 

  return render_template("editItem.html", editsSaved=editsSaved, initialState=initialState, inputIsValid=inputIsValid, itemId=current_item_id, current_item_name=current_item_name, current_item_price=current_item_price, current_item_quantity=current_item_quantity, current_item_inventory=current_item_inventory) 

@app.route("/create", methods=["POST", "GET"])
def create() : 
  inputIsValid=True
  if request.method == "POST": 
    item_name = request.form['item_name']
    item_price = request.form['item_price']
    item_quantity = request.form['item_quantity']
    item_inventory_value = request.form['item_inventory_value']
    inputs = [item_name, item_price, item_quantity, item_inventory_value]
    inputIsValid = validateInput(inputs)
    if inputIsValid : 

      add_item = f"""INSERT INTO inventory 
      (item_name, item_price, item_quantity, item_inventory_value) VALUES ("{item_name}", {item_price}, {item_quantity}, {item_inventory_value})
      """
      updateInventory(conn, add_item)
  return render_template("create.html", inputIsValid=inputIsValid)

@app.route("/delete", methods=["POST", "GET"])
def delete() : 
  items = updateInventory(conn, "SELECT item_id FROM inventory")
  numItems = len(items)
  itemNames = updateInventory(conn, "SELECT item_name FROM inventory")
  itemQuantities = updateInventory(conn, "SELECT item_quantity FROM inventory")
  itemPrices = updateInventory(conn, "SELECT item_price FROM inventory")
  inventoryItemValues = updateInventory(conn, "SELECT item_inventory_value FROM inventory")
  return render_template("delete.html", items=items, numItems=numItems, itemNames=itemNames, itemQuantities=itemQuantities, itemPrices=itemPrices, inventoryItemValues=inventoryItemValues)

@app.route("/deleteItem", methods=["POST", "GET"])
def deleteItem() :
  deleted = False
  current_item_id = request.args.get('itemId')
  delete_affirmative = request.args.get('delete_affirmative')
  print(current_item_id)
  if request.method and delete_affirmative: 
    deleted = True
    delete_item = f"""DELETE FROM inventory WHERE item_id = {current_item_id}"""
    select_item = """SELECT * FROM inventory"""
    updateInventory(conn, delete_item)
    req = updateInventory(conn, select_item)
    print(req)
  return render_template('deleteItem.html',itemId=current_item_id, deleted=deleted)



@app.route("/list")
def seeList() : 
  items = updateInventory(conn, "SELECT item_id FROM inventory")
  numItems = len(items)
  itemNames = updateInventory(conn, "SELECT item_name FROM inventory")
  itemQuantities = updateInventory(conn, "SELECT item_quantity FROM inventory")
  itemPrices = updateInventory(conn, "SELECT item_price FROM inventory")
  inventoryItemValues = updateInventory(conn, "SELECT item_inventory_value FROM inventory")
  return render_template("list.html", items=items, numItems=numItems, itemNames=itemNames, itemQuantities=itemQuantities, itemPrices=itemPrices, inventoryItemValues=inventoryItemValues)

@app.route("/export")
def export() : 
  full_inventory = []
  inventory_columns = ('ITEM ID', 'ITEM NAME', 'ITEM PRICE', 'ITEM QUANTITY', 'ITEM INVENTORY VALUE')
  get_inventory_data = """SELECT * FROM inventory"""
  inventory_data = updateInventory(conn, get_inventory_data)
  full_inventory.append(inventory_columns)
  for data in inventory_data : 
    full_inventory.append(data)
  print(full_inventory)

  with open("inventory.csv", "wb") as write_file : 
    for item in full_inventory:
      writeRow = " ".join([str(i) for i in item]) + "\n"
      write_file.write(writeRow.encode())

  with open("inventory.csv") as fp : 
    file = fp.read()
    return Response(
        file,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=inventory.csv"})



if __name__ == "__main__": 
  app.run(debug=True)