# Real-Time Web Scraping Guide

## Overview

The Smart Procurement System now includes **real-time web scraping** capabilities to fetch live commodity prices from various sources. This replaces the simulated price updates with actual market data.

## Features

### 1. **Multi-Source Data Fetching**
- Yahoo Finance API for commodity futures
- Support for Metal Price API (optional, requires API key)
- Support for Commodities API (optional, requires API key)
- Fallback to web scraping from investing.com
- Intelligent caching to reduce API calls

### 2. **Supported Materials**
- **Copper**: Fetched from copper futures (HG=F)
- **Aluminum**: Fetched from aluminum futures (ALI=F)
- **Steel**: Fetched from steel company stocks as proxy (MT - ArcelorMittal)

### 3. **Automatic Fallback**
- If web scraping fails, the system automatically falls back to simulated data
- Configurable via `USE_FALLBACK_ON_SCRAPE_FAIL` in config

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Enable/disable real-time scraping
ENABLE_REAL_TIME_SCRAPING=true

# How often to scrape (in seconds)
SCRAPING_INTERVAL=300

# Optional API keys for premium data
METAL_PRICE_API_KEY=your_key_here
COMMODITIES_API_KEY=your_key_here
```

### Getting API Keys (Optional)

While the system works without API keys using Yahoo Finance, you can get better data with these free APIs:

#### Metal Price API
1. Visit: https://metalpriceapi.com/
2. Sign up for free tier (1,000 requests/month)
3. Copy your API key
4. Add to `.env`: `METAL_PRICE_API_KEY=your_key`

#### Commodities API
1. Visit: https://commodities-api.com/
2. Sign up for free tier (100 requests/month)
3. Copy your API key
4. Add to `.env`: `COMMODITIES_API_KEY=your_key`

## How It Works

### Price Scraping Flow

```
1. Check cache (5-minute validity)
   ↓
2. If cache invalid, fetch from sources:
   - Try Yahoo Finance (primary)
   - Try Metal Price API (if key provided)
   - Try Commodities API (if key provided)
   - Try web scraping (backup)
   ↓
3. If all fail, use fallback prices with variation
   ↓
4. Update cache and database
   ↓
5. Trigger forecasts and alerts
```

### Data Sources Priority

1. **Yahoo Finance** (Free, no API key needed)
   - Copper: HG=F (Copper Futures)
   - Aluminum: ALI=F (Aluminum Futures)
   - Steel: MT (ArcelorMittal stock as proxy)

2. **Metal Price API** (Optional, requires key)
   - Direct metal prices in USD per ton

3. **Commodities API** (Optional, requires key)
   - Comprehensive commodity data

4. **Web Scraping** (Backup)
   - investing.com and other sources
   - May require updates if site structure changes

5. **Fallback** (Last resort)
   - Base prices with random variation
   - Ensures system always has data

## Usage

### Enable Real-Time Scraping

```python
# In config.py or .env
ENABLE_REAL_TIME_SCRAPING = True
```

### Disable Real-Time Scraping

```python
# Falls back to simulated updates
ENABLE_REAL_TIME_SCRAPING = False
```

### Test the Scraper

Run the scraper module directly:

```bash
python -m utils.price_scraper
```

Output:
```
Fetching real-time commodity prices...

Current Prices:
Copper: $8543.21 per ton
Aluminum: $2387.45 per ton
Steel: $812.33 per ton

