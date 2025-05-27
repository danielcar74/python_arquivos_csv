import pandas as pd
import os
import re


def validar_colunas_numericas(df, colunas):
    erros = {}
    padrao = re.compile(r'[^0-9]')  # Detecta qualquer coisa que não seja número

    for coluna in colunas:
        if coluna in df.columns:
            linhas_invalidas = df[df[coluna].astype(str).str.contains(padrao, na=False)]
            if not linhas_invalidas.empty:
                erros[coluna] = linhas_invalidas
    return erros


def comparar_arquivos():
    try:
        print("🚀 Iniciando comparação de arquivos...")

        # Caminho fixo dos arquivos
        pasta = r'C:\Users\brcda174\Documents\rotina_1P\comparar'
        arquivo_1 = os.path.join(pasta, 'arquivo_1.csv')
        arquivo_2 = os.path.join(pasta, 'arquivo_2.csv')

        print(f"🔍 Lendo arquivos...\n - {arquivo_1}\n - {arquivo_2}")

        df1 = pd.read_csv(arquivo_1, sep=';', dtype=str)
        df2 = pd.read_csv(arquivo_2, sep=';', dtype=str)

        print(f"✅ Arquivo 1 carregado com {len(df1)} linhas.")
        print(f"✅ Arquivo 2 carregado com {len(df2)} linhas.")

        # Verificar se colunas necessárias existem
        colunas_necessarias = ['SKU_VTEX', 'RMS']
        for coluna in colunas_necessarias:
            if coluna not in df1.columns or coluna not in df2.columns:
                raise Exception(f"A coluna '{coluna}' não foi encontrada em um dos arquivos.")

        # ✔️ Verificar se RMS e SKU_VTEX possuem apenas números
        print("\n🔎 Verificando se RMS e SKU_VTEX possuem apenas números...")

        erros_arquivo1 = validar_colunas_numericas(df1, colunas_necessarias)
        erros_arquivo2 = validar_colunas_numericas(df2, colunas_necessarias)

        if not erros_arquivo1:
            print("✅ Arquivo 1: Todas as entradas nas colunas RMS e SKU_VTEX possuem apenas números.")
        else:
            print("❌ Arquivo 1: Foram encontrados valores com letras ou símbolos:")
            for coluna, linhas in erros_arquivo1.items():
                print(f"\nColuna: {coluna}")
                print(linhas[[coluna]])

        if not erros_arquivo2:
            print("✅ Arquivo 2: Todas as entradas nas colunas RMS e SKU_VTEX possuem apenas números.")
        else:
            print("❌ Arquivo 2: Foram encontrados valores com letras ou símbolos:")
            for coluna, linhas in erros_arquivo2.items():
                print(f"\nColuna: {coluna}")
                print(linhas[[coluna]])

        # Criar chaves de comparação baseadas no par SKU_VTEX + RMS
        df1['chave'] = df1['SKU_VTEX'].astype(str) + '|' + df1['RMS'].astype(str)
        df2['chave'] = df2['SKU_VTEX'].astype(str) + '|' + df2['RMS'].astype(str)

        # Verificar se todos os pares do arquivo 1 estão no arquivo 2
        chaves_arquivo1 = set(df1['chave'])
        chaves_arquivo2 = set(df2['chave'])

        chaves_faltando = chaves_arquivo1 - chaves_arquivo2

        if not chaves_faltando:
            print("\n✅ Todos os pares SKU_VTEX + RMS do Arquivo 1 estão presentes no Arquivo 2.")
        else:
            print(f"\n❌ Existem {len(chaves_faltando)} pares SKU_VTEX + RMS do Arquivo 1 que NÃO estão no Arquivo 2:")
            for chave in chaves_faltando:
                sku, rms = chave.split('|')
                print(f" - SKU_VTEX: {sku} | RMS: {rms}")

        # Verificar se todos os campos do arquivo 1 estão no arquivo 2 (validação geral de linhas)
        colunas_para_merge = [col for col in df1.columns if col != 'chave' and col in df2.columns]

        linhas_em_comum = pd.merge(df1[colunas_para_merge], df2[colunas_para_merge],
                                   on=colunas_para_merge, how='left', indicator=True)

        linhas_nao_encontradas = linhas_em_comum[linhas_em_comum['_merge'] == 'left_only']

        if linhas_nao_encontradas.empty:
            print("\n✅ Todos os registros completos do Arquivo 1 estão presentes no Arquivo 2.")
        else:
            print(f"\n❌ Existem {len(linhas_nao_encontradas)} registros do Arquivo 1 que NÃO estão completamente no Arquivo 2.")
            print(linhas_nao_encontradas)

        print("\n🔍 Comparação finalizada.")

    except FileNotFoundError as fnf_error:
        print(f"\n❌ Arquivo não encontrado: {fnf_error}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")


# 🚀 Executar
if __name__ == "__main__":
    comparar_arquivos()
