from BACK.MODULES.module  import search_pc , save_pc , microwork 
from langchain.tools      import tool
 
 
@tool
def save_tool(texto: str):
    
    """ Salva uma nova informação na base vetorial do Pinecone."""
     
    return save_pc(texto)
     

@tool
def search_tool(texto: str):
    
    """ Busca informações relevantes na base de conhecimento utilizando busca vetorial no Pinecone."""
    
    return search_pc(texto)


@tool
def mw_tool(day: int):
    
    """Consulta as vendas a partir do dia informado até a data atual, atualiza o Firestore e retorna o Top 10 de vendedores."""
    
    return microwork(day)