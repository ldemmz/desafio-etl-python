# Desafio de projeto


O desafio a seguir é parte do Bootcamp Ciência de Dados 2023, realizado na plataforma Dio e patrocinado pelo Santander. Conforme solicitado, fomos desafiados a reimaginar o processo de ETL e aplicá-lo de acordo com nossa abordagem. Realizei minhas alterações e espero que gostem do resultado.


**Bibliotecas utilizadas:**

*   [Pandas](https://pandas.pydata.org/docs/)
*   [Matplotlib](https://matplotlib.org/stable/index.html)

**Contato:**

*   [Github](https://github.com/ldemmz)
*   [Linkedin](https://www.linkedin.com/in/leonardor99/)
*   [Instagram](https://www.instagram.com/lel_lql/)



## Passo a passo
### Importando bibliotecas:
```
import pandas as pd
import matplotlib.pyplot as plt
```

O comandos a seguir corresponde à extração do arquivo para o dataframe. É aconselhável utilizar o comando "print" para verificar os dados que estão sendo recebidos e seus tipos.

```
df = pd.read_csv('arquivo_para_teste.csv', delimiter = ";").set_index("UserID")
print(df)
print(df.dtypes)
```

### Exibição do comando "print"
#### Informações da tabela 
|   UserID   | Nome_aluno  | Nota_N1 | Nota_N2 | Média | Mensagem |
|:----------:|:-----------:|:-------:|:-------:|:-----:|:--------:|
|    1.0     | Leopoldino  |  4,00   |  7,00   | 5,50  |   NaN    |
|    2.0     |   Shiroe    |  7,00   | 10,00   | 8,50  |   NaN    |
|    3.0     |    Alice    |  9,00   |  9,00   | 9,00  |   NaN    |
|    4.0     |    Nemo     |  0,00   |  2,00   | 1,00  |   NaN    |
|    NaN     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |
|    ...     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |
|    NaN     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |
|    NaN     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |
|    NaN     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |
|    NaN     |    NaN      |   NaN   |   NaN   |  NaN  |   NaN    |


**Total de linhas:**  1064
**Total de colunas:**  5

#### Tipo dos dados
| Coluna      | Tipo de Dado |
| :---:       | :---:        |
| Nome_aluno  | object       |
| Nota_N1     | object       |
| Nota_N2     | object       |
| Média       | object       |
| Mensagem    | float64      |
---


Dadas as informações, é evidente que o arquivo contém várias linhas em branco e algumas colunas com tipos de dados incorretos. Portanto, iremos iniciar o processo removendo o conteúdo redundante.

```
# Nota-se que no arquivo há linhas sem utilidade alguma, portanto iremos tirá-las juntamente com o "NaN".

df.dropna(how="all", inplace=True)
df["Mensagem"].fillna('', inplace=True)

# Alteraremos o "dtype" de cada um dos itens e formataremos as notas, substituindo as vírgulas por pontuações.

df.index = df.index.astype(int)
df["Mensagem"] = df["Mensagem"].astype(str)

def transformar_notas(df, columns):
    for col in columns:
        if df[col].dtype not in [float, int]:
            df[col] = df[col].str.replace(',', '.').astype(float)

# Aplicando a função nas colunas relacionadas as notas.

coluna_de_notas = ["Nota_N1", "Nota_N2", "Média"]
transformar_notas(df, coluna_de_notas)
print(df)
print(df.dtypes)
```


### Exibição do comando "print"
#### Dados da tabela
|   UserID   | Nome_aluno  | Nota_N1 | Nota_N2 | Média | Mensagem |
|:----------:|:-----------:|:-------:|:-------:|:-----:|:--------:|
|     1      | Leopoldino  |   4.0   |   7.0   |  5.5  |          |
|     2      |   Shiroe    |   7.0   |  10.0   |  8.5  |          |
|     3      |    Alice    |   9.0   |   9.0   |  9.0  |          |
|     4      |    Nemo     |   0.0   |   2.0   |  1.0  |          |


#### Tipo dos dados
|   Coluna   |    Tipo de Dado    |
|:----------:|:-------------------:|
| Nome_aluno |       object        |
|  Nota_N1   |      float64        |
|  Nota_N2   |      float64        |
|   Média    |      float64        |
|  Mensagem  |       object        |
---



No próximo passo, iremos criar uma função para classificar os comentários com base na pontuação de cada aluno.

***Observação: A proposta do processo de ETL do desafio contava com a ajuda da IA generativa da OpenAI (GPT-4), contudo, acabei não a incluindo nesse projeto, pois além de ser paga, não havia necessidade de usá-la*.**

```
def gerar_mensagem_nota(x):
  if x >= 7.0:
    return "Aluno aprovado."
  elif x > 4.0 and x < 7:
    return "Aluno em recuperação."
  else:
    return "Aluno reprovado."

df["Mensagem"] = df["Média"].apply(gerar_mensagem_nota)
print(df)
```

### Exibição do comando "print"
|   UserID   | Nome_aluno  | Nota_N1 | Nota_N2 | Média |         Mensagem         |
|:----------:|:-----------:|:-------:|:-------:|:-----:|:------------------------:|
|     1      | Leopoldino  |   4.0   |   7.0   |  5.5  | Aluno em recuperação.    |
|     2      |   Shiroe    |   7.0   |  10.0   |  8.5  | Aluno aprovado.          |
|     3      |    Alice    |   9.0   |   9.0   |  9.0  | Aluno aprovado.          |
|     4      |    Nemo     |   0.0   |   2.0   |  1.0  | Aluno reprovado.         |
---


Para encerrar, geraremos um gráfico de classificação da turma, onde a cor das barras será determinada pela mensagem recebida. Após isso, converteremos o gráfico em uma imagem, a baixaremos e exportaremos a tabela de mensagens para um arquivo Excel no formato xlsx.

```
# Novo dataframe ordenado pela média dos alunos

df_grafico = df.sort_values(by='Média')

# Seleção de cor por mensagem

mensagem_cor = {
    "Aluno aprovado.": "#34a889",
    "Aluno em recuperação.": "#e0e082",
    "Aluno reprovado.": "#cc6d56"
}

cor_barra = df_grafico["Mensagem"].map(mensagem_cor)

#Plotagem do gráfico

plt.figure(figsize=(8, 5))
plt.bar(df_grafico["Nome_aluno"],df_grafico["Média"],color=cor_barra)
plt.xlabel("Aluno",fontsize=15,labelpad=20)
plt.ylabel("Média",fontsize=15,labelpad=30,rotation=0)
plt.title("Ranking dos melhores alunos",fontsize=20)
plt.xticks(rotation=45, fontsize=9, ha="right")

#Ajuste de layout

plt.tight_layout()

```
### Exibindo ranking de alunos de acordo com a média
![Ranqueamento de Alunos](https://github.com/ldemmz/desafio-etl-python/raw/main/ranqueamento%20de%20alunos.png)

### Exportando itens (imagem do ranqueamento + planilha com comentários)

```
plt.savefig("ranqueamento de alunos.png", bbox_inches="tight")
df.to_excel("arquivo_final.xlsx")
```




