import requests
import pandas as pd

# Lista de SKUs ou ProductIDs (Exemplo fictício)
lista_ids = ['3568113']  # Substituir pelos IDs reais dos produtos

# URL base da API de PDP
url_base = "https://carrefourbr.vtexcommercestable.com.br/api/io/_v/api/intelligent-search/product_search"

resultados = []

for product_id in lista_ids:
    params = {
        'fq': f'productId:{product_id}'
    }
    
    response = requests.get(url_base, params=params)
    
    if response.status_code == 200:
        dados = response.json()
        if dados:
            produto = dados[0]
            nome = produto.get('productName')
            url = 'https://www.carrefour.com.br' + produto.get('linkText')
            sku = produto.get('productId')

            # Busca código de homologação na ficha técnica
            codigo_homologacao = 'Não encontrado'
            try:
                for grupo in produto.get('specificationGroups', []):
                    if grupo.get('name').lower() == 'ficha técnica':
                        for item in grupo.get('specifications', []):
                            if 'homologação' in item.get('name').lower():
                                codigo_homologacao = ', '.join(item.get('values'))
                                break
            except Exception:
                pass

            resultados.append({
                'Nome': nome,
                'URL': url,
                'ProductID': sku,
                'Codigo_Homologacao': codigo_homologacao
            })
            
            print(f"Capturado: {nome} - {codigo_homologacao}")
        else:
            print(f"Nenhum dado para ProductID {product_id}")

    else:
        print(f"Erro na API para ProductID {product_id}")

# Salvar resultado em CSV
#df = pd.DataFrame(resultados)
#df.to_csv('produtos_homologacao_carrefour.csv', index=False, encoding='utf-8')

#print("Captura finalizada. CSV gerado.")
