#---------------------------------------------------------------------#
# Author:       petru.giurca@ge.com	       
# SSO:          212772048  
# Description:  Getting HW & SW info from VDC/NorCap compute instances  
#---------------------------------------------------------------------#

import psutil
import platform
from datetime import datetime


def norcap_instance(bytes, suffix="B"):
    
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")

# Boot Time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# CPU information
print("="*40, "CPU Info", "="*40)

# Number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))

# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
print("="*40, "Memory Information", "="*40)

# Get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {norcap_instance(svmem.total)}")
print(f"Available: {norcap_instance(svmem.available)}")
print(f"Used: {norcap_instance(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)

# Get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {norcap_instance(swap.total)}")
print(f"Free: {norcap_instance(swap.free)}")
print(f"Used: {norcap_instance(swap.used)}")
print(f"Percentage: {swap.percent}%")

# Disk Information
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# Get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    print(f"  Total Size: {norcap_instance(partition_usage.total)}")
    print(f"  Used: {norcap_instance(partition_usage.used)}")
    print(f"  Free: {norcap_instance(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# Get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {norcap_instance(disk_io.read_bytes)}")
print(f"Total write: {norcap_instance(disk_io.write_bytes)}")

# Network information
print("="*40, "Network Information", "="*40)
# Get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# Get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {norcap_instance(net_io.bytes_sent)}")
print(f"Total Bytes Received: {norcap_instance(net_io.bytes_recv)}")

