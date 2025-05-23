class IPAddress:
    def __init__(self, address):
        if isinstance(address, str):
            if '.' in address: 
                parts = list(map(int, address.split('.')))
                if len(parts) != 4 or any(part < 0 or part > 255 for part in parts):
                    raise ValueError("Invalid IP address format")
                self.address = parts
            else:  
                if len(address) != 32 or any(c not in ('0', '1') for c in address):
                    raise ValueError("Invalid bit string format")
                self.address = [
                    int(address[0:8], 2),
                    int(address[8:16], 2),
                    int(address[16:24], 2),
                    int(address[24:32], 2)
                ]
        elif isinstance(address, list) and len(address) == 4:
            self.address = address.copy()
        else:
            raise ValueError("Invalid IP address format")
    
    def toBits(self):
        return ''.join(f'{octet:08b}' for octet in self.address)
    
    def toIPv4(self):
        return '.'.join(map(str, self.address))
    
    def isMask(self):
        bit_str = self.toBits()
        found_zero = False
        for bit in bit_str:
            if found_zero and bit == '1':
                return False
            if bit == '0':
                found_zero = True
        return True
    
    def maskBits(self):
        if not self.isMask():
            raise ValueError("Not a valid network mask")
        return self.toBits().count('1')
    
    def __and__(self, other):
        if not isinstance(other, IPAddress):
            raise TypeError("Operand must be IPAddress")
        return IPAddress([
            self.address[i] & other.address[i] for i in range(4)
        ])
    
    def __or__(self, other):
        if not isinstance(other, IPAddress):
            raise TypeError("Operand must be IPAddress")
        return IPAddress([
            self.address[i] | other.address[i] for i in range(4)
        ])
    
    def __invert__(self):
        return IPAddress([255 - octet for octet in self.address])
    
    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            return False
        return self.address == other.address
    
    def __str__(self):
        return self.toIPv4()


class IPToolIF:
    @staticmethod
    def isValid(ip):
        try:
            IPAddress(ip.toIPv4() if isinstance(ip, IPAddress) else ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def areSameNet(ip1, ip2, mask):
        if not all([IPToolIF.isValid(ip) for ip in [ip1, ip2, mask]]):
            return False
        
        ip1 = ip1 if isinstance(ip1, IPAddress) else IPAddress(ip1)
        ip2 = ip2 if isinstance(ip2, IPAddress) else IPAddress(ip2)
        mask = mask if isinstance(mask, IPAddress) else IPAddress(mask)
        
        network1 = IPToolIF.network(ip1, mask)
        network2 = IPToolIF.network(ip2, mask)
        
        return network1 == network2
    
    @staticmethod
    def broadcast(ip, mask):
        if not all([IPToolIF.isValid(ip) for ip in [ip, mask]]):
            raise ValueError("Invalid IP address or mask")
        
        ip = ip if isinstance(ip, IPAddress) else IPAddress(ip)
        mask = mask if isinstance(mask, IPAddress) else IPAddress(mask)
        
        network = IPToolIF.network(ip, mask)
        wildcard = ~mask
        
        broadcast_addr = IPAddress([
            network.address[i] | wildcard.address[i] for i in range(4)
        ])
        return broadcast_addr
    
    @staticmethod
    def network(ip, mask):
        if not all([IPToolIF.isValid(ip) for ip in [ip, mask]]):
            raise ValueError("Invalid IP address or mask")
        
        ip = ip if isinstance(ip, IPAddress) else IPAddress(ip)
        mask = mask if isinstance(mask, IPAddress) else IPAddress(mask)
        
        return ip & mask
    

ip1 = IPAddress("26.225.184.146")
ip2 = IPAddress("26.220.183.158")
mask = IPAddress("255.0.0.0")

print("O ip é valido: ")
print(IPToolIF.isValid(ip1))  

print("estao na mesma rede: ")
print(IPToolIF.areSameNet(ip1, ip2, mask))  

print("Broadcast: ")
print(IPToolIF.broadcast(ip1, mask).toIPv4())  

print("Network: ")
print(IPToolIF.network(ip1, mask).toIPv4())  


print(ip1.toBits())  
print(mask.maskBits())  
print(mask.isMask())  