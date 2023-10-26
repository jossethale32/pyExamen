import socket
import mysql.connector
import threading
import requests

# Configura la conexión a la base de datos\
mydb = mysql.connector
try:
    mydb = mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="pago_en_linea")
except mysql.connector.Error as err:
    print("DB-"+str(err))
    mydb.close()
except Exception as g:
    print("DB-"+str(g))
    mydb.close()

# Configura el servidor de sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Función para manejar las conexiones de los clientes
def handle_client(client_socket,addr):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.startswith('C'):
                # print("Consultar")
                _, id = data.split(',')
                pagos = getPagos(id)
                client_socket.send(str(pagos).encode('utf-8'))
            elif data.startswith('P'):
                # print("Pagos")
                _, id, _, _, _, = data.split(',')
                _, _, cuota, _, _,= data.split(',')
                _, _, _, fecha, _, = data.split(',')
                _, _, _, _, monto = data.split(',')
                spagos = setPagos(id,cuota,fecha,monto)
                client_socket.send(str(spagos).encode('utf-8'))
            elif data.startswith('R'):
                print("Reversion")
                # _, id_usuario, nuevo_nombre = data.split(',')
                # actualizar_usuario(int(id_usuario), nuevo_nombre)
                # usuarios = leer_usuarios()
                # client_socket.send(str(usuarios).encode('utf-8'))
            elif data.startswith('E'):
                print("Salir")
                break
            else:
                print("Nuevo Cliente IP: " + str(data))
        except socket.timeout as erroT:
            print(erroT)
            break
        except Exception as erro:
            print(erro)
            break
    client_socket.close()

def getPagos(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM pagos where `ID CLIENTE` = "+id)
        pagos = cursor.fetchall()
        return pagos
    except mysql.connector.Error as e:
        print("⚠️No se pudo actualizar la lista de Pagos")

def setPagos(id,cuota,fecha,monto):
    state=""
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT ESTADO FROM pagos where `ID CLIENTE` = "+id)
        state = cursor.fetchone()
    except mysql.connector.Error as e:
        # print("⚠️No se pudo verificar el estado de esa cuota")
        return "Algo Fallo del lado del server!"
    
    if state[0] == "A":
        # SE PUEDE REALIZAR PAGO
 
        cursor = mydb.cursor()
        cursor.execute("UPDATE pagos set `ESTADO` = 'P' where `ID CLIENTE` = "+id)
        mydb.commit()
    elif state[0] == "P":
        # NO SE PUEDE REALIZAR PAGO PORQUE ESTA PAGADO
        return "Cuota ya se encuentra Pagada.."
    elif state[0] == "F":
        # SE PUEDE PAGAR LO QUE DEBE DE LA CUOTA
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT MONTO FROM pagos where `ID CLIENTE` = "+id+" AND CUOTA = "+cuota)
            montof = cursor.fetchone()
        except mysql.connector.Error as e:
            return "Algo Fallo del lado del server!"
        
        # HACER CALULOS PARA ACTUALIZAR PAGO
        monto = float(monto) #Monto a pagar
        montof = float(montof[0]) #Monto faltante por pagar
        diferencia = montof - monto
        estatusPagado =""
        if diferencia < 0:
            # Estoy pagando de mas no puedo!
            return "No se puede pagar mas!"
        elif diferencia == 0:
            # Puede pagar porque esta dando lo que le falta
            cursor = mydb.cursor()
            cursor.execute("UPDATE pagos set MONTO = "+str(diferencia)+" where `ID CLIENTE` = "+id+" AND CUOTA = "+cuota)
            mydb.commit()
        

        return "Cuota ya se encuentra Pagada.."

# Función para iniciar el servidor de sockets
def start_server():
    print("Servidor Iniciado...\nEsperando Conexion...")
    
    while True:
        try:
            client_socket, addr = server_socket.accept()
            # print(f"Cliente conectado: {addr} ")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,addr))
            client_handler.start()
        except KeyboardInterrupt:
            server_socket.close()
            break
        except Exception as ee:
            print(ee)

# Inicia el servidor de sockets
start_server()