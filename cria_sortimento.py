import pandas as pd
import os
import re
from datetime import datetime


def validar_colunas_apenas_numeros(df, colunas):
    erros = {}
    padrao = re.compile(r'[^0-9]')

    for coluna in colunas:
        if coluna in df.columns:
            linhas_invalidas = df[df[coluna].astype(str).str.contains(padrao, na=False)]
            if not linhas_invalidas.empty:
                erros[coluna] = linhas_invalidas
    return erros


def verificar_campos_vazios(df):
    return df[df.isnull().any(axis=1) | (df.astype(str) == '').any(axis=1)]


def main():
    print("🚀 Iniciando rotina de consolidação de arquivos...")

    # Definir o caminho padrão dos arquivos
    pasta = r'C:\Users\brcda174\Documents\rotina_1P\sortimento'

    # Nomes dos arquivos de entrada
    arquivo_novo = os.path.join(pasta, 'novo.csv')
    arquivo_hist = os.path.join(pasta, 'hist.csv')

    try:
        if not os.path.exists(arquivo_novo):
            print(f"❌ Arquivo não encontrado: {arquivo_novo}")
            return

        if not os.path.exists(arquivo_hist):
            print(f"❌ Arquivo não encontrado: {arquivo_hist}")
            return

        print(f"🔍 Lendo arquivo: {arquivo_hist}")
        df_hist = pd.read_csv(arquivo_hist, sep=';', dtype=str)
        print(f"✅ Arquivo HIST carregado com {len(df_hist)} linhas.")

        print(f"🔍 Lendo arquivo: {arquivo_novo}")
        df_novo = pd.read_csv(arquivo_novo, sep=';', dtype=str)
        print(f"✅ Arquivo NOVO carregado com {len(df_novo)} linhas.")

        # Consolidação dos arquivos
        df_consolidado = pd.concat([df_hist, df_novo], ignore_index=True)
        print(f"📊 Arquivo consolidado com {len(df_consolidado)} linhas.")

        # Verificar campos vazios
        vazios = verificar_campos_vazios(df_consolidado)
        if not vazios.empty:
            print(f"\n⚠️ Existem {len(vazios)} linhas com campos vazios ou nulos:")
            print(vazios)
        else:
            print("\n✅ Nenhum campo vazio encontrado.")

        # Verificar caracteres não numéricos nas colunas SKU_VTEX e RMS
        colunas_verificar = ['SKU_VTEX', 'RMS']
        erros = validar_colunas_apenas_numeros(df_consolidado, colunas_verificar)

        if erros:
            print("\n❌ Foram encontrados valores não numéricos nas colunas:")
            for coluna, linhas in erros.items():
                print(f"\n🔴 Coluna: {coluna}")
                print(linhas)
        else:
            print("\n✅ Todos os valores nas colunas SKU_VTEX e RMS estão corretos (somente números).")

        # Gerar arquivo de saída
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_saida = f"sortimento_pronto_{timestamp}.csv"
        caminho_saida = os.path.join(pasta, nome_saida)

        df_consolidado.to_csv(caminho_saida, sep=';', index=False, encoding='utf-8-sig')
        print(f"\n💾 Arquivo consolidado salvo com sucesso em: {caminho_saida}")

    except FileNotFoundError as fnf_error:
        print(f"\n❌ Erro: Arquivo não encontrado - {fnf_error}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
