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

# ปุ่มเลือกความเร็วเสียง (ช้า - ปกติ - เร็ว)
speed_option = st.radio(
    "ปรับความเร็วเสียงอ่าน:",
    options=["ช้า (Slow)", "ปกติ (Normal)", "เร็ว (Fast)"],
    index=1,
    horizontal=True
)

def clean_text_for_gtts(text):
    # 1. สั่งลบเครื่องหมายสี่เหลี่ยม (#) และดอกจัน (*) ทั้งหมดออก เพื่อไม่ให้ AI อ่านคำว่า "สี่เหลี่ยม" หรือ "ดอกจัน"
    text = text.replace("#", " ").replace("*", " ")
    
    # 2. ลบสัญลักษณ์ตัวเปิดปิดคำพูดอื่น ๆ ที่อาจจะทำให้สะดุด
    text = text.replace("“", " ").replace("”", " ").replace('"', " ")
    
    # 3. เทคนิคช่วยปรับเว้นวรรคคำลงท้ายให้ Google อ่านเว้นจังหวะหายใจเนียนขึ้น
    text = text.replace("ครับ", "ครับ   ").replace("ค่ะ", "ค่ะ   ").replace("นะครับ", "นะครับ   ").replace("นะคะ", "นะคะ   ")
    
    # ยุบช่องว่างซ้ำซ้อนให้เหลือช่องเดียว
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่านด้วยระบบ Google (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังส่งข้อความให้ระบบ Google แปลงเสียงอ่าน..."):
            cleaned_text = clean_text_for_gtts(text_input)
            
            OUTPUT_FILE = "google_speech.mp3"
            
            # เช็คความเร็วที่เลือกจากปุ่มกด
            # gTTS รองรับการตั้งค่า slow เป็น True (ช้า) หรือ False (ปกติ/เร็ว)
            if speed_option == "ช้า (Slow)":
                is_slow = True
            else:
                is_slow = False
                
            # เรียกใช้ระบบ gTTS ของ Google
            tts = gTTS(text=cleaned_text, lang='th', slow=is_slow)
            tts.save(OUTPUT_FILE)
            
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ Google แปลงเสียงให้เสร็จเรียบร้อยแล้วครับ!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
