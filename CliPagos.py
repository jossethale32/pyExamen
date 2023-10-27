import tkinter as tk
from tkinter import ttk, messagebox
import socket
import requests
import datetime
import mysql.connector
from datetime import datetime as tt


# Función para enviar mensajes al servidor
def enviar_mensaje(mensaje):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        # client_socket.settimeout(5)
        client_socket.send(mensaje.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
    except TimeoutError as e:
        messagebox.showerror("⚠️Error", "Servidor no Responde")
        client_socket.close()
        response = ""
    except socket.timeout as ee:
        messagebox.showerror("⚠️Error", "Error de parte del servidor")
        client_socket.close()
        response = ""
    return response


def enviar_mensajeTest(mensaje):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        client_socket.send(mensaje.encode('utf-8'))
        client_socket.close()
    except TimeoutError as e:
        messagebox.showerror("⚠️Error", "Servidor no Responde")
        client_socket.close()
    except socket.timeout as ee:
        messagebox.showerror("⚠️Error", "Error de parte del servidor")
        client_socket.close()


def detect_public_ip():
    try:
        raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
        answer = raw.json()["Answer"].split()[4]
    except Exception as e:
        return 'Error: {0}'.format(e)
    else:
        return answer


public = detect_public_ip()
enviar_mensajeTest(public)


def updateFind(event):
    # print(str(len(entry_idcli.get())))
    if (len(entry_idcli.get()) > 8):
        messagebox.showerror("Alerta", "Limite de Caracteres de ID es 8")
        entry_idcli.delete(0, tk.END)
        entry_idcli.insert(0, "")
        entry_idcli.focus()

def updateFindrevert(event):
    # print(str(len(entry_idcli.get())))
    if (len(entry_idclic.get()) > 18):
        messagebox.showerror("Alerta", "Limite de Caracteres de ID es 18")
        entry_idclic.delete(0, tk.END)
        entry_idclic.insert(0, "")
        entry_idclic.focus()


def close_win():
    root.destroy()


def disable_event():
    pass


def consultar_cuotas():
    # Crear una ventana secundaria.
    # ventana_secundaria = tk.Toplevel()
    ventana_secundaria.iconbitmap("ic_icon.ico")
    ventana_secundaria.deiconify()
    ventana_secundaria.title("Consultas Pagos")
    ventana_secundaria.config(width=1000, height=600)
    ventana_secundaria.protocol("WM_DELETE_WINDOW", disable_event)
    # Crear un botón dentro de la ventana secundaria
    # para cerrar la misma.

    label_idcli = tk.Label(ventana_secundaria, text="#Cod Cliente: ")
    # label_idcli.place(x=20,y=20)
    label_idcli.grid(row=1, column=0, pady=5)

    # entry_idcli = tk.Entry(ventana_secundaria)
    # entry_idcli.place(x=100,y=20)
    entry_idcli.grid(row=1, column=1, pady=5)
    entry_idcli.focus()

    boton_buscar = ttk.Button(
        ventana_secundaria,
        text="Buscar",
        command=subconsultar
    )
    # boton_buscar.place(x=250, y=20)
    boton_buscar.grid(row=1, column=2, pady=5)

    boton_cerrar = ttk.Button(
        ventana_secundaria,
        text="Cerrar ventana",
        command=ventana_secundaria.withdraw
    )
    # boton_cerrar.place(x=420, y=20)
    boton_cerrar.grid(row=1, column=3, pady=5)

    # Tabla para mostrar pagos

    tabla.heading("ID CLIENTE", text="ID CLIENTE")
    tabla.heading("CUOTA", text="CUOTA")
    tabla.heading("MONTO", text="MONTO")
    tabla.heading("FECHA PAGO", text="FECHA PAGO")
    tabla.heading("PAGOFECHAREALIZACION", text="PAGOFECHAREALIZACION")
    tabla.heading("ESTADO", text="ESTADO")

    tabla.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Configura la función de selección de pago cuando se hace clic en la tabla
    # tabla.bind('<ButtonRelease-1>', seleccionar_pago)

    entry_idcli.bind('<KeyRelease>', updateFind)
    return id


def validarInput(entrada):
    if entrada.isdigit():
        return 1
    else:
        return 0


def parseTrama(entrada):
    cont = 0
    PosPrimerNum = 0
    for digit in entrada:
        cont = cont + 1
        if int(digit) > 0:
            PosPrimerNum = cont
            break
    return entrada[PosPrimerNum - 1:len(entrada)]


def subconsultar():
    resp = validarInput(str(entry_idcli.get()))
    if resp == 1:
        idTrama = parseTrama(str(entry_idcli.get()))
        response = enviar_mensaje('C' + ',' + str(idTrama))
        # print(response)
        try:
            pagos = eval(response)  # Convierte la cadena de texto a una lista de usuarios
            tabla.delete(*tabla.get_children())  # Limpia la tabla antes de agregar nuevos datos
            for pay in pagos:
                if "datetime" in pay:
                    # now = datetime.strptime(pay, "%d/%m/%Y %H:%M:%S").date().strftime('%Y-%d-%m')
                    tabla.insert('', 'end', values=pay.strftime("%Y-%m-%d"))
                else:
                    tabla.insert('', 'end', values=pay)
        except Exception as e:
            print("CLI-" + str(e))
    else:
        messagebox.showerror("⚠️Alerta", "ID no valido")

    ventana_secundaria.update_idletasks()


def reversion():
    # Crear una ventana secundaria.
    # ventana_secundaria = tk.Toplevel()
    ventana_tercearia.iconbitmap("ic_icon.ico")
    ventana_tercearia.deiconify()
    ventana_tercearia.title("Reversion")
    ventana_tercearia.config(width=1000, height=600)
    ventana_tercearia.protocol("WM_DELETE_WINDOW", disable_event)
    # Crear un botón dentro de la ventana secundaria
    # para cerrar la misma.

    label_idcli = tk.Label(ventana_tercearia, text="#Cod Cliente: ")
    # label_idcli.place(x=20,y=20)
    label_idcli.grid(row=1, column=0, pady=5)

    # entry_idcli = tk.Entry(ventana_secundaria)
    # entry_idcli.place(x=100,y=20)
    entry_idclic.grid(row=1, column=1, pady=5)
    entry_idclic.focus()

    boton_buscar3 = ttk.Button(
        ventana_tercearia,
        text="Buscar",
        command=subconsultar3
    )
    # boton_buscar.place(x=250, y=20)
    boton_buscar3.grid(row=1, column=2, pady=5)

    boton_cerrar3 = ttk.Button(
        ventana_tercearia,
        text="Cerrar ventana",
        command=ventana_tercearia.withdraw
    )
    # boton_cerrar.place(x=420, y=20)
    boton_cerrar3.grid(row=1, column=4, pady=5)

    boton_revertir = ttk.Button(
        ventana_tercearia,
        text="Revertir",
        command=reversion3
    )
    # boton_cerrar.place(x=420, y=20)
    boton_revertir.grid(row=1, column=3, pady=5)

    # Tabla para mostrar pagos

    tabla3.heading("ID CLIENTE", text="ID CLIENTE")
    tabla3.heading("CUOTA", text="CUOTA")
    tabla3.heading("MONTO", text="MONTO")
    tabla3.heading("FECHA PAGO", text="FECHA PAGO")
    tabla3.heading("PAGOFECHAREALIZACION", text="PAGOFECHAREALIZACION")
    tabla3.heading("ESTADO", text="ESTADO")
    tabla3.heading("REFERENCIA", text="REFERENCIA")
    tabla3.heading("MONTO_ANTERIOR", text="MONTO_ANTERIOR")
    tabla3.column("MONTO_ANTERIOR", stretch="no", minwidth=0, width=0)

    tabla3.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    # Configura la función de selección de pago cuando se hace clic en la tabla
    # tabla.bind('<ButtonRelease-1>', seleccionar_pago)

    entry_idclic.bind('<KeyRelease>', updateFindrevert)
    return id


def my_functions(x):
    return x[::-1]


def validarInputs(entrada):
    if entrada.isdigit():
        return 1
    else:
        return 0


def parseTramas(entrada):
    cont = 0
    PosPrimerNum = 0
    for digit in entrada:
        cont = cont + 1
        if int(digit) > 0:
            PosPrimerNum = cont
            break
    return entrada[PosPrimerNum - 1:len(entrada)]

def reversion3():
    try:
        now = tt.now().date()
        now.strftime("%Y-%m-%d")
        now = str(now)
        # Obtener la fila seleccionada de la tabla
        selected_item = tabla3.selection()[0]  # Retorna el ID de la fila seleccionada

        # Obtener los valores de las columnas correspondientes en la fila seleccionada
        id_cliente = tabla3.item(selected_item, 'values')[0]
        cuota = tabla3.item(selected_item, 'values')[1]
        estado = tabla3.item(selected_item, 'values')[5]  # Obtener el valor de la columna ESTADO
        pagadofecha = tabla3.item(selected_item, 'values')[4]  # Obtener el valor de la columna REFERENCIAS
        referencia = tabla3.item(selected_item, 'values')[6]  # Obtener el valor de la columna REFERENCIAS
        monto_anterior = tabla3.item(selected_item, 'values')[7]  # Obtener el valor de la columna MONTO_ANTERIOR

        # Conectar a la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            port=3308,
            user="root",
            password="",
            database="pago_en_linea"
        )

        cursor = mydb.cursor()

        # Verificar si la columna REFERENCIAS tiene datos y el ESTADO es 'P'
        if referencia and estado == 'P':
            # Realizar la reversión en la base de datos
            if now ==str(pagadofecha):
                cursor.execute(
                    "UPDATE pagos SET `ESTADO` = 'A', `REFERENCIA` = NULL, `PAGOFECHAREALIZACION` = NULL, `MONTO` = %s WHERE `ID CLIENTE` = %s AND `CUOTA` = %s",
                    (monto_anterior, id_cliente, cuota))
                mydb.commit()

                # Mostrar ventana de éxito
                messagebox.showinfo("00 Exitoso", "Reversión exitosa")

                # Actualizar la tabla para mostrar el valor de MONTO_ANTERIOR en la columna MONTO
                tabla3.item(selected_item, values=(id_cliente, cuota, monto_anterior, referencia, "", "A", "Revertido"))

                ventana_tercearia.update_idletasks()
            else:
                messagebox.showwarning("Alerta", "Esta Cuota no puede ser Revertida! Fechas no Coinciden!")
        else:
            # Mostrar mensaje si la columna REFERENCIAS está vacía o el ESTADO no es 'P'
            messagebox.showwarning("Alerta", "La columna REFERENCIAS está vacía o el ESTADO no es 'P'. No se puede revertir la cuota.")

    except mysql.connector.Error as err:
        # Mostrar ventana de error si hay un error en la base de datos
        messagebox.showerror("Error en la base de datos", str(err))

    finally:
        cursor.close()
        mydb.close()
        subconsultar3()

