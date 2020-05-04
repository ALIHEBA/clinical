
import mysql.connector
from flask import Flask, redirect, url_for, request,render_template,flash, send_file
from flask_table import Table, Col
from io import BytesIO
import os
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="CMMS"
)
mycursor = mydb.cursor()
app = Flask(__name__)
app.config['UPLOAD_FOLDER']  ="C:/Users/Lenovo/CMMS/static/uploads"
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/Equipments', methods=['POST','GET'])
def Equipments():
  if request.method == 'POST':
    equipment = request.form["Equipment"]
    installation = request.form["Installation date"]
    warranty = request.form["Warranty date"]
    if equipment == '':
      mycursor.execute("SELECT * FROM Equipment")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }
      return render_template("Equipments.html",data=data)
      # return render_template("Equipments.php",data=data)

    else :
      mycursor.execute("SELECT * FROM Equipment WHERE Name= '" +equipment+ "' AND Installation_date = '" +installation+ "' AND Warranty_expires = '" +warranty+ "' ")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }
      return render_template("Equipments.html",data=data)
      # return render_template("Equipments.php",data=data)

  else:
    mycursor.execute("SELECT * FROM Equipment")
    row_headers=[x[0] for x in mycursor.description] 
    myresult = mycursor.fetchall()
    data={
    'message':"data retrieved",
    'rec':myresult,
    'header':row_headers
    }
    return render_template("Equipments.html",data=data)
    # return render_template("Equipments.php",data=data)

@app.route('/addEquipment', methods=['POST','GET'])
def addEquipment():
  if request.method == 'POST':
    Asset_ID = request.form["Asset_ID"]
    Name = request.form["Name"]
    Serial_number = request.form["Serial_number"]
    Model_number = request.form["Model_number"]
    Model_name = request.form["Model_name"]
    Manufacturer = request.form["Manufacturer"]
    Installation_date = request.form["Installation_date"]
    Warranty_expires = request.form["Warranty_expires"]
    Facility = request.form["Facility"]
    Building = request.form["Building"]
    Floor = request.form["Floor"]
    Department = request.form["Department"]
    Scrapping_date = request.form["Scrapping_date"]
    filedata = request.files['Data_sheet'] 
    # sheet = filedata.filename
    sheet = Name+'_'+Asset_ID+'.pdf'
    uploads_dir = "C:/Users/Lenovo/CMMS/static/uploads"
    filedata.save(os.path.join(uploads_dir, sheet))  
    sql = "INSERT INTO Equipment(Asset_ID, Name ,Serial_number ,Model_number,Model_name,Manufacturer,Installation_date,Warranty_expires,Facility,Building,Floor,Department,Scrapping_date,Data_sheet) VALUES (%s,%s,%s, %s ,%s ,%s,%s, %s ,%s,%s,%s,%s,%s,%s )"
    val = (Asset_ID, Name ,Serial_number ,Model_number,Model_name,Manufacturer,Installation_date,Warranty_expires,Facility,Building,Floor,Department,Scrapping_date, sheet)
    mycursor.execute(sql, val)
    mydb.commit() 
    return render_template("/addEquipment.html")
	
  else:
    return render_template("/addEquipment.html")
 
@app.route('/parts', methods=['POST','GET'])
def parts():

  if request.method == 'POST':
    Name = request.form["Name"]
    print(Name)
    if Name != '' :
      mycursor.execute("SELECT Inventory.Part_Number,Inventory.Name,Inventory.Asset_ID,Inventory.Vendor,Inventory.Cost,Inventory.Quantity,Equipment.Name as Asset_Name FROM `Inventory` JOIN `Equipment` WHERE Equipment.Asset_ID=Inventory.Asset_ID AND Inventory.Name = '" +Name+ "'") 
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }
    else:
      mycursor.execute("SELECT Inventory.Part_Number,Inventory.Name,Inventory.Asset_ID,Inventory.Vendor,Inventory.Cost,Inventory.Quantity,Equipment.Name as Asset_Name FROM `Inventory` JOIN `Equipment` WHERE Equipment.Asset_ID=Inventory.Asset_ID")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }

    return render_template("parts.html",data=data)

  else:
    mycursor.execute("SELECT Inventory.Part_Number,Inventory.Name,Inventory.Asset_ID,Inventory.Vendor,Inventory.Cost,Inventory.Quantity,Equipment.Name as Asset_Name FROM `Inventory` JOIN `Equipment` WHERE Equipment.Asset_ID=Inventory.Asset_ID")
    row_headers=[x[0] for x in mycursor.description] 
    myresult = mycursor.fetchall()
    data={
    'message':"data retrieved",
    'rec':myresult,
    'header':row_headers
    }
    return render_template("parts.html",data=data)

@app.route('/addParts' , methods=['POST','GET'] )
def addParts():
 if request.method == 'POST':
   Part_Number = request.form["Part_Number"]
   Name = request.form["Name"]
   Asset_ID = request.form["Asset_ID"]
   Vendor = request.form["Vendor"]
   Cost = request.form["Cost"]
   Quantity = request.form["Quantity"]
   sql = "INSERT INTO Inventory(Part_Number, Name ,Asset_ID ,Vendor,Cost,Quantity) VALUES (%s,%s,%s, %s ,%s ,%s)"
   val = (Part_Number, Name ,Asset_ID ,Vendor,Cost,Quantity)
   mycursor.execute(sql, val)
   mydb.commit() 
    
   return render_template("addParts.html")

 else:

   return render_template("addParts.html")
	
