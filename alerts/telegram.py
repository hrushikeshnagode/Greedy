import logging
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SEND_ALERTS

logger = logging.getLogger(__name__)

class TelegramAlerts:
    """
    Sends trade alerts via Telegram
    """
    
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = SEND_ALERTS and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
        
        if self.enabled:
            try:
                import telegram
                self.bot = telegram.Bot(token=self.token)
                logger.info("✓ Telegram alerts enabled")
            except Exception as e:
                logger.error(f"Telegram setup failed: {e}")
                self.enabled = False
        else:
            logger.warning("⚠️  Telegram alerts disabled (set TELEGRAM_TOKEN in .env)")
    
    def send_message(self, message):
        """Send a message to Telegram"""
        if not self.enabled:
            return False
        
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def send_trade_alert(self, trade_data):
        """Send trade execution alert"""
        side = trade_data['side']
        pair = trade_data['pair']
        price = trade_data['entry_price']
        size = trade_data['position_size']
        regime = trade_data['regime']
        signal_str = trade_data['signal_strength']
        
        message = f"""
🤖 **GREEDY Bot** - Trade Executed
═══════════════════════════════════
📊 {side} {pair}
💰 Price: ${price:.2f}
📦 Size: {size:.4f}
🎯 Regime: {regime}
⚡ Confidence: {signal_str:.1f}%
═════════════��═════════════════════
        """
        return self.send_message(message)
    
    def send_close_alert(self, trade_data):
        """Send trade close alert"""
        pair = trade_data['pair']
        entry = trade_data['entry_price']
        exit_price = trade_data['exit_price']
        pnl = trade_data['pnl']
        pnl_pct = trade_data['pnl_pct']
        
        emoji = "✅" if pnl > 0 else "❌"
        
        message = f"""
{emoji} **Trade Closed**
═══════════════════════════════════
📊 {pair}
📈 Entry: ${entry:.2f}
📉 Exit: ${exit_price:.2f}
💵 P&L: ${pnl:.2f} ({pnl_pct:.2f}%)
═══════════════════════════════════
        """
        return self.send_message(message)
    
    def send_daily_summary(self, summary):
        """Send daily P&L summary"""
        message = f"""
📊 **Daily Summary**
═══════════════════════════════════
📈 Trades: {summary['total_trades']}
💵 P&L: ${summary['total_pnl']:.2f}
📊 Win Rate: {summary['win_rate']:.1f}%
🎯 Avg Win: ${summary['avg_win']:.2f}
🎯 Avg Loss: ${summary['avg_loss']:.2f}
═══════════════════════════════════
        """
        return self.send_message(message)
