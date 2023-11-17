def generate_adj_matrix(cenario):
    matrix = []

    for v1 in cenario:
        adj = []

        for v2 in cenario:
            adj.append(generate_score(v1, v2))

        matrix.append(adj)

    return matrix

def generate_score(v1, v2):
    if v1["course"] == v2["course"] and v1["code"] == v2["code"]:
        return 0

    if v1["teacher"] == v2["teacher"]:
        #points += 1
        return 1

    if v1["semester"] == v2["semester"] and v1["course"] == v2["course"]:
        #points += 2
        return 1

    return 0


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