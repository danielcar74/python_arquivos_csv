import pandas as pd
import os
import re
from datetime import datetime

def validar_colunas_apenas_numeros(df, colunas):
    erros = {}
    padrao = re.compile(r'[^0-9]')  # Detecta qualquer coisa que não seja número

    for coluna in colunas:
        if coluna in df.columns:
            linhas_invalidas = df[df[coluna].astype(str).str.contains(padrao, na=False)]
            if not linhas_invalidas.empty:
                erros[coluna] = linhas_invalidas
    return erros


def verificar_campos_vazios(df):
    return df[df.isnull().any(axis=1) | (df.astype(str) == '').any(axis=1)]


def main():
    print("Iniciando rotina de consolidação de arquivos...")

    # Definir o caminho padrão dos arquivos
    pasta = r'C:\Users\brcda174\Documents\rotina_1P\zerar'

    # Nomes dos arquivos A e B
    arquivo_a = os.path.join(pasta, 'arquivo_a.csv')
    arquivo_b = os.path.join(pasta, 'arquivo_b.csv')

    try:
        # Leitura dos CSVs com separador ';'
        df_a = pd.read_csv(arquivo_a, sep=';', dtype=str)
        df_b = pd.read_csv(arquivo_b, sep=';', dtype=str)

        print(f"Arquivo A carregado com {len(df_a)} linhas.")
        print(f"Arquivo B carregado com {len(df_b)} linhas.")

        # Consolidação dos arquivos (append)
        df_c = pd.concat([df_b, df_a], ignore_index=True)

        print(f"Arquivo consolidado com {len(df_c)} linhas.")

        # Verificar campos vazios
        vazios = verificar_campos_vazios(df_c)
        if not vazios.empty:
            print(f"\nAtenção: Existem {len(vazios)} linhas com campos vazios ou nulos.")
            print(vazios)
        else:
            print("\nNenhum campo vazio encontrado.")

        # Verificar caracteres inválidos nas colunas Loja, RMS e IDVTEX
        colunas_verificar = ['Loja', 'RMS', 'IDVTEX']
        erros = validar_colunas_apenas_numeros(df_c, colunas_verificar)

        if erros:
            print("\nForam encontrados valores não numéricos nas colunas:")
            for coluna, linhas in erros.items():
                print(f"\nColuna: {coluna}")
                print(linhas)
        else:
            print("\nTodos os valores nas colunas Loja, RMS e IDVTEX estão corretos (somente números).")

        # Gerar arquivo de saída
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_saida = f"ZERAR_ESTOQUE_NFOOD_{timestamp}.csv"
        caminho_saida = os.path.join(pasta, nome_saida)

        df_c.to_csv(caminho_saida, sep=';', index=False, encoding='utf-8-sig')
        print(f"\nArquivo consolidado salvo em: {caminho_saida}")

    except FileNotFoundError as fnf_error:
        print(f"\nErro: Arquivo não encontrado - {fnf_error}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")


if __name__ == "__main__":
    main()
