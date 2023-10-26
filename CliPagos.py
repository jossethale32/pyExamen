import tkinter as tk
from tkinter import ttk, messagebox
import socket
import requests
import datetime

# Función para enviar mensajes al servidor
def enviar_mensaje(mensaje):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        client_socket.settimeout(5)
        client_socket.send(mensaje.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
    except TimeoutError as e:
        messagebox.showerror("⚠️Error", "Servidor no Responde")
        client_socket.close()
        response=""
    except socket.timeout as ee:
        messagebox.showerror("⚠️Error", "Error de parte del servidor")
        client_socket.close()
        response=""
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

public=detect_public_ip()
enviar_mensajeTest(public)


def updateFind(event):
    # print(str(len(entry_idcli.get())))
    if(len(entry_idcli.get())>8):
        messagebox.showerror("Alerta", "Limite de Caracteres de ID es 8")
        entry_idcli.delete(0,tk.END)
        entry_idcli.insert(0,"")
        entry_idcli.focus()

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
    cont=0
    PosPrimerNum=0
    for digit in entrada:
        cont=cont + 1
        if int(digit)>0:
            PosPrimerNum=cont
            break
    return entrada[PosPrimerNum-1:len(entrada)]
def subconsultar():
    resp=validarInput(str(entry_idcli.get()))
    if resp==1:
        idTrama=parseTrama(str(entry_idcli.get()))
        response = enviar_mensaje('C'+','+str(idTrama))
        # print(response)
        try:
            pagos = eval(response)  # Convierte la cadena de texto a una lista de usuarios
            tabla.delete(*tabla.get_children())  # Limpia la tabla antes de agregar nuevos datos
            for pay in pagos:
                if "datetime" in pay:
                    tabla.insert('', 'end', values=pay.strftime("%Y-%m-%d"))
                else:
                    tabla.insert('', 'end', values=pay)
        except Exception as e:
            print("CLI-"+str(e))
    else:
        messagebox.showerror("⚠️Alerta", "ID no valido")

def reversion():
    print("Revertir cuotas")

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
    ventana_secundariaP.geometry("+%d+%d" %(x+200,y+200))

    # contenido de la ventana
    lblPago = tk.Label(ventana_secundariaP, text="#Trama Pago: ")
    lblPago.grid(row=0, column=0, padx=10,pady=10)

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
    if(len(entry_pago.get())>26):
        messagebox.showinfo("Alerta!", "Has superado el límite máximo de caracteres\n    Trama sugerida:\n00001001 : Codigo de cliente\n01 : Cuota\n20230110 : Fecha\n00020000 : MONTO")
        entry_pago.delete(0,tk.END)
        entry_pago.insert(0,"")
        entry_pago.focus()

def payManager():
    # print("Pay Manager")
    codCli=""
    cuota=""
    fecha=""
    monto=""
    if entry_pago.get().isdigit():
        codCli=parseTrama(str(entry_pago.get()[0:8]))
        cuota=parseTrama(str(entry_pago.get()[8:10]))
        fecha=parseTrama(str(entry_pago.get()[10:18]))
        monto=parseTrama(str(entry_pago.get()[19:26]))
    else:
        messagebox.showwarning("Alerta!", "Debes Ingresar solo digitos numericos!")
        entry_pago.delete(0,tk.END)
        entry_pago.insert(0,"")
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

tabla = ttk.Treeview(ventana_secundaria, columns=("ID CLIENTE", "CUOTA","MONTO","FECHA PAGO","PAGOFECHAREALIZACION","ESTADO"), show="headings")

root.mainloop()