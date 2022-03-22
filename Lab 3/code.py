import board 
import time 
import digitalio 
import analogio
import busio 
from digitalio import DigitalInOut 
from adafruit_esp32spi import adafruit_esp32spi 
import adafruit_esp32spi.adafruit_esp32spi_socket as socket 
import adafruit_minimqtt.adafruit_minimqtt as MQTT 
 
def on_connect(mqtt_client, userdata, flags, rc): 
    ''' 
    This function will be called when the mqtt_client is connected success-
fully to the broker. 
    ''' 
    print("Connected to MQTT Broker!") 
    print("Flags: {0}\n RC: {1}".format(flags, rc)) 
 
def on_publish(mqtt_client, userdata, topic, pid): 
    ''' 
    This method is called when the mqtt_client publishes data to a feed. 
    ''' 
    print("Published to {0} with PID {1}".format(topic, pid)) 
 

INT_MODE = 0
VOLT_MODE = 1
mode = INT_MODE

ADC_HIGH = 65535

thermistor_pin = board.A2
thermistor = analogio.AnalogIn(thermistor_pin)
photoresistor_pin = board.A1
photoresistor = analogio.AnalogIn(photoresistor_pin)


ADC_REF_therm = thermistor.reference_voltage
ADC_REF_photo = photoresistor.reference_voltage


# convert ADC input value back to voltage
def adc_to_voltage_therm(adc_value):
    return  ADC_REF_therm * (float(adc_value)/float(ADC_HIGH))

def adc_to_voltage_photo(adc_value):
    return  ADC_REF_photo * (float(adc_value)/float(ADC_HIGH))

def get_heat():
    return adc_to_voltage_therm(thermistor.value)

def get_light():
    return adc_to_voltage_photo(photoresistor.value)


# Set MQTT definitions 
teamid = "4" #TODO: fill in your teamid 
mqtt_topic = f"uoft/p3/4/" 
 
# Get wifi details and more from a secrets.py file 
try: 
    from secrets import secrets 
except ImportError: 
    print("WiFi secrets are kept in secrets.py, please add them there!") 
    raise 
 
# Set up SPI pins 
esp32_cs = DigitalInOut(board.CS1) 
esp32_ready = DigitalInOut(board.ESP_BUSY) 
esp32_reset = DigitalInOut(board.ESP_RESET) 
 
# Connect the RP2040 to the Nina W102 uBlox module's onboard ESP32 chip via SPI connections 
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1) 
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset) 


 # Check if ESP32 chip found and ready to connect and print chip details 
if esp.status == adafruit_esp32spi.WL_IDLE_STATUS: 
    print("ESP32 found and in idle mode") 
print("Firmware vers.", esp.firmware_version) 
print("MAC addr:", [hex(i) for i in esp.MAC_address]) 
 
# Print SSIDs for all discovered networks and their signal strengths 
for ap in esp.scan_networks(): 
    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi'])) 
 
# Try to connect to your WiFI network (using the SSID and password from secrets.py) 
print("Connecting to AP...") 
while not esp.is_connected: 
    try: 
        print(f"connecting to {secrets["ssid"]} with {secrets["password"]}")
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e: 
        print("could not connect to AP, retrying: ", e) 
        continue 
    print(".", end="") 
 
# If successfully connected, print IP 
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi) 
print("My IP address is", esp.pretty_ip(esp.ip_address)) 
 
# Set up socket 
socket.set_interface(esp) 
 
# Set up a MiniMQTT Client 
MQTT.set_socket(socket, esp) 
mqtt_client = MQTT.MQTT(broker='test.mosquitto.org',port=1883) 
 
# Connect callback handlers to mqtt_client 
mqtt_client.on_connect = on_connect 
mqtt_client.on_publish = on_publish 
 
# Try to connect to MQTT client 
print("Attempting to connect to %s" % mqtt_client.broker) 
mqtt_client.connect() 


# Publish to MQTT topic 
while True: 
    heat = get_heat()
    light = get_light()
    print(heat, light)
    mqtt_client.publish(mqtt_topic + "light", light)
    mqtt_client.publish(mqtt_topic + "heat", heat)
    time.sleep(1)
    


