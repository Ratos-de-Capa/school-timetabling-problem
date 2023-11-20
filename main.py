from utils.json import read_json_data
from models.schedules import Schedules
import networkx as nx
import csv

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

    course = graph.nodes[discipline_index]['course']
    
    isNightCourse = course == 'SIN'
    hasSaturdayClass = course not in ['SIN', 'CCO']
    days = 0


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
                    
                    day[j].append({
                            'name': graph.nodes[discipline_index]['name'],
                            'code': graph.nodes[discipline_index]['code'],
                            'semester': graph.nodes[discipline_index]['semester'],
                            'course': graph.nodes[discipline_index]['course'],
                            'teacher': graph.nodes[discipline_index]['teacher'],
                            'ch': graph.nodes[discipline_index]['ch'],
                            'horario': j
                            })
                    
                    added = True
                    
                    break
            
            if (added):
                break

    return schedules

def getSchedules(data):
    schedules = Schedules()
    course_graph = generate_course_graph(data)

    courses = ['SIN', 'CCO', 'others']

    # for course in courses:
    #     for index in course_graph.nodes:
    #         if course == "others":
    #             schedules = allocate_discipline(course_graph, index, schedules)
    #             continue       
    
    #         if course_graph.nodes[index]['course'] == course:
    #             schedules = allocate_discipline(course_graph, index, schedules)

    for index in course_graph.nodes:
        if course_graph.nodes[index]['course'] == 'SIN':
            schedules = allocate_discipline(course_graph, index, schedules)

    for index in course_graph.nodes:
        if course_graph.nodes[index]['course'] == 'CCO':
            schedules = allocate_discipline(course_graph, index, schedules)

    for index in course_graph.nodes:
        if course_graph.nodes[index]['course'] != 'CCO' and course_graph.nodes[index]['course'] != 'SIN':
            #print(f"allocating course: {course_graph.nodes[index]['course']}")
            schedules = allocate_discipline(course_graph, index, schedules)

    return schedules.__dict__


def write_csv(data):
    with open('schedules.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Horário", "Disciplina", "Código", "Professor", "CH", "Semestre", "Curso"])
        
        for disc in data:
            writer.writerow([disc['horario'], disc['name'], disc['code'], disc['teacher'], disc['ch'], disc['semester'], disc['course']])

def obter_siglas_horarios(lista_horarios):
    siglas = []

    def formatar_sigla(dia_semana, periodo, horario_no_dia):
        horario = (horario_no_dia / dia_semana) % 14 + 1
        return '{}{}{}'.format(dia_semana, periodo, horario_no_dia % 14 + 1 )

    def get_periodo(horario):
        return 'M' if horario % 14 <= 5 else ('T' if horario % 14 <= 10 else 'N')
    
    def get_periodo_number(horario):
        return 0 if horario % 14 <= 5 else (5 if horario % 14 <= 10 else 10)
        
    
    def get_number_by_day(day):
        if day == 'monday':
            return 2
        elif day == 'tuesday':
            return 3
        elif day == 'wednesday':
            return 4
        elif day == 'thursday':
            return 5
        elif day == 'friday':
            return 6
        elif day == 'saturday':
            return 7

    # cria mapa de silgas por id unico de horario
    
    siglasPerDisc = {}
    
    for horario in lista_horarios:
        sigla = formatar_sigla(get_number_by_day(horario['day']), get_periodo(horario['value']), horario['value'] - get_periodo_number(horario['value']))
        siglasPerDisc[horario['key']].append(sigla) if horario['key'] in siglasPerDisc else siglasPerDisc.update({horario['key']: [sigla]})
    
    result = {}

    for dics in siglasPerDisc:
        for sigla in siglasPerDisc[dics]:
                
            prox = sigla[0] + sigla[1] + str(int(sigla[2]) + 1) 
            prox2 = sigla[0] + sigla[1] + str(int(sigla[2]) + 2)
            
            newSigla = sigla
            
            if prox in siglasPerDisc[dics]:
                newSigla = sigla[0] + sigla[1] + sigla[2:] + str(int(sigla[2]) + 1)
                siglasPerDisc[dics].remove(prox)
                
            elif prox2 in siglasPerDisc[dics]:
                newSigla = sigla[0] + sigla[1] + sigla[2:] + str(int(sigla[2]) + 1)
                siglasPerDisc[dics].remove(prox2)
                
            result[dics].append(newSigla) if dics in result else result.update({dics: [newSigla]})

    return result
        

def getId(horario):
    return horario['code'] + '-' + horario['course']

if __name__ == "__main__":
    data = read_json_data("./cenarios/cenario1.json")
    schedules = getSchedules(data)
    #print(schedules)


    horarios = []
    horariosMap = {}

    for day in schedules:
        if day == 'length':
            continue
             
        for harario in schedules[day]:
                for disc in harario:
                    print(disc)
                    horarios.append({ 'key': getId(disc), 'value': disc['horario'], 'day': day })
                    horariosMap[getId(disc)] = disc
        
    result = obter_siglas_horarios(horarios)
    
    for item in result:
        comp = ''
        for sigla in result[item]:
            comp += sigla + ' '
        
        horariosMap[item]['horario'] = comp 
            
    
    write_csv(horariosMap.values())
    
    
    print("Horários gerados com sucesso!")
    #getSchedules(data)