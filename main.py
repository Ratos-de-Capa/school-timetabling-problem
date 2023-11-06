import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
from ortools.sat.python import cp_model

def get_teacher(row):
    teacher = ""
    for col in df.columns[6:]:
        if row[col] == "X":
            teacher = col
    return teacher

def get_cenario(path):
    df = pd.read_csv(path) # path example csv/cenario-2semestre.csv

    # Aplica a função para criar a coluna "prof"
    df['prof'] = df.apply(get_teacher, axis=1)

    # Seleciona apenas as colunas desejadas
    df = df[['Curso', 'Semestre', 'Código', 'Disciplina', 'CH', 'prof']]

    # Converte o DataFrame para uma lista de dicionários
    items = df.to_dict(orient='records')

    # Exibe os itens
    # for item in items:
    #     print(item)
        
    print(items)
    
class Vertice:
    def __init__(self, curso, semestre, codigo, disciplina, ch, prof):
        self.curso = curso
        self.semestre = semestre
        self.codigo = codigo
        self.disciplina = disciplina
        self.ch = ch
        self.prof = prof

def read_json_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def school_timetabling(data):
    # Número total de unidades de tempo
    num_unidades_tempo = 74

    # Criar o modelo CP-SAT
    model = cp_model.CpModel()

    # Variáveis de decisão
    aulas = {}
    for vertex_id, vertice in enumerate(data):
        for unidade_tempo in range(num_unidades_tempo):
            aulas[(vertex_id, unidade_tempo)] = model.NewBoolVar(f"{vertice['Disciplina']} - Unidade {unidade_tempo + 1}")

    # Restrições
    for vertex_id, vertice in enumerate(data):
        model.Add(sum(aulas[(vertex_id, unidade_tempo)] for unidade_tempo in range(num_unidades_tempo)) == 1)

    # Objetivo (minimizar a alocação de aulas)

    # Criar o solucionador
    solver = cp_model.CpSolver()

    # Configurar as opções do solucionador (se necessário)
    solver.parameters.max_time_in_seconds = 10  # Define um limite de tempo em segundos

    # Encontrar a solução
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Imprimir a alocação de aulas
        for vertex_id, vertice in enumerate(data):
            for unidade_tempo in range(num_unidades_tempo):
                if solver.Value(aulas[(vertex_id, unidade_tempo)]) == 1:
                    print(f"Curso: {vertice['Curso']}, Semestre: {vertice['Semestre']}, Disciplina: {vertice['Disciplina']}, Professor: {vertice['prof']}")
                    print(f"Alocado na Unidade de Tempo: {unidade_tempo + 1}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

if __name__ == "__main__":
    data = read_json_data("cenario1.json")
    school_timetabling(data)