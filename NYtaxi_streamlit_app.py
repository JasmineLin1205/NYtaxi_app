import streamlit as st

def intro():
    st.markdown("<h1 style='text-align: center;'>基於紐約計程車軌跡數據 🚕</h1>", unsafe_allow_html=True)
    #st.title("基於紐約計程車軌跡數據 🚕")
    #st.sidebar.success("Select a a page above.")
    # SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
    


def select_identity():
    selected_identity = st.sidebar.radio("", ["司機", "乘客"], key='identity_selector')
    st.session_state.selected_identity = selected_identity

def main():
    st.set_page_config(layout="wide")
    intro()
    
    # 在应用程序的开头初始化选择状态
    if 'selected_identity' not in st.session_state:
        st.session_state.selected_identity = '司機' 

    # 调用 select_identity() 函数
    select_identity()

    # 根据用户选择的身份显示相应的页面内容
    if st.session_state.selected_identity == '司機':
       selected_page = st.sidebar.selectbox("請選擇想查看的內容", ["密度熱圖","區域收入","油資查詢","最短路徑","人流聚集地"])

       if selected_page == "密度熱圖":
           from TaxidataMap import show_taxidata_map
           show_taxidata_map()

       elif selected_page == "區域收入":
           from Dateregionmerge_1 import show_date_region_merge
           show_date_region_merge()
           
       elif selected_page == "油資查詢":
           from Oil import show_oil
           show_oil()
           
       elif selected_page == "最短路徑":
           from Pathpeakoff_new import show_path
           show_path()
           
       elif selected_page == "人流聚集地":
           from Taxidriver_pickup_locations import show_taxidriver_pickup    
           show_taxidriver_pickup()    

    elif st.session_state.selected_identity == '乘客':
        selected_page = st.sidebar.selectbox("請選擇想查看的內容", ["行程時間","觀光景點","最短路徑","計程車聚集地"])

        if selected_page == "行程時間":
            from peakoff import show_peakoff
            show_peakoff()
            
        elif selected_page == "觀光景點":
            from Attractions2 import show_attractions
            show_attractions()    
        
        elif selected_page == "最短路徑":
            from Pathpeakoff_new import show_path
            show_path()
            
        elif selected_page == "計程車聚集地":
            from Taxipassenger_dropoff_locations import show_taxipassenger_dropoff    
            show_taxipassenger_dropoff()    
        

if __name__ == '__main__':
    main()

    



    
