from scapy.all import Ether
from scapy.all import ARP
from scapy.all import srp
import ipaddress

def main():
    myip = input("What is Your IP ?:")
    netmask = input("What is SubnetMask ?:")
    hwaddr = 'ff:ff:ff:ff:ff:ff'

    cidr = gen_cidr(myip, netmask)
    print('Scanning on: ' + cidr + '\n')

    pkt = Ether(dst=hwaddr)/ARP(op=1, pdst=cidr)    # op=1:arpリクエスト(ブロードキャスト) op=2:arpレスポンス(ユニキャスト)
    ans, uans = srp(pkt, timeout=30)

    print("")
    for send, recv in ans:
        print(recv.sprintf('%ARP.psrc% is up.'))


def gen_cidr(ip, netmask):
    ipv4 = ipaddress.ip_address(ip)
    netmask = ipaddress.ip_address(netmask)
    netaddr = ipaddress.ip_interface(int(ipv4) & int(netmask))
    netaddr = str(netaddr).split('/')[0]

    cidr = bin(int(netmask)).count('1')
    return str(netaddr) + '/' + str(cidr)

if __name__ == '__main__':
    main()
