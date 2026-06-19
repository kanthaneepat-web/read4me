import streamlit as st
import asyncio
import edge_tts
import os
import re

st.set_page_config(page_title="เครื่องมืออ่านบทความยาวฟรี", page_icon="🎙️")
st.title("🎙️ เครื่องมืออ่านบทความส่วนตัวของ Ginny")
st.write("วางบทความยาวแค่ไหนก็ได้ลงในกล่องด้านล่าง แล้วกดฟังได้เลยฟรี 100% ไม่จำกัดคำครับ")

text_input = st.text_area("วางบทความของคุณที่นี่:", height=300, placeholder="ก๊อปปี้เนื้อหาบทความมาวางตรงนี้...")
speed = st.slider("ปรับความเร็วเสียง:", min_value=0.8, max_value=2.0, value=1.0, step=0.1)

def advanced_clean_text(text):
    # 1. เคลียร์สัญลักษณ์ตัวหนา/ตัวเอียง/อัญประกาศ ทั้งหมดที่เป็นตัวทำลายจังหวะเว้นวรรคของ AI
    text = text.replace("**", " ").replace("*", " ").replace("“", " ").replace("”", " ").replace('"', " ")
    
    # 2. พจนานุกรมเปลี่ยนคำภาษาอังกฤษเป็นคำอ่านไทยแบบเว้นวรรคถูกต้อง เพื่อแก้ปัญหาสัทศาสตร์ AI
    # (หากจินนี่มีคำไหนเพิ่ม สามารถพิมพ์เพิ่มในรูปแบบนี้ได้เลยครับ)
    dictionary = {
        r"\bState of Being\b": "สเตท ออฟ บีอิ้ง",
        r"\bAlign\b": "อะไลน์",
        r"\bHigher Self\b": "ไฮ เออร์ เซลฟ์",
        r"\bExcitement\b": "เอ็ก ไซท์ เม้นท์",
        r"\bZero expectation\b": "ซี โร่ เอ็ก เปก เต ชั่น",
        r"\bBelief System\b": "บี ลีฟ ซิส เต็ม",
        r"\bSynchronicity\b": "ซิง โคร นิ ซิ ตี้",
        r"\bHuman Design\b": "ฮิว แมน ดี ไซน์",
        r"\bStrategy\b": "สแตรท เต จี",
        r"\bAuthority\b": "ออ ทอ ริ ตี้",
        r"\bGenerator\b": "เจ เนอ เร เตอร์",
        r"\bManifesting Generator\b": "แมนิเฟสติ้ง เจเนอเรเตอร์",
        r"\bProjector\b": "โปร เจก เตอร์",
        r"\bManifestor\b": "แมนิ เฟส เตอร์",
        r"\bReflector\b": "รี เฟลก เตอร์",
        r"\bNot-Self\b": "น็อต เซลฟ์",
        r"\bNeurons that fire together wire together\b": "นิวรอน แดท ไฟเออร์ ทูเกเธอร์ ไวเออร์ ทูเกเธอร์",
        r"\bNeuroscience\b": "นิว โร ไซ เอนซ์",
        r"\bMP3\b": "เอ็ม พี สาม",
        r"\bTikTok\b": "ติ๊ก ต๊อก",
        r"\bYouTube\b": "ยู ทูป",
        r"\bFacebook\b": "เฟซ บุ๊ก"
    }
    
    for english_word, thai_reading in dictionary.items():
        text = re.sub(english_word, thai_reading, text, flags=re.IGNORECASE)
        
    # 3. จัดการการเว้นวรรคภาษาไทย: เติมช่องว่างหลังเครื่องหมายวรรคตอน เพื่อบังคับให้ AI พักหายใจ
    text = text.replace("ครับ", "ครับ ").replace("ค่ะ", "ค่ะ ").replace("นะรับ", "นะครับ ").replace("นะคะ", "นะคะ ")
    text = text.replace("?", "? ").replace("!", "! ")
    
    # ยุบช่องว่างซ้ำซ้อน
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่าน (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังแปลงบทความยาวเป็นเสียงพอดแคสต์..."):
            cleaned_text = advanced_clean_text(text_input)
            speed_change = int((speed - 1.0) * 100)
            speed_str = f"{speed_change:+}%" if speed_change != 0 else "+0%"
            
            # กลับมาใช้ Premwadee เพราะอ่านคำภาษาไทยที่เราแปลงแล้วได้นุ่มนวลที่สุดครับ
            VOICE = "th-TH-PremwadeeNeural" 
            OUTPUT_FILE = "speech.mp3"
            
            async def generate_voice():
                communicate = edge_tts.Communicate(cleaned_text, VOICE, rate=speed_str)
                await communicate.save(OUTPUT_FILE)
            
            asyncio.run(generate_voice())
            
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ แปลงเสียงเสร็จเรียบร้อย!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
