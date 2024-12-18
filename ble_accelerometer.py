import asyncio
from bleak import BleakScanner

# Threshold for determining movement
MOVEMENT_THRESHOLD = 0.5  # Adjust this value based on your needs

def is_moving(accel_data):
    """Determine if the tag is moving based on accelerometer data."""
    x, y, z = accel_data
    # Simple threshold check to determine movement
    return abs(x) > MOVEMENT_THRESHOLD or abs(y) > MOVEMENT_THRESHOLD or abs(z) > MOVEMENT_THRESHOLD

def parse_accelerometer_data(data):
    """Parse the accelerometer data from the raw packet."""
    x = int.from_bytes(data[14:16], byteorder='little', signed=True) / 256.0
    y = int.from_bytes(data[16:18], byteorder='little', signed=True) / 256.0
    z = int.from_bytes(data[18:20], byteorder='little', signed=True) / 256.0
    return (x, y, z)

async def main():
    devices = await BleakScanner.discover()

    for device in devices:
        # Fallback for device name if not available
        device_name = device.name if device.name else "Unknown Device"

        # Assuming the accelerometer data is in the manufacturer data
        manufacturer_data = device.metadata.get('manufacturer_data')
        
        if manufacturer_data:
            for key, value in manufacturer_data.items():
                if len(value) >= 20:  # Check if the data length is sufficient
                    accel_data = parse_accelerometer_data(value)
                    print(f"Device: {device_name}, Address: {device.address}")
                    print(f"Accelerometer Data: X={accel_data[0]}, Y={accel_data[1]}, Z={accel_data[2]}")
                    
                    if is_moving(accel_data):
                        print("Status: Moving")
                    else:
                        print("Status: Stationary")
                    print()

if __name__ == "__main__":
    asyncio.run(main())
