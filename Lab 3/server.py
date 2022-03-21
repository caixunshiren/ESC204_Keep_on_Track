''' 
ESC204 2022W Widget Lab 3IoT, Part 8 
Task: Implement an MQTT receiver. 
''' 
import paho.mqtt.client as mqtt 
 

topic = "uoft/p3/4/"
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
        print("got light data " + str(msg.payload))
        with open("light.txt", "w+") as f:
            f.write(str(msg.payload) + '\n')
    elif msg.topic == topic + "heat":
        print("got heat data " + str(msg.payload))
        with open("heat.txt", "w+") as f:
            f.write(str(msg.payload) + '\n')

def start_server():
    client = mqtt.Client() 
    client.on_connect = on_connect 
    client.on_message = on_message 
    client.connect("test.mosquitto.org", 1883, 60) 
    client.loop_forever()

if __name__ == "__main__":
    start_server()