import socket
import mysql.connector
import threading
import requests
import random
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configura la conexión a la base de datos\
mydb = mysql.connector
try:
    mydb = mysql.connector.connect(
        host="localhost",
        #port=3308,
        user="root",
        password="",
        database="pago_en_linea")
except mysql.connector.Error as err:
    print("DB-" + str(err))
    mydb.close()
except Exception as g:
    print("DB-" + str(g))
    mydb.close()

# Configura el servidor de sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)



# Función para manejar las conexiones de los clientes
def handle_client(client_socket, addr):
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
                _, _, cuota, _, _, = data.split(',')
                _, _, _, fecha, _, = data.split(',')
                _, _, _, _, monto = data.split(',')
                spagos = setPagos(id, cuota, fecha, monto)
                client_socket.send(str(spagos).encode('utf-8'))
                # print(str(id) + '\n'+str(cuota)+'\n'+str(fecha)+'\n'+str(monto))
            elif data.startswith('R'):
                _, id, cuota,monto_anterior = data.split(',')
                resultado_reversion = revertir_cuota(id, cuota,monto_anterior)
                client_socket.send(str(resultado_reversion).encode('utf-8'))

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
        cursor.execute("SELECT * FROM pagos where `ID CLIENTE` = " + id)
        pagos = cursor.fetchall()
        return pagos
    except mysql.connector.Error as e:
        print("⚠️No se pudo actualizar la lista de Pagos")


def revertir_cuota(id, cuota, monto_anterior):
    try:
        # Conectar a la base de datos
        cursor = mydb.cursor()

        # Realizar la reversión en la base de datos y establecer MONTO como monto_anterior
        cursor.execute(
            "UPDATE pagos SET `ESTADO` = 'A', `REFERENCIA` = NULL, `PAGOFECHAREALIZACION` = NULL, `MONTO` = %s WHERE `ID CLIENTE` = %s AND `CUOTA` = %s",
            (monto_anterior, id, cuota))
        mydb.commit()

        return "00"  # Código para reversión exitosa
    except mysql.connector.Error as err:
        print("Error en la base de datos: ", err)
        return "01"  # Código para error en la base de datos

