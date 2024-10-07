from typing import List
from loguru import logger
from websocket import create_connection
import json

class KrakenWebsocketAPI:

    """
    Class for reading real time trades from Kraken WS API
    """
    URL='wss://ws.kraken.com/v2'
    def __init__(self, product_id:str):
        """
        product_id Currency pair for which trades will be fetched
        """
        self.product_id=product_id

        """Establish connection to Kraken web api"""
        self._ws = create_connection(self.URL)
        logger.info('Connection established')

        """Subscribe to the trades"""
        self._subscribe(product_id)

    def _subscribe(self, product_id:str):
        logger.info('Subscribing to the trades for {product_id}')
        msg = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade',
                'symbol': [product_id],
                'snapshot': False
            }
        }
        self._ws.send(json.dumps(msg))
        logger.info('Subcription successful !!')

        for product_id in [product_id]:
            _ = self._ws.recv()
            _ = self._ws.recv()


    def get_trades(self) -> List[dict]:
        """Return latest batch of trades"""
        message = self._ws.recv()

        if 'heartbeat' in message:
            logger.info('Received heartbeat')
            return []
        
        message = json.loads(message)

        trades=[]
        for trade in message['data']:
            breakpoint()
        
        return trades

    def is_done(self) -> bool:
        """Returns true if Kraken WS API connection is closed"""
        False

    