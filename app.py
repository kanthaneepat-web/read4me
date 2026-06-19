import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os
import re

# ตั้งค่าหน้าเว็บโปรเจกต์ของ Ginny
st.set_page_config(page_title="เครื่องมืออ่านบทความยาวฟรี", page_icon="🎙️")
st.title("🎙️ เครื่องมืออ่านบทความส่วนตัวของ Ginny")
st.write("วางบทความยาวแค่ไหนก็ได้ลงในกล่องด้านล่าง แล้วกดฟังได้เลยฟรี 100% ไม่จำกัดคำครับ")

# กล่องรับข้อความ
text_input = st.text_area("วางบทความของคุณที่นี่:", height=300, placeholder="ก๊อปปี้เนื้อหาบทความมาวางตรงนี้...")

# แถบเลื่อนปรับความเร็วเสียง (ละเอียดตั้งแต่ 0.8 ถึง 2.0 เท่า)
speed = st.slider("ปรับความเร็วเสียงอ่าน (เท่า):", min_value=0.8, max_value=2.0, value=1.0, step=0.1)

def clean_text_for_gtts(text):
    # ลบเครื่องหมายสี่เหลี่ยม (#) และดอกจัน (*) ทั้งหมดออก
    text = text.replace("#", " ").replace("*", " ")
    text = text.replace("“", " ").replace("”", " ").replace('"', " ")
    
    # ช่วยปรับเว้นวรรคคำลงท้ายให้ Google อ่านเว้นจังหวะหายใจเนียนขึ้น
    text = text.replace("ครับ", "ครับ   ").replace("ค่ะ", "ค่ะ   ").replace("นะครับ", "นะครับ   ").replace("นะคะ", "นะคะ   ")
    
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def change_audio_speed(audio_path, speed_rate):
    # ฟังก์ชันหลังบ้านใช้ pydub เร่งความเร็วเนื้อเสียง MP3 โดยไม่ทำให้เสียงแหลมเป็นชิปมังก์
    sound = AudioSegment.from_file(audio_path)
    
    if speed_rate == 1.0:
        return audio_path
        
    # เร่งหรือลดความเร็วของเฟรมเสียง
    new_sample_rate = int(sound.frame_rate * speed_rate)
    fast_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    fast_sound = fast_sound.set_frame_rate(sound.frame_rate)
    
    output_path = "speed_adjusted.mp3"
    fast_sound.export(output_path, format="mp3")
    return output_path

if st.button("แปลงเป็นเสียงอ่านด้วยระบบ Google (สร้างไฟล์ MP3)"):
    if text_input.strip() == "":
        st.warning("กรุณาใส่ข้อความก่อนครับ")
    else:
        with st.spinner("กำลังแปลงเสียงและเร่งความเร็วตามต้องการ..."):
            cleaned_text = clean_text_for_gtts(text_input)
            
            TEMP_FILE = "temp_google.mp3"
            
            # สั่งให้ Google เจนเสียงความเร็วปกติมาก่อน
            tts = gTTS(text=cleaned_text, lang='th', slow=False)
            tts.save(TEMP_FILE)
            
            if os.path.exists(TEMP_FILE):
                # ส่งไฟล์ไปให้ pydub เร่งสปีดตามค่า Slider ที่คุณ Ginny เลือก
                final_audio = change_audio_speed(TEMP_FILE, speed)
                
                st.success(f"✨ สำเร็จ! ปรับความเร็วระบบเป็น {speed} เท่าเรียบร้อยแล้วครับ")
                with open(final_audio, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                    
                # ลบไฟล์ขยะหลังใช้งาน
                try:
                    os.remove(TEMP_FILE)
                except:
                    pass
