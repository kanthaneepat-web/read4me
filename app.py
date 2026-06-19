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
speed = st.slider("ปรับความเร็วเสียง:", min_value=0.8, max_value=2.0, value=1.0, step=0.1)

def clean_text_for_tts(text):
    # ปรับปรุงระบบเว้นวรรค: ลบเครื่องหมายเน้นคำ (**, *, “ , ”) ออกทั้งหมด 
    # เพื่อให้โมเดลสองภาษาคำนวณจังหวะการเว้นวรรคตามโครงสร้างประโยคได้ถูกต้อง ไม่สะดุดกลางคำ
    text = text.replace("**", " ").replace("*", " ").replace("“", " ").replace("”", " ").replace('"', " ")
    
    # ยุบช่องว่างที่ซ้ำซ้อนให้เนียนตา
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่าน (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังแปลงบทความยาวเป็นเสียงพอดแคสต์..."):
            cleaned_text = clean_text_for_tts(text_input)
            speed_change = int((speed - 1.0) * 100)
            speed_str = f"{speed_change:+}%" if speed_change != 0 else "+0%"
            
            # เปลี่ยนมาใช้โมเดลเสียงรองรับสองภาษา (Multilingual) แท้ ๆ ของ Microsoft
            VOICE = "th-TH-NiwatNeural"
            OUTPUT_FILE = "speech.mp3"
            
            async def generate_voice():
                communicate = edge_tts.Communicate(cleaned_text, VOICE, rate=speed_str)
                await communicate.save(OUTPUT_FILE)
            
            asyncio.run(generate_voice())
            
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ แปลงเสียงเสร็จเรียบร้อย!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
