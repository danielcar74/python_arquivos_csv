import pandas as pd
import re
import os
from datetime import datetime

def verificar_colunas_numericas(file_path):
    try:
        # Leitura do arquivo CSV com separador ';'
        df = pd.read_csv(file_path, sep=';', dtype=str)

        # Remove espaços e padroniza nomes das colunas para evitar erro
        df.columns = df.columns.str.strip().str.upper()

        # Define os nomes padrão das colunas a serem validadas
        colunas_necessarias = ['RMS', 'IDVTEX', 'LOJA']

        # Verifica se as colunas necessárias existem
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                print(f"Erro: A coluna '{coluna}' não foi encontrada no arquivo.")
                print(f"Colunas encontradas no arquivo: {list(df.columns)}")
                return

        # Função para checar se contém caracteres não numéricos
        def contem_letras(valor):
            if pd.isna(valor):
                return False
            return bool(re.search(r'[A-Za-z]', str(valor)))

        # Função para identificar quais colunas possuem erro em uma linha
        def colunas_com_erro(linha):
            erros = []
            for coluna in colunas_necessarias:
                if contem_letras(linha[coluna]):
                    erros.append(coluna)
            return ', '.join(erros)

        # Filtra linhas que possuem erro em pelo menos uma coluna
        erros = df[
            df['RMS'].apply(contem_letras) |
            df['IDVTEX'].apply(contem_letras) |
            df['LOJA'].apply(contem_letras)
        ].copy()

        # Adiciona coluna indicando quais colunas estão com erro
        erros['COLUNAS_COM_ERRO'] = erros.apply(colunas_com_erro, axis=1)

        quantidade_erros = len(erros)

        if quantidade_erros > 0:
            print(f"\nForam encontradas {quantidade_erros} linhas com erros nas colunas RMS, IDVTEX ou LOJA.\n")
            print(erros)

            # Gera nome do arquivo com data e hora
            agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nome_arquivo = f"erros_{agora}.xlsx"

            # Pega o diretório do arquivo CSV
            diretorio = os.path.dirname(file_path)
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)

            # Salva o arquivo Excel
            erros.to_excel(caminho_arquivo, index=False)

            print(f"\nRelatório de erros salvo em:\n{caminho_arquivo}\n")

        else:
            print("\nNenhum erro encontrado. Todas as colunas possuem apenas números.\n")

    except FileNotFoundError:
        print("Erro: Arquivo não encontrado. Verifique o caminho informado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    file_path = input("Digite o caminho completo do arquivo CSV a ser analisado: ")
    verificar_colunas_numericas(file_path)
