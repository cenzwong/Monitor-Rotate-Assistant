#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

const int pinDHT11_DATA = 27;
const int pinPhotoresistor = 35;

DHT dht(pinDHT11_DATA, DHT11);

// Replace the next variables with your SSID/Password combination
const char* ssid = "--------";
const char* password = "--------";

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
const char* mqtt_server = "172.16.11.48";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;



// LED Pin
const int ledPin = 4;

void setup() {
  Serial.begin(115200);
  // default settings
  // (you can also pass in a Wire library object like &Wire2)

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == "myName/test") {
    Serial.print("Changing output to ");
    if(messageTemp == "on"){
      Serial.println("on");
      digitalWrite(ledPin, HIGH);
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      digitalWrite(ledPin, LOW);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("myName/test");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  // do that once five second
  if (now - lastMsg > 1000) {
    lastMsg = now;
    
    // Temperature in Celsius
    static float temperature;
    // Uncomment the next line to set temperature in Fahrenheit 
    // (and comment the previous temperature line)
    static float humidity;
    static float light;
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    light = analogRead(pinPhotoresistor);
    Serial.print("temperature: ");
    Serial.println(temperature);
    Serial.print("humidity ");
    Serial.println(humidity);
    Serial.print("light ");
    Serial.println(light);
    // Convert the value to a char array
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
//    Serial.print("Temperature: ");
//    Serial.println(tempString);
    client.publish("sensor/temperature", tempString);

    dtostrf(humidity, 1, 2, tempString);
    client.publish("sensor/humidity", tempString);

    dtostrf(light, 1, 2, tempString);
    client.publish("sensor/light", tempString);

  }
}
