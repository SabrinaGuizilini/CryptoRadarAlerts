import firebase_admin
from firebase_admin import credentials, firestore
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import os

def initialize_firebase():
    """Inicializa o Firebase se ainda não estiver inicializado."""
    if not firebase_admin._apps:
        firebase_json_path = os.path.expanduser("~/firebase.json")
        cred = credentials.Certificate(firebase_json_path)
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    """Garante que o Firestore esteja disponível e retorna o cliente."""
    initialize_firebase()
    return firestore.client()

def get_cotation(cripto, value, type_, currency):
    """ Obtém a cotação de uma criptomoeda e verifica se atingiu um valor alvo. """
    cg = CoinGeckoAPI()
    try:
        price_data = cg.get_price(ids=cripto, vs_currencies=currency)
        if cripto not in price_data or currency not in price_data[cripto]:
            return None 

        price = price_data[cripto][currency]

        if (type_ == "alta" and price >= value) or (type_ != "alta" and price <= value):
            return price, datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    except Exception as e:
        print(f"Erro ao obter cotação: {e}")

    return None


def retrieve_active_alerts():
    """Obtém alertas não enviados do Firestore."""
    db = get_firestore_client()

    try:
      alerts = db.collection("alerts").where(filter=firestore.FieldFilter("enviado", "==", False))
      docs = alerts.stream()

      filtered_alerts = [
          {"cripto": doc.to_dict()["cripto"], "email": doc.to_dict()["email"], "moeda": doc.to_dict()["moeda"], "nome": doc.to_dict()["nome"], "tipo": doc.to_dict()["tipo"], "valor": doc.to_dict()["valor"], "cotacao_atual": price, "horario_cotacao_atual": time, "id": doc.id}
          for doc in docs
          if (result := get_cotation(doc.to_dict()["cripto"], doc.to_dict()["valor"], doc.to_dict()["tipo"], doc.to_dict()["moeda"])) is not None
          for price, time in [result]
        ]

      return filtered_alerts

    except Exception as e:
        print(f"Erro ao recuperar alertas: {e}")
        return []


def change_enviado_field(doc_id):
    """Atualiza os campos enviado e data_envio do registro na Firestore."""
    db = get_firestore_client()
    doc_ref = db.collection("alerts").document(doc_id)
    try:
        doc_ref.update({"enviado": True})
        doc_ref.update({"data_envio": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    except Exception as e:
        print(f"Erro ao atualizar os campos enviado e/ou data_envio: {e}")
        