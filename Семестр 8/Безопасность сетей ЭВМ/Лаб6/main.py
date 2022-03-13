from winpcapy import WinPcap, WinPcapUtils


def send_packet_device_name(device_name, packet_buffer):
    with WinPcap(device_name) as capture:
        capture.send(packet_buffer)


def ethernetip(src_mac=b'\x00\x00\x00\x00\x00\x00', dst_mac=b'\x00\x00\x00\x00\x00\x00'):
    type = b'\x08\x00'
    header = dst_mac + src_mac + type
    return header


def ipheader(src_ip, dst_ip):
    version = b'\x45\x00'
    length = b'\x00\x28'
    identification = b'\xab\xcd'
    flags = b'\x00\x00'
    protocol = b'\x40\x06'
    checksum = b'\x00\x00'
    header = version + length + identification + flags + protocol + checksum + src_ip + dst_ip
    return header


def tcpheader(src_port, dst_port):
    sequence = b'\x00\x00\x00\x00'
    ack = b'\x00\x00\x00\x00'
    flags = b'\x50\x02\x00\x00'
    window = b'\xff\xff'
    checksum = b'\x00\x00'
    urgent = b'\x00\x00'
    header = src_port + dst_port + sequence + ack + flags + window + checksum + urgent
    return header


def send_packet(device_name, src_ip, src_port, dst_ip, dst_port, msg):
    src_ip = b''.join([int(i).to_bytes(1, 'big') for i in src_ip.split('.')])
    dst_ip = b''.join([int(i).to_bytes(1, 'big') for i in dst_ip.split('.')])
    src_port = src_port.to_bytes(2, 'big')
    dst_port = dst_port.to_bytes(2, 'big')
    msg = msg.encode('utf-8')
    ethernet = ethernetip()
    ip_header = ipheader(src_ip, dst_ip)
    tcp_header = tcpheader(src_port, dst_port)
    packet = ethernet + ip_header + tcp_header + msg
    send_packet_device_name(device_name, packet)


device_name = "\\Device\\NPF_{EE5AAD83-CD76-4A0B-8C83-C120882BE16A}"
src_ip = '192.168.136.1'
src_port = 12345

dst_ip = input(f"{'Destination IP:': <20}")
dst_port = int(input(f"{'Destination port:': <20}"))
msg = input(f"{'Message:': <20}")

send_packet(device_name, src_ip, src_port, dst_ip, dst_port, msg)
