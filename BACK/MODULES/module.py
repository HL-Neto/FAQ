
import os
import requests
import firebase_admin

from dotenv                 import load_dotenv
from datetime               import date
from firebase_admin         import credentials, firestore
from BACK.DATABASE.pinecone import retriever, vector_store

load_dotenv()




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


    
    
" ----- MICROWORK ------ "
    
  
def microwork(d):
    
    
    api_url        = os.environ["MICROWK_BASE_URL"]
    api_credential = os.environ["MICROWORK_API_CREDENTIAL"]
    
    
    if not firebase_admin._apps:
        cred_path = os.environ["FIREBASE_CREDENTIALS_PATH"]
        cred      = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


    db  = firestore.client()
    col = db.collection("vendedores")

    delet_all_users()
    
    hoje         = date.today()
    data_inicial = hoje.replace(day = d).strftime("%Y-%m-%d") + " 00:00"
    data_final   = hoje.strftime("%Y-%m-%d") + " 23:59"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_credential}",
    }


    payload = {
        "idrelatorioconfiguracao": 248,
        "idrelatorioconsulta": 50,
        "idrelatorioconfiguracaoleiaute": 248,
        "idrelatoriousuarioleiaute": 514,
        "ididioma": 1,
        "listaempresas": [1,2,3,4,5,6],
        "filtros":f"""Periododamovimentacaoinicial={data_inicial};
    ComExpedicao=True;
    ComAutorizacaoExpedicao=True;
    Cor=null;
    Municipio=null;
    Consorcio=null;
    SemAutorizacaoExpedicao=True;
    SemExpedicao=True;
    Modelodoveiculo=null;
    Periododamovimentacaofinal={data_final};
    DesconsiderarEstornadoDevolvido=False;
    TipoVeiculo=null;
    Pessoa=null;
    Tipodemovimento=10;
    Tipodevenda=null;
    Origemdavenda=null;
    FinanceiraLeasing=null;
    TipoPessoa=null;
    EquipeCRM=null;
    FinanceiraCalculo=null;
    Vendedor=null;
    Estadodoveiculo=null;
    MovimentosCancelados=False;
    Pontodevendadovendedor=null;
    ContatoCRM=null
    """
    }
    
    
    
    

    res  = requests.post(api_url, headers=headers, json=payload, timeout=60,)
    res.raise_for_status()
    data = res.json()
    
        
    for doc in data:

        nome       = doc["vendedor"]
        quantidade = doc["quantidade"]
        valor      = doc["valordocfiscal"]
        search     = col.where("nome", "==", nome).stream()
        vendedores = list(search)

        if vendedores:
            
            for vendedor in vendedores:
                
                vendedor.reference.update({"quantidade_motos": firestore.Increment(quantidade) , "valor": firestore.Increment(valor)})

        else:
            
            col.add({ "nome": nome, "quantidade_motos": quantidade , "valor": valor })
        
             
    

    return top10()


    

" ----- FIREBASE ------ "


def top10():
    db = firestore.client()
    col_ref = db.collection("vendedores")

    search = (
        col_ref
        .order_by("valor", direction=firestore.Query.DESCENDING)
        .order_by(
            "quantidade_motos",
            direction=firestore.Query.DESCENDING
        )
        .limit(10)
        .stream()
    )

    vendedores = []

    for doc in search:
        dados = doc.to_dict()
        dados["id"] = doc.id
        vendedores.append(dados)

    
    return vendedores

def delet_all_users():
    
    db      = firestore.client()
    col_ref = db.collection("vendedores")


    for doc in col_ref.stream():
        doc.reference.delete()
   
   