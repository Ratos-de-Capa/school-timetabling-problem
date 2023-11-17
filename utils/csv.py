import pandas as pd

def get_teacher(row):
    teacher = ""
    for col in df.columns[6:]:
        if row[col] == "X":
            teacher = col
    return teacher


def get_cenario(path):
    df = pd.read_csv(path)  # path example csv/cenario-2semestre.csv

    # Aplica a função para criar a coluna "prof"
    df["prof"] = df.apply(get_teacher, axis=1)

    # Seleciona apenas as colunas desejadas
    df = df[["Curso", "Semestre", "Código", "Disciplina", "CH", "prof"]]

    # Converte o DataFrame para uma lista de dicionários
    items = df.to_dict(orient="records")

    # Exibe os itens
    # for item in items:
    #     print(item)
    
    