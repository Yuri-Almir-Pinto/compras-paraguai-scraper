from extractors.base_page_list import BasePageList
from extractors.product import Product
from extractors.standard import ScrapingException, InvalidElementException
import pandas as pd
import streamlit as st
import time

def main():
    url = ""
    clicked_resgatar = False
        
    with st.container(border=True):
        col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        
        with col1:
            url = st.text_input("Page URL", "")
        with col2:
            clicked_resgatar = st.button("Resgatar")
        
    page_list = BasePageList.restore(url)
    
    try:
        if clicked_resgatar:
            with st.spinner("Resgatando dados..."):
                page_list = BasePageList(url)
                page_list.set_all_product_details()
                page_list.save()
    except ScrapingException or InvalidElementException as e:
        st.error(f"Erro ao resgatar dados. O site providenciado não é uma página válida do Compras Paraguai. \nErro: {e}")
        return
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return
    
    if page_list is None:
        st.warning("Nenhum dado guardado encontrado para essa URL foi encontrado. Por favor, digite uma URL e clique em 'Resgatar'. ")
        return
    
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

if __name__ == "__main__":
    main()