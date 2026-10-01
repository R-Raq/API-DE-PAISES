import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("REST_COUNTRIES_API_KEY")

BASE_URL = "https://api.restcountries.com/countries/v5"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def requisicao(url, params=None):
    try:
        resposta = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        resposta.raise_for_status()

        return resposta.json()

    except requests.RequestException as erro:
        print("Erro ao fazer requisição:")
        print(erro)

        return None


def contagem_de_paises():
    resposta = requisicao(BASE_URL)

    if resposta:
        return resposta["data"]["meta"]["total"]


def buscar_pais(nome_do_pais):
    resposta = requisicao(
        f"{BASE_URL}/name",
        params={
            "q": nome_do_pais
        }
    )

    if resposta:
        return resposta["data"]["objects"]

    return []


def mostrar_populacao(nome_do_pais):
    lista_de_paises = buscar_pais(nome_do_pais)

    if lista_de_paises:

        for pais in lista_de_paises:
            nome = pais["names"]["common"]
            populacao = pais["population"]

            print(
                "{}: {} habitantes".format(
                    nome,
                    populacao
                )
            )

    else:
        print("País não encontrado")


def mostrar_moedas(nome_do_pais):
    lista_de_paises = buscar_pais(nome_do_pais)

    if lista_de_paises:

        for pais in lista_de_paises:

            nome = pais["names"]["common"]

            print("Moedas do", nome)

            moedas = pais["currencies"]

            for moeda in moedas:
                print(
                    "{} - {}".format(
                        moeda["name"],
                        moeda["code"]
                    )
                )

    else:
        print("País não encontrado")


def ler_nome_do_pais():
    if len(sys.argv) >= 3:
        return " ".join(sys.argv[2:])

    print("É preciso passar o nome do país")

    return None


if __name__ == "__main__":

    if not API_KEY:
        print("Erro: API key não encontrada no arquivo .env")
        sys.exit(1)

    if len(sys.argv) == 1:

        print("## Bem vindo ao sistema de países ##")

        print(
            "Uso: python paises.py <ação> <nome do país>"
        )

        print(
            "Ações disponíveis: contagem, moeda, populacao"
        )

    else:

        argumento1 = sys.argv[1]

        if argumento1 == "contagem":

            numero_de_paises = contagem_de_paises()

            if numero_de_paises is not None:

                print(
                    "Existem {} países no mundo todo".format(
                        numero_de_paises
                    )
                )

        elif argumento1 == "moeda":

            pais = ler_nome_do_pais()

            if pais:
                mostrar_moedas(pais)

        elif argumento1 == "populacao":

            pais = ler_nome_do_pais()

            if pais:
                mostrar_populacao(pais)

        else:
            print("Argumento inválido")
