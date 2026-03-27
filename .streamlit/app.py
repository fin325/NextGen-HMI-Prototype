import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import plotly.graph_objects as go

# Конфигурация страницы
st.set_page_config(page_title="VW HMI Prototype", layout="wide")

# Инициализация состояния (чтобы значения не сбрасывались при обновлении)
if 'temp' not in st.session_state:
    st.session_state.temp = 22
if 'fan_speed' not in st.session_state:
    st.session_state.fan_speed = 2

# Заголовок в стиле приборной панели
st.markdown(f"<h1 style='text-align: center; color: #001E50;'>VOLKSWAGEN Digital Cockpit</h1>", unsafe_allow_html=True)
st.write("---")

# Создаем колонки для интерфейса
col_map, col_ctrl = st.columns([2, 1])

with col_map:
    st.subheader("📍 Navigation & Status")
    # Имитация карты через Plotly (просто для визуала)
    fig = go.Figure(go.Scattermapbox(lat=[51.49], lon=[7.41], mode='markers+text', marker=dict(size=15, color='blue')))
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=12, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    st.info("Destination: VW Infotainment, Bochum")

with col_ctrl:
    st.subheader("🌡️ Climate Control")
    st.metric("Cabin Temperature", f"{st.session_state.temp} °C")
    
    # Визуальный слайдер
    new_temp = st.slider("Manual Adjust", 16, 30, st.session_state.temp)
    st.session_state.temp = new_temp

    st.write("---")
    st.subheader("🎙️ Voice Assistant")
    st.write("Say: 'Set temperature to 25' or 'Установи 20 градусов'")
    
    # Кнопка записи голоса
    audio = mic_recorder(start_prompt="🎤 Start Voice Command", stop_prompt="🛑 Stop", key='recorder')

    if audio:
        r = sr.Recognizer()
        try:
            # Преобразование аудио в текст
            audio_data = sr.AudioFile(io.BytesIO(audio['bytes']))
            with audio_data as source:
                recorded_audio = r.record(source)
            
            # Распознавание (поддерживает русский и английский)
            text = r.recognize_google(recorded_audio, language="ru-RU").lower()
            st.success(f"Recognized: '{text}'")

            # Логика команд
            import re
            nums = re.findall(r'\d+', text)
            if nums:
                st.session_state.temp = int(nums[0])
                st.rerun()
            else:
                st.warning("Temperature value not found in speech.")
        except Exception as e:
            st.error("Could not process audio. Try again.")

st.write("---")
st.caption("Developed for Volkswagen Infotainment Ausbildung Application © 2024")
