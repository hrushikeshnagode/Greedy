import ccxt
import logging
from config.settings import (
    BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_TESTNET,
    LIVE_TRADING
)

logger = logging.getLogger(__name__)

class TradeExecutor:
    """
    Executes trades on Binance via CCXT
    Paper trading on testnet, live trading on mainnet
    """
    
    def __init__(self):
        if BINANCE_TESTNET:
            self.exchange = ccxt.binance({
                'apiKey': BINANCE_API_KEY,
                'secret': BINANCE_API_SECRET,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'sandboxMode': True,
                }
            })
            self.exchange.set_sandbox_mode(True)
            logger.info("✓ Connected to Binance TESTNET (Paper Trading)")
        else:
            self.exchange = ccxt.binance({
                'apiKey': BINANCE_API_KEY,
                'secret': BINANCE_API_SECRET,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                }
            })
            logger.warning("⚠️  LIVE TRADING MODE - REAL MONEY AT RISK")
    
    def get_balance(self, symbol='USDT'):
        """Get account balance for a symbol"""
        try:
            balance = self.exchange.fetch_balance()
            return balance[symbol]['free']
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return 0
    
    def get_ticker(self, pair):
        """Get current price for a pair"""
        try:
            ticker = self.exchange.fetch_ticker(pair)
            return ticker['last']
        except Exception as e:
            logger.error(f"Error fetching ticker for {pair}: {e}")
            return None
    
    def place_buy_order(self, pair, amount, price=None):
        """
        Place a buy order
        If price is None, uses market order
        """
        try:
            if price:
                order = self.exchange.create_limit_buy_order(pair, amount, price)
                logger.info(f"✓ BUY order placed: {amount} {pair} @ {price}")
            else:
                order = self.exchange.create_market_buy_order(pair, amount)
                logger.info(f"✓ MARKET BUY order placed: {amount} {pair}")
            return order
        except Exception as e:
            logger.error(f"Error placing buy order: {e}")
            return None
    
    def place_sell_order(self, pair, amount, price=None):
        """
        Place a sell order
        If price is None, uses market order
        """
        try:
            if price:
                order = self.exchange.create_limit_sell_order(pair, amount, price)
                logger.info(f"✓ SELL order placed: {amount} {pair} @ {price}")
            else:
                order = self.exchange.create_market_sell_order(pair, amount)
                logger.info(f"✓ MARKET SELL order placed: {amount} {pair}")
            return order
        except Exception as e:
            logger.error(f"Error placing sell order: {e}")
            return None
    
    def fetch_ohlcv(self, pair, timeframe='4h', limit=100):
        """
        Fetch OHLCV candles
        Returns: DataFrame with columns [timestamp, open, high, low, close, volume]
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(pair, timeframe, limit=limit)
            import pandas as pd
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {pair}: {e}")
            return None
    
    def cancel_order(self, pair, order_id):
        """Cancel an open order"""
        try:
            result = self.exchange.cancel_order(order_id, pair)
            logger.info(f"✓ Order {order_id} cancelled")
            return result
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return None
