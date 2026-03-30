import pandas as pd

def processar_meu_projeto_adm(nome_arquivo):
    try:
        # 1. Integração: O Pandas abre o seu Excel específico
        df = pd.read_excel(nome_arquivo)
        
        # 2. Regra de Negócio: Cálculo da Margem de Contribuição Nominal (R$)
        df['Margem_Contribuicao'] = df['Valor_Venda'] - df['Custo_Variavel']
        
        # 3. Regra de Negócio: Cálculo da Eficiência (Margem %)
        # Isso mostra qual produto é "melhor para o caixa" proporcionalmente
        df['Margem_Percentual'] = ((df['Margem_Contribuicao'] / df['Valor_Venda']) * 100).round(2)
        
        # 4. Visão Gerencial: Agrupando por Categoria
        # Vamos ver a soma do lucro e a média da margem percentual por setor
        resumo = df.groupby('Categoria').agg({
            'Margem_Contribuicao': 'sum',
            'Margem_Percentual': 'mean'
        }).round(2).rename(columns={'Margem_Contribuicao': 'Lucro_Total_RS', 'Margem_Percentual': 'Margem_Media_Perc'})

        print("--- Relatório de Eficiência por Categoria ---")
        print(resumo)

        # 5. Exportação: Salva o resultado em um novo Excel para a diretoria
        resumo.to_excel("relatorio_estrategico.xlsx")
        print("\nSucesso! O relatório 'relatorio_estrategico.xlsx' foi gerado.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado na pasta.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# EXECUÇÃO: Substitua pelo nome real do seu arquivo
processar_meu_projeto_adm("vendas_mensais.xlsx")
