import logging

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    def __init__(self):
        pass
    
    def analyze_market_condition(self, nifty_data, vix_data, mmi_data):
        """Analyze market conditions and provide insights"""
        
        analysis = {
            'market_condition': '',
            'recommendation': '',
            'risk_level': '',
            'asset_allocation': '',
            'reasoning': []
        }
        
        try:
            # Analyze VIX
            vix_value = float(vix_data['current_value']) if vix_data else 20
            
            if vix_value < 15:
                analysis['reasoning'].append("VIX below 15 indicates low volatility - market complacency")
                vix_signal = "low_volatility"
            elif vix_value > 25:
                analysis['reasoning'].append("VIX above 25 indicates high volatility - market fear")
                vix_signal = "high_volatility"
            else:
                analysis['reasoning'].append("VIX in normal range - moderate volatility")
                vix_signal = "normal_volatility"
            
            # Analyze MMI
            mmi_signal = "neutral"
            if mmi_data:
                mmi_value = int(mmi_data['mmi_value']) if mmi_data['mmi_value'].isdigit() else 50
                
                if mmi_value < 25:
                    analysis['reasoning'].append("MMI below 25 - Extreme Fear zone")
                    mmi_signal = "extreme_fear"
                elif mmi_value < 40:
                    analysis['reasoning'].append("MMI below 40 - Fear zone")
                    mmi_signal = "fear"
                elif mmi_value > 75:
                    analysis['reasoning'].append("MMI above 75 - Extreme Greed zone")
                    mmi_signal = "extreme_greed"
                elif mmi_value > 60:
                    analysis['reasoning'].append("MMI above 60 - Greed zone")
                    mmi_signal = "greed"
                else:
                    analysis['reasoning'].append("MMI in neutral zone")
                    mmi_signal = "neutral"
            
            # Analyze NIFTY trend
            nifty_signal = "neutral"
            if nifty_data:
                change_percent = float(nifty_data['change_percent'].replace('%', '')) if '%' in str(nifty_data['change_percent']) else 0
                
                if change_percent > 2:
                    analysis['reasoning'].append("NIFTY up >2% - Strong bullish momentum")
                    nifty_signal = "strong_bullish"
                elif change_percent > 0.5:
                    analysis['reasoning'].append("NIFTY up >0.5% - Bullish trend")
                    nifty_signal = "bullish"
                elif change_percent < -2:
                    analysis['reasoning'].append("NIFTY down >2% - Strong bearish momentum")
                    nifty_signal = "strong_bearish"
                elif change_percent < -0.5:
                    analysis['reasoning'].append("NIFTY down >0.5% - Bearish trend")
                    nifty_signal = "bearish"
            
            # Combine signals for final recommendation
            analysis.update(self._get_recommendation(nifty_signal, vix_signal, mmi_signal))
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            analysis.update({
                'market_condition': 'Unable to analyze',
                'recommendation': 'Hold current positions',
                'risk_level': 'Medium',
                'asset_allocation': '50% Equity, 50% Debt'
            })
        
        return analysis
    
    def _get_recommendation(self, nifty_signal, vix_signal, mmi_signal):
        """Generate recommendation based on combined signals"""
        
        # Scoring system
        equity_score = 0
        
        # NIFTY signals
        if nifty_signal == "strong_bullish":
            equity_score += 2
        elif nifty_signal == "bullish":
            equity_score += 1
        elif nifty_signal == "strong_bearish":
            equity_score -= 2
        elif nifty_signal == "bearish":
            equity_score -= 1
        
        # VIX signals
        if vix_signal == "low_volatility":
            equity_score += 1
        elif vix_signal == "high_volatility":
            equity_score -= 2
        
        # MMI signals
        if mmi_signal == "extreme_fear":
            equity_score += 2  # Contrarian signal
        elif mmi_signal == "fear":
            equity_score += 1
        elif mmi_signal == "extreme_greed":
            equity_score -= 2
        elif mmi_signal == "greed":
            equity_score -= 1
        
        # Generate recommendation
        if equity_score >= 3:
            return {
                'market_condition': 'Bullish',
                'recommendation': 'BUY',
                'risk_level': 'Medium',
                'asset_allocation': '70% Equity, 30% Debt'
            }
        elif equity_score >= 1:
            return {
                'market_condition': 'Moderately Bullish',
                'recommendation': 'ACCUMULATE',
                'risk_level': 'Medium',
                'asset_allocation': '60% Equity, 40% Debt'
            }
        elif equity_score <= -3:
            return {
                'market_condition': 'Bearish',
                'recommendation': 'SELL/REDUCE',
                'risk_level': 'High',
                'asset_allocation': '30% Equity, 70% Debt'
            }
        elif equity_score <= -1:
            return {
                'market_condition': 'Moderately Bearish',
                'recommendation': 'HOLD/REDUCE',
                'risk_level': 'Medium-High',
                'asset_allocation': '40% Equity, 60% Debt'
            }
        else:
            return {
                'market_condition': 'Neutral',
                'recommendation': 'HOLD',
                'risk_level': 'Medium',
                'asset_allocation': '50% Equity, 50% Debt'
            }
