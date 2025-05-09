
import streamlit as st
import openai
import time

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------
openai.api_key = "sk-..."  # <- Coloca aquí tu clave secreta
assistant_id = "asst_..."  # <- Coloca aquí tu ID del asistente

# ---------------------------
# TÍTULO DE LA APP
# ---------------------------
st.set_page_config(page_title="Asistente TUPA", page_icon="🤖")
st.title("Asistente Virtual sobre el TUPA")
st.markdown("Haz tus consultas sobre trámites administrativos")

# ---------------------------
# INICIALIZAR ESTADO DE SESIÓN
# ---------------------------
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.session_state.messages = []

# ---------------------------
# INGRESO DEL USUARIO
# ---------------------------
user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )
    st.session_state.messages.append(("usuario", user_input))

    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    with st.spinner("Pensando..."):
        while True:
            status = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            if status.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        for msg in reversed(messages.data):
            if msg.role == "assistant":
                respuesta = msg.content[0].text.value
                st.session_state.messages.append(("asistente", respuesta))
                break

# ---------------------------
# MOSTRAR HISTORIAL DEL CHAT
# ---------------------------
for rol, mensaje in st.session_state.messages:
    if rol == "usuario":
        with st.chat_message("Usuario"):
            st.markdown(mensaje)
    else:
        with st.chat_message("Asistente"):
            st.markdown(mensaje)
