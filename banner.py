import socket

def get_banner(ip, port):
    try:
        # 1. Crear el objeto socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. Tiempo de espera para no quedar bloqueados
        s.settimeout(3)
        
        # 3. Conectar al objetivo
        s.connect((ip, port))
        
        # 4. Enviar una petición genérica (opcional pero ayuda en HTTP)
        # Algunos servidores no hablan hasta que tú no digas algo.
        if port == 80:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        
        # 5. Recibir la respuesta (el "Banner")
        banner = s.recv(1024)
        
        return banner.decode().strip()
    
    except Exception as e:
        return f"Error: No se pudo obtener el banner ({e})"
    finally:
        s.close()

# Prueba de concepto
target = "192.168.1.10" # IP de una máquina víctima (o tu router)
print(f"[*] Inspeccionando {target}...")
print(f"[+] Banner detectado: \n{get_banner(target, 80)}")