import streamlit as st
from typing import Optional
from utils.matchmaking import respond_query, Professor

def main():
    # Streamlit app title
    st.title("SciConnect")
    st.write("Preencha os campos abaixo para encontrar professores que possam orientar seu projeto de pesquisa.")

    # Input fields for the student's details
    theme_enjoyed = st.text_input("Tema de interesse", "IA")
    course = st.text_input("Curso", "Ciencia da Computacao")
    academic_or_product = st.selectbox("Prefere a área acadêmica ou de desenvolvimento de produto?", ["Acadêmico", "Produto"])
    semester = st.text_input("Semestre", "5")
    has_idea = st.selectbox("Já tem uma ideia de projeto?", ["sim", "não"], help='Uma ideia de projeto pode ser um aplicativo, um sitema, um caso de uso que você deseja desenvolver')
    idea = None
    if has_idea == "sim":
        idea = st.text_area("Ideia do Projeto", "Quero desenvolver um modelo em que eu consiga por meio de linguagem natural dizer o timbre de um instrumento o descrevendo e o modelo conseguir reproduzir esse timbre num audio")

    # Button to perform the query
    if st.button("Encontrar os Professores"):
        # Execute the function and get the output
        matching_professors = respond_query(theme_enjoyed, course, academic_or_product, semester, has_idea, idea)
        
        # Display the results for the first four professors
        if matching_professors:
            st.write("Professores encontrados:")
            for idx, professor in enumerate(matching_professors[:4]):
                # Professor's photo
                if 'photo_url' in professor.metadata:
                    st.image(professor.metadata['photo_url'], width=150)
                
                # Professor's name
                st.subheader(professor.metadata.get('name', "Unknown Name"))
                
                # Professor's email
                st.write(f"Email: {professor.metadata.get('email', 'No email available')}")
                
                # Research Area
                st.write(f"Research Area: {professor.metadata.get('research_interests', 'No research area provided')}")
                
                # Description
                st.write(f"Description: {professor.metadata.get('description', 'No description available')}")
                
                # Reasoning for matching
                st.write(f"Match Reasoning: {professor.metadata.get('reasoning', 'No reasoning available')}")

                # Divider for each professor
                st.markdown("---")
        else:
            st.write("No matching professors found.")

if __name__ == "__main__":
    main()
