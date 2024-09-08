from extractors.base_page_list import BasePageList
from extractors.product import Product
import pandas as pd

if __name__ == "__main__":
    import streamlit as st
    
    url = st.text_input("Page URL", "")
    st.divider()
    page_list = BasePageList.restore("https://www.comprasparaguai.com.br/tablet--samsung/")
    
    items = {
        "key": [],
        "value": []
    }
    
    for key, value in page_list.all_details.items():
        items["key"].append(key)
        items["value"].append("")
    
    df = pd.DataFrame(items)
    
    edited_df = st.data_editor(df, 
                               column_config= {
                                      "key": st.column_config.TextColumn("Propriedade", width="small", disabled=True),
                                      "value": st.column_config.TextColumn("Valor", width="large")
                               },
                               width=10000
                               )
    
    to_search: dict[str, str] = {}
    
    for i, row in edited_df.iterrows():
        if row["value"] != "":
            to_search[row["key"]] = row["value"]
        
    to_show: list[Product] = []      
    
    for page in page_list:
        for product in page.product_list:
            if all(key in product.details and value.lower() in product.details[key].lower() for key, value in to_search.items()):
                to_show.append(product)
    
    for product in to_show:
        st.write(f"Name: {product.name}, url: {product.page_url}")