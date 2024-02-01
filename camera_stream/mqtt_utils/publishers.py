from paho.mqtt import client as mqtt_client


class BasePublisher:
    def __init__(self, client_instance: mqtt_client.Client) -> None:
        self._client_instance: mqtt_client.Client = client_instance

    def send(self, topic: str, msg: str) -> None:
        status: int = self._client_instance.publish(topic, msg)[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
