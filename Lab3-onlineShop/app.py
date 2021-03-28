from flask import Flask, request, jsonify
import json
import collections
import hashlib
from datetime import datetime
import _datetime
import DBController as DBC
app = Flask(__name__)
#ruta principal
@app.route('/')
def saludo():
    return 'Lab3-onlineShop'
#ruta para insertar nuevo usuario
@app.route('/newUser', methods=['POST'])
def createNewUser():
    try:
        data = request.get_json()
        print(data)
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        #encripcion del password
        usPass = hashlib.md5(data['password'].encode('utf-8'))
        usNameEncode = hashlib.md5(data['username'].encode('utf-8'))
        usPassEncode = (usNameEncode.hexdigest() + usPass.hexdigest()).encode('utf-8')
        ecriptedPass = (hashlib.md5(usPassEncode).hexdigest()).encode('utf-8')
        #email
        email = data['email'].encode('utf-8')
        #insertamos fecha con formato de SQL
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dbConnection.insertNewUser(data['username'], ecriptedPass, email, now)
        return jsonify({'message: ': 'Nuevo usuario creado.'})
    except Exception as ex:
        print(ex)
        return jsonify({'message: ': 'Ocurrio un error.'})
#ruta para modificar usuario y contraseña
@app.route('/modify/<userId>', methods=['PUT'])
def modify_user_info(userId):
    try:
        data = request.get_json()
        print(data)
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        #encripcion del password
        usPass = hashlib.md5(data['password'].encode('utf-8'))
        usNameEncode = hashlib.md5(data['username'].encode('utf-8'))
        usPassEncode = (usNameEncode.hexdigest() + usPass.hexdigest()).encode('utf-8')
        ecriptedPass = (hashlib.md5(usPassEncode).hexdigest()).encode('utf-8')
        #email
        email = data['email'].encode('utf-8')
        dbConnection.updateUser(data['username'], ecriptedPass, email, userId)
        return jsonify({'message: ': 'Informacion de usuario modificada.'})
    except Exception as ex:
        print(ex)
        return jsonify({'message: ': 'Ocurrio un error.'})
if(__name__ == '__main__'):
    app.run(debug=True)
#Consultar la informacion del usuario en base a su username
@app.route('/oneUser/<user>', methods=['GET'])
def get_one_user(user):
    try:
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        salida = dbConnection.getUser(user)
        return jsonify(salida)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error'})
#Consultar la informacion de la compra de un usuario en base a su username
@app.route('/oneCompra/<userId>', methods=['GET'])
def get_one_Compra(userId):
    try:
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        salida = dbConnection.getCompra(userId)
        return jsonify(salida)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error'})
#Consultar compras que se encuentren en un rango especifico de fecha
@app.route('/oneFechaCompra/<fechaHoraCompra>/<fechaHoraCompra2>', methods=['GET'])
def get_one_Fecha_Compra(fechaHoraCompra, fechaHoraCompra2):
    try:
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        salida = dbConnection.getCompraRange(fechaHoraCompra, fechaHoraCompra2)
        return jsonify(salida)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error'})
#Consultar compras que se encuentren en un rango especifico de valor 
@app.route('/oneTotalCompra/<TotalCompra>/<TotalCompra2>', methods=['GET'])
def get_one_Total_Compra(TotalCompra, TotalCompra2):
    try:
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        salida = dbConnection.getRangeTotalCompra(TotalCompra, TotalCompra2)
        return jsonify(salida)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error'})
#Consultar la lista de todos los productos y el precio de cada uno 
@app.route('/allUsers', methods=['GET'])
def get_all_users():
    try:
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        salida = dbConnection.getAllUsers()
        return jsonify(salida)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error.'})
#editar el monto total de una compra
@app.route('/SetTotalCompra/<idCompra>', methods=['PUT'])
def update_creation_Total(idCompra):
    try:
        data = request.get_json()
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        dbConnection.updateTotal(data['TotalCompra'], idCompra)
        return jsonify({'message': 'Total Actualizado Exitosamente.'})
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error.'})
#Editar la cantidad y precio de un detalle de compra
@app.route('/SetCantidadPrecio/<idDetalleCompra>', methods=['PUT'])
def update_Cantidad_Precio(idDetalleCompra):
    try:
        data = request.get_json()
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        dbConnection.updateCantidadPrecio(data['cantidad'],data['precio'], idDetalleCompra)
        return jsonify({'message': 'Cantidad y precio Actualizado Exitosamente.'})
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un error.'})

#Insertar una nueva compra
@app.route('/newCompra', methods=['POST'])
def create_new_compra():
    try:
        data = request.get_json()
        dbConnection = DBC.dbController('127.0.0.1', 3306, 'mollinedoLopez99*', 'karlaMoll', 'onlineShop')
        Total = data['totalCompra']
        userID = data['userID']

        #insertamos fecha
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        print(Total)
        print(userID)

        dbConnection.insertCompras(Total, now, userID)

        return jsonify({'message': 'Compra creada con exito.'})

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'Ocurrio un problema'})