import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_nifty_data(self):
        """Scrape NIFTY 50 data from NSE or reliable source"""
        try:
            # Using NSE API endpoint
            url = "https://www.nseindia.com/api/allIndices"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                for index in data['data']:
                    if index['index'] == 'NIFTY 50':
                        return {
                            'name': 'NIFTY 50',
                            'current_price': index['last'],
                            'change': index['change'],
                            'change_percent': index['percentChange'],
                            'pe_ratio': index.get('pe', 'N/A')  # May not be available
                        }
            
            # Fallback to web scraping
            return self._scrape_nifty_fallback()
            
        except Exception as e:
            logger.error(f"Error fetching NIFTY data: {e}")
            return self._scrape_nifty_fallback()
    
    def _scrape_nifty_fallback(self):
        """Fallback method using web scraping"""
        try:
            url = "https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data (selectors may need adjustment)
            price_element = soup.find('span', {'class': 'span_price_wrap'})
            change_element = soup.find('span', {'class': 'span_price_change_prcnt'})
            
            if price_element and change_element:
                price = price_element.text.strip()
                change_text = change_element.text.strip()
                
                return {
                    'name': 'NIFTY 50',
                    'current_price': price,
                    'change': change_text,
                    'change_percent': change_text,
                    'pe_ratio': 'N/A'
                }
            
        except Exception as e:
            logger.error(f"Fallback scraping failed: {e}")
            return None
    
    def get_nifty_vix(self):
        """Scrape NIFTY VIX data"""
        try:
            url = "https://www.nseindia.com/api/allIndices"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                for index in data['data']:
                    if 'VIX' in index['index']:
                        return {
                            'name': 'NIFTY VIX',
                            'current_value': index['last'],
                            'change': index['change'],
                            'change_percent': index['percentChange']
                        }
            
        except Exception as e:
            logger.error(f"Error fetching VIX data: {e}")
            return None
    
    def get_mmi_data(self):
        """Scrape MMI data from TickerTape"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        try:
            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
            
            driver.get("https://www.tickertape.in/market-mood-index")
            
            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            
            # Find MMI value (selector may need adjustment)
            mmi_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='mmi-value']"))
            )
            
            mmi_value = mmi_element.text.strip()
            
            # Find MMI status
            status_element = driver.find_element(By.CSS_SELECTOR, "[data-testid='mmi-status']")
            mmi_status = status_element.text.strip()
            
            driver.quit()
            
            return {
                'mmi_value': mmi_value,
                'mmi_status': mmi_status
            }
            
        except Exception as e:
            logger.error(f"Error fetching MMI data: {e}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def get_pe_ratio(self):
        """Get NIFTY 50 PE ratio from reliable source"""
        try:
            # Using alternative source for PE ratio
            url = "https://www.niftyindices.com/reports/historical-data"
            response = self.session.get(url)
            
            # This would need specific parsing based on the website structure
            # For now, returning a placeholder
            return {
                'pe_ratio': 'N/A',
                'source': 'Manual update required'
            }
            
        except Exception as e:
            logger.error(f"Error fetching PE ratio: {e}")
            return None