def subconsultar3():
    resp = validarInputs(str(entry_idclic.get()))
    if resp == 1:
        idTrama = parseTramas(str(entry_idclic.get()))
        response = enviar_mensaje('C' + ',' + str(idTrama))
        # print(response)
        try:
            pagos = eval(response)  # Convierte la cadena de texto a una lista de usuarios
            tabla3.delete(*tabla3.get_children())  # Limpia la tabla antes de agregar nuevos datos
            for pay in pagos:
                if "datetime" in pay:
                    tabla3.insert('', 'end', values=pay.strftime("%Y-%m-%d"))
                else:
                    tabla3.insert('', 'end', values=pay)
        except Exception as e:
            print("CLI-" + str(e))
    else:
        messagebox.showerror("⚠️Alerta", "ID no valido")


### ZONA DE PAGO
### ZONA DE PAGO

def pagar_cuotas():
    # Preparar ventanda para ingreso de trama de pago
    ventana_secundariaP.iconbitmap("ic_icon.ico")
    ventana_secundariaP.deiconify()
    ventana_secundariaP.title("Control de Pagos")
    ventana_secundariaP.config(width=1000, height=600)
    ventana_secundariaP.protocol("WM_DELETE_WINDOW", disable_event)

    # centrar la ventana secundaria
    x = root.winfo_x()
    y = root.winfo_y()
    ventana_secundariaP.geometry("+%d+%d" % (x + 200, y + 200))

    # contenido de la ventana
    lblPago = tk.Label(ventana_secundariaP, text="#Trama Pago: ")
    lblPago.grid(row=0, column=0, padx=10, pady=10)

    entry_pago.grid(row=0, column=1, padx=15, pady=10)
    entry_pago.focus()

    btn_efectuar = tk.Button(ventana_secundariaP, text="  EFECTUAR PAGO  ", command=payManager)
    btn_efectuar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    boton_cerrar2 = tk.Button(ventana_secundariaP, text="  Cerrar ventana  ", command=ventana_secundariaP.withdraw)
    boton_cerrar2.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # VALIDAR 26 caracteres de trama para pago
    entry_pago.bind('<KeyRelease>', updatePago)


