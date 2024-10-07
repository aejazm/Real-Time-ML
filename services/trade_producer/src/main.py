from quixstreams import Application
from loguru import logger
from kraken_websocket_api import KrakenWebsocketAPI

def produce_trades(
        kafka_broker_address: str,
        kafka_topic: str,
        product_id: str,
):
    """
        Reads trades from Kraken WebSocket API & saves to kafka_topic
        Args:
        kafka_broker_address: Kafka broker which receives the trades
        kafka_topic: Topic to which trade will be posted
        product_id: Currency pair whose trades are received

        Returns:
        None
    """


    # Step 1: Create an Application instance with Kafka config
    app = Application(kafka_broker_address)
    # Step 2: Define a topic "trades" with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')
    # Create an Kraken API object
    kraken_api = KrakenWebsocketAPI(product_id=product_id)
    # Step 3: Create a Producer instance
    with app.get_producer() as producer:

        while True:

            trades=kraken_api.get_trades()

            for trade in trades:

                # Step 4: Serialize the event using the defined Topic
                message = topic.serialize(key=trade.product_id, value=trade.model_dump())
                # Produce the message into the Kafka topic
                logger.debug("Going to produce trade")
                producer.produce(topic=topic.name, value=message.value, key=message.key)
                logger.debug(f"Trade pushed to Kafka {trade}")
                from time import sleep
                sleep(1)

if __name__ == "__main__":

    #from src.config 
    import config
    cfg = config.config
    produce_trades(
        kafka_broker_address=cfg.kafka_broker_address,
        kafka_topic=cfg.kafka_topic,
        product_id=cfg.product_id,
    )