Generated 90 records
```

## API Endpoints

### Check Scraping Status

```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-10-15T17:30:00",
  "last_update": "2024-10-15T17:25:00",
  "last_scrape": "2024-10-15T17:29:45",
  "scraping_enabled": true
}
```

### Get Current Prices

```bash
GET /api/prices/current
```

Response includes `source` field:
```json
{
  "prices": [
    {
      "material": "Copper",
      "price": 8543.21,
      "source": "Real-time Market Data",
      "change_24h": -1.2
    }
  ]
}
```

## Caching Strategy

- **Cache Duration**: 5 minutes
- **Purpose**: Reduce API calls and avoid rate limiting
- **Behavior**: 
  - First request fetches fresh data
  - Subsequent requests within 5 minutes use cache
  - After 5 minutes, fetches fresh data again

## Error Handling

### Scraping Failures

The system handles failures gracefully:

1. **Network Error**: Retries with backup sources
2. **API Rate Limit**: Uses cache or fallback
3. **Invalid Data**: Validates and rejects bad data
4. **Complete Failure**: Falls back to simulated updates

### Logging

All scraping activities are logged:

```
[17:30:00] Scraping real-time prices...
✓ Real-time prices updated successfully

[17:35:00] Scraping real-time prices...
✗ Error scraping prices: Connection timeout
  Falling back to simulated update...
```

## Performance Considerations

### API Rate Limits

- **Yahoo Finance**: No official limit, but be respectful
- **Metal Price API**: 1,000 requests/month (free tier)
- **Commodities API**: 100 requests/month (free tier)

### Optimization Tips

1. **Increase Cache Duration**: Reduce API calls
   ```python
   scraper.cache_duration = 600  # 10 minutes
   ```

2. **Increase Scraping Interval**: Less frequent updates
   ```env
   SCRAPING_INTERVAL=600  # 10 minutes
   ```

3. **Use API Keys**: Better reliability and data quality

## Troubleshooting

### Issue: Prices Not Updating

**Solution**:
1. Check `ENABLE_REAL_TIME_SCRAPING=true` in `.env`
2. Verify internet connection
3. Check logs for error messages
4. Test scraper: `python -m utils.price_scraper`

### Issue: API Rate Limit Exceeded

**Solution**:
1. Increase `SCRAPING_INTERVAL` to 600 or higher
2. Use multiple API keys (rotate them)
3. Rely on Yahoo Finance (no rate limit)

### Issue: Inaccurate Prices

**Solution**:
1. Add API keys for better data sources
2. Verify material mapping in scraper
3. Check if futures prices need conversion

### Issue: Scraping Takes Too Long

**Solution**:
1. Reduce timeout values
2. Disable slow sources
3. Increase cache duration

## Advanced Configuration

### Custom Price Sources

Add your own data sources by extending the scraper:

```python
# In utils/price_scraper.py

def _get_custom_api_price(self, material: str) -> Optional[float]:
    """Fetch from your custom API"""
    url = f"https://your-api.com/prices/{material}"
    response = self.session.get(url)
    return response.json()['price']
```

### Material Mapping

Customize how materials map to data sources:

```python
# In utils/price_scraper.py

MATERIAL_SYMBOLS = {
    'Copper': 'HG=F',
    'Aluminum': 'ALI=F',
    'Steel': 'MT',
    'Gold': 'GC=F',  # Add new materials
    'Silver': 'SI=F'
}
```

## Best Practices

1. **Always Enable Fallback**: Ensures system reliability
2. **Use Caching**: Reduces API calls and improves performance
3. **Monitor Logs**: Track scraping success/failure rates
4. **Test Regularly**: Verify data sources are still working
5. **Update Selectors**: Web scraping may break if sites change
6. **Respect Rate Limits**: Don't scrape too frequently
7. **Use API Keys**: Better data quality and reliability

## Future Enhancements

Potential improvements for the scraping system:

- [ ] Support for more materials (Gold, Silver, Platinum, etc.)
- [ ] Integration with Bloomberg API
- [ ] Machine learning for price validation
- [ ] Distributed scraping across multiple servers
- [ ] Real-time WebSocket connections
- [ ] Historical data backfilling
- [ ] Price anomaly detection
- [ ] Multi-currency support

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys periodically
- Monitor API usage to detect unauthorized access
- Use HTTPS for all API calls

## Support

For issues or questions:
1. Check logs in console output
2. Review this guide
3. Test individual components
4. Check API provider status pages
5. Verify network connectivity

---

**Last Updated**: October 2024  
**Version**: 1.0.0
