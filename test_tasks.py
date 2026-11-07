
import subprocess

# Test WiFi interface name
result = subprocess.run('netsh interface show interface', shell=True, capture_output=True, text=True)
print("=== NETWORK INTERFACES ===")
print(result.stdout)

# Test brightness
result2 = subprocess.run(['powershell', '-Command', 
    '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'],
    capture_output=True, text=True)
print("=== BRIGHTNESS ===")
print("Value:", result2.stdout.strip())
print("Error:", result2.stderr.strip())

# Test Bluetooth
result3 = subprocess.run(['powershell', '-Command',
    'Get-PnpDevice -Class Bluetooth | Select-Object Status, FriendlyName | Format-Table'],
    capture_output=True, text=True)
print("=== BLUETOOTH DEVICES ===")
print(result3.stdout)
print("Error:", result3.stderr.strip())
