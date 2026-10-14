from BACK.MODULES.module  import search_pc , save_pc
from langchain.tools      import tool
 
 
@tool
def save_tool(texto: str):
    
    """ Salva uma nova informação na base vetorial do Pinecone."""
     
    return save_pc(texto)
     

@tool
def search_tool(texto: str):
    
    """ Busca informações relevantes na base de conhecimento utilizando busca vetorial no Pinecone."""
    
    return search_pc(texto)