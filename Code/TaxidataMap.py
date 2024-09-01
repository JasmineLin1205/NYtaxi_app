import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def show_taxidata_map():
    # 创建区域选择框
    region_options = {
        "布魯克林": "brooklyn",
        "曼哈頓": "manhattan",
        "皇后區": "queens",
        "布朗克斯": "bronx",
        "史泰登島": "statenisland"
    }

    # 在侧边栏中选择区域和上下半年
    selected_region = st.sidebar.selectbox("選擇區域", list(region_options.keys()))
    selected_half_year = st.sidebar.selectbox('選擇要看上/半年', ['上半年', '下半年'])
    file_prefix = region_options[selected_region].lower().replace(" ", "_")
    # 根据选择加载相应的数据
    if selected_half_year == '上半年':
        data_file =  f"{file_prefix}_taxi_data_123456.csv"
    else:
        data_file = f"{file_prefix}_taxi_data_789101112.csv"
    
    st.subheader(f'{selected_region} - {selected_half_year} 熱點分析')

    # 加载第一个数据块
    chunk_size = 1000000  # 设置每块的大小
    chunks = pd.read_csv(data_file, low_memory=False, chunksize=chunk_size)
    taxi_df = next(chunks)
    start_time = st.selectbox("選擇時段:", [datetime.time(i, 0) for i in range(24)], format_func=lambda x: x.strftime("%H:%M"))
    end_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(hours=1)).time()
    # 根据用户选择的区域筛选数据
    selected_taxi_df = taxi_df[taxi_df['pickup_datetime'] == selected_region]
    taxi_df['pickup_datetime'] = pd.to_datetime(taxi_df['pickup_datetime']).dt.time
    selected_taxi_df = taxi_df[(taxi_df['pickup_datetime'] >= start_time) & (taxi_df['pickup_datetime'] < end_time)]

    # 获取选中区域的中心坐标
    region_coordinates = {
        "brooklyn": {"lat": 40.7024, "lon": -73.9870},#布魯克林大橋附近
        "manhattan": {"lat": 40.7831, "lon": -73.9712},#第81街自然历史博物馆"。这是美国纽约市一家著名的自然历史博物馆
        "queens": {"lat": 40.76225, "lon": -73.92563},#皇后区的百老汇"。Broadway 是一条著名的大街或街道名
        "bronx": {"lat": 40.8318, "lon": -73.9236},#布朗克斯科学博物馆（The Bronx Museum of the Arts，一家致力于现代和当代艺术的博物馆，提供各种艺术展览和文化活动
        "statenisland": {"lat": 40.6023, "lon": -74.06343}#史泰登岛快速公路"。这是一条位于纽约市的公路，通常用于连接史泰登岛（Staten Island）与其他纽约市区域
    }
    
    mapbox_center = region_coordinates.get(region_options[selected_region], {"lat": 40.7024, "lon": -73.9870})

    # 创建密度热图
    fig = px.density_mapbox(selected_taxi_df, lat='pickup_latitude', lon='pickup_longitude', radius=12, color_continuous_scale='Jet')
    # 調整圖表的大小
    fig.update_traces(zmin=0, zmax=2)
    fig.update_layout(width=1440, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox_center=mapbox_center)  # 设置地图中心
    fig.update_layout(mapbox_zoom=15)
    fig.update_layout(coloraxis_colorbar=dict(title="Density"))
    fig.update_layout(title="上車地點密度熱圖", title_font_size=16)

    # 调整透明度
    fig.update_traces(opacity=0.8)

    # 显示热图
    st.plotly_chart(fig, use_container_width=False)

    #下車地點密度熱圖
    # 根据用户选择的时间范围筛选数据
    taxi_df['dropoff_datetime'] = pd.to_datetime(taxi_df['dropoff_datetime']).dt.time
    selected_taxi_df = taxi_df[(taxi_df['dropoff_datetime'] >= start_time) & (taxi_df['dropoff_datetime'] < end_time)]

    # 获取选中区域的中心坐标
    region_coordinates = {
        "brooklyn": {"lat": 40.7024, "lon": -73.9870},#布魯克林大橋附近
        "manhattan": {"lat": 40.7831, "lon": -73.9712},#第81街自然历史博物馆"。这是美国纽约市一家著名的自然历史博物馆
        "queens": {"lat": 40.76225, "lon": -73.92563},#皇后区的百老汇"。Broadway 是一条著名的大街或街道名
        "bronx": {"lat": 40.8318, "lon": -73.9236},#布朗克斯科学博物馆（The Bronx Museum of the Arts，一家致力于现代和当代艺术的博物馆，提供各种艺术展览和文化活动
        "statenisland": {"lat": 40.6023, "lon": -74.06343}#史泰登岛快速公路"。这是一条位于纽约市的公路，通常用于连接史泰登岛（Staten Island）与其他纽约市区域
    }
    
    mapbox_center = region_coordinates.get(region_options[selected_region], {"lat": 40.7024, "lon": -73.9870})

    # 创建密度热图
    fig = px.density_mapbox(selected_taxi_df, lat='dropoff_latitude', lon='dropoff_longitude', radius=18, color_continuous_scale='Jet')
    # 調整圖表的大小
    fig.update_traces(zmin=0, zmax=2)
    fig.update_layout(width=1440, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox_center=mapbox_center)  # 设置地图中心
    fig.update_layout(mapbox_zoom=15)
    fig.update_layout(coloraxis_colorbar=dict(title="Density"))
    fig.update_layout(title="下車地點密度熱圖", title_font_size=16)

    # 调整透明度
    fig.update_traces(opacity=0.8)

    # 显示热图
    st.plotly_chart(fig, use_container_width=False)