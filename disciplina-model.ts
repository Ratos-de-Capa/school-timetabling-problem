export class Disciplina {
  curso: string;
  semestre: string;
  codigo: string;
  nome: string;
  ch: string;
  prof: string;
  //conflitos: Conflito[];
}

export class Conflito {
  codigo: string;
  type: string | number;
}

let vertexs: Disciplina[];