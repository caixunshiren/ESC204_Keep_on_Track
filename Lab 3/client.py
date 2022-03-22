''' 
ESC204 2022W Widget Lab 3IoT, Part 8 
Task: Implement an MQTT receiver. 
''' 
import paho.mqtt.client as mqtt 
import time
 
# The callback for when the client receives a CONNACK response from the server. 
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    # Subscribing in on_connect() means that if we lose the connection and 
    # reconnect then subscriptions will be renewed. 
     
    teamid = "4" #TODO: fill in your team ID 
    client.subscribe(f"uoft/p3/{teamid}/msg") 
 
# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
    print(msg.topic+": "+str(msg.payload)) 


def start_server():
    client = mqtt.Client() 
    client.on_connect = on_connect 
    client.on_message = on_message 
    client.connect("test.mosquitto.org", 1883, 60) 
    time.sleep(5)
    client.publish( "uoft/p3/4/msg", 'hello world')

if __name__ == "__main__":
    start_server()