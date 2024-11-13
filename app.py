import streamlit as st  
import requests  
import matplotlib.patches as patches  
import matplotlib.pyplot as plt  
from PIL import Image  
from random import randrange
import pandas as pd
import urllib3

st.set_page_config("Tanigich va TTS", '🔗', 'wide')

st.markdown("# :rainbow[Dasturiy yordamchi]")  

#Tasvirni aniqlash
def image_detect(image):  
    files = {'image': image}  
    headers = {'X-Api-Key': f"{st.secrets['API_TOKEN']}"}  
    try:  
        response = requests.post(st.secrets['API_URL'], headers=headers, files=files)  
        if response.status_code == 200:  
            st.info("Hammasi joyida")
            return response.json()  
        else:  
            return f"Xatolik: {response.status_code}, {response.text}"  
    except Exception as e:  
        return f"Xatolik: {e}"  

#Audioga o'tkazish
def text_to_audio(text):    
    try:  
        headers = {"Content-Type": "application/json"}  
        data = {"text": text}  
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  
        
        response = requests.post(st.secrets['OAPI_URL'], headers=headers, json=data, verify=False)  
        
        if response.status_code == 200:  
            return response.content 
        else:  
            return None   
    except Exception as ex:  
        st.error(f"xatolik: {ex}")  
        return None  


tab1,tab2,tab3 = st.tabs(["🔈Audio chat", "🗒 Tasvirni aniqlash", "📍 Test Pill"])
# Matndan audio o'tkazish qismimiz  
with tab1:
    matn = st.chat_input("Matn kiriting")
    if matn:
        with st.spinner("Audio yaratilmoqda iltimos ozgina vaqt kuting..."):
            st.markdown(f"> ### ✍️ :rainbow[{matn.capitalize()}]")
            audio_data = text_to_audio(matn)  
            if audio_data:  
                st.audio(audio_data, format='audio/ogg', autoplay=True)
            else:  
                st.error("Audio yaratishda xatolik yuz berdi.")
     
with tab2:
    st.markdown("> :green[Rasmni shu qismga yuklang]")  
    image_file = st.file_uploader("Aniqlanayotgan tasvirni yuklang", type=['jpg', 'png']) 

    if image_file:  
        with st.spinner('Tasvir aniqlanayabdi, iltimos ozgina vaqt kutib turing...'):  
            row1, row2 = st.columns(2)  
            row1.image(image_file, caption='Dastlabki tasvir', use_container_width=True)  

            detect_result = image_detect(image_file)  
            if isinstance(detect_result, str):  # Agar xatolik bo'lsa  
                row2.error(detect_result)  
            else:  
                data = []
                # Natijalarni ko'rsatish  
                for i in range(len(detect_result)):  
                    data.append(
                        {
                            "labels": detect_result[i]['label'],
                            'confidence': float(detect_result[i]['confidence'])
                        }
                    )
                dataFrame = pd.DataFrame(data)
                row2.dataframe(data, use_container_width=True)

                image = Image.open(image_file)  
                fig, ax = plt.subplots()  
                ax.imshow(image)  
                ax.axis('off')  
                colors = ['#e14c2c', '#c87765', '#2aad95', '#2dd549', '#24a076', '#cae128', '#ee7b15', '#164bc4', '#6f25cc', '#9832be', '#f12f70', '#d82429', '#ead62d' ,'#60d41e', '#6aa549', '#16cb97']
                # Har bir aniqlangan belgi uchun chiziq va matnni qo'shamiz  
                for item in detect_result:  
                    label = item['label']  
                    x1 = int(item['bounding_box']['x1'])  
                    y1 = int(item['bounding_box']['y1'])  
                    x2 = int(item['bounding_box']['x2'])  
                    y2 = int(item['bounding_box']['y2'])  

                    rect_width = x2 - x1 
                    rect_height = y2 - y1
                    rect = patches.Rectangle((x1, y1), rect_width, rect_height, linewidth=1, edgecolor=colors[randrange(len(colors))], facecolor='none')  

                    ax.add_patch(rect)  
                    ax.text(x1, y1 - 10, f'{label.capitalize()} ({x1}, {y1})', color='red', fontsize=8)  

                # Faqat bitta natijaviy rasmni chiqaramiz  
                st.pyplot(fig, use_container_width=True)

with tab3:
    selection = st.pills("O'zbekisotnning poytaxi?", ["Toshkent", "Andijon", "Samarqand", "Buxoro"])
    if selection:
        if selection=="Toshkent":
            st.markdown(f"Sizning tanlovingiz: {selection} va siz :green[to'g'ri javob berdingiz]")
        else:
            st.markdown(f"Sizning tanlovingiz: {selection} va siz :red[noto'g'ri javob berdingiz afsus]")
    
    # options = ["North", "East", "South", "West"]
    # selection = st.segmented_control(
    #     "Directions", options, selection_mode="multi"
    # )
    # st.markdown(f"Your selected options: {selection}.")

    # option_map = {
    # 0: ":material/add:",
    # 1: ":material/zoom_in:",
    # 2: ":material/zoom_out:",
    # 3: ":material/zoom_out_map:",
    # }
    # selection = st.segmented_control(
    #     "Tool",
    #     options=option_map.keys(),
    #     format_func=lambda option: option_map[option],
    #     selection_mode="single",
    # )
    # st.write(
    #     "Your selected option: "
    #     f"{None if selection is None else option_map[selection]}"
    # )
        