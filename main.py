from utils.json import read_json_data
from models.schedules import Schedules
import networkx as nx

def generate_course_graph(data):
    G = nx.Graph()

    for i in range(len(data)):
        G.add_node(i, course=data[i]['course'], semester=data[i]['semester'], teacher=data[i]['teacher'], ch=data[i]['ch'], code=data[i]['code'], name=data[i]['name'])

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if (data[i]['course'] == data[j]['course'] and data[i]['semester'] == data[j]['semester']) or data[i]['teacher'] == data[j]['teacher']:
                G.add_edge(i, j)

    return G

def available(graph, index, day, selectedSchedule):
    # Restrição de horários sequenciais
    count = 0
    for i in range(graph.nodes[index]['ch']):
        if day[selectedSchedule - i]:
            # verifica se ja possui a disciplina no horario anterior
            for j in range(len(day[selectedSchedule - i])):
                if (graph.nodes[index]['code'] == day[selectedSchedule - i][j]['code'] and
                        graph.nodes[index]['course'] == day[selectedSchedule - i][j]['course']):
                    count += 1
                    break
    if count >= 2 and graph.nodes[index]['ch'] >= 4:
        return False

    # Restrição de professor e conflitos com vértices adjacentes
    for adj_node in graph.neighbors(index):
        for j in range(len(day[selectedSchedule])):
            if graph.nodes[adj_node]['teacher'] == day[selectedSchedule][j]['teacher']:
                return False

    # Restrição de semestre e curso
    for j in range(len(day[selectedSchedule])):
        if (graph.nodes[index]['course'] == day[selectedSchedule][j]['course'] and
                graph.nodes[index]['semester'] == day[selectedSchedule][j]['semester']):
            return False

    # verificar se o professor já deu 8 aulas no mesmo dia
    count = 0
    for i in range(len(day)):
        for j in range(len(day[i])):
            if graph.nodes[index]['teacher'] == day[i][j]['teacher']:
                count += 1

        if count >= 6:
            return False
        
    
    # verifica se ja possui 2 aulas de determinada disciplina no mesmo dia    
    classPerDay = 0
    for i in range(len(day)):
        for j in range(len(day[i])):
            if graph.nodes[index]['code'] == day[i][j]['code'] and graph.nodes[index]['course'] == day[i][j]['course']:
                classPerDay += 1
        
        if graph.nodes[index]['ch'] > 3 and classPerDay >= 2:
            return False


    return True

def allocate_discipline(graph, discipline_index, schedules: Schedules):
    day_dict = {
        0: schedules.monday,
        1: schedules.tuesday,
        2: schedules.wednesday,
        3: schedules.thursday,
        4: schedules.friday,
        5: schedules.saturday
    }
    
    isNightCourse = False
    hasSaturdayClass = False
    days = 0

    if graph.nodes[discipline_index]['course'] == 'SIN':
        isNightCourse = True
    elif graph.nodes[discipline_index]['course'] == 'CCO':
        pass
    else:
        hasSaturdayClass = True   

    ch = int(graph.nodes[discipline_index]['ch'])

    for i in range(ch):
        for day in day_dict.values():
            added = False
        
            if (not hasSaturdayClass and day == schedules.saturday):
                continue
            
            for j in range(len(day)):
                if (isNightCourse and j < 10):
                    continue

                if available(graph, discipline_index, day, j):
                    day[j].append({'name': graph.nodes[discipline_index]['name'], 'code': graph.nodes[discipline_index]['code'],
                                   'semester': graph.nodes[discipline_index]['semester'], 'course': graph.nodes[discipline_index]['course'],
                                   'teacher': graph.nodes[discipline_index]['teacher'], 'ch': graph.nodes[discipline_index]['ch'],
                                   'horario': j})
                    added = True
                    break
            
            if (added):
                break

    return schedules

def getSchedules(data):
    schedules = Schedules()
    course_graph = generate_course_graph(data)

    courses = ['SIN', 'CCO', 'others']

    for course in courses:
        for index in course_graph.nodes:
            if course == "others":
                schedules = allocate_discipline(course_graph, index, schedules)
                continue       
    
            if course_graph.nodes[index]['course'] == course:
                schedules = allocate_discipline(course_graph, index, schedules)

    # for index in course_graph.nodes:
    #     if course_graph.nodes[index]['course'] == 'SIN':
    #         schedules = allocate_courses(course_graph, index, schedules)

    return schedules.__dict__

if __name__ == "__main__":
    data = read_json_data("./cenarios/cenario1.json")
    print(getSchedules(data))
    #getSchedules(data)