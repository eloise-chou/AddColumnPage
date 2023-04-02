"""
API tool for collection stocks for shopee.

"""

import requests as rq
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger('Shopee_API')
API_URL = "https://shopee.com.my/api/v4/product/get_purchase_quantities_for_selected_model"


def wait_for_some_second(sec :float = 1.0):
    def fn_decorator(fn):
        def waited_function(*args, **kargs):
            import time 
            time.sleep(sec)
            print(f"Dealing with ID = {kargs.get('model_id', None)}")
            result = fn(*args, **kargs)
            return result
        return waited_function
    return fn_decorator


def get_param_dict(item_id:int , model_id:int , shop_id:int) :
    """    
    Returns a dictionary with keys 'itemId', 'modelId', 'shopId' and
    their corresponding integer values.
    """
    return dict(itemId=item_id, modelId = model_id, shopId=shop_id)

def get_shopee_api_dict(params) -> Dict[str, Any]:
    """    
    Returns a dictionary with data obtained from a GET request to Shopee
    API using the provided parameters.
    """
    my_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    req = rq.get(API_URL, params=params, headers=my_headers)
    return req.json()

def get_normal_stock_from_dict(shopee_api_return_dict:Dict[str, Any]) -> int:
    """    
    Returns the value associated with the 'normal_stock' key from the
    provided Shopee API response dictionary.
    """
    try:
        return shopee_api_return_dict['normal_stock']
    except KeyError as ke:
        raise ke
    
def get_display_price_from_dict(shopee_api_return_dict:Dict[str, Any]) -> int:
    """    
    Returns the value associated with the 'display_price' key from the
    provided Shopee API response dictionary.
    """
    try:
        return shopee_api_return_dict['selected_price_and_stock']['display_price']
    except KeyError as ke:
        raise ke

@wait_for_some_second(sec = 1)
def get_normal_stock_price(item_id:int , model_id:int , shop_id:int) -> Tuple[int, int]:
    """
    Returns the value of the 'normal_stock' key from the Shopee API response
    dictionary obtained using the provided
    item_id, model_id, and shop_id parameters.
    """
    params = get_param_dict(item_id , model_id , shop_id)
    request_dict = get_shopee_api_dict(params=params)
    try:
        normal_stock_q = get_normal_stock_from_dict(request_dict)
        display_price = get_display_price_from_dict(request_dict)
                                         #/100000 because the orig price is somehow bluffed
        return normal_stock_q, display_price /100_000
    except KeyError as ke:
        logger.warning(f"Model Info {params} has no 'normal_stock' key!")
