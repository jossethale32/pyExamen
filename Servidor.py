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
                print("Pagos")
                # usuarios = leer_usuarios()
                # client_socket.send(str(usuarios).encode('utf-8'))
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