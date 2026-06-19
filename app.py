import streamlit as st
import asyncio
import edge_tts
import os
import re

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="เครื่องมืออ่านบทความยาวฟรี", page_icon="🎙️")
st.title("🎙️ เครื่องมืออ่านบทความส่วนตัวของ Ginny")
st.write("วางบทความยาวแค่ไหนก็ได้ลงในกล่องด้านล่าง แล้วกดฟังได้เลยฟรี 100% ไม่จำกัดคำครับ")

# สร้างกล่องรับข้อความ
text_input = st.text_area("วางบทความของคุณที่นี่:", height=300, placeholder="ก๊อปปี้เนื้อหาบทความมาวางตรงนี้...")

# ตัวเลือกความเร็วเสียง
speed = st.slider("ปรับความเร็วเสียง:", min_value=0.8, max_value=2.0, value=1.0, step=0.1)

def clean_text_for_tts(text):
    # 1. แก้ไขการเว้นวรรค: ลบเครื่องหมายดอกจัน (*) ที่ใช้ทำตัวหนา/ตัวเอียง ออกทั้งหมด 
    # เพราะเครื่องหมายเหล่านี้ทำให้ AI สับสนและเว้นจังหวะหายใจผิดปกติ
    text = text.replace("**", " ").replace("*", " ")
    
    # 2. ปรับคำอ่านภาษาอังกฤษยอดฮิตในบทความ ให้เปลี่ยนเป็นคำอ่านไทยเนียน ๆ ก่อนส่งให้ AI 
    # วิธีนี้จะช่วยแก้ปัญหา AI อ่านคำอังกฤษแล้วเสียงเพี้ยน รวน หรือสำเนียงไม่ชัด
    replacements = {
        r"\bState of Being\b": "สเตท ออฟ บีอิ้ง",
        r"\bAlign\b": "อะไลน์",
        r"\bHigher Self\b": "ไฮเออร์ เซลฟ์",
        r"\bExcitement\b": "เอ็กไซท์เม้นท์",
        r"\bZero expectation\b": "ซีโร่ เอ็กซ์เปกเตชั่น",
        r"\bBelief System\b": "บีลีฟ ซิสเต็ม",
        r"\bSynchronicity\b": "ซิงโครนิซิตี้",
        r"\bHuman Design\b": "ฮิวแมน ดีไซน์",
        r"\bStrategy\b": "สแตรทเตจี",
        r"\bAuthority\b": "ออทอริตี้",
        r"\bGenerator\b": "เจเนอเรเตอร์",
        r"\bManifesting Generator\b": "แมนิเฟสติ้ง เจเนอเรเตอร์",
        r"\bProjector\b": "โปรเจกเตอร์",
        r"\bManifestor\b": "แมนิเฟสเตอร์",
        r"\bNot-Self\b": "น็อต เซลฟ์",
        r"\bMP3\b": "เอ็มพีสาม",
        r"\bTikTok\b": "ติ๊กต๊อก",
        r"\bYouTube\b": "ยูทูป",
        r"\bFacebook\b": "เฟซบุ๊ก"
    }
    
    for english_word, thai_reading in replacements.items():
        text = re.sub(english_word, thai_reading, text, flags=re.IGNORECASE)
        
    # 3. ยุบช่องว่างที่ซ้ำซ้อนให้เหลือช่องเดียว เพื่อจังหวะการเว้นวรรคที่สมบูรณ์
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if st.button("แปลงเป็นเสียงอ่าน (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังแปลงบทความยาวเป็นเสียงพอดแคสต์..."):
            # ปรับแต่งข้อความหลังบ้านให้เนียนก่อนส่งให้คุณเปรมวดีอ่าน
            cleaned_text = clean_text_for_tts(text_input)
            
            # คำนวณความเร็วเสียง
            speed_change = int((speed - 1.0) * 100)
            speed_str = f"{speed_change:+}%" if speed_change != 0 else "+0%"
            
            VOICE = "th-TH-PremwadeeNeural"
            OUTPUT_FILE = "speech.mp3"
            
            async def generate_voice():
                communicate = edge_tts.Communicate(cleaned_text, VOICE, rate=speed_str)
                await communicate.save(OUTPUT_FILE)
            
            asyncio.run(generate_voice())
            
            # แสดงเครื่องเล่นเสียงบนหน้าเว็บ
            if os.path.exists(OUTPUT_FILE):
                st.success("✨ แปลงเสียงเสร็จเรียบร้อย!")
                with open(OUTPUT_FILE, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
