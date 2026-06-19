import streamlit as st
from gtts import gTTS
import os
import re

# ตั้งค่าหน้าเว็บโปรเจกต์ของ Ginny
st.set_page_config(page_title="เครื่องมืออ่านบทความยาวฟรี", page_icon="🎙️")
st.title("🎙️ เครื่องมืออ่านบทความส่วนตัวของ Ginny")
st.write("วางบทความยาวแค่ไหนก็ได้ลงในกล่องด้านล่าง แล้วกดฟังได้เลยฟรี 100% ไม่จำกัดคำครับ")

# กล่องรับข้อความ
text_input = st.text_area("วางบทความของคุณที่นี่:", height=300, placeholder="ก๊อปปี้เนื้อหาบทความมาวางตรงนี้...")

def clean_text_for_gtts(text):
    # 1. ลบเครื่องหมายสี่เหลี่ยม (#) และเครื่องหมายดอกจัน (*) ทั้งหมดออก เพื่อไม่ให้ AI อ่านคำว่า "สี่เหลี่ยม" หรือ "ดอกจัน"
    text = text.replace("#", " ").replace("*", " ")
    
    # 2. ลบสัญลักษณ์อัญประกาศหรือเครื่องหมายอื่น ๆ ที่อาจจะหลุดมา
    text = text.replace("“", " ").replace("”", " ").replace('"', " ")
    
    # 3. เทคนิคช่วยปรับเว้นวรรคท้ายประโยคให้ Google เว้นจังหวะหายใจได้ดีขึ้น ไม่รัวเป็นปืนกล
    text = text.replace("ครับ", "ครับ   ").replace("ค่ะ", "ค่ะ   ").replace("นะครับ", "นะครับ   ").replace("นะคะ", "นะคะ   ")
    
    # 4. ยุบช่องว่างที่ซ้ำซ้อนให้เหลือช่องเดียวเพื่อจังหวะการอ่านที่สม่ำเสมอ
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่านด้วยระบบ Google (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังส่งข้อความให้ระบบ Google แปลงเสียงอ่านคุณภาพสูง..."):
            cleaned_text = clean_text_for_gtts(text_input)
            
            OUTPUT_FILE = "google_speech.mp3"
            
            # เรียกใช้ระบบ gTTS ของ Google เลือกภาษาไทย (th)
            tts = gTTS(text=cleaned_text, lang='th', lang_check=True)
            tts.save(OUTPUT_FILE)
            
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ Google แปลงเสียงให้เสร็จเรียบร้อยแล้วครับ!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
