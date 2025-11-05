# Streamlit
import streamlit as st
from groq import Groq
#Nombre de la pagina
st.set_page_config(page_title="Inteligencia Artificial", page_icon="😆", layout="centered");

#Inicio del Chatbot
modelosIA = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b'];
nombreBot = "Jarvis"


def configurarPagina():
    st.title("Chatea con Jarvis")
    st.sidebar.title("Configuracion de Jarvis")
    elegirModelo = st.sidebar.selectbox("Escoge un modelo", options=modelosIA, index=0);

    st.sidebar.title("Chats")
    # Reiniciar el chat en caso de que querramos iniciar conversacion nueva
    if st.sidebar.button("Nuevo Chat"): 
        st.session_state.mensajes = []
    return elegirModelo

#Crea el usuario usando la clave generada por Groq que guardé en secrets.toml 
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        # "role: user" indica que el mensaje fue enviado por el usuario.
        model=modelo, 
        messages=[
                {"role": "system", "content": "Tu creador es Kevin. Tenlo en cuenta cuando te pregunten"},
                {"role": "system", "content": f"Sos {nombreBot}, un asistente virtual amigable y experto en inteligencia artificial. Siempre recordá que tu nombre es {nombreBot}."}, # Agregue esto para que ya al iniciar tenga un nombre definido 
                {"role": "user", "content": mensajeDeEntrada}
            ], 
        stream=True # Para tener una respuesta en vivo debo tener stream en True
    )
    

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat: mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "";
    for frase in chat_completo:
        if frase.choices[0].delta.content:           
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()        
    modelo = configurarPagina();
    area_chat()
    mensaje = st.chat_input("Escriba su mensaje:");

    if mensaje:
        actualizar_historial("user", mensaje, "😁")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()
                
if __name__ == "__main__":
    main();