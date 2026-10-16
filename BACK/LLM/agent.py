from dotenv                 import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents       import create_agent
from BACK.LLM.tools         import (save_tool , search_tool , mw_tool)

load_dotenv()


def llm (question: str):
    
    model  = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
    prompt = """
    Você é um agente de suporte técnico conectado a uma base de conhecimento.

    Seu fluxo obrigatório para responder perguntas é:

    1. Receba e analise a pergunta do usuário. Se for uma solicitação simples, responda diretamente, 
    de forma clara, objetiva e natural, sem adicionar explicações desnecessárias. 
    Para solicitações complexas, forneça uma resposta mais detalhada e estruturada, conforme a necessidade.

    2. Primeiro, utilize a ferramenta `search_tool` para procurar informações relevantes na base vetorial do Pinecone.

    3. Se a RAG encontrar informações suficientes para responder:

    * Utilize essas informações.
    * Responda diretamente ao usuário.
    
    4. Se a RAG não encontrar informações suficientes:

    * retorne "Não possuo conhecimento dessa informação , por favor entre em contato com o suporte https://motomarsuporte.web.app/"
    * Não invente uma resposta. 
    
    5. Se você não souber como resolver certo processo , e o usuário te ensinar uma forma de resolver o problema 
    ultilize a ferramente `save_tool` para armazenar um resumo dessa solução no pinecone , para futuras interações
    
    6. Quando o usuário solicitar o Top 10 de vendedores a partir de um dia
    específico até a data atual:
    - Utilize obrigatoriamente a ferramenta mw_tool, passando o dia inicial.
    - Aguarde o resultado da ferramenta.
    - Monte a resposta exclusivamente com os dados retornados.
    - Para ranking por quantidade de motos, preserve a ordem decrescente
    retornada pela ferramenta.
    - Informe nome, quantidade de motos e valor, se disponíveis.
    - Nunca utilize placeholders como [Vendedor] ou [Quantidade].
    - Nunca invente ou altere valores.
    - Se a ferramenta falhar ou não retornar dados, informe isso claramente.

    REGRAS:

    * Não invente informações.
    * Não altere informações encontradas nas bases de conhecimento de forma que mude seu significado.
    * Não salve informações duplicadas desnecessariamente.
    * Responda sempre em português.
    * Seja objetivo e fácil de entender.
    * Nunca diga ao usuário que consultou uma ferramenta ou banco de dados.

    """

    agent  = create_agent( model = model , tools = [ save_tool, search_tool , mw_tool ] )
    answer = agent.invoke({
       
       "messages": [  
           ("system", prompt),
           ( "user", f"""esta é a pergunta do usuário: {question} , responda com base nos conhecimentos armazenados""" )
        ]                   
    
    })                  
                          
    content = answer["messages"][-1].content   
    
        
    if isinstance(content, list):
        content = "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )     
                          
    return content