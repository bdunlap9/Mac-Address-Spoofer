import asyncio, random, subprocess, sys, netifaces

async def spoof_mac(new_mac: str):
    """
    Spoofs the MAC address of the current interface with the new MAC address.
    """
    try:
        # Get the current interface name
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        
        # Disable the interface
        await asyncio.create_subprocess_shell(f'netsh interface set interface "{iface}" admin=disable')
        
        # Set the new MAC address
        if sys.platform == 'win32':
            # Convert the new MAC address to a byte array
            new_mac_bytes = bytes.fromhex(new_mac.replace(':', ''))
            
            # Set the new MAC address in the registry
            await asyncio.create_subprocess_shell(f'reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{iface}\\Ndi\\params\\NetworkAddress" /f /v "NetworkAddress" /t REG_BINARY /d {new_mac_bytes.hex()}')
        else:
            await asyncio.create_subprocess_shell(f'sudo ifconfig {iface} hw ether {new_mac}')
        
        # Enable the interface
        await asyncio.create_subprocess_shell(f'netsh interface set interface "{iface}" admin=enable')
        
        print(f'Spoofed MAC address of {iface} to {new_mac}')
        
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')
        
async def main():
    # Set the new MAC address
    new_mac = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
    
    await spoof_mac(new_mac)

if __name__ == '__main__':
    asyncio.run(main())