import pandas as pd
import matplotlib.pyplot as plt

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
        }).rename(columns={'Margem_Contribuicao': 'Lucro_Total_RS', 'Margem_Percentual': 'Margem_Media_Perc'})

        # 5. Ordenar pelo lucro (do maior para o menor)
        resumo = resumo.sort_values(by='Lucro_Total_RS', ascending=False)

        # 5.5 Criando a variável Lucro_total_geral que será usada na criação da Perc_Acumulada.
        # 0 .cumsum soma o lucro da linha atual com as anteriores
        lucro_total_geral = resumo['Lucro_Total_RS'].sum()
        resumo['Perc_Acumulada'] = (resumo['Lucro_Total_RS'].cumsum() / lucro_total_geral) * 100

        # 6. Criando uma função para classificar em A, B ou C.
        def classificar_abc(porcentagem):
            if porcentagem <= 80:
                return 'A'
            elif porcentagem <= 95:
                return 'B'
            else:
                return 'C'

        # 7. Aplicando a classificação 80/20 de Pareto 
        resumo['Curva_ABC'] = resumo['Perc_Acumulada'].apply(classificar_abc)
        resumo = resumo.round(2)

        # --- GERANDO O GRÁFICO ---
        plt.style.use('ggplot')
        plt.figure(figsize=(10, 6))
        resumo['Lucro_Total_RS'].sort_values().plot(kind='barh', color='seagreen')
        plt.title('Lucro Total por Categoria')
        plt.xlabel('Lucro (R$)')
        plt.tight_layout()
        plt.savefig("grafico_lucro.png") # Salva a imagem na pasta
        
        print("--- Relatório de Eficiência por Categoria ---")
        print(resumo)

        # 5. Exportação: Salva o resultado em um novo Excel para a diretoria
        resumo.to_excel("relatorio_estrategico.xlsx")
        print("\nSucesso! O relatório 'relatorio_estrategico.xlsx' foi gerado.")

      # --- NOVO GRÁFICO DE PARETO APRIMORADO ---
        fig, ax1 = plt.subplots(figsize=(14, 7)) 

        # 1. Configuração das Barras de Lucro (Eixo Esquerdo)
        barras = ax1.bar(resumo.index, resumo['Lucro_Total_RS'], color='skyblue', label='Lucro Individual')
        ax1.set_ylabel('Lucro (R$)', fontsize=12, color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue') # Pinta os números do eixo de azul
        plt.xticks(rotation=45, ha='right') # Inclina e alinha os nomes das categorias

        # --- ADICIONAR VALORES EM CIMA DAS BARRAS ---
        for barra in barras:
            height = barra.get_height()
            ax1.annotate(f'{height:.0f}', # Texto formatado sem casas decimais
                         xy=(barra.get_x() + barra.get_width() / 2, height),
                         xytext=(0, 3),  # Deslocamento de 3 pontos para cima
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, color='black')

        # 2. Configuração da Linha da Porcentagem Acumulada (Eixo Gêmeo Direito)
        ax2 = ax1.twinx()
        linha = ax2.plot(resumo.index, resumo['Perc_Acumulada'], color='red', marker='D', ms=7, label='% Acumulada')
        ax2.set_ylabel('Porcentagem Acumulada (%)', fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red') # Pinta os números do eixo de vermelho
        ax2.set_ylim(0, 110) # Garante que a escala vá até 100%

        # --- ADICIONAR PORCENTAGENS NA LINHA ---
        y_acumulado = resumo['Perc_Acumulada'].tolist()
        for i, txt in enumerate(y_acumulado):
            ax2.annotate(f'{txt:.1f}%', # Texto formatado com 1 casa decimal e o símbolo %
                         xy=(i, y_acumulado[i]),
                         xytext=(0, 8), # Deslocamento de 8 pontos para cima
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, color='red', weight='bold')

        # 3. Título e Legendas Combinadas Abaixo do Gráfico
        plt.title('Curva ABC - Análise de Pareto Estratégica', fontsize=16, pad=20)
        
        # Combinando as legendas dos dois eixos em uma única caixa
        lns = [barras, linha[0]]
        labs = [l.get_label() for l in lns]
        
        # bbox_to_anchor move a legenda. loc='upper center' alinha o topo dela ao centro.
        ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
                   ncol=2, fontsize=11, frameon=True)
        
        plt.tight_layout() # Essencial para que a legenda de baixo não seja cortada
        plt.savefig("grafico_pareto_abc.png") # Salvando com nome novo
        print("Gráfico de Pareto Profissional 'grafico_pareto_abc.png' gerado com sucesso!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado na pasta.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# EXECUÇÃO: Substitua pelo nome real do seu arquivo
processar_meu_projeto_adm("vendas_mensais.xlsx")
