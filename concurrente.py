import threading
from scapy.all import IP, TCP, sr1, send
import time

# Limitar a 10 hilos simultáneos
max_hilos = threading.Semaphore(10)

def scan_target(ip):
    # El 'with' adquiere el semáforo y lo libera automáticamente al terminar
    with max_hilos:
        packet = IP(dst=ip)/TCP(dport=80, flags="S")
        resp = sr1(packet, timeout=1, verbose=0)
        
        if resp is not None:
            if resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
                print(f"[+] {ip} - Puerto 80 ABIERTO")
                # Cerramos con RST para no dejar la conexión a medias
                send(IP(dst=ip)/TCP(dport=80, flags="R"), verbose=0)
            else:
                print(f"[-] {ip} - Puerto 80 Cerrado/Rechazado")
        else:
            # Si resp es None, el firewall hizo DROP
            pass 

# Rango de red
base_ip = "192.168.1."
threads = []

for i in range(1, 255):
    ip_actual = base_ip + str(i)
    t = threading.Thread(target=scan_target, args=(ip_actual,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n--- Escaneo de red Clase C completado con éxito ---")