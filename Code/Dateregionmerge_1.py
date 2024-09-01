import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

def show_date_region_merge():
    
    st.subheader("紐約區域的區域收入")
    
    @st.cache_data
    def load_data(file_path, columns_to_load):
        data = pd.read_csv(file_path, usecols=columns_to_load, parse_dates=["pickup_datetime"])
        return data
    
    col1, col2 = st.columns(2)
    
    # 创建日期选择器
    with col1:
        start_date = st.date_input("選擇開始日期", datetime(2013, 1, 1))
    
    with col2:
        end_date = st.date_input("選擇結束日期", datetime(2013, 1, 31))
    
    # 创建区域选择框
    region_options = {
        "布魯克林": "brooklyn",
        "曼哈頓": "manhattan",
        "皇后區": "queens",
        "布朗克斯": "bronx",
        "史泰登島": "statenisland"
    }
    
    col3, col4 = st.columns(2)
    with col3:
        selected_region = st.selectbox("選擇區域", list(region_options.keys()))
    
    # 根据用户选择的区域加载社区数据
    if selected_region == "布魯克林":
        community_options = {
            "布魯克林 - 布魯克林高地": "brooklyn_heights_data.csv",
            "布魯克林 - 威廉斯堡": "brooklyn_williamsburg_data.csv",
            "布魯克林 - 布希威克": "brooklyn_bushwick_data.csv",
            "布魯克林 - 格林角": "brooklyn_greenpoint_data.csv",
            "布魯克林 - 紐約大學布魯克林分校": "brooklyn_nyu_brooklyn_data.csv",
            "布魯克林 - 布希威克": "brooklyn_bushwick_data.csv",
            "布魯克林 - 帕克斯洛普": "brooklyn_park_slope_data.csv",
            "布魯克林 - 布魯克林海軍造船廠": "brooklyn_navy_yard_data.csv",
            "布魯克林 - 布萊頓海灘": "brooklyn_brighton_beach_data.csv",
            "布魯克林 - 康尼島": "brooklyn_coney_island_data.csv",
            "布魯克林 - 奧爾加德公園": "brooklyn_prospect_park_data.csv"
        }
        show_total_income = st.checkbox("顯示總收入")  # 在此处定义 show_total_income
    elif selected_region == "曼哈頓":
        community_options = {
            "曼哈頓 - 上西區": "manhattan_upper_east_side_data.csv",
            "曼哈頓 - 上東區": "manhattan_upper_west_side_data.csv",
            "曼哈頓 - 華盛頓高地": "manhattan_washington_heights_data.csv",
            "曼哈頓 - 蘇豪區": "manhattan_soho_data.csv",
            "曼哈頓 - 中城": "manhattan_midtown_data.csv",
            "曼哈頓 - 哈莱姆": "manhattan_harlem_data.csv",
            "曼哈頓 - 格林尼治村": "manhattan_greenwich_village_data.csv",
            "曼哈頓 - 金融區": "manhattan_financial_district_data.csv",
            "曼哈頓 - 東村": "manhattan_east_village_data.csv",
            "曼哈頓 - 蓮花區": "manhattan_chinatown_data.csv"
        }
    
        show_total_income = st.checkbox("顯示總收入") 
    elif selected_region == "皇后區":
        community_options = {
            "皇后區 - 阿斯托利亞": "queens_astoria_data.csv",
            "皇后區 - 長島城": "queens_long_island_city_data.csv",
            "皇后區 - 班霍斯特": "queens_bayside_data.csv",
            "皇后區 - 法拉盛": "queens_far_rockaway_data.csv",
            "皇后區 - 法拉盛": "queens_flushing_data.csv",
            "皇后區 - 杰克遜高地": "queens_jackson_heights_data.csv",
            "皇后區 - 基瓦納": "queens_kew_gardens_data.csv",
            "皇后區 - 皇后村": "queens_queens_village_data.csv",
            "皇后區 - 里士滿山": "queens_richmond_hill_data.csv",
            "皇后區 - 惠特斯通": "queens_whitestone_data.csv",
        }
    
        show_total_income = st.checkbox("顯示總收入") 
    elif selected_region == "布朗克斯":
        community_options = {
            "布朗克斯 - 奧斯汀街": "bronx_austin_street_data.csv",
            "布朗克斯 - 南布朗克斯": "bronx_south_bronx_data.csv",
            "布朗克斯 - 布朗克斯河": "bronx_bronx_river_data.csv",
            "布朗克斯 - 福德漢姆": "bronx_fordham_data.csv",
            "布朗克斯 - 莫瑞森尼亞": "bronx_morrisania_data.csv",
            "布朗克斯 - 北布朗克斯": "bronx_north_bronx_data.csv",
            "布朗克斯 - 河谷": "bronx_riverdale_data.csv",
            "布朗克斯 - 西布朗克斯": "bronx_west_bronx_data.csv",
            "布朗克斯 - 西班牙哈林": "bronx_spanish_harlem_data.csv"
        }
        show_total_income = st.checkbox("顯示總收入") 
    elif selected_region == "史泰登島":
        community_options = {
            "史泰登島 - 北岸": "statenisland_north_shore_data.csv",
            "史泰登島 - 安納代爾": "staten_island_annadale_data.csv",
            "史泰登島 - 克利夫頓": "staten_island_clifton_data.csv",
            "史泰登島 - 東根山": "staten_island_dongan_hills_data.csv",
            "史泰登島 - 東岸": "staten_island_east_shore_data.csv",
            "史泰登島 - 艾爾廷維爾": "staten_island_eltingville_data.csv",
            "史泰登島 - 格拉斯米爾": "staten_island_grasmere_data.csv",
            "史泰登島 - 格里特基爾斯": "staten_island_great_kills_data.csv",
            "史泰登島 - 休谢诺特": "staten_island_huguenot_data.csv",
            "史泰登島 - 米德蘭海灘": "staten_island_midland_beach_data.csv",
            "史泰登島 - 羅斯維爾": "staten_island_rossville_data.csv",
            "史泰登島 - 聖喬治": "staten_island_st_george_data.csv",
            "史泰登島 - 斯台普頓": "staten_island_stapleton_data.csv",
            "史泰登島 - 湯普金斯維爾": "staten_island_tompkinsville_data.csv",
            "史泰登島 - 托滕維爾": "staten_island_tottenville_data.csv"
        }
    
        show_total_income = st.checkbox("顯示總收入") 
    else:
        community_options = {}
    
    # 在用户选择区域后再显示社区选择框
    with col4:
       selected_community = st.multiselect("選擇社區", list(community_options.keys()))
    
    # 构建文件路径根据用户选择的区域和时间段
    file_prefix = region_options[selected_region].lower().replace(" ", "_")
    file_h1 = f"{file_prefix}_taxi_data_123456.csv"
    file_h2 = f"{file_prefix}_taxi_data_789101112.csv"
    
    # 选择要加载的列
    columns_to_load = ["pickup_datetime", "trip_distance"]
    
    # 加载数据
    data_h1 = load_data(file_h1, columns_to_load)
    data_h2 = load_data(file_h2, columns_to_load)
    
    # 根据日期范围筛选数据
    filtered_data_h1 = data_h1[(data_h1["pickup_datetime"].dt.date >= start_date) & (data_h1["pickup_datetime"].dt.date <= end_date)]
    filtered_data_h2 = data_h2[(data_h2["pickup_datetime"].dt.date >= start_date) & (data_h2["pickup_datetime"].dt.date <= end_date)]
    
    # 计算两个数据集的收入总和
    total_income_h1 = filtered_data_h1["trip_distance"].sum()
    total_income_h2 = filtered_data_h2["trip_distance"].sum()
    
    # 美元兑台币的汇率
    usd_to_twd_exchange_rate = 31.92
    
    # 计算总收入并将其转换为台币，并保留小数点后一位
    combined_total_income_usd = round(total_income_h1 + total_income_h2, 1)
    combined_total_income_twd = round(combined_total_income_usd * usd_to_twd_exchange_rate, 1)
    
    # 显示社区收入（美元和台币，保留小数点后一位）
    if selected_community:
        st.write(f"{selected_region} 在所選日期範圍內的社區收入：")
        community_table_data = []  # 创建一个空列表来存储表格数据
        for community in selected_community:
            community_file = community_options[community]
            community_data = pd.read_csv(community_file, usecols=columns_to_load, parse_dates=["pickup_datetime"])
            # 确保 "pickup_datetime" 列包含日期时间数据
            community_data["pickup_datetime"] = pd.to_datetime(community_data["pickup_datetime"], errors='coerce')
    
            # 删除无效日期时间值（如果有的话）
            community_data = community_data.dropna(subset=["pickup_datetime"])
    
            # 然后再进行筛选
            community_filtered_data = community_data[(community_data["pickup_datetime"].dt.date >= start_date) & (community_data["pickup_datetime"].dt.date <= end_date)]
    
            community_income_usd = community_filtered_data["trip_distance"].sum()
            community_income_twd = community_income_usd * usd_to_twd_exchange_rate
            
            # 将数据添加到表格数据列表中
            community_table_data.append([community, f"{community_income_twd:.1f} 台幣", f"{community_income_usd:.1f} 美元"])
            
            #st.write(f"{community}： {community_income_twd:.1f} 台幣 ({community_income_usd:.1f} 美元)")
        
        
        # 计算每列的总和并添加到表格的最后一行
        total_twd = sum(float(row[1].split()[0]) for row in community_table_data)  # 台幣
        total_usd = sum(float(row[2].split()[0]) for row in community_table_data)  # 美元
        
    
        # 添加总计行
        community_table_data.append(['總計', f'{total_twd:.1f} 台幣', f'{total_usd:.1f} 美元'])
        
        
        # 计算平均收入
        if start_date and end_date:
            selected_days = (end_date - start_date).days + 1  # 计算选定的天数
    
            for row in community_table_data:
                region = row[0]
                twd_income = float(row[1].split()[0])
                usd_income = float(row[2].split()[0])
        
                average_twd = twd_income / selected_days
                average_usd = usd_income / selected_days
        
                row.append(f'{average_twd:.1f} 台幣/天')
                row.append(f'{average_usd:.1f} 美元/天')
                
            average_twd = total_twd / selected_days
            average_usd = total_usd / selected_days    

        # 使用st.table()显示带有平均收入的表格
        st.table(pd.DataFrame(community_table_data, columns=["區域", "台幣總和", "美元總和", "平均台幣/天", "平均美元/天"]))
        
        # 顯示平均收入
        #st.write(f"平均收入：{average_twd:.1f} 台幣 / {average_usd:.1f} 美元（每天）")
        
        # 顯示總收入
        if show_total_income:
            st.write(f"{selected_region} 在所選日期範圍內的總收入（台幣）：", combined_total_income_twd, "台幣")
            st.write(f"{selected_region} 在所選日期範圍內的總收入（美元）：", combined_total_income_usd, "美元")
            
        
        # 移除總計行
        community_table_data = community_table_data[:-1]
        
       
        # 设置字体参数为微軟正黑體
        plt.rcParams['font.family'] = 'Microsoft JhengHei'

        # 提取区域、平均台币
        regions = [row[0] for row in community_table_data]
        average_twd = [int(float(row[2].split()[0])) for row in community_table_data]

        # 动态生成颜色和推出程度
        colors = plt.cm.Oranges(np.linspace(0, 1, len(average_twd)))  # 生成颜色
        explode = [0.1] * len(average_twd)  # 生成推出程度

        # 创建一个新的图表
        fig, ax = plt.subplots(figsize=(4, 4))
        

        # 绘制圆饼图，将labels参数设置为空字符串，保留autopct参数以显示百分比
        wedges, _, autotexts = ax.pie(
            average_twd,
            labels=[''] * len(regions),  # 设置为空字符串，移除中文字标签
            autopct='%1.1f%%',  # 显示百分比标签
            startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            textprops=dict(size=18),  # 设置百分比标签的字体大小
            colors=colors,
            explode=explode
        )
        
        # 调整百分比标签的位置
        for autotext in autotexts:
            autotext.set(size=10)  # 设置字体大小
            autotext.set_horizontalalignment('center')  # 设置水平对齐方式
            autotext.set_position((1.25 * autotext.get_position()[0], 1.25 * autotext.get_position()[1]))  # 设置位置偏移

        # 添加自定义图例
        legend_labels = [f"{region}: {twd} 美元" for region, twd in zip(regions, average_twd)]
        ax.legend(wedges, legend_labels, title="區域", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # 显示图表
        st.pyplot(fig)

