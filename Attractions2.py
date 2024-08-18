import streamlit as st
import folium
from streamlit_folium import st_folium


def show_attractions():
    
    st.subheader('觀光景點')
    
    # 創建一個 Folium 地圖
    m = folium.Map(location=[40.70876, -73.921789], zoom_start=12)

    # 初始化 FeatureGroup 用於管理地圖要素
    fg = folium.FeatureGroup(name="觀光地點")

    # 定义不同的类别颜色
    category_colors = {
        "布魯克林景點": "blue",
        "曼哈頓景點":"orange",
        "布朗克斯景點":"green",
        "皇后區景點":"purple",
        "史泰登島景點": "red",
    }

    attractions = {
        #布魯克林
        "布魯克林大橋": {
            "location": [40.706086, -73.996864],
            "description": "布魯克林大橋是紐約市的標誌性建築之一。",
            "opening_hours": "每天上午9:00 - 下午6:00",
            "ticket_price": "$10成人，$5兒童",
            "category": "布魯克林景點"
        },
        "布魯克林博物館": {
            "location": [40.671090, -73.963285],
            "description": "布魯克林博物館擁有豐富的藝術和文化收藏品。",
            "opening_hours": "週一至週五上午10:00 - 下午5:00，週末上午11:00 - 下午6:00",
            "ticket_price": "$15成人，兒童免費",
            "category": "布魯克林景點"
        },
        "布魯克林公園": {
            "location": [40.669773, -73.965355],
            "description": "這是一個美麗的公園，適合散步和放鬆。",
            "opening_hours": "每天上午6:00 - 晚上10:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "康尼島": {
            "location": [40.575544, -73.970702],
            "description": "康尼島有著美麗的海灘和娛樂設施。",
            "opening_hours": "每天上午9:00 - 下午8:00",
            "ticket_price": "$25成人，$15兒童",
            "category": "布魯克林景點"
        },
        "布魯克林高地公園": {
            "location": [40.700925, -73.995436],
            "description": "提供壯觀的城市全景。",
            "opening_hours": "每天上午8:00 - 晚上10:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "布魯克林橋公園": {
            "location": [40.704243, -73.995040],
            "description": "一個寬敞的公園，適合戶外活動。",
            "opening_hours": "每天上午6:00 - 晚上11:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "威廉斯堡": {
            "location": [40.712775, -73.964512],
            "description": "威廉斯堡是個充滿活力的社區。",
            "opening_hours": "每天上午9:00 - 下午7:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "普勒肯斯公園": {
            "location": [40.660202, -73.969583],
            "description": "一個大型城市公園，提供休閒活動。",
            "opening_hours": "每天上午8:00 - 晚上9:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "紐約水族館": {
            "location": [40.575535, -73.973361],
            "description": "一個有趣的水族館，適合家庭遊玩。",
            "opening_hours": "每天上午10:00 - 下午6:00",
            "ticket_price": "$30成人，$20兒童",
            "category": "布魯克林景點"
        },
        
        "布魯克林廣場公園": {
            "location": [40.665446, -73.962994],
            "description": "一個寧靜的公園，適合散步。",
            "opening_hours": "每天上午7:00 - 晚上10:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "布魯克林歷史社區": {
            "location": [40.699771, -73.993535],
            "description": "了解布魯克林的歷史。",
            "opening_hours": "週一至週五上午9:00 - 下午5:00，週末休息",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "布殊威克公園": {
            "location": [40.708760, -73.921789],
            "description": "一個充滿藝術的社區。",
            "opening_hours": "每天上午10:00 - 下午6:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "瓦納士特大道": {
            "location": [40.675188, -74.013942],
            "description": "瓦納士特大道有很多有趣的商店和餐廳。",
            "opening_hours": "每天上午11:00 - 晚上9:00",
            "ticket_price": "免費",
            "category": "布魯克林景點"
        },
        "紐約行動影院": {
            "location": [40.680578, -73.955120],
            "description": "紐約行動影院是一家結合電影院和餐廳的場所，提供精彩的電影和美食體驗。",
            "opening_hours": "週一至週日，上午11:00 - 晚上9:00",
            "ticket_price": "電影票價：$12起，食物價格視菜單而定",
            "category": "布魯克林景點"
        },
        #曼哈頓
        "自由女神像": {
            "location": [40.689247, -74.044502],
            "description": "自由女神像位於自由島上，是美國的象徵，禮物來自法國，象徵著自由和民主。",
            "opening_hours": "週一至週日，上午8:30 - 晚上6:30",
            "ticket_price": "船票：$19.25起",
            "category": "曼哈頓景點"
        },
        "帝國大廈": {
            "location": [40.748817, -73.985428],
            "description": "帝國大廈是曼哈頓的標誌性摩天大樓，提供壯觀的城市全景，夜晚照明華麗。",
            "opening_hours": "週一至週日，上午8:00 - 晚上2:00",
            "ticket_price": "門票：$45起",
            "category": "曼哈頓景點"
        },
        "中央公園": {
            "location": [40.785091, -73.968285],
            "description": "中央公園位於曼哈頓中心，是一個大型城市公園，提供放鬆和休閒的場所。",
            "opening_hours": "週一至週日，全天開放",
            "ticket_price": "免費入場",
            "category": "曼哈頓景點"
        },
        "時代廣場": {
            "location": [40.758896, -73.985130],
            "description": "時代廣場是紐約市的繁忙廣場，以其霓虹燈牌和繁華夜生活而聞名。",
            "opening_hours": "全天開放",
            "ticket_price": "免費入場",
            "category": "曼哈頓景點"
        },
        "大都會藝術博物館": {
            "location": [40.779436, -73.963244],
            "description": "大都會藝術博物館是世界著名的藝術博物館，收藏了各種藝術品和文物。",
            "opening_hours": "週一至週日，上午10:00 - 晚上5:30",
            "ticket_price": "建議捐款：$25",
            "category": "曼哈頓景點"
        },
        "百老匯": {
            "location": [40.759011, -73.984472],
            "description": "百老匯是世界著名的劇院區，提供多樣化的音樂劇和戲劇表演。",
            "opening_hours": "表演時間視劇場和表演而定",
            "ticket_price": "票價視劇場和表演而定",
            "category": "曼哈頓景點"
        },
        "自然歷史博物館": {
            "location": [40.781324, -73.973988],
            "description": "自然歷史博物館展示了自然歷史和文化，擁有大量的展品和恐龍骨骼。",
            "opening_hours": "週一至週日，上午10:00 - 晚上5:45",
            "ticket_price": "建議捐款：$23",
            "category": "曼哈頓景點"
        },
        "洛克菲勒中心": {
            "location": [40.758740, -73.978675],
            "description": "洛克菲勒中心包括洛克菲勒廣場、觀景台和著名的圣誕樹。",
            "opening_hours": "週一至週日，上午8:00 - 晚上12:00",
            "ticket_price": "觀景台門票：$41起",
            "category": "曼哈頓景點"
        },
        "大都會歌劇院": {
            "location": [40.772884, -73.984788],
            "description": "大都會歌劇院享有國際聲譽，提供精彩的歌劇演出。",
            "opening_hours": "表演時間視劇場和表演而定",
            "ticket_price": "票價視劇場和表演而定",
            "category": "曼哈頓景點"
        },
        "華爾街": {
            "location": [40.706877, -74.011265],
            "description": "華爾街是全球金融中心的所在地，你可以參觀紐約證券交易所和自由女神金幣。",
            "opening_hours": "週一至週五，白天開放",
            "ticket_price": "免費參觀，但金融博物館門票：$23",
            "category": "曼哈頓景點"
        },
        #布朗克斯
        "布朗克斯動物園": {
            "location": [40.850594, -73.878247],
            "description": "布朗克斯動物園是美國最大的都市動物園之一，擁有眾多動物種類。",
            "opening_hours": "週一至週日，上午10:00 - 晚上5:00",
            "ticket_price": "成人門票：$39.95",
            "category": "布朗克斯景點"
        },
        "紐約植物園": {
            "location": [40.862488, -73.877692],
            "description": "紐約植物園擁有多個花園和溫室，展示各種植物種類。",
            "opening_hours": "週一至週日，上午10:00 - 晚上6:00",
            "ticket_price": "成人門票：$28",
            "category": "布朗克斯景點"
        },
        "布朗克斯博物館": {
            "location": [40.861448, -73.883488],
            "description": "布朗克斯博物館展示了有關紐約市及其歷史的各種展品。",
            "opening_hours": "週一至週日，上午10:00 - 晚上5:00",
            "ticket_price": "成人門票：$15",
            "category": "布朗克斯景點"
        },
        "美國印第安博物館": {
            "location": [40.830191, -73.921419],
            "description": "美國印第安博物館展示了印第安各個部落的藝術和文化。",
            "opening_hours": "週一至週日，上午10:00 - 晚上5:00",
            "ticket_price": "成人門票：$25",
            "category": "布朗克斯景點"
        },
        "布朗克斯公共圖書館": {
            "location": [40.860025, -73.893027],
            "description": "布朗克斯公共圖書館提供各種圖書、活動和資源，供社區居民使用。",
            "opening_hours": "週一至週五，上午9:00 - 晚上9:00；週六，上午10:00 - 下午5:00",
            "ticket_price": "免費入場",
            "category": "布朗克斯景點"
        },
        "布朗克斯酒廠": {
            "location": [40.800947, -73.912968],
            "description": "布朗克斯酒廠是一家生產手工啤酒的酒廠，提供品酒和導覽。",
            "opening_hours": "週五，下午4:00 - 晚上7:00；週六，中午12:00 - 晚上7:00",
            "ticket_price": "品酒套餐價格視選擇而定",
            "category": "布朗克斯景點"
        },
        "布朗克斯公園": {
            "location": [40.852893, -73.860271],
            "description": "布朗克斯公園是一個大型城市公園，提供許多戶外活動和休閒設施。",
            "opening_hours": "週一至週日，全天開放",
            "ticket_price": "免費入場",
            "category": "布朗克斯景點"
        },
        "克拉克瓦特小河角國家自然保護區": {
            "location": [40.883833, -73.905204],
            "description": "克拉克瓦特小河角國家自然保護區是一個保護海濱生態系統的自然區域。",
            "opening_hours": "週一至週日，全天開放",
            "ticket_price": "免費入場",
            "category": "布朗克斯景點"
        },
        "巴特盧留著花園": {
            "location": [40.870697, -73.805573],
            "description": "巴特盧留著花園是一個古老的庄園，擁有美麗的花園和歷史建築。",
            "opening_hours": "週一至週日，上午10:00 - 下午5:00",
            "ticket_price": "成人門票：$8",
            "category": "布朗克斯景點"
        },
        "布朗克斯小動物園": {
            "location": [40.852020, -73.878392],
            "description": "布朗克斯小動物園是一個小型動物園，展示了各種動物品種。",
            "opening_hours": "週一至週日，上午10:00 - 下午5:00",
            "ticket_price": "成人門票：$12.95",
            "category": "布朗克斯景點"
        },
            "喬治華盛頓大橋": {
            "location": [40.851180, -73.950242],
            "description": "喬治華盛頓大橋是一個著名的橋樑，可步行或自行車穿越。",
            "opening_hours": "全天開放",
            "ticket_price": "免費入場",
            "category": "布朗克斯景點"
        },
        #皇后區
        "紐約科學博物館": {
            "location": [40.747105, -73.846718],
            "description": "一個寓教於樂的博物館。",
            "opening_hours": "週一至週五上午9:30 - 下午5:30，週末上午10:00 - 下午6:00",
            "ticket_price": "$25成人，$15兒童",
            "category": "皇后區景點"
        },
        "皇后區博物館": {
            "location": [40.739362, -73.841742],
            "description": "皇后區博物館是一個展示皇后區歷史和文化的博物館。",
            "opening_hours": "週三至週日，上午10:00 - 下午5:00",
            "ticket_price": "成人門票：$8",
            "category": "皇后區景點"
        },
        "法拉盛中心": {
            "location": [40.763045, -73.830694],
            "description": "法拉盛中心是一個購物中心和餐廳聚集地，提供多種購物和美食選擇。",
            "opening_hours": "週一至週日，時間視商家而定",
            "ticket_price": "免費入場",
            "category": "皇后區景點"
        },
        "皇后區植物園": {
            "location": [40.751741, -73.836748],
            "description": "皇后區植物園擁有美麗的花園和植物展示，是個休閒的好地方。",
            "opening_hours": "週一至週日，上午8:00 - 下午8:00",
            "ticket_price": "免費入場",
            "category": "皇后區景點"
        },
        "舊湯普金斯網球館": {
            "location": [40.748913, -73.845652],
            "description": "舊湯普金斯網球館是一個網球訓練和比賽場地，歡迎網球愛好者。",
            "opening_hours": "週一至週日，上午7:00 - 晚上11:00",
            "ticket_price": "場地租借費用視時間而定",
            "category": "皇后區景點"
        },
        "皇后國際嘉年華": {
            "location": [40.747365, -73.844269],
            "description": "皇后國際嘉年華是一個多元文化的節慶，提供美食、表演和活動。",
            "opening_hours": "週六，上午10:00 - 下午6:00",
            "ticket_price": "免費入場",
            "category": "皇后區景點"
        },
        "羅克薩普公園": {
            "location": [40.702203, -73.819410],
            "description": "羅克薩普公園是一個城市公園，提供許多戶外活動和休閒設施。",
            "opening_hours": "週一至週日，全天開放",
            "ticket_price": "免費入場",
            "category": "皇后區景點"
        },
        "皇后區國際機場觀景台": {
            "location": [40.641311, -73.778139],
            "description": "皇后區國際機場觀景台是一個觀賞飛機起降的好地方。",
            "opening_hours": "週一至週日，上午8:00 - 下午7:00",
            "ticket_price": "免費入場",
            "category": "皇后區景點"
        },

        "皇后區國際網球中心": {
            "location": [40.749603, -73.846960],
            "description": "皇后區國際網球中心是美國公開賽的主場地，有豐富的網球歷史。",
            "opening_hours": "週一至週日，時間視賽事而定",
            "ticket_price": "賽事門票價格視賽事而定",
            "category": "皇后區景點"
        },
        "喬治瓦什區（Astoria）": {
            "location": [40.772014, -73.930267],
            "description": "喬治瓦什區是一個多元文化的社區，提供美食、娛樂和文化體驗。",
            "opening_hours": "週一至週日，時間視商家而定",
            "ticket_price": "消費價格視選擇而定",
            "category": "皇后區景點"
        },
        #史泰登島
        "史泰登島渡輪": {
            "location": [40.643646, -74.073971],
            "description": "史泰登島渡輪是一個提供免費渡輪服務，可欣賞到曼哈頓市區的美景。",
            "opening_hours": "週一至週日，全天運行",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "史泰登島動物園": {
            "location": [40.621266, -74.116408],
            "description": "史泰登島動物園是一個小型動物園，展示了各種動物品種。",
            "opening_hours": "週一至週日，上午10:00 - 下午4:45",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "史泰登島博物館": {
            "location": [40.601211, -74.153384],
            "description": "史泰登島博物館展示了島嶼的歷史和文化。",
            "opening_hours": "週一至週日，上午11:00 - 下午5:00",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "海珍館": {
            "location": [40.578760, -74.090864],
            "description": "海珍館是一個水族館，展示了各種海洋生物。",
            "opening_hours": "週一至週日，上午10:00 - 下午5:00",
            "ticket_price": "成人門票：$11.95",
            "category": "史泰登島景點"
        },
        "史泰登島植物園": {
            "location": [40.643725, -74.103364],
            "description": "史泰登島植物園擁有美麗的花園和植物展示。",
            "opening_hours": "週一至週日，上午8:00 - 下午6:00",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "史泰登島風景步道": {
            "location": [40.579149, -74.151410],
            "description": "史泰登島風景步道是一個適合遠足和自然觀察的地方。",
            "opening_hours": "週一至週日，全天開放",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "褔特海灘公園": {
            "location": [40.567790, -74.104190],
            "description": "褔特海灘公園是一個海灘休閒公園，提供海灘和休閒設施。",
            "opening_hours": "週一至週日，上午7:00 - 晚上7:00",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "史泰登島街頭藝術": {
            "location": [40.640063, -74.075205],
            "description": "史泰登島街頭藝術是一個露天藝術展覽，展示了藝術家的作品。",
            "opening_hours": "週六，上午10:00 - 下午4:00",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "亞蘭茲奇史密斯博物館": {
            "location": [40.602684, -74.150403],
            "description": "亞蘭茲奇史密斯博物館展示了史泰登島的藝術和文化。",
            "opening_hours": "週一至週日，上午12:00 - 下午5:00",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
        "史泰登島運動場": {
            "location": [40.639978, -74.164672],
            "description": "史泰登島運動場是一個提供運動和休閒設施的場所。",
            "opening_hours": "週一至週日，時間視場地而定",
            "ticket_price": "免費入場",
            "category": "史泰登島景點"
        },
    }
    # 在你的 for 循環中，使用自定義樣式的 Popup
    for attraction, data in attractions.items():
        location = data["location"]
        description = data["description"]
        opening_hours = data["opening_hours"]
        ticket_price = data["ticket_price"]
        category = data["category"]

        popup_content = f"<b>{attraction}</b><br>經度: {location[0]}, 緯度: {location[1]}<br>{description}<br><br>"
        popup_content += f"<b>營業時間:</b> {opening_hours}<br>"
        popup_content += f"<b>票價:</b> {ticket_price}"

        # 設置自定義樣式的 Popup
        popup = folium.Popup(popup_content, max_width=300)  # 調整 max_width 參數

        marker = folium.Marker(
            location=location,
            popup=popup,
            tooltip=attraction,
            icon=folium.Icon(color=category_colors.get(category, "gray"))
        )
        fg.add_child(marker)
    # 將 FeatureGroup 添加到地圖中
    m.add_child(fg)

    # 使用 st_folium 函數將地圖嵌入到 Streamlit 中
    st_folium(
        m,
        width=1800,
        height=750,
    )
    # 添加图例
    st.sidebar.header("地圖圖例")
    for category, color in category_colors.items():
        st.sidebar.markdown(f'<font color="{color}">&#9632;</font> {category}', unsafe_allow_html=True)