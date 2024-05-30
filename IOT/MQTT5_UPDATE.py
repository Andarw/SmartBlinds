from awsiot import mqtt5_client_builder
from awscrt import mqtt5, http
import threading
from concurrent.futures import Future
import time
import json
from light_intensity import light_intensity
from DHT12 import read_dht12
import uuid
import datetime

received_all_event = threading.Event()
future_stopped = Future()
future_connection_success = Future()
message_topic = "raspberrypi_data"

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))


# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure")
    print("Connection failed with exception:{}".format(lifecycle_connection_failure.exception))

def send_data_with_MQTT():
	
	client = mqtt5_client_builder.mtls_from_path(
	endpoint="a3lb2w5wa5b5li-ats.iot.eu-north-1.amazonaws.com",
	cert_filepath="/home/iot/Desktop/certificate.pem.crt",
	pri_key_filepath="/home/iot/Desktop/private.pem.key",
	ca_filepath="/home/iot/Desktop/AmazonRootCA1.pem",
	http_proxy_options=None,
	on_publish_received=on_publish_received,
	on_lifecycle_stopped=on_lifecycle_stopped,
	on_lifecycle_connection_success=on_lifecycle_connection_success,
	on_lifecycle_connection_failure=on_lifecycle_connection_failure,
	client_id=str(uuid.uuid4()))
	print("MQTT5 Client Created")
	print("Connecting to endpoint with client ID")
	
	global future_connection_success
	global future_stopped
	if future_connection_success is None and future_stopped is None:
		future_stopped = Future()
		future_connection_success = Future()
	
	# Start client
	client.start()
	lifecycle_connect_success_data = future_connection_success.result(100)
	connack_packet = lifecycle_connect_success_data.connack_packet
	negotiated_settings = lifecycle_connect_success_data.negotiated_settings
	
	# Subscribe
	subscribe_future = client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
	subscriptions=[mqtt5.Subscription(
	topic_filter=message_topic,
	qos=mqtt5.QoS.AT_LEAST_ONCE)]))
	suback = subscribe_future.result(100)
	
	#format Json
	temperature, humidity = read_dht12()
	light_int = light_intensity()
	current_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
	rdate = current_time.strftime("%Y-%m-%d %H:%M:%S")
	
	message = {
	'temperature': str(temperature),
	'humidity': str(humidity),
	'intensity': str(light_int),
	'rdate': rdate
	}
	
	publish_future = client.publish(mqtt5.PublishPacket(
	topic=message_topic,
	payload=json.dumps(message),
	qos=mqtt5.QoS.AT_LEAST_ONCE
	))
	
	publish_completion_data = publish_future.result(100)
	time.sleep(1)
	
	# Unsubscribe
	
	unsubscribe_future = client.unsubscribe(unsubscribe_packet=mqtt5.UnsubscribePacket(
	topic_filters=[message_topic]))
	unsuback = unsubscribe_future.result(100)
	
	client.stop()
	
	future_stopped.result(100)
	print("Succesfull!!!")
	global received_all_event
	received_all_event = threading.Event()
	future_stopped = None
	future_connection_success = None
