# Placeholder adapter for eBay. OAuth and Sell API calls to be added.
from ..config import EBAY_APP_ID, EBAY_ENV

def config_ok() -> bool:
    return bool(EBAY_APP_ID)
