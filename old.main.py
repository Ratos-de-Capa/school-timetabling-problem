from utils.json import read_json_data
from models.schedules import Schedules


def available(graph, index, day, selectedSchedule):

    # Restrição de horários sequenciais
    count = 0
    for i in range(graph[index]['ch']):
        if day[selectedSchedule - i]:
            # verifica se ja possui a disciplina no horario anterior
            for j in range(len(day[selectedSchedule - i])):
                if graph[index]['code'] == day[selectedSchedule - i][j]['code'] and graph[index]['course'] == day[selectedSchedule - i][j]['course']:
                    count += 1
                    break
    if count >= 2 and graph[index]['ch'] >= 4:
        return False


    # Restricao de professor
    for j in range(len(day[selectedSchedule])):
        if graph[index]['teacher'] == day[selectedSchedule][j]['teacher']:
            return False

    # Restricao de semestre e curso
    for j in range(len(day[selectedSchedule])):
        if graph[index]['course'] == day[selectedSchedule][j]['course'] and graph[index]['semester'] == day[selectedSchedule][j]['semester']:
            return False
        
    # verificar se o professor ja deu 8 aulas no mesmo dia
    count = 0
    for i in range(len(day)):
        for j in range(len(day[i])):
            if graph[index]['teacher'] == day[i][j]['teacher']:
                count += 1
            
        if count >= 6:
            return False
        #count = 0
    
    return True


def allocateSinCourses(graph, index, schedules: Schedules):    
    day_dict = {
        0: schedules.monday,
        1: schedules.tuesday,
        2: schedules.wednesday,
        3: schedules.thursday,
        4: schedules.friday,
        #5: schedules.saturday
    }
    
    for i in range(int(graph[index]['ch'])):
        for day in day_dict.values():
            for j in range(len(day)):
                if (j < 10):
                    continue
                
                if available(graph, index, day, j):
                    day[j].append({ 'name': graph[index]['name'],'code': graph[index]['code'] ,'semester': graph[index]['semester'], 'course': graph[index]['course'], 'teacher': graph[index]['teacher'], 'ch': graph[index]['ch'], 'horario': j})
                    break   

    return schedules

def allocateCcoCourses(graph, index, schedules: Schedules):
    day_dict = {
        0: schedules.monday,
        1: schedules.tuesday,
        2: schedules.wednesday,
        3: schedules.thursday,
        4: schedules.friday,
        #5: schedules.saturday
    }
    
    for i in range(int(graph[index]['ch'])):
        for day in day_dict.values():    
            for j in range(len(day)):
                if available(graph, index, day, j):
                    day[j].append({ 'name': graph[index]['name'],'code': graph[index]['code'] ,'semester': graph[index]['semester'], 'course': graph[index]['course'], 'teacher': graph[index]['teacher'], 'ch': graph[index]['ch'], 'horario': j})
                    break

    return schedules

def allocateOtherCourses(graph, index, schedules: Schedules):
    day_dict = {
        0: schedules.monday,
        1: schedules.tuesday,
        2: schedules.wednesday,
        3: schedules.thursday,
        4: schedules.friday,
        5: schedules.saturday
    }
    
    for i in range(int(graph[index]['ch'])):
        for day in day_dict.values():    
            for j in range(len(day)):
                if available(graph, index, day, j):
                    day[j].append({ 'name': graph[index]['name'],'code': graph[index]['code'] ,'semester': graph[index]['semester'], 'course': graph[index]['course'], 'teacher': graph[index]['teacher'], 'ch': graph[index]['ch'], 'horario': j})
                    break

    return schedules


def getSchedules(graph):
    schedules = Schedules()
    
    for i in range(len(graph)):
        if graph[i]['course'] == 'SIN':
            schedules = allocateSinCourses(graph, i, schedules)
    
    for i in range(len(graph)):
        if graph[i]['course'] == 'CCO':
            schedules = allocateCcoCourses(graph, i, schedules)
    
    for i in range(len(graph)):
        if graph[i]['course'] != 'CCO' and graph[i]['course'] != 'SIN':
            schedules = allocateOtherCourses(graph, i, schedules)
    
    return schedules.__dict__

if __name__ == "__main__":
    cenario1 = read_json_data("./cenarios/cenario1.json")

    #matrix = generate_adj_matrix(cenario1)

    #cores = graphColoring(matrix, 74)

    print(getSchedules(cenario1))
