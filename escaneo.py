import socket
import time
import random

# Configuración del objetivo
target = "scanme.nmap.org"  # IP o Dominio de prueba
puertos = [22, 80, 443]

print(f"--- Iniciando escaneo silencioso en: {target} ---")

for puerto in puertos:
    try:
        # Creamos el socket (AF_INET = IPv4, SOCK_STREAM = TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Timeout corto para no esperar eternamente
        s.settimeout(2)
        
        # Intentamos la conexión (connect_ex devuelve 0 si tiene éxito)
        result = s.connect_ex((target, puerto))
        
        if result == 0:
            print(f"[+] Puerto {puerto}: ABIERTO")
        else:
            print(f"[-] Puerto {puerto}: CERRADO / FILTRADO")
            
        s.close() # ¡Importante! Siempre cerrar la conexión
        
        # --- EL FACTOR SIGILO ---
        espera = random.randint(3, 7)
        print(f"... Durmiendo {espera} segundos para evitar detección ...")
        time.sleep(espera)

    except Exception as e:
        print(f"Error en el escaneo: {e}")

print("--- Escaneo finalizado ---")