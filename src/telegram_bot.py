import os
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.bot_token)
    
    def format_message(self, nifty_data, vix_data, mmi_data, analysis):
        """Format the market data into a nice message"""
        
        message = "📊 *Daily Market Update*\n"
        message += "=" * 30 + "\n\n"
        
        # NIFTY 50 Data
        if nifty_data:
            change_emoji = "📈" if float(str(nifty_data['change_percent']).replace('%', '')) > 0 else "📉"
            message += f"🔹 *NIFTY 50*\n"
            message += f"   Price: {nifty_data['current_price']}\n"
            message += f"   Change: {nifty_data['change']} ({nifty_data['change_percent']}) {change_emoji}\n"
            if nifty_data['pe_ratio'] != 'N/A':
                message += f"   PE Ratio: {nifty_data['pe_ratio']}\n"
            message += "\n"
        
        # NIFTY VIX Data
        if vix_data:
            vix_emoji = "😰" if float(vix_data['current_value']) > 20 else "😌"
            message += f"🔹 *NIFTY VIX*\n"
            message += f"   Value: {vix_data['current_value']} {vix_emoji}\n"
            message += f"   Change: {vix_data['change']} ({vix_data['change_percent']})\n\n"
        
        # MMI Data
        if mmi_data:
            mmi_emoji = self._get_mmi_emoji(mmi_data['mmi_value'])
            message += f"🔹 *Market Mood Index*\n"
            message += f"   Value: {mmi_data['mmi_value']} {mmi_emoji}\n"
            message += f"   Status: {mmi_data['mmi_status']}\n\n"
        
        # Analysis and Recommendations
        message += "📈 *Market Analysis*\n"
        message += "-" * 20 + "\n"
        message += f"Condition: {analysis['market_condition']}\n"
        message += f"Recommendation: *{analysis['recommendation']}*\n"
        message += f"Risk Level: {analysis['risk_level']}\n"
        message += f"Asset Allocation: {analysis['asset_allocation']}\n\n"
        
        # Reasoning
        if analysis['reasoning']:
            message += "💡 *Key Insights:*\n"
            for reason in analysis['reasoning']:
                message += f"• {reason}\n"
        
        message += "\n⚠️ *Disclaimer:* This is for educational purposes only. Please consult a financial advisor before making investment decisions."
        
        return message
    
    def _get_mmi_emoji(self, mmi_value):
        """Get emoji based on MMI value"""
        try:
            value = int(mmi_value) if str(mmi_value).isdigit() else 50
            if value < 25:
                return "😱"  # Extreme Fear
            elif value < 40:
                return "😟"  # Fear
            elif value < 60:
                return "😐"  # Neutral
            elif value < 75:
                return "😊"  # Greed
            else:
                return "🤑"  # Extreme Greed
        except:
            return "😐"
    
    def send_message(self, message):
        """Send message to Telegram"""
        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info("Message sent successfully to Telegram")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
