import streamlit as st
from api_client import query


st.title("Harry Potter RAG System")
st.write("Hello, I'm Your assistant feel free to ask anything about harry potter books")

question=st.text_input("say something ..")


if st.button("send"):
    if question.strip():

        with st.spinner("wait a second .."):

            try:
                respnse=query(question)
                st.write("Answer: ")
                st.write(respnse["answer"])
                #print each source in a spearate line if found
                if respnse["sources"]:
                    st.write("sources: ")
                    for src in respnse["sources"]:   
                        st.write(src)

            except Exception:
                st.error("Something went wrong.")

    else:
        st.warning("No question found")




