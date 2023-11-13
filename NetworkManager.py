import subprocess
import re

# 使用 iwlist 扫描附近的 WiFi 网络
def scan_wifi():
    # 扫描无线网络
    scan_output = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan']).decode('utf-8')

    # 正则表达式来匹配网络名称（ESSID）
    networks = re.findall("ESSID:\"(.+?)\"", scan_output)
    return networks

def open_ap():
    config = open('/etc/dhcpcd.conf','w')
    new_config = open('config_file/dhcpcd_OpenAP.txt')
    
    # 把dhcpcd.conf的註解刪掉
    config.write(new_config.read())
    # 重起dhcpcd
    subprocess.run(['sudo', 'service', 'dhcpcd', 'restart'])
    # 開啟AP和dns
    subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'])
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'dnsmasq'])
    
    config.close()
    new_config.close()

def open_wifi():
    config = open('/etc/dhcpcd.conf','w')
    new_config = open('config_file/dhcpcd_OpenWifi.txt')
    
    # 關閉AP
    subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'])
    # 將dhcpcd.conf的指令註解掉
    config.write(new_config.read())
    # 重新啟動dhcpcd
    subprocess.run(['sudo', 'service', 'dhcpcd', 'restart'])
    
    config.close()
    new_config.close()


def hex_to_unicode(hex_string):
    """
    Converts a hexadecimal string to its corresponding Unicode string.
    
    Args:
    hex_string (str): A string containing hexadecimal numbers.
    
    Returns:
    str: The corresponding Unicode string.
    """
    # Split the hex string into chunks of 6 characters, each representing one Unicode character
    chunks = [hex_string[i:i+6] for i in range(0, len(hex_string), 6)]
    
    # Convert each chunk to Unicode and concatenate
    unicode_string = ''.join(bytes.fromhex(chunk).decode('utf-8', errors='replace') for chunk in chunks)
    
    return unicode_string

def parse_ssid(ssid):
    if '"' in ssid:
        return ssid.replace('"',"")
    else:
        return hex_to_unicode(ssid)

network_pattern = r'network={[^}]*}'
ssid_pattern = r'.*ssid=(.*)\n.*'

network_list = []

def get_network_ssid_list():
    wpa_config = open("/etc/wpa_supplicant/wpa_supplicant.conf","r")

    global network_list
    network_list = re.findall(network_pattern,wpa_config.read())
    ssid_list = [re.findall(ssid_pattern,network)[0] for network in network_list]
    wpa_config.close()
    return ssid_list

def add_network(new_network):
    wpa_config = open("/etc/wpa_supplicant/wpa_supplicant.conf","a")
    wpa_config.write(new_network)
    wpa_config.close()

def remove_network_by_index(network_index):
    if network_index >= len(network_list):
        return 0
    wpa_config_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
    with open(wpa_config_path, "r") as f:
        network_context = f.read()
    network_context = network_context.replace(network_list[network_index], "", 1)
    with open(wpa_config_path, "w") as f:
        f.write(network_context)
    return 1

def remove_all_network():
    get_network_ssid_list()
    wpa_config_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
    with open(wpa_config_path, "r") as f:
        network_context = f.read()
    for network in network_list:
        network_context = network_context.replace(network, "", 1)
    network_context = network_context.rstrip("\n")
    with open(wpa_config_path, "w") as f:
        f.write(network_context)
        
    