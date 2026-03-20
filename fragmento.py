from scapy.all import IP, TCP, sr1
import random

target_ip = "1.1.1.1" # Cambia esto por tu IP de pruebas
port = 80

# 1. Construimos el paquete IP (Capa 3)
ip_packet = IP(dst=target_ip)

# 2. Construimos el segmento TCP con el Flag 'S' (SYN) (Capa 4)
tcp_segment = TCP(dport=port, flags="S", sport=random.randint(1024, 65535))

# 3. Enviamos y esperamos UN solo paquete de respuesta (sr1 = Send and Receive 1)
print(f"Enviando SYN a {target_ip}:{port}...")
response = sr1(ip_packet/tcp_segment, timeout=2, verbose=0)

# 4. Analizamos la respuesta del enemigo
if response is None:
    print("Resultado: FILTRADO (El Firewall tiró el paquete).")
elif response.haslayer(TCP):
    if response.getlayer(TCP).flags == 0x12: # 0x12 es SYN-ACK en hexadecimal
        print(f"Resultado: ¡PUERTO {port} ABIERTO! (Recibido SYN-ACK)")
        # Enviamos un RST para cerrar silenciosamente
        rst_packet = IP(dst=target_ip)/TCP(dport=port, flags="R")
        send(rst_packet, verbose=0)
    elif response.getlayer(TCP).flags == 0x14: # 0x14 es RST-ACK
        print(f"Resultado: PUERTO CERRADO (El host respondió directamente).")