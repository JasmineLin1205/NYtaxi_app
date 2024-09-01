import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopy.distance
import requests
import googlemaps
from geopy.distance import geodesic
import datetime

# 函式：計算行車時間
def calculate_travel_time(distance_in_km):
    average_speed_kmph = 30
    travel_time_minutes = (distance_in_km / average_speed_kmph) * 60
    return travel_time_minutes

# 函式：計算距離
def calculate_distance(start_coords, end_coords):
    return geodesic(start_coords, end_coords).kilometers

# 函式：計算費用
def calculate_fare(distance_miles, time_of_day, is_weekday):
    # 基础费用
    base_fare = 4.00 if (time_of_day >= 20 or time_of_day < 6) else 3.00
    # 每英里的计程车费用
    per_mile_rate = 2.18
    # 夜间附加费
    night_surcharge = custom_night_surcharge if (time_of_day >= 20 or time_of_day < 6) else 0.0
    # 尖峰时间附加费
    peak_hour_surcharge = custom_peak_surcharge if (is_weekday and (time_of_day >= 16 and time_of_day < 20)) else 0.0
    # 计算总费用，包括基础费用、每英里费用、夜间附加费、尖峰时间附加费
    total_fare = base_fare + distance_miles * per_mile_rate + night_surcharge + peak_hour_surcharge
    # 应用时间倍率
    total_fare *= travel_time_multiplier
    # 返回计算出的总费用
    return total_fare

