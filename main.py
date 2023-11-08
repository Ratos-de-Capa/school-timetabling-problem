import json


class Conflito:
  codigo: str
  type: str | int

class Disciplina:    
  curso: str
  semestre: str
  codigo: str
  nome: str
  ch: str
  prof: str
  conflitos: list[Conflito]


class Vertice:
    def __init__(self, curso, semestre, codigo, disciplina, ch, prof):
        self.curso: str = curso
        self.semestre: str = semestre
        self.codigo: str = codigo
        self.disciplina: str = disciplina
        self.ch: str = ch
        self.prof: str = prof
        
        self.conflitos: list[Conflito] = []


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
    

def read_json_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def generate_adj_matrix(cenario):
    matrix = []

    for v1 in cenario:
        print(v1)
        adj = []
        
        for v2 in cenario:
            adj.append(generate_score(v1, v2))

        matrix.append(adj)

    return matrix


def generate_score(v1: Vertice, v2: Vertice):
    points = 0

    if v1['course'] == v2['course'] and \
        v1['code'] == v2['code']:
        return points

    if v1['teacher'] == v2['teacher']:
        points += 1

    if v1['semester'] == v2['semester'] and \
        v1['course'] == v2['course']:
        points += 2

    return points


if __name__ == "__main__":
    cenario1 = read_json_data('./cenario1.json')

    matrix = generate_adj_matrix(cenario1)

    print(matrix)