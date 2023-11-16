import json

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

    print(items)

class Conflito:
    def __init__(self, codigo, type):
        self.codigo: str = codigo
        self.type: str | int = type


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


def read_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def generate_adj_matrix(cenario):
    matrix = []

    for v1 in cenario:
        adj = []

        for v2 in cenario:
            adj.append(generate_score(v1, v2))

        matrix.append(adj)

    return matrix

def get_color():
    pass


def coloracao_por_matriz_adjacencia(matriz_adjacencia):
    num_vertices = len(matriz_adjacencia)
    schedules = [-1] * num_vertices  # Inicializa todas as cores como -1
    num_cores = 74

    def eh_cor_segura(vertice, cor):
        for i in range(num_vertices):
            if matriz_adjacencia[vertice][i] == 1 and schedules[i] == cor:
                return False
        return True

    def colorir_util(vertice, num_cores):
        if vertice == num_vertices:
            return True

        # aqui tem que aplicar a funao que retorna exatamente os horarios que podem ser usados
        for cor in range(num_cores):
            if eh_cor_segura(vertice, cor):
                schedules[vertice] = cor
                if colorir_util(vertice + 1, num_cores):
                    return True
                schedules[vertice] = -1

    if not colorir_util(0, num_cores):
        return "Não é possível colorir o grafo com as cores especificadas."

    resultado = {}
    for vertice, cor in enumerate(schedules):
        resultado[vertice] = cor

    return resultado


def generate_score(v1: Vertice, v2: Vertice):
    points = 0

    if v1["course"] == v2["course"] and v1["code"] == v2["code"]:
        return points

    if v1["teacher"] == v2["teacher"]:
        points += 1
        return 1

    if v1["semester"] == v2["semester"] and v1["course"] == v2["course"]:
        points += 2
        return 1

    return points

#   getHorarios(vertice, resultudo: [{ vertice: cor }]): cor[];
#           validar horarios por regas;
#           agrupar em padroes definos por CH;
#           }

def graphColoring(adjacencyMatrix, numColors):
    numVertices = len(adjacencyMatrix)
    colors = [-1] * numVertices
    
    def canUseColor(vertex, color):
        for i in range(numVertices):
            if adjacencyMatrix[vertex][i] == 1 and colors[i] == color:
                return False
        return True
    
    def assignColor(vertex):
        for color in range(numColors):
            if canUseColor(vertex, color):
                return color
    
    for vertex in range(numVertices):
        colors[vertex] = assignColor(vertex)
    
    return colors

#---------------------------------------------------------------------

def available(graph, index, horarios, horarioEscolhido):

    # Restrição de horários sequenciais
    count = 0
    for i in range(graph[index]['ch']):
        if horarios[horarioEscolhido - i]:
            # verifica se ja possui a disciplina no horario anterior
            for j in range(len(horarios[horarioEscolhido - i])):
                if graph[index]['code'] == horarios[horarioEscolhido - i][j]['code'] and graph[index]['course'] == horarios[horarioEscolhido - i][j]['course']:
                    count += 1
                    break
    if count >= 2 and graph[index]['ch'] >= 4:
        return False


    # Restricao de professor
    for j in range(len(horarios[horarioEscolhido])):
        if graph[index]['teacher'] == horarios[horarioEscolhido][j]['teacher']:
            return False

    # Restricao de semestre e curso
    for j in range(len(horarios[horarioEscolhido])):
        if graph[index]['course'] == horarios[horarioEscolhido][j]['course'] and graph[index]['semester'] == horarios[horarioEscolhido][j]['semester']:
            return False

    
    return True


def allocateSinCourses(graph, index, horarios):
    for i in range(int(graph[index]['ch'])):
        for j in range(len(horarios)):
            if (j > 10 and j < 15) or (j > 24 and j < 29) or (j > 38 and j < 43) or (j > 52 and j < 57) or (j > 66 and j < 71):
                if available(graph, index, horarios, j):
                    horarios[j].append({ 'name': graph[index]['name'],'code': graph[index]['code'] ,'semester': graph[index]['semester'], 'course': graph[index]['course'], 'teacher': graph[index]['teacher'], 'ch': graph[index]['ch'], 'horario': j})
                    break

    return horarios


def allocateOtherCourses(graph, index, horarios):
    for i in range(int(graph[index]['ch'])):
        for j in range(len(horarios)):
            if available(graph, index, horarios, j):
                horarios[j].append({ 'name': graph[index]['name'],'code': graph[index]['code'] ,'semester': graph[index]['semester'], 'course': graph[index]['course'], 'teacher': graph[index]['teacher'], 'ch': graph[index]['ch'], 'horario': j})
                break

    return horarios


def getHorarios(array, graph):
    horarios = [[] for i in range(74)]
    
    for i in range(len(array)):
        if graph[i]['course'] == 'SIN':
            horarios = allocateSinCourses(graph, i, horarios)
    
    for i in range(len(array)):
        if graph[i]['course'] != 'SIN':
            horarios = allocateOtherCourses(graph, i, horarios)
    
    return horarios

if __name__ == "__main__":
    cenario1 = read_json_data("./cenario1.json")

    matrix = generate_adj_matrix(cenario1)

    cores = graphColoring(matrix, 74)

    print(getHorarios(cores, cenario1))
