import pandas as pd

def sku_check_stock(row: pd.Series) -> str:

    stock_for_product = row['stock_for_product']
    promotion_stock = row['promotion_stock']

    if stock_for_product == -1:
        return "info not complete"
    
    if stock_for_product == 0:
        return "OOS"
    
    if stock_for_product < promotion_stock:
        return "low stock"
    
    return "OK"

def sku_check_stock_price(row:pd.Series) -> str:
    current_stock = row['stock_for_product']
    promotion_stock = row['promotion_stock']
    current_price = row['price_for_product']
    promotion_price= row['promotion_price']
    
    if current_price == -1 or current_stock == -1:
        return "info not complete"

    if current_stock == 0:
        return "OOS"
    elif current_stock > promotion_stock and current_price > promotion_price:
        return "OK"
    elif current_stock < promotion_stock and current_price > promotion_price:
        return "low stock"
    elif current_stock > promotion_stock and current_price < promotion_price:
        return "fail_op"
    elif current_stock < promotion_stock and current_price < promotion_price:
        return "low stock, fail_op"
    else:
        return "unknow"