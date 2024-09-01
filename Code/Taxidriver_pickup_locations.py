import streamlit as st
import pandas as pd
import folium
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import datetime 
from datetime import datetime, timedelta

def show_taxidriver_pickup():

    st.subheader("人流聚集地")
    # 读取CSV文件
    @st.cache_data
    def load_data(file_path, columns_to_load):
        data = pd.read_csv(file_path, usecols=columns_to_load)
        return data

    # 创建一个字典，将月份名称映射到对应的文件名
    month_data_files = {
        "1月": "trip_data_1.csv",
        "2月": "trip_data_2.csv",
        "3月": "trip_data_3.csv",
        "4月": "trip_data_4.csv",
        "5月": "trip_data_5.csv",
        "6月": "trip_data_6.csv",
        "7月": "trip_data_7.csv",
        "8月": "trip_data_8.csv",
        "9月": "trip_data_9.csv",
        "10月": "trip_data_10.csv",
        "11月": "trip_data_11.csv",
        "12月": "trip_data_12.csv"
    }

    col1, col2 = st.columns(2)
    with col1:
        # 添加一个下拉菜单以选择月份
        selected_month = st.selectbox("選擇要顯示的月份", list(month_data_files.keys()))
    with col2:
        # 添加星期选择框
        selected_weekday = st.selectbox("選擇星期", ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"])

    # 创建一个时间选择框，以小时为单位
    selected_time = st.slider("選擇時間", 0, 23, 0, step=1)

    # 将选定的时间转换为 datetime 对象
    selected_datetime = datetime.now().replace(hour=selected_time, minute=0, second=0)

    # 显示选定的时间
    st.write(f"你選擇時間是：{selected_datetime.strftime('%H:%M')}")

    # 构建月份数据文件路径
    month_data_file = month_data_files[selected_month]

    # 根据月份选择相应的列名，保持列名前导空格
    if selected_month in ["1月", "2月"]:
        columns_for_clustering = ["pickup_latitude", "pickup_longitude"]
    else:
        columns_for_clustering = [" pickup_latitude", " pickup_longitude"]

    # 加载选择月份的数据并选择前2000个样本（根据需要调整）
    data = pd.read_csv(month_data_file, usecols=columns_for_clustering)

    sample_data = data.head(2000)

    # 根据区域设置不同的DBSCAN参数
    region_dbscan_params = {
        "布魯克林": {"eps": 1.0, "min_samples": 10},
        "曼哈頓": {"eps": 1.5, "min_samples": 20},
        "布朗克斯": {"eps": 0.8, "min_samples": 10},
        "皇后區": {"eps": 1.2, "min_samples": 8},
        "史泰登島": {"eps": 0.1, "min_samples": 2}
    }

    # 添加一个下拉菜单以选择区域
    selected_region = st.selectbox("選擇想看的區域", list(region_dbscan_params.keys()))

    # 获取用户选择的区域的DBSCAN参数值
    selected_params = region_dbscan_params[selected_region]
    eps = selected_params["eps"]
    min_samples = selected_params["min_samples"]

    # 标准化纬度和经度
    scaler = StandardScaler()
    scaled_coords = scaler.fit_transform(sample_data[columns_for_clustering])

    # 使用DBSCAN算法查找簇
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    # 对DataFrame进行深度复制
    sample_data_copy = sample_data.copy()

    # 在复制的DataFrame上使用DBSCAN进行拟合和预测
    sample_data_copy["Cluster"] = dbscan.fit_predict(scaled_coords)

    # 创建一个字典，将区域映射到中心坐标
    region_coordinates = {
        "布魯克林": [40.6782, -73.9442],
        "曼哈頓": [40.7891, -73.9592],
        "布朗克斯": [40.8370, -73.8654],
        "皇后區": [40.7282, -73.7949],
        "史泰登島": [40.5795, -74.1502]
    }

    # 获取用户选择的区域的中心坐标
    selected_coords = region_coordinates[selected_region]

    # 创建以选定区域的中心坐标为中心的Folium地图
    m = folium.Map(location=selected_coords, zoom_start=13)
    

    if not sample_data_copy.empty:
        for _, row in sample_data_copy.iterrows():
            if "pickup_latitude" in data.columns:
                popup_content = f"緯度: {row['pickup_latitude']}經度: {row['pickup_longitude']}"
                folium.Marker(
                    location=(row["pickup_latitude"], row["pickup_longitude"]),
                    popup=folium.Popup(popup_content, parse_html=True),
                    icon=folium.Icon(color="blue")
                ).add_to(m)
            else:
                popup_content = f"緯度: {row[' pickup_latitude']}經度: {row[' pickup_longitude']}"
                folium.Marker(
                    location=(row[" pickup_latitude"], row[" pickup_longitude"]),
                    popup=folium.Popup(popup_content, parse_html=True),
                    icon=folium.Icon(color="blue")
                ).add_to(m)

        st.write(f"計程車聚集地點地圖（{selected_region}）：")
        m.save("map.html")
        with open("map.html", "r", encoding="utf-8") as f:
            html = f.read()

        st.components.v1.html(html, width=1440, height=600)

        # 添加一张图片

        st.image("region.jpg", caption="紐約五大區區域劃分", width=1000)

    else:
        st.write(f"找不到{selected_region}的計程車聚集地點。")