def setPagos(id, cuota, fecha, monto):
    now = datetime.now().date()
    now.strftime("%Y-%m-%d")
    now = str(now)
    state = ""

    # Consultar estado de pago segun cliente y cuota y fecha
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT ESTADO FROM pagos where `ID CLIENTE` = " + id + " AND CUOTA = " + str(cuota))
        state = cursor.fetchone()[0]
        # cursor.close()
    except mysql.connector.Error as e:
        # print("⚠️No se pudo verificar el estado de esa cuota")
        return "Algo Fallo del lado del server! " + str(e)

    # Si el estado esta activo para pagar
    if state[0] == "A":
        # SE PUEDE REALIZAR PAGO
        cursor = mydb.cursor(buffered=True)
        sql = "SELECT MONTO FROM pagos where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` = %s"
        val = (id, cuota, fecha)
        try:
            cursor.execute(sql, val)
            montof = cursor.fetchone()[0]
        except mysql.connector.Error as e:
            return "1-Algo Fallo del lado del server! " + str(e)

        # HACER CALULOS PARA ACTUALIZAR PAGO
        monto = float(monto)  # Monto a pagar
        montof = float(montof)  # Monto faltante por pagar
        diferencia = montof - monto
        if diferencia < 0:
            # Estoy pagando de mas no puedo!
            return "No se puede pagar de mas!"
        elif diferencia == 0:
            # Puede pagar porque esta dando lo que le falta
            cursor = mydb.cursor()
            try:
                refer = str("RFM-") + str(random.randint(1, 857567567))
                sql = "UPDATE pagos set MONTO = %s,`PAGOFECHAREALIZACION` = %s, ESTADO='P', REFERENCIA = %s where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` like %s"

                val = (str(diferencia), now, str(refer), id, cuota, fecha)
                cursor.execute(sql, val)
                mydb.commit()
                return "00"
            except mysql.connector.Error as e:
                try:
                    print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    return "01"
                except IndexError:
                    print("MySQL Error: %s" % str(e))
                    return "01"
            except TypeError as e:
                print(e)
                return "01"
            except ValueError as e:
                print(e)
                return "01"
            except Exception as e:
                print(e)
                return "01"
        elif diferencia > 0:
            # Aun queda debiendo solo reducir monto
            cursor = mydb.cursor()
            try:
                sql = "UPDATE pagos set MONTO = %s,`PAGOFECHAREALIZACION` = %s, ESTADO='F' where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` like %s"

                val = (str(diferencia), now, id, cuota, fecha)
                cursor.execute(sql, val)
                mydb.commit()
                return "00"
            except mysql.connector.Error as e:
                try:
                    print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    return "01"
                except IndexError:
                    print("MySQL Error: %s" % str(e))
                    return "01"
            except TypeError as e:
                print(e)
                return "01"
            except ValueError as e:
                print(e)
                return "01"
            except Exception as e:
                print(e)
                return "01"
    elif state[0] == "P":
        # NO SE PUEDE REALIZAR PAGO PORQUE ESTA PAGADO
        return "Cuota ya se encuentra Pagada.."
    # Si esta media pagada
    elif state[0] == "F":
        # SE PUEDE PAGAR LO QUE DEBE DE LA CUOTA
        cursor = mydb.cursor(buffered=True)
        sql = "SELECT MONTO FROM pagos where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` = %s"
        val = (id, cuota, fecha)
        try:
            cursor.execute(sql, val)
            montof = cursor.fetchone()[0]
        except mysql.connector.Error as e:
            return "1-Algo Fallo del lado del server! " + str(e)

        # HACER CALULOS PARA ACTUALIZAR PAGO
        monto = float(monto)  # Monto a pagar
        montof = float(montof)  # Monto faltante por pagar
        diferencia = montof - monto
        if diferencia < 0:
            # Estoy pagando de mas no puedo!
            return "No se puede pagar mas!"
        elif diferencia == 0:
            # Puede pagar porque esta dando lo que le falta
            cursor = mydb.cursor()
            try:
                sql = "UPDATE pagos set MONTO = %s,`PAGOFECHAREALIZACION` = %s, ESTADO='P', REFERENCIA = %s where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` like %s"

                val = (str(diferencia), now, str(refer), id, cuota, fecha)
                cursor.execute(sql, val)
                mydb.commit()
                return "00"
            except mysql.connector.Error as e:
                try:
                    print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    return "01"
                except IndexError:
                    print("MySQL Error: %s" % str(e))
                    return "01"
            except TypeError as e:
                print(e)
                return "01"
            except ValueError as e:
                print(e)
                return "01"
            except Exception as e:
                print(e)
                return "01"
        elif diferencia > 0:
            # Aun queda debiendo solo reducir monto
            cursor = mydb.cursor()
            try:
                sql = "UPDATE pagos set MONTO = %s,`PAGOFECHAREALIZACION` = %s, ESTADO='F' where `ID CLIENTE` = %s AND CUOTA = %s AND `FECHA PAGO` like %s"

                val = (str(diferencia), now, id, cuota, fecha)
                mydb.commit()
                return "00"
            except mysql.connector.Error as e:
                try:
                    print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    return "01"
                except IndexError:
                    print("MySQL Error: %s" % str(e))
                    return "01"
            except TypeError as e:
                print(e)
                return "01"
            except ValueError as e:
                print(e)
                return "01"
            except Exception as e:
                print(e)
                return "01"


# Función para iniciar el servidor de sockets
def start_server():
    print("Servidor Iniciado...\nEsperando Conexion...")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            # print(f"Cliente conectado: {addr} ")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()
        except KeyboardInterrupt:
            server_socket.close()
            break
        except Exception as ee:
            print(ee)


# Inicia el servidor de sockets
start_server()
