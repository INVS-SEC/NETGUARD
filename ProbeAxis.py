import socket
import ipaddress
import datetime

is_ip = False
is_hostname = False
ip_found = False
open_ports = []
closed_ports = []
time = datetime.datetime.now() 
log_file = open(f"scan_log_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w")

print("===================================")
print("             ProbeAxis             ")
print("===================================")

target = input("Enter the target hostname or IP address: ")

log_file.write(f"Scan started at {datetime.datetime.now()}\n")
log_file.write(f"Target: {target}\n")

try:
    ip = ipaddress.ip_address(target)
    print("Type = IP") 
    is_ip = True
    target_ip = ip
    ip_found = True
    
except ValueError:
    print("Type = Hostname")
    is_hostname = True

if is_hostname:
    try:
        ipAddress = socket.gethostbyname(target)
        print(f"Target = {target}")
        print(f"IP Address = {ipAddress}")
        print("Status = Resolved")
        target_ip = ipaddress.ip_address(ipAddress)
        ip_found = True
    except socket.gaierror:
        print(f"Could not resolve {target}. Please check the hostname and try again.")
        print("Status = Failed")
elif is_ip:
    print("Target already an IP address.")
    print("Status = Resolved")

log_file.write(f"Type: {'IP' if is_ip else 'Hostname'}\n")
log_file.write(f"Status: {'Resolved' if ip_found else 'Failed'}\n")

if ip_found:
    log_file.write(f"Target IP: {target_ip}\n")
    if target_ip.is_private:
        print("IP Type = Private")
        log_file.write("IP Type: Private\n")
    else:
        print("IP Type = Public")
        log_file.write("IP Type: Public\n")
else:
    print("IP Type = N/A")
    log_file.write("IP Type: N/A\n")



    
if ip_found:
    for port in range(75, 86):
        try:
            connection = socket.create_connection((str(target_ip), port))
            print(f"Port {port} is open on {target_ip}.")
            portConnectionStatus = True
            connection.close()
            open_ports.append(port)
            log_file.write(f"Port {port} is open on {target_ip}.\n")
        except (socket.timeout, ConnectionRefusedError):
            print(f"Port {port} is closed on {target_ip}.")
            portConnectionStatus = False
            closed_ports.append(port)
            log_file.write(f"Port {port} is closed on {target_ip}.\n")

log_file.close()

print("OPEN PORTS:")
for item in open_ports:
    print(item)

print("CLOSED PORTS:")
for item in closed_ports:
    print(item)

