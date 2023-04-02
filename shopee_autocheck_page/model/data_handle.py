import logging 
import pandas as pd
from typing import Tuple

from model.request import get_normal_stock_price

logger = logging.getLogger('Shopee_API')
logger.setLevel(logging.WARNING)


def df_column_to_stock_price(data: pd.Series) -> Tuple[int,int]:
    try:
        item_id     :int = data["item_id"]
        model_id    :int = data["model_id"]
        shop_id     :int = data["shop_id"] 
        item_detail = get_normal_stock_price(
            item_id     =  item_id,
            model_id    = model_id,
            shop_id     = shop_id,
        )
        return item_detail
    except Exception as e:
        logger.warning(e)
        return -1, -1


def df_create_stock_price(data: pd.Series):
    item_detail = df_column_to_stock_price(data)
    data['stock_for_product'] = item_detail[0]
    data['price_for_product'] = item_detail[1]
    return data