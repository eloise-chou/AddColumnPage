import streamlit as st
from datetime import datetime
import pandas as pd
import model.validate
from model.data_handle import df_column_to_stock_price
import model.file

### Read file
st.header("檔案上傳")
st.caption("請上傳 csv 檔。欄位請改成 shop_id, item_id, model_id,promotion_stock")
input_csv_file =  st.file_uploader("檔案：", type = 'csv', help= "請上傳 csv 檔。欄位請改成 shop_id, item_id, model_id,promotion_stock")


### Display table
if input_csv_file is not None:
    df = pd.read_csv(input_csv_file)

    st.write(df)
### Button -> Fetch and Check (Call model)
validation_option = st.selectbox(
    '檢查項目',
    ('庫存','庫存及價格'))

validation_function_map = {
    '庫存': model.validate.sku_check_stock,
    '庫存及價格': model.validate.sku_check_stock_price
}
validation_function = validation_function_map[validation_option]

if st.button("檢查"):
    fetched_df = df.copy()

    total_num = len(fetched_df)
    df_fetch_progress_bar = st.progress(0, text="處理進度")

    for i, row in fetched_df.iterrows():
        percent_complete = (i+1) / total_num
        current_model_id = row['model_id']
        df_fetch_progress_bar.progress(percent_complete, text= f"處理進度：{current_model_id:,}" )
        stock, price = df_column_to_stock_price(row)
        print(stock)
        fetched_df.loc[i, 'stock_for_product'] = stock
        fetched_df.loc[i, 'price_for_product'] = price

        stock_status = validation_function(fetched_df.iloc[i])
        fetched_df.loc[i, 'sku_check']         = stock_status

## Display new table

    fetched_df = fetched_df.drop(fetched_df.columns[:2], axis = 1)
    fetched_df


### 下載 Logger 報告

    today_date = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    st.download_button(
        label       = "下載商品庫存檢查報告",
        data        = model.file.df_to_csv_utf8(fetched_df),
        file_name   = f"{today_date}_checked.csv",
        mime        = 'text/csv'
    )