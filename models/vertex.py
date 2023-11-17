from conflict import Conflict

class Vertice:
    def __init__(self, course, semester, code, name, ch, teacher):
        self.course: str = course
        self.semester: str = semester
        self.code: str = code
        self.name: str = name
        self.ch: str = ch
        self.teacher: str = teacher
        self.conflitos: list[Conflict] = []
