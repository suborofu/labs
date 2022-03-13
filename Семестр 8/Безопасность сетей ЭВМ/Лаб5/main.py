from winpcapy import WinPcapUtils
import dpkt
from datetime import datetime

protocol = {
    6: 'TCP',
    17: 'UDP',
}


def packet_callback(win_pcap, param, header, pkt_data):
    eth = dpkt.ethernet.Ethernet(pkt_data)
    if not isinstance(eth.data, dpkt.ip.IP):
        return
    packet = eth.data
    if packet.p != 6:
        return

    packet_callback.counter += 1
    message = (
        f"Packet №{packet_callback.counter}\n"
        f"\t{'time': <16}: {datetime.now():%d.%m.%Y %H:%M:%S}\n"
        f"\t{'source': <16}: {'%d.%d.%d.%d' % tuple(packet.src)}:{packet.tcp.sport if packet.p == 6 else packet.udp.sport}\n"
        f"\t{'destination': <16}: {'%d.%d.%d.%d' % tuple(packet.dst)}:{packet.tcp.dport if packet.p == 6 else packet.udp.dport}\n"
        f"\t{'protocol': <16}: {protocol[packet.p]}\n"
        f"\t{'length': <16}: {packet.len}\n"
    )
    print(message)


packet_callback.counter = 0

WinPcapUtils.capture_on_device_name(device_name="\\Device\\NPF_{380D2CEF-6641-47E4-A4D8-7411E41AFE28}",
                                    callback=packet_callback)