def updatePago(event):
    # print(str(len(entry_idcli.get())))
    if (len(entry_pago.get()) > 26):
        messagebox.showinfo("Alerta!",
                            "Has superado el límite máximo de caracteres\n    Trama sugerida:\n00001001 : Codigo de cliente\n01 : Cuota\n20230110 : Fecha\n00020000 : MONTO")
        entry_pago.delete(0, tk.END)
        entry_pago.insert(0, "")
        entry_pago.focus()


def payManager():
    # print("Pay Manager")
    codCli = ""
    cuota = ""
    fecha = ""
    monto = ""
    if entry_pago.get().isdigit():
        codCli = parseTrama(str(entry_pago.get()[0:8]))
        cuota = parseTrama(str(entry_pago.get()[8:10]))
        fecha = parseTrama(str(entry_pago.get()[10:18]))
        monto = parseTrama(str(entry_pago.get()[19:26]))

        # parsear monto a decimales
        montoDecimas = str(str(monto)[::-1])[0:2]
        montosinDecimas = str(str(str(monto)[::-1])[2:len(monto)])[::-1]
        montoFinal = float(str(montosinDecimas) + '.' + str(montoDecimas))

        # parsear fecha
        ano = str(fecha)[0:4]
        dia = str(fecha)[4:6]
        mes = str(fecha)[6:8]
        toStrindDate = str(mes) + '/' + str(dia) + '/' + str(ano)
        now = datetime.datetime.strptime(toStrindDate + " 00:00:00", "%d/%m/%Y %H:%M:%S").date().strftime('%Y-%d-%m')

        # Recibir respuesta del server
        response = enviar_mensaje('P' + ',' + str(codCli) + ',' + str(cuota) + ',' + str(now) + ',' + str(montoFinal))
        if 'Algo Fallo' in response:
            messagebox.showerror("Error!", "Algo Fallo con su pago\nVuelvalo a intentar nuevamente")
        elif 'No se puede pagar de mas!' in response:
            messagebox.showwarning("Alerta!", "No puedes pagar de más!")
        elif '00' in response:
            messagebox.showinfo("Exito!", "Pago Realizado con Exito!\nPuedes Consultar Cuotas Pendientes..")
        elif '01' in response:
            messagebox.showerror("Error!", "Transaccion Fallida!")
        else:
            messagebox.showerror("Error Interno", "0x001 " + str(response))

    else:
        messagebox.showwarning("Alerta!", "Debes Ingresar solo digitos numericos!")
        entry_pago.delete(0, tk.END)
        entry_pago.insert(0, "")
        entry_pago.focus()


