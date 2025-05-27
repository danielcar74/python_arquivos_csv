import pandas as pd


def verificar_erro_rms(csv_path, output_path, chunk_size=10000):
    try:
        # Inicializar um DataFrame para acumular os erros
        erros_acumulados = pd.DataFrame()

        # Ler o arquivo em chunks para economizar memória
        for chunk in pd.read_csv(csv_path, delimiter=';', encoding='utf-8', chunksize=chunk_size):
            # Verificar as colunas disponíveis
            print("Colunas encontradas no chunk:", chunk.columns)

            # Verificar se as colunas necessárias existem
            colunas_necessarias = ['RMS', 'IDVTEX']
            for coluna in colunas_necessarias:
                if coluna not in chunk.columns:
                    raise ValueError(f"Coluna '{coluna}' não encontrada no arquivo.")

            # Identificar RMS que possuem mais de um IDVTEX diferente
            rms_duplicados = chunk.groupby('RMS')['IDVTEX'].nunique()
            rms_com_erro = rms_duplicados[rms_duplicados > 1].index

            # Filtrar todas as duplas RMS e IDVTEX para esses RMS com mais de um IDVTEX diferente
            linhas_com_erro = chunk[chunk['RMS'].isin(rms_com_erro)]
            erros_acumulados = pd.concat([erros_acumulados, linhas_com_erro], ignore_index=True)

        # Salvar o CSV com os erros acumulados
        if not erros_acumulados.empty:
            erros_acumulados.to_csv(output_path, index=False, sep=';', encoding='utf-8')
            print(f"Encontrados {len(erros_acumulados)} registros com RMS associados a mais de um IDVTEX diferente.")
            print("Linhas com erro salvas em:", output_path)
        else:
            print("Nenhum erro encontrado. Todos os RMS possuem um único IDVTEX.")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")


# Caminhos corrigidos para o arquivo CSV e o arquivo de saída
csv_path = r"C:\Users\brcda174\Desktop\teste_prg\arquivo_teste.csv"
output_path = r"C:\Users\brcda174\Desktop\teste_prg\erro01.csv"
verificar_erro_rms(csv_path, output_path)
