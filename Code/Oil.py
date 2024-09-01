import streamlit as st
import requests
from bs4 import BeautifulSoup

def show_oil():

    # 指定URL获取石油价格的功能
    def scrape_oil_prices(oil_type):
        url = 'https://www2.moeaea.gov.tw/oil111'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            grid_tab_contents = soup.select('div.grid_tab_content')
            oil_prices = []

            for content in grid_tab_contents:
                ul_element = content.find('ul', class_='cont_18')
                if ul_element:
                    li_elements = ul_element.find_all('li')
                    for li in li_elements:
                        strong_element = li.find('div', class_='col-4')
                        if strong_element and oil_type in strong_element.text.strip():
                            price = li.find('div', class_='col-5 text-center').find('strong').text.strip()
                            oil_prices.append(price)

            return oil_prices

    # Streamlit UI
    st.subheader('油資查詢')

    # 用户输入石油类型
    oil_type = st.text_input('請輸入要查詢的石油類型（例如：92、95、98）', '92')

    # 用户输入距离和油耗
    #汽车费用 = (距离 / 100) * 油耗 * 油价
    
    container = st.container()

    with container:
        col1, col2 = st.columns(2)
        with col1:
            distance = st.number_input('請輸入行駛的距離（km）', value=0.0)
        with col2:
            fuel_efficiency = st.number_input('請輸入汽車的油耗（km/L）', value=0.0)

    if st.button('計算'):
        oil_prices = scrape_oil_prices(oil_type)
        if oil_prices:
            price_per_liter = float(oil_prices[0])  # 假设只查询到一个价格
            total_cost = (distance / 100) * fuel_efficiency * price_per_liter
            st.write(f"{oil_type} 石油價格: {price_per_liter} 元/公升")
            st.write(f"預計的油資為: {total_cost:.2f} 元")
        else:
            st.write('未找到相关石油價格数据或出现错误。')
