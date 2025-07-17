import logging
from scraper import MarketDataScraper
from analyzer import MarketAnalyzer
from telegram_bot import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        scraper = MarketDataScraper()
        analyzer = MarketAnalyzer()
        notifier = TelegramNotifier()
        
        # Scrape data
        logger.info("Scraping market data...")
        nifty_data = scraper.get_nifty_data()
        vix_data = scraper.get_nifty_vix()
        mmi_data = scraper.get_mmi_data()
        
        # Analyze data
        logger.info("Analyzing market conditions...")
        analysis = analyzer.analyze_market_condition(nifty_data, vix_data, mmi_data)
        
        # Format and send message
        logger.info("Formatting and sending message...")
        message = notifier.format_message(nifty_data, vix_data, mmi_data, analysis)
        
        success = notifier.send_message(message)
        
        if success:
            logger.info("Market update sent successfully!")
        else:
            logger.error("Failed to send market update")
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        
        # Send error notification
        try:
            notifier = TelegramNotifier()
            error_message = f"❌ *Market Update Error*\n\nFailed to fetch market data: {str(e)}"
            notifier.send_message(error_message)
        except:
            pass

if __name__ == "__main__":
    main()
