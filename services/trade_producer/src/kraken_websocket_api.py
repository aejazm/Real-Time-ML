from typing import List
from loguru import logger
from websocket import create_connection
import json 
from pydantic import BaseModel

class Trade(BaseModel):
    product_id: str
    quantity: float
    price: float
    timestamp_ms: int 

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
        logger.info(f'Subscribing to the trades for {product_id}')
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
            trades.append(
                Trade(
                        product_id=trade['symbol'],
                        price=trade['price'],
                        quantity=trade['qty'],
                        timestamp_ms=self.to_ms(trade['timestamp'])
                    )
            )
        
        return trades
    
    @staticmethod
    def to_ms(timestamp: str) -> int:
        """
        A function that transforms a timestamps expressed
        as a string like this '2024-06-17T09:36:39.467866Z'
        into a timestamp expressed in milliseconds.

        Args:
            timestamp (str): A timestamp expressed as a string.

        Returns:
            int: A timestamp expressed in milliseconds.
        """
        # parse a string like this '2024-06-17T09:36:39.467866Z'
        # into a datetime object assuming UTC timezone
        # and then transform this datetime object into Unix timestamp
        # expressed in milliseconds
        from datetime import datetime, timezone

        timestamp = datetime.fromisoformat(timestamp[:-1]).replace(tzinfo=timezone.utc)
        return int(timestamp.timestamp() * 1000)

    def is_done(self) -> bool:
        """Returns true if Kraken WS API connection is closed"""
        False

    