@app.route('/editEquipment', methods=['POST','GET'])
def editEquipment():
  if request.method == 'POST':
    Asset_ID = request.form["Asset_ID"]
    Installation_date = request.form["Installation_date"]
    Warranty_expires = request.form["Warranty_expires"]
    Facility = request.form["Facility"]
    Building = request.form["Building"]
    Floor = request.form["Floor"]
    Department = request.form["Department"]
    Scrapping_date = request.form["Scrapping_date"]
    sql = """UPDATE Equipment set Installation_date=%s,Warranty_expires=%s,Facility=%s,Building=%s,Floor=%s,Department=%s,Scrapping_date=%s where Asset_ID=%s """
    val = (Installation_date,Warranty_expires,Facility,Building,Floor,Department,Scrapping_date,Asset_ID)
    mycursor.execute(sql, val)
    mydb.commit() 
    return render_template("/editEquipment.html")
	
  else:
    return render_template("/editEquipment.html")

@app.route('/editParts', methods=['POST','GET'])
def editParts():
  if request.method == 'POST':
    Part_Number = request.form["Part_Number"]
    Vendor = request.form["Vendor"]
    Cost = request.form["Cost"]
    Quantity = request.form["Quantity"]
    sql = """UPDATE Inventory set Vendor=%s,Cost=%s,Quantity=%s where Part_Number=%s """
    val = (Vendor,Cost,Quantity,Part_Number)
    mycursor.execute(sql, val)
    mydb.commit() 
    return render_template("/editParts.html")
	
  else:
    return render_template("/editParts.html")

@app.route('/Reports', methods=['POST','GET'])
def Reports():
  return render_template('Reports.html')


@app.route('/addOrder', methods=['POST','GET'])
def addOrder():
  if request.method == 'POST':
    Asset_ID = request.form["Asset_ID"]
    Name = request.form["Name"]
    Order_number = request.form["Order_number"]
    Status = request.form["Status"]
    Demand_PM= request.form["Repair/PM"]
    Due_date = request.form["Due_date"]
    Creation__date = request.form["Creation__date"]
    PM_date = request.form["PM_date"]
    PM_frequency = request.form["PM_frequency"]
    Priority = request.form["Priority"]
    Description = request.form["Description"]
    Demand_cost = request.form["Demand_cost"] 
    sql = "INSERT INTO Work_orders(Asset_ID, Name ,Order_number ,Status,`Repair/PM`,Due_date,Creation__date,PM_date,PM_frequency,Priority,Description,Demand_cost) VALUES (%s, %s ,%s ,%s,%s, %s ,%s,%s,%s,%s,%s,%s )"
    val = (Asset_ID, Name ,Order_number ,Status,Demand_PM,Due_date,Creation__date,PM_date,PM_frequency,Priority,Description,Demand_cost)
    mycursor.execute(sql, val)
    mydb.commit() 
    return render_template("/addOrder.html")
	
  else:
    return render_template("/addOrder.html")

@app.route('/editOrder', methods=['POST','GET'])
def editOrder():
  if request.method == 'POST':
    Name = request.form["Name"]
    Order_number = request.form["Order_number"]
    Status = request.form["Status"]
    Demand_PM= request.form["Repair/PM"]
    Due_date = request.form["Due_date"]
    Creation__date = request.form["Creation__date"]
    PM_date = request.form["PM_date"]
    PM_frequency = request.form["PM_frequency"]
    Priority = request.form["Priority"]
    Description = request.form["Description"]
    Demand_cost = request.form["Demand_cost"]
    sql = """UPDATE Work_orders set Name=%s,Status=%s,`Repair/PM`=%s,Due_date=%s,Creation__date=%s,PM_date=%s,PM_frequency=%s,Priority=%s,Description=%s,Demand_cost=%s  where Order_number=%s """
    val = (Name,Status,Demand_PM,Due_date,Creation__date,PM_date,PM_frequency,Priority,Description,Demand_cost,Order_number)
    mycursor.execute(sql, val)
    mydb.commit() 
    return render_template("/editOrder.html")
	
  else:
    return render_template("/editOrder.html")

@app.route('/View workorders', methods=['POST','GET'])
def View workorders():
	if request.method == "POST":
        details = request.form
        Order_number= details['Order_number']
        Asset_ID = details['Asset_ID']
	Name = details['Name']
	Status = details['Status']
	Creation_date= details['Creation_date']
	Demand = details['Demand']
	Start_date = details['Start_date']
	Due_date = details['Due_date']
	PM_date = details['PM_date']
	PM_frequancy = details['PM_frequancy']
	Priority = details['Priority']
	Description= details['Description']
	Association= details['Association']
	Demand_cost= details['Demand_cost']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO workorders(Order_number,Asset_ID ,Name,Status,Creation_date,Demand,Start_date,Due_date,PM_date,PM_frequancy,Priority,Description,Association,Demand_cost) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_number,Asset_ID ,Name,Status,Creation_date,Demand,Start_date,Due_date,PM_date,PM_frequancy,Priority,Description,Association,Demand_cost))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('workorders.html')

  if request.method == 'POST':
    view workorders = request.form["workorders"]
    installation = request.form["Installation date"]
    warranty = request.form["Warranty date"]
    if View workorders == '':
      mycursor.execute("SELECT * FROM workorders")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }
      return render_template("workorders.html",data=data)

    else :
      mycursor.execute("SELECT * FROM workorders WHERE Name= '" +workorders+ "' AND Installation_date = '" +installation+ "' AND Warranty_expires = '" +warranty+ "' ")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
      }
      return render_template("workorders.html",data=data)
     

  else:
    mycursor.execute("SELECT * FROM workorders")
    row_headers=[x[0] for x in mycursor.description] 
    myresult = mycursor.fetchall()
    data={
    'message':"data retrieved",
    'rec':myresult,
    'header':row_headers
    }
    return render_template("workorders.html",data=data)
   

if __name__ == '__main__':
	app.run(debug=True)