### ZONA DE PAGO
### ZONA DE PAGO

# Interfaz gráfica de usuario con Tkinter
root = tk.Tk()
root.title("PaySocket")
root.iconbitmap("ic_icon.ico")

root.eval('tk::PlaceWindow . center')

# Botones
button_crear = tk.Button(root, text="Consultar Cuotas", command=consultar_cuotas)
button_crear.grid(row=0, column=0, padx=10, pady=10)

button_actualizar = tk.Button(root, text="Pagar Cuotas", command=pagar_cuotas)
button_actualizar.grid(row=0, column=1, padx=10, pady=10)

button_eliminar = tk.Button(root, text="Reversion de Cuotas", command=reversion)
button_eliminar.grid(row=0, column=2, padx=10, pady=10)

ventana_secundaria = tk.Toplevel()
ventana_secundaria.withdraw()
entry_idcli = tk.Entry(ventana_secundaria)

ventana_secundariaP = tk.Toplevel()
ventana_secundariaP.withdraw()
entry_pago = tk.Entry(ventana_secundariaP)

ventana_secundariaP2 = tk.Toplevel()
ventana_secundariaP2.withdraw()
entry_pago2 = tk.Entry(ventana_secundariaP2)

tabla = ttk.Treeview(ventana_secundaria,
columns=("ID CLIENTE", "CUOTA", "MONTO", "FECHA PAGO", "PAGOFECHAREALIZACION", "ESTADO"),show="headings")

ventana_tercearia = tk.Toplevel()
ventana_tercearia.withdraw()
entry_idclic = tk.Entry(ventana_tercearia)

tabla3 = ttk.Treeview(ventana_tercearia,
columns=("ID CLIENTE", "CUOTA", "MONTO", "FECHA PAGO", "PAGOFECHAREALIZACION", "ESTADO","REFERENCIA","MONTO_ANTERIOR"),show="headings")

root.mainloop()