import streamlit as st
import requests as rq
import json
from openai import OpenAI

st.title("Bienvenue sur ChatBot Online !")
st.write("Entrez simplement votre clé API et vous pouvez commencer à discuter (en précisant évidemment s'il s'agit de MistralAI ou OpenAI) !")
st.markdown("_Si vous ne savez pas comment récupérer votre clé API, consultez ce petit [guide pratique](http://localhost:8501/Guide_API)._")

company = st.sidebar.radio("Entreprise :", ["MistralAI", "OpenAI"])
API_key = st.text_input("Votre clé d'API :", type="password")  # Masquer la clé

def chatbot():
    prompt = st.text_area("Prompt :")

    if company == "MistralAI":
        if st.button("⬆️ Envoyer"):
            if prompt.strip():
                with st.spinner("Réponse en cours..."):
                    headers = {
                        "Authorization": f"Bearer {API_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "mistral-medium",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Parle en français et sois toujours précis dans ce que tu dis. Si tu ne sais pas, il est acceptable de l'admettre."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }

                    response = rq.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

                    if response.status_code == 200:
                        result = response.json()
                        st.info(f"#### Mistral AI :\n{result["choices"][0]["message"]["content"]}")
                    else:
                        st.error(f"Erreur {response.status_code} : {response.text}")

            else:
                st.warning("Veuillez taper un message avant d'envoyer !")

    elif company == "OpenAI":
        model = st.selectbox("Modèle :", ["gpt-4o", "gpt-3.5-turbo"])

        if st.button("⬆️ Envoyer"):
            if prompt.strip():
                with st.spinner("Réponse en cours..."):
                    try:
                        client = OpenAI(api_key=API_key)
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.info(f"#### ChatGPT :\n{response.choices[0].message.content}")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

            else:
                st.warning("Veuillez taper un message avant d'envoyer !")

if __name__ == "__main__":
    chatbot()
