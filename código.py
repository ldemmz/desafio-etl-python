

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('arquivo_para_teste.csv', delimiter = ";").set_index("UserID")

df.dropna(how="all", inplace=True)
df["Mensagem"].fillna('', inplace=True)
df.index = df.index.astype(int)
df["Mensagem"] = df["Mensagem"].astype(str)

def transformar_notas(df, columns):
    for col in columns:
        if df[col].dtype not in [float, int]:
            df[col] = df[col].str.replace(',', '.').astype(float)

coluna_de_notas = ["Nota_N1", "Nota_N2", "Média"]
transformar_notas(df, coluna_de_notas)

def gerar_mensagem_nota(x):
  if x >= 7.0:
    return "Aluno aprovado."
  elif x > 4.0 and x < 7:
    return "Aluno em recuperação."
  else:
    return "Aluno reprovado."

df["Mensagem"] = df["Média"].apply(gerar_mensagem_nota)

df_grafico = df.sort_values(by='Média')

mensagem_cor = {
    "Aluno aprovado.": "#34a889",
    "Aluno em recuperação.": "#e0e082",
    "Aluno reprovado.": "#cc6d56"
}
cor_barra = df_grafico["Mensagem"].map(mensagem_cor)

plt.figure(figsize=(8, 5))
plt.bar(df_grafico["Nome_aluno"],df_grafico["Média"],color=cor_barra)
plt.xlabel("Aluno",fontsize=15,labelpad=20)
plt.ylabel("Média",fontsize=15,labelpad=30,rotation=0)
plt.title("Ranking dos melhores alunos",fontsize=20)
plt.xticks(rotation=45, fontsize=9, ha="right")

plt.tight_layout()

plt.savefig("ranqueamento de alunos.png", bbox_inches="tight")
df.to_excel("arquivo_final.xlsx")