def show_peakoff():
    # Streamlit app
    st.subheader('行程時間計算')
    mode = st.selectbox("選擇你想要的方式", ("手動輸入經緯度", "在地圖上選擇點"))
    
    if mode == "手動輸入經緯度":
        # Define peak hours
        peak_start_morning = 7
        peak_end_morning = 9
        peak_start_evening = 17
        peak_end_evening = 19

        
        # 使用st.columns创建两列布局
        col1, col2 = st.columns(2)
        # 在第一列中放置输入控件
        with col1:
            pickup_location = st.text_input("上車地點 : 緯度, 經度")
        with col2:
            dropoff_location = st.text_input("下車地點 : 緯度, 經度")
        # 分隔线
        st.markdown("---")

        # 第二列布局
        st.markdown("**時間設定**")
        
        # 使用st.columns创建两列布局
        col3, col4 = st.columns(2)

        # 在第一列中放置输入控件
        with col3:
            current_hour = st.slider("選擇小時", min_value=0, max_value=23)
            current_minute = st.slider("選擇分鐘", min_value=0, max_value=59)
        # 在第二列中放置输入控件
        with col4:
            input_day_of_week = st.selectbox("請選擇今天是星期幾：", ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"])
            custom_peak_multiplier = st.number_input("請輸入尖峰時間的倍率", min_value=1.0, value=1.5, format="%.1f")
        pickup_time = current_hour * 60 + current_minute
        if input_day_of_week == "星期一" or input_day_of_week == "星期二" or input_day_of_week == "星期三" or input_day_of_week == "星期四" or input_day_of_week == "星期五":
            # 假设尖峰时间是早上7点到9点，下午5点到7点
            if (7 * 60 <= pickup_time <= 9 * 60) or (17 * 60 <= pickup_time <= 19 * 60):
                time_category = "尖峰时间"
                travel_time_multiplier = custom_peak_multiplier  # 使用自定义尖峰时间倍率
                #peak_surcharge = custom_peak_surcharge  # 使用自定义尖峰时间附加费
            else:
                time_category = "離峰时间"
                travel_time_multiplier = 1.0
                #peak_surcharge = 0.0
        else:
            time_category = "離峰时间"
            travel_time_multiplier = 1.0
            #peak_surcharge = 0.0

        # 创建 Folium 地图并设置中心坐标
        center_coordinates = [40.7743, -73.5940]
        
        # 创建地图
        m = folium.Map(location=center_coordinates, zoom_start=12)
        
        # 使用 FeatureGroup 存儲標記
        marker_group = folium.FeatureGroup()

        # 创建会话状态
        if 'selected_location' not in st.session_state:
            st.session_state.selected_location = []

        # 添加地图的点击事件处理程序
        def on_click_map(e):
            lat, lon = e.latlng
            st.session_state.selected_location.append((lat, lon))

            # 清除之前的标记
            marker_group.clear_layers()

            # 添加新标记
            marker = folium.Marker([lat, lon], popup=f"经度: {lon:.6f}, 纬度: {lat:.6f}")
            marker.add_to(marker_group)
            marker_group.add_to(m)

            # 显示地图
            #folium_static(m)

        # 绑定地图的点击事件
        m.add_child(marker_group)
        m.add_child(folium.LatLngPopup())
        m.add_child(folium.ClickForMarker(popup="点击选择位置"))
        # 獲取當前時間
        current_time = datetime.datetime.now()

        # 檢查當前日期是否是工作日（周一至周五）
        is_weekday = current_time.weekday() < 5
        if st.button("計算行程時間"):
            pickup_latitude, pickup_longitude = map(float, pickup_location.split(','))
            dropoff_latitude, dropoff_longitude = map(float, dropoff_location.split(','))
        
            if (40.4961 <= pickup_latitude <= 40.9155) and (-74.2655 <= pickup_longitude <= -73.6995) and \
                (40.4961 <= dropoff_latitude <= 40.9155) and (-74.2655 <= dropoff_longitude <= -73.6995):
                location_valid = True
            else:
                location_valid = False
        
            if location_valid:
                coords_1 = (pickup_latitude, pickup_longitude)
                coords_2 = (dropoff_latitude, dropoff_longitude)
                distance_km = geopy.distance.geodesic(coords_1, coords_2).kilometers
            
                pickup_time = current_hour * 60 + current_minute
                if input_day_of_week == "星期一" or input_day_of_week == "星期二" or input_day_of_week == "星期三" or input_day_of_week == "星期四" or input_day_of_week == "星期五":
                    # 假设尖峰时间是早上7点到9点，下午5点到7点
                    if (7 * 60 <= pickup_time <= 9 * 60) or (17 * 60 <= pickup_time <= 19 * 60):
                        time_category = "尖峰时间"
                        travel_time_multiplier = custom_peak_multiplier  # 使用自定义尖峰时间倍率
                        #peak_surcharge = custom_peak_surcharge  # 使用自定义尖峰时间附加费
                    else:
                        time_category = "離峰时间"
                        travel_time_multiplier = 1.0
                        #peak_surcharge = 0.0
                else:
                    time_category = "離峰时间"
                    travel_time_multiplier = 1.0
                    #peak_surcharge = 0.0
                
                distance = calculate_distance(coords_1, coords_2)

                    
                # 根據距離計算行程時間，假設每公里行駛時間為10分鐘
                travel_time_minutes = calculate_travel_time(distance) * travel_time_multiplier

                total_duration = travel_time_minutes
            
                st.write(f"上車地點：({pickup_latitude}, {pickup_longitude})")
                st.write(f"下車地點：({dropoff_latitude}, {dropoff_longitude})")
                st.write(f"現在時間：{current_hour:02d}:{current_minute:02d}")
                st.write(f"距離：{distance_km:.2f} 公里")
                st.write(f"時間分類：{time_category}")
                st.write(f"估計行車時間：{total_duration:.2f} 分鐘")
            else:
                st.warning("請輸入有效的布魯克林地點經緯度")
        # 显示地图
        folium_static(m, width=1440, height=600)
    else:
    
        google_maps_api_key = "AIzaSyDtCdXwEIN6EIAluLAozjxh9WrDLxUTbuk"
        gmaps = googlemaps.Client(key=google_maps_api_key)
        brooklyn_center = [40.6782, -73.9442]
        m = folium.Map(location=brooklyn_center, zoom_start=12, control_scale=True)

        locations = {
            #布魯克林
            "Brooklyn Bridge": (40.7061, -73.9969),
            "Prospect Park": (40.6602, -73.9690),
            "Coney Island": (40.5750, -73.9822),
            "DUMBO": (40.7033, -73.9881),
            "Williamsburg": (40.7143, -73.9618),
            "Park Slope": (40.6721, -73.9776),
            "Greenpoint": (40.7245, -73.9419),
            "Red Hook": (40.6763, -74.0094),
            "Fort Greene": (40.6912, -73.9742),
            "Ditmas Park": (40.6376, -73.9638),
            "Bay Ridge": (40.6340, -74.0239),
            "Bedford-Stuyvesant": (40.6872, -73.9418),
            "Sunset Park": (40.6454, -74.0101),
            "Windsor Terrace": (40.6539, -73.9756),
            "Gowanus": (40.6736, -73.9901),
            "Borough Park": (40.6332, -73.9966),
            "Sheepshead Bay": (40.5863, -73.9435),
            "Canarsie": (40.6350, -73.9061),
            "Marine Park": (40.6097, -73.9336),
            "Mill Basin": (40.6103, -73.9106),
            "Dyker Beach Park": (40.6072,-74.0147),
            "Washington Cemetery": (40.6369,-73.9811),
            "Holy Cross Cemetery": (40.6239,-73.9866),
            "Lincoln Terrace Park": (40.6593, -73.9257),
            "Colonel David Marcus Playground":(40.5984,-73.9619),
            "Paerdegat Park":(40.6304,-73.9310),
            "Brooklyn Museum": (40.6719, -73.9635),
            "Barclays Center": (40.6827, -73.9754),
            "Brooklyn Botanic Garden": (40.6688, -73.9652),
            "Brooklyn Navy Yard": (40.7023, -73.9709),
            "Green-Wood Cemetery": (40.6569, -73.9894),
            "Industry City": (40.6555, -74.0088),
            "Brooklyn Heights Promenade": (40.6957, -73.9974),
            #曼哈頓
            "Central Park": (40.7851, -73.9683),
            "Empire State Building": (40.7488, -73.9857),
            "Times Square": (40.7589, -73.9851),
            "Brooklyn Bridge": (40.7061, -73.9969),
            "Grand Central Terminal": (40.7527, -73.9772),
            "The Metropolitan Museum of Art": (40.7794, -73.9632),
            "One World Trade Center": (40.7128, -74.0134),
            "Statue of Liberty": (40.6892, -74.0445),
            "The High Line": (40.7471, -74.0043),
            "Museum of Modern Art (MoMA)": (40.7614, -73.9776),
            "Broadway": (40.7618, -73.9848),
            "Madison Square Garden": (40.7505, -73.9934),
            "Rockefeller Center": (40.7587, -73.9787),
            "The Museum of Natural History": (40.7813, -73.9730),
            "Chinatown": (40.7158, -73.9970),
            "Union Square": (40.7359, -73.9911),
            "Columbia University": (40.8075, -73.9626),
            "Harlem": (40.8116, -73.9465),
            "East Village": (40.7271, -73.9822),
            "West Village": (40.7358, -74.0034),
            "Washington Square Park": (40.7308, -73.9973),
            #皇后區
            "Flushing Meadows-Corona Park": (40.7469, -73.8447),
            "Queens Botanical Garden": (40.7512, -73.8287),
            "Queens Museum": (40.7454, -73.8446),
            "Astoria Park": (40.7770, -73.9248),
            "Rockaway Beach": (40.5863, -73.8113),
            "Socrates Sculpture Park": (40.7684, -73.9382),
            "Queensbridge Park": (40.7558, -73.9465),
            "Gantry Plaza State Park": (40.7460, -73.9576),
            "Jamaica Bay Wildlife Refuge": (40.6154, -73.8314),
            "Forest Park": (40.7007, -73.8655),
            "Queens Center Mall": (40.7367, -73.8743),
            "Flushing Chinatown": (40.7587, -73.8321),
            "Queens College": (40.7365, -73.8204),
            "Astoria Ditmars": (40.7751, -73.9121),
            "Queensboro Bridge": (40.7553, -73.9507),
            "St. John's University": (40.7214, -73.7955),
            "JFK Airport": (40.6413, -73.7781),
            #布朗克斯
            "Bronx Zoo": (40.8505, -73.8785),
            "New York Botanical Garden": (40.8618, -73.8800),
            "Bronx Museum of the Arts": (40.8317, -73.9223),
            "Yankee Stadium": (40.8296, -73.9262),
            "Wave Hill": (40.8977, -73.9124),
            "Arthur Avenue (Little Italy of the Bronx)": (40.8541, -73.8880),
            "Van Cortlandt Park": (40.8892, -73.8988),
            "The Cloisters": (40.8648, -73.9318),
            "Bronx Park": (40.8581, -73.8794),
            "Orchard Beach": (40.8522, -73.7922),
            "Bronx Community College": (40.8563, -73.9115),
            "Bronx Zoo": (40.8505, -73.8785),
            "Yankee Stadium": (40.8296, -73.9262),
            "Fordham University": (40.8612, -73.8901),
            #史泰登岛
            "Staten Island Ferry Terminal": (40.6437, -74.0726),
            "Snug Harbor Cultural Center": (40.6437, -74.1015),
            "Richmond Town": (40.5710, -74.1474),
            "Staten Island Zoo": (40.6262, -74.1164),
            "Fort Wadsworth": (40.6014, -74.0570),
            "Alice Austen House": (40.6142, -74.0636),
            "Conference House Park": (40.5053, -74.2503),
            "Wolfe's Pond Park": (40.5076, -74.2060),
            "Great Kills Park": (40.5402, -74.1252),
            "The Seguine Mansion": (40.5115, -74.2007),
            "Staten Island Mall": (40.5834, -74.1575),
            "Snug Harbor Cultural Center": (40.6437, -74.1015),
            "Staten Island Children's Museum": (40.6407, -74.0768),
            #增加的
            "The Seguine Mansion": (40.5115, -74.2007),
            "East Williamsburg Industrial Park": (40.7128, -73.9375),
            "LaGuardia Community College": (40.7465, -73.9434),
            "Saint Michael's Cemetery": (40.7005, -73.8363),
            "Edo Seaplane Base": (40.7696, -73.8945),
        }

        # 使用st.columns创建两列布局
        col1, col2 = st.columns(2)
        # 在第一列中放置输入控件
        with col1:
            # 獲取用戶輸入和計算結果
            start_location_input = st.text_input("輸入或選擇上車地點的名稱:", key="start")
            end_location_input = st.text_input("輸入或選擇下車地點的名稱:", key="end")

            # 如果用户输入了名称，尝试查找匹配的坐标
            start_coords = locations.get(start_location_input)
            end_coords = locations.get(end_location_input)
        
        # 在第二列中放置输入控件
        with col2:
            # 如果找到匹配的坐标，显示下拉菜单
            if start_coords:
                start_location = st.selectbox("選擇上車地點:", [start_location_input] + list(locations.keys()), index=0)
            else:
                start_location = st.selectbox("選擇上車地點:", list(locations.keys()))

            if end_coords:
                end_location = st.selectbox("選擇下車地點:", [end_location_input] + list(locations.keys()), index=0)
            else:
                end_location = st.selectbox("選擇下車地點:", list(locations.keys()))

        # 获取所选位置的经纬度坐标
        start_coords = locations.get(start_location, start_coords)
        end_coords = locations.get(end_location, end_coords)


        # 添加所有地点的标记
        for location, coords in locations.items():
            folium.Marker(
                location=coords,
                popup=location,
            ).add_to(m)

        # 添加起点标记（红色）
        folium.Marker(
            location=start_coords,
            popup=f"起點: {start_location}",
            icon=folium.Icon(color='red')
        ).add_to(m)

        # 添加终点标记（綠色）
        folium.Marker(
            location=end_coords,
            popup=f"终點: {end_location}",
            icon=folium.Icon(color='green')
        ).add_to(m)

        # 计算距离
        distance = calculate_distance(start_coords, end_coords)

        # 使用 Google Maps Directions API 获取路线信息
        directions = gmaps.directions(
            start_coords,
            end_coords,
            mode="walking",
            avoid=["ferries", "tolls", "indoor"],
            language="zh-TW"
        )


        # 提取路线坐标点
        route_coordinates = [
            (step["start_location"]["lat"], step["start_location"]["lng"])
            for step in directions[0]["legs"][0]["steps"]
        ]
        route_coordinates.append(
            (
                directions[0]["legs"][0]["end_location"]["lat"],
                directions[0]["legs"][0]["end_location"]["lng"],
            )
        )

        # 添加路线到地图上
        folium.PolyLine(
            locations=route_coordinates,
            color="blue",
            weight=5,
            opacity=0.7
        ).add_to(m)

        # Define peak hours
        peak_start_morning = 7
        peak_end_morning = 9
        peak_start_evening = 17
        peak_end_evening = 19
        
        # 獲取當前時間
        current_time = datetime.datetime.now()

        # 檢查當前日期是否是工作日（周一至周五）
        is_weekday = current_time.weekday() < 5
        # 分隔线
        st.markdown("---")

        # 第二列布局
        st.markdown("**時間設定**")
        col3, col4 = st.columns(2)

        # 在第一列中放置时间选择控件
        with col3:
 
            current_hour = st.slider("請選擇現在時間(幾時)", min_value=0, max_value=23)
            current_minute = st.slider("請選擇現在時間(幾分)", min_value=0, max_value=59)

        # 在第二列中放置其他时间控件
        with col4:
            input_day_of_week = st.selectbox("請選擇今天是星期幾：", ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"])
            custom_peak_multiplier = st.number_input("請輸入尖峰時間的倍率", min_value=1.0, value=1.5, format="%.1f")
        pickup_time = current_hour * 60 + current_minute
        if input_day_of_week == "星期一" or input_day_of_week == "星期二" or input_day_of_week == "星期三" or input_day_of_week == "星期四" or input_day_of_week == "星期五":
            # 假设尖峰时间是早上7点到9点，下午5点到7点
            if (7 * 60 <= pickup_time <= 9 * 60) or (17 * 60 <= pickup_time <= 19 * 60):
                time_category = "尖峰时间"
                travel_time_multiplier = custom_peak_multiplier  # 使用自定义尖峰时间倍率
                #peak_surcharge = custom_peak_surcharge  # 使用自定义尖峰时间附加费
            else:
                time_category = "離峰时间"
                travel_time_multiplier = 1.0
                #peak_surcharge = 0.0
        else:
            time_category = "離峰时间"
            travel_time_multiplier = 1.0
            #peak_surcharge = 0.0
        
        # 根據距離計算行程時間，假設每公里行駛時間為10分鐘
        travel_time_minutes =  calculate_travel_time(distance)* travel_time_multiplier
        # 调用费用计算函数
        # ... （其餘的程式碼）

        # 提取路線坐標點
        # ... （其餘的程式碼）

        # 添加路線到地圖上
        # ... （其餘的程式碼）

        # 獲取當前時間並計算費用
        # ... （其餘的程式碼）
         # 调用费用计算函数计算费用
        #fare = calculate_taxi_fare(distance, current_hour, is_weekday, travel_time_multiplier, custom_night_surcharge, custom_peak_surcharge)

        # 转换美元费用为台币
        #twd_amount = round(fare * 30.585, 1)
        show_map_button = st.button("計算行程時間")

        # 显示地图
        st.components.v1.html(m._repr_html_(), height=600)
        if show_map_button:
            # 将数据整理成二维数组
            data = [
                {"項目": "上車地點", "結果": f"{start_location} ({start_coords[0]}, {start_coords[1]})"},
                {"項目": "下車地點", "結果": f"{end_location} ({end_coords[0]}, {end_coords[1]})"},
                {"項目": "現在時間", "結果": f"{current_hour:02d}:{current_minute:02d}"},
                {"項目": "距離", "結果": f"{distance:.2f} 公里"},
                {"項目": "時間分類", "結果": time_category},
                {"項目": "估計行車時間", "結果": f"{travel_time_minutes:.2f} 分鐘"},
            ]

            # 使用st.table()显示表格
            st.table(data)


   




#假設尖峰時間為平日早上 7:00 到 9:00，下午 5:00 到 7:00
#其他時間為離峰時間。