''' 
ESC204 2022W Widget Lab 3IoT, Part 8 
Task: Implement an MQTT receiver. 
''' 
import paho.mqtt.client as mqtt 
import time, math

topic = "uoft/p3/4/"
start = None
# The callback for when the client receives a CONNACK response from the server. 
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    # Subscribing in on_connect() means that if we lose the connection and 
    # reconnect then subscriptions will be renewed. 
     
    teamid = "4" #TODO: fill in your team ID 
    client.subscribe(topic + "light") 
    client.subscribe(topic + "heat") 
 
# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
   
    if msg.topic == topic + "light":
        with open("light.txt", "a") as f:
            f.write(msg.payload.decode("utf-8") + " " + str(round(time.time(), 1)) + "\n")
    elif msg.topic == topic + "heat":
        with open("heat.txt", "a") as f:
            v = float(msg.payload.decode("utf-8"))
            print(f'v: {v}')
            R = (3.3-v)/(v/10000)
            print(f'R: {R}')
            tK = 1/(1/298.15 - math.log(R/10000)/3950)
            tC = tK - 273.15 
            f.write(str(tC) + " " + str(round(time.time(), 1)) + "\n")

def start_server():
    client = mqtt.Client() 
    client.on_connect = on_connect 
    client.on_message = on_message 
    client.connect("test.mosquitto.org", 1883, 60) 
    client.loop_forever()

if __name__ == "__main__":
    start_server()