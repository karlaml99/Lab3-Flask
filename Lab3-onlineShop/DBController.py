import pymysql
class dbController:
    def __init__(self, hostIP, hostPort, hostPass, dbUser, dbName):
        #atributos
        self.host = hostIP
        self.port = hostPort
        self.username = dbUser
        self.db = dbName
        self.password = hostPass 
        #conexion a mysql
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.db
        )
        #ejecutar acciones - canal entre db y programa
        self.cursor = self.connection.cursor()
     #metodo para hacer un insert en la base de datos
    def insertNewUser(self, usName, usPass, email, now):
        sql = "INSERT INTO usuarios (username, password, email, creationDate) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (usName, usPass, email, now))
        self.connection.commit()
        self.dbCloseConnection()
    #metodo para modificar usuario, contraseña y correo
    def updateUser(self, usName, usPass, email, idU):
        sql = "UPDATE Usuarios SET username = %s, password = %s, email = %s WHERE idUsuario = %s"
        self.cursor.execute(sql, (usName, usPass, email, idU))
        self.connection.commit()
        self.dbCloseConnection()
    #metoddo para cerrar la conexion a la base de datos
    def dbCloseConnection(self):
        self.connection.close()
    #consultar informacion de usuario
    def getUser(self, usName):
        sql = "SELECT * FROM usuarios WHERE username = %s"
        self.cursor.execute(sql, usName)
        rows = self.cursor.fetchall()
        self.dbCloseConnection()
        print(rows)
    #consultar informacion de compra
    def getCompra(self, usName):
        sql = "SELECT * FROM Compras WHERE userID = %s"
        self.cursor.execute(sql, usName)
        rows = self.cursor.fetchall()
        self.dbCloseConnection()
        print(rows)
    #Consultar compras que se encuentren en un rango especifico de fecha
    def getRangeTotalCompra(self, total1, total2):
        sql = "SELECT * FROM Compras WHERE TotalCompra between %s and %s"
        self.cursor.execute(sql, (total1, total2))
        rows = self.cursor.fetchall()
        self.dbCloseConnection()
        print(rows)
    #Consultar la lista de todos los productos y el precio de cada uno 
    def getAllUsers(self):
        self.cursor.execute("SELECT nombreProducto, precioUnitario FROM productos")
        rows = self.cursor.fetchall()
        self.dbCloseConnection()
        print (rows) 
    #editar el monto total de una compra
    def updateTotal(self, newMonto, TotalCompra):
        sql = "UPDATE compras SET TotalCompra=%s WHERE idCompra = %s"
        self.cursor.execute(sql, (newMonto, TotalCompra))
        self.connection.commit()
        self.dbCloseConnection()
    #Editar la cantidad y precio de un detalle de compra
    def updateCantidadPrecio(self,cantidad,precio,idDetalleCompra):
        sql = "UPDATE detalleCompras SET cantidad=%s, precio=%s WHERE idDetalleCompra = %s"
        self.cursor.execute(sql, (cantidad,precio,idDetalleCompra))
        self.connection.commit()
        self.dbCloseConnection()
    #insertar compra
    def insertCompras(self, usTotalC, now, userID):
        sql = "INSERT INTO Compras(totalCompra, fechaHoraCompra, IDUsuario) VALUES(%s, %s, %s);"
        self.cursor.execute(sql, (usTotalC, now, userID))
        self.connection.commit()
        self.dbCloseConnection()