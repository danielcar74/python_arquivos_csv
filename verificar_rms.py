import pandas as pd

def verificar_erro_rms(csv_path, output_path):
    try:
        # Carregar o arquivo CSV com delimitador correto
        df = pd.read_csv(csv_path, delimiter=';')

        # Verificar as colunas disponíveis
        print("Colunas encontradas no arquivo:", df.columns)

        # Verificar se as colunas necessárias existem
        colunas_necessarias = ['RMS', 'IDVTEX']
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(f"Coluna '{coluna}' não encontrada no arquivo.")

        # Agrupar por RMS e contar IDVTEX únicos
        rms_duplicados = df.groupby('RMS')['IDVTEX'].nunique()
        rms_com_erro = rms_duplicados[rms_duplicados > 1]

        # Encontrar as linhas com erro
        linhas_com_erro = df[df['RMS'].isin(rms_com_erro.index)]

        # Salvar o CSV com os erros
        if not linhas_com_erro.empty:
            linhas_com_erro.to_csv(output_path, index=False, sep=';', encoding='utf-8')
            print(f"Encontrados {len(rms_com_erro)} RMS com mais de um SKU_VTEX.")
            print("Linhas com erro:")
            print(linhas_com_erro)
            print(f"Encontrados {len(rms_com_erro)} RMS com mais de um IDVTEX.")
            print("Linhas com erro salvas em:", output_path)
        else:
            print("Nenhum erro encontrado. Todos os RMS possuem um único IDVTEX.")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Solicitar o caminho do arquivo CSV e do arquivo de saída ao usuário
csv_path = input("Digite o caminho completo do arquivo CSV: ")
output_path = input("Digite o caminho completo para salvar o arquivo com erros: ")
verificar_erro_rms(csv_path, output_path)
