from scapy.all import IP, TCP, sr1
import time

def check_zombie(zombie_ip):
    # Enviamos dos paquetes para ver cómo incrementa el IPID
    p1 = sr1(IP(dst=zombie_ip)/TCP(dport=445, flags="SA"), timeout=2, verbose=0)
    if p1 is None:
        return "Inalcanzable"
    
    initial_id = p1.id
    time.sleep(1) # Esperamos un poco
    
    p2 = sr1(IP(dst=zombie_ip)/TCP(dport=445, flags="SA"), timeout=2, verbose=0)
    final_id = p2.id
    
    diff = final_id - initial_id
    
    if diff == 1:
        return f"CANDIDATO PERFECTO (ID incrementó en {diff})"
    elif diff > 1:
        return f"RUIDOSO (ID incrementó en {diff}, alguien más lo está usando)"
    else:
        return "NO SIRVE (IPID Aleatorio o Fijo)"

# Prueba con una IP de tu red (ej. una impresora o router viejo)
target_zombie = "192.168.1.15" 
print(f"Analizando {target_zombie}: {check_zombie(target_zombie)}")