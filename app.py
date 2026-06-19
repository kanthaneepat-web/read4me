import streamlit as st
import asyncio
import edge_tts
import os
import re

# ตั้งค่าหน้าเว็บโปรเจกต์ของ Ginny
st.set_page_config(page_title="เครื่องมืออ่านบทความยาวฟรี", page_icon="🎙️")
st.title("🎙️ เครื่องมืออ่านบทความส่วนตัวของ Ginny")
st.write("วางบทความยาวแค่ไหนก็ได้ลงในกล่องด้านล่าง แล้วกดฟังได้เลยฟรี 100% ไม่จำกัดคำครับ")

# กล่องรับข้อความ
text_input = st.text_area("วางบทความของคุณที่นี่:", height=300, placeholder="ก๊อปปี้เนื้อหาบทความมาวางตรงนี้...")

# ปุ่มเลือกความเร็วเสียงแบบกด เลือกง่ายๆ เร็วขึ้นจริงแน่นอน
speed_option = st.radio(
    "ปรับความเร็วเสียงอ่าน:",
    options=["ปกติ (Normal)", "เร็วขึ้นเล็กน้อย (1.2x)", "เร็ว (1.4x)", "เร็วมาก (1.6x)"],
    index=0,
    horizontal=True
)

def clean_text_for_tts(text):
    # ลบเครื่องหมายสี่เหลี่ยม (#) และดอกจัน (*) ทั้งหมดออก ไม่ให้ออกเสียงคำว่าสี่เหลี่ยมหรือดอกจัน
    text = text.replace("#", " ").replace("*", " ")
    text = text.replace("“", " ").replace("”", " ").replace('"', " ")
    
    # ยุบช่องว่างซ้ำซ้อน
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่าน (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังแปลงบทความยาวเป็นเสียงพอดแคสต์..."):
            cleaned_text = clean_text_for_tts(text_input)
            
            # แปลงปุ่มกดให้เป็นคำสั่งเปอร์เซ็นต์ความเร็วของ Microsoft แบบตรงตัว
            if speed_option == "เร็วขึ้นเล็กน้อย (1.2x)":
                speed_str = "+20%"
            elif speed_option == "เร็ว (1.4x)":
                speed_str = "+40%"
            elif speed_option == "เร็วมาก (1.6x)":
                speed_str = "+60%"
            else:
                speed_str = "+0%" # ความเร็วปกติ
            
            # ใช้โมเดลเสียงรองรับสองภาษา (Multilingual) ที่จะอ่านคำอังกฤษได้ดีขึ้น
            VOICE = "th-TH-NiwatNeural"
            OUTPUT_FILE = "speech.mp3"
            
            async def generate_voice():
                communicate = edge_tts.Communicate(cleaned_text, VOICE, rate=speed_str)
                await communicate.save(OUTPUT_FILE)
            
            asyncio.run(generate_voice())
            
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ แปลงเสียงและปรับความเร็วเสร็จเรียบร้อย!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
