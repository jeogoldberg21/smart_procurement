"""
Price forecasting model using Facebook Prophet
"""
import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

class PriceForecastModel:
    """
    Forecasting model for material prices
    """
    
    def __init__(self):
        self.models = {}
        self.forecasts = {}
    
    def prepare_data(self, df, material):
        """
        Prepare data for Prophet model
        """
        material_df = df[df['material'] == material].copy()
        material_df = material_df.rename(columns={'date': 'ds', 'price': 'y'})
        material_df['ds'] = pd.to_datetime(material_df['ds'])
        material_df = material_df[['ds', 'y']].sort_values('ds')
        return material_df
    
    def train_model(self, df, material):
        """
        Train Prophet model for a specific material
        """
        # Prepare data
        train_data = self.prepare_data(df, material)
        
        # Initialize and train model
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05,
            interval_width=0.95
        )
        
        model.fit(train_data)
        self.models[material] = model
        
        return model
    
    def forecast(self, material, periods=7):
        """
        Generate forecast for specified periods
        """
        if material not in self.models:
            raise ValueError(f"Model for {material} not trained yet")
        
        model = self.models[material]
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=periods)
        
        # Generate forecast
        forecast = model.predict(future)
        
        # Store forecast
        self.forecasts[material] = forecast
        
        return forecast
    
    def get_recommendation(self, df, material, forecast_df):
        """
        Generate buy/wait recommendation based on forecast
        """
        # Get current price (latest in historical data)
        current_price = df[df['material'] == material]['price'].iloc[-1]
        
        # Get forecasted prices for next 7 days
        future_prices = forecast_df.tail(7)['yhat'].values
        avg_future_price = np.mean(future_prices)
        min_future_price = np.min(future_prices)
        max_future_price = np.max(future_prices)
        
        # Calculate price change percentage
        price_change_pct = ((avg_future_price - current_price) / current_price) * 100
        
        # Calculate potential savings/loss
        potential_savings = current_price - min_future_price
        potential_loss = max_future_price - current_price
        
        # More sensitive decision logic (reduced threshold from 2% to 1%)
        if price_change_pct > 1.0:
            recommendation = "BUY NOW"
            reason = f"Price expected to rise by {price_change_pct:.1f}% in next 7 days"
            confidence = "High" if price_change_pct > 2 else "Medium"
        elif price_change_pct < -1.0:
            recommendation = "WAIT"
            reason = f"Price expected to drop by {abs(price_change_pct):.1f}% in next 7 days"
            confidence = "High" if price_change_pct < -2 else "Medium"
        else:
            # Even for stable prices, give actionable advice
            if potential_savings > potential_loss:
                recommendation = "WAIT"
                reason = f"Price may drop to ${min_future_price:.2f}/ton. Wait for better opportunity"
                confidence = "Medium"
            elif potential_loss > potential_savings * 1.5:
                recommendation = "BUY NOW"
                reason = f"Price may rise to ${max_future_price:.2f}/ton. Buy before increase"
                confidence = "Medium"
            else:
                recommendation = "MONITOR"
                reason = "Price expected to remain stable. Monitor for changes"
                confidence = "Medium"
        
        # Find best day to buy in next 7 days
        best_day_idx = np.argmin(future_prices)
        
        return {
            'material': material,
            'current_price': round(current_price, 2),
            'avg_forecast_price': round(avg_future_price, 2),
            'min_forecast_price': round(min_future_price, 2),
            'price_change_pct': round(price_change_pct, 2),
            'recommendation': recommendation,
            'reason': reason,
            'confidence': confidence,
            'best_day_to_buy': best_day_idx + 1,
            'potential_savings': round(max(0, potential_savings), 2)
        }
    
    def train_all_materials(self, df, materials):
        """
        Train models for all materials
        """
        results = {}
        
        for material in materials:
            try:
                # Train model
                self.train_model(df, material)
                
                # Generate forecast
                forecast = self.forecast(material, periods=7)
                
                # Get recommendation
                recommendation = self.get_recommendation(df, material, forecast)
                
                results[material] = {
                    'forecast': forecast,
                    'recommendation': recommendation
                }
                
                print(f"[OK] Trained model for {material}")
                
            except Exception as e:
                print(f"[ERROR] Error training model for {material}: {str(e)}")
                results[material] = None
        
        return results

def simple_linear_forecast(df, material, periods=7):
    """
    Fallback: Simple linear regression forecast if Prophet fails
    """
    from sklearn.linear_model import LinearRegression
    
    material_df = df[df['material'] == material].copy()
    material_df['date'] = pd.to_datetime(material_df['date'])
    material_df = material_df.sort_values('date')
    
    # Prepare features
    X = np.arange(len(material_df)).reshape(-1, 1)
    y = material_df['price'].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast
    future_X = np.arange(len(material_df), len(material_df) + periods).reshape(-1, 1)
    future_y = model.predict(future_X)
    
    # Create forecast dataframe
    last_date = material_df['date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
    
    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': future_y,
        'yhat_lower': future_y * 0.95,
        'yhat_upper': future_y * 1.05
    })
    
    return forecast_df

if __name__ == '__main__':
    # Test the model
    import os
    
    # Load data
    df = pd.read_csv('../data/material_prices.csv')
    
    # Initialize model
    model = PriceForecastModel()
    
    # Train for all materials
    results = model.train_all_materials(df, ['Copper', 'Aluminum', 'Steel'])
    
    # Print recommendations
    for material, result in results.items():
        if result:
            print(f"\n{material}: {result['recommendation']['recommendation']}")
            print(f"  {result['recommendation']['reason']}")
