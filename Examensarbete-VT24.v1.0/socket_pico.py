"""
Program does the following:
- Reads temperature from a DS18B20 temperature sensor
- Sends temperature to a Socket server over Wi-Fi
- Measures latency every time the program sends the temperature
- Calculates the average latency since the program started

Variables which needs to be changed:
- SSID and PASSWORD in the connect_to_wifi function
- Server IP and port in the connect_to_socket_server function
- The used data pin in the end of the program

If you intend to use this program as a permanent solution,
then the if statement in the end needs to be removed.
New versions of this code will not have this code anymore
since it was used to calculate the average latency only.
"""

# Imported modules
import network
import usocket as socket
import machine
import onewire, ds18x20
import utime
import time
import ujson

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

    # Return value of cyw43_wifi_link_status
    # define CYW43_LINK_DOWN (0)
    # define CYW43_LINK_JOIN (1)
    # define CYW43_LINK_NOIP (2)
    # define CYW43_LINK_UP (3)
    # define CYW43_LINK_FAIL (-1)
    # define CYW43_LINK_NONET (-2)
    # define CYW43_LINK_BADAUTH (-3)

    # Raspberry Pi Pico WiFi docs: https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

def connect_to_socket_server() -> str:
    # Create socket with: AF_INET -> IPv4 and SOCK_STREAM -> TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(("SERVER_IP", "PORT"))
    print("Connected to server")
    return client_socket

# Read from DS18B20 temperature sensor.
def read_temperature() -> float:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        pass
    tempC = ds_sensor.read_temp(rom)
    return tempC

# Used to calculate averages
total_latency = 0
loop_counter = 0

def send_temperature(client_socket) -> None:
    global total_latency # Float
    global loop_counter # Int

    # Reads the current temperature.
    temperature = read_temperature()
    print("Current temperature:", temperature)
    
    # Encode payload as JSON
    payload = {"temperature": temperature}
    json_payload = ujson.dumps(payload)

    # Times latency in milliseconds.
    start_time = utime.ticks_ms()
    client_socket.sendall(json_payload)
    response_bytes = client_socket.recv(1024)
    end_time = utime.ticks_ms()

    # Decode response from bytes to string
    response = response_bytes.decode("utf-8")
    print(f"Received from server: {response}")

    # Calculate latency
    latency = (end_time - start_time) / 1000.0
    total_latency += latency

    print(f"Current latency: {latency} seconds")
    print(f"Average latency: {total_latency / loop_counter} seconds")
    print(f"The program has looped {loop_counter} times.")

if __name__ == "__main__":
    connect_to_wifi()
    client_socket = connect_to_socket_server()

    # Set pin and find sensor
    ds_pin = machine.Pin("PIN")
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)

    # Main loop
    while True:
        try: 
            values = send_temperature(client_socket)
            loop_counter += 1

            if loop_counter == 300:
                print('--------------------------------------------')
                print(f'The average latency was: {total_latency / loop_counter} seconds')
                break
            time.sleep(10)

        except KeyboardInterrupt:
            print("User ended the program.")
            break
