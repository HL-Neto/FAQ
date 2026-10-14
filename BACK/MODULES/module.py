
from BACK.DATABASE.pinecone import retriever, vector_store


" ----- PINECONE ------ "

def search_pc (pergunta: str):
    
    documentos = retriever.invoke(pergunta)

    if not documentos:
        
        return "Nenhuma informação relevante foi encontrada."

    return "\n\n".join(
       
        documento.page_content
        for documento in documentos
    
    )
    
def save_pc (texto: str):
    

    vector_store.add_texts([texto])

    return "Informação armazenada com sucesso no Pinecone."


    

    
  
