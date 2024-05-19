# Imported modules
import network
import urequests
import ujson
import machine
import onewire, ds18x20
import utime
import time
import gc

def connect_to_wifi() -> None:
    # WiFi and network settings
    SSID = "SSID"
    PASSWORD = "PASSWORD"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting to connect...")
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3: # If the wlan status isn't CYW43_LINK_UP
        raise RuntimeError("network connection failed")
    else:
        print("connected")
        status = wlan.ifconfig()
        print("ip = " + status[0])

# Read from DS18B20 temperature sensor.
def read_temperature() -> float:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        pass
    tempC = ds_sensor.read_temp(rom)
    return tempC  # Return temperature and ROMs

# Used to calculate Averages
total_latency = 0
loop_counter = 0

def send_temperature() -> None:
    global total_latency # Float
    global loop_counter# Int

    # Reads the current temperature
    temperature = read_temperature()
    print("Current temperature:", temperature)

    # Prepares POST
    url = "http://SERVER_IP:PORT/update_temperature"
    payload = {"temperature": temperature}
    json_payload = ujson.dumps(payload)
    headers = {"Content-Type": "application/json"}

    # Times latency in milliseconds.
    start_time = utime.ticks_ms()
    response = urequests.post(url, data=json_payload, headers=headers)  # Pass JSON payload
    end_time = utime.ticks_ms()

    print(f"Received from server: {response}")
    
    # Calculate latency
    latency = (end_time - start_time) / 1000
    total_latency += latency

    gc.collect()  # Perform garbage collection

    print(f"Latency: {latency} seconds")
    print(f"Average latency: {total_latency / loop_counter} seconds")
    print(f"The program has looped {loop_counter} times.")

if __name__ == "__main__":
    connect_to_wifi()

    # Set pin and find sensor
    ds_pin = machine.Pin("PIN")
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)

    # Main loop
    while True:
        try: 
            values = send_temperature()
            loop_counter += 1

            if loop_counter == 300:
                print('--------------------------------------------')
                print(f'The average latency was: {total_latency / loop_counter} seconds')
                break
            time.sleep(10)

        except KeyboardInterrupt:
            print("User ended the program.")
            break
