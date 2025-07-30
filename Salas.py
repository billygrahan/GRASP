import random
import copy

iteracoes = 1000

Professores = [
    ("Mairton", 8),
    ("Reuber", 6),
    ("Cenez", 7),
    ("Tatiane", 5),
    ("Eurinardo", 9),
    ("Pytagoras", 5)
]

qtd_salas = 6
horarios_do_dia = 4
dias_da_semana = 5

def criar_salas():
    return [[["" for _ in range(dias_da_semana)] for _ in range(horarios_do_dia)] for _ in range(qtd_salas)]

def pode_alocar(salas, sala, hora, dia, professor):
    # Restrição para choque de horario
    for i, sala in enumerate(salas):
        if i != sala and sala[hora][dia] == professor:
            return False
    
    #mairton não pode dar aula na sexta a tarde
    if professor == "Mairton" and dia == 4 :
        return False
    
    return True

def construcao():
    salas = criar_salas()
    carga = {p[0]: p[1] for p in Professores}
    tentativas = 0
    while sum(carga.values()) > 0 and tentativas < 10000: # Limite de tentativas para evitar loops infinitos
        prof = random.choice([p for p in Professores if carga[p[0]] > 0])
        nome = prof[0]
        sala = random.randint(0, qtd_salas - 1)
        hora = random.randint(0, horarios_do_dia - 1)
        dia = random.randint(0, dias_da_semana - 1)

        if salas[sala][hora][dia] == "" and pode_alocar(salas, sala, hora, dia, nome):
            salas[sala][hora][dia] = nome
            carga[nome] -= 1
        tentativas += 1
    return salas

def avaliar(salas):
    prof_salas = {p[0]: set() for p in Professores}
    for i, sala in enumerate(salas):
        for linha in sala:
            for prof in linha:
                if prof != "":
                    prof_salas[prof].add(i)
    custo = sum(len(salas_set) - 1 for salas_set in prof_salas.values())
    return custo

def buscaLocal(salas):
    melhor = copy.deepcopy(salas)
    melhor_custo = avaliar(melhor)

    novo = copy.deepcopy(melhor)
    prof = random.choice([p[0] for p in Professores])
    origem = []
    for i, sala in enumerate(novo):
        for l in range(horarios_do_dia):
            for c in range(dias_da_semana):
                if sala[l][c] == prof:
                    origem.append((i, l, c))
    sala_old, hora_old, dia_old = random.choice(origem)

    tentativas = 0
    while tentativas < 100: # Limite de tentativas para evitar loops infinitos
        new_sala = random.randint(0, qtd_salas - 1)
        new_hora = random.randint(0, horarios_do_dia - 1)
        new_dia = random.randint(0, dias_da_semana - 1)
        if novo[new_sala][new_hora][new_dia] == "" and pode_alocar(novo, new_sala, new_hora, new_dia, prof):
            novo[sala_old][hora_old][dia_old] = ""
            novo[new_sala][new_hora][new_dia] = prof
            break
        #elif novo[new_sala][new_hora][new_dia] != "" and
        tentativas += 1

    custo_novo = avaliar(novo)
    if custo_novo < melhor_custo:
        melhor = novo
        melhor_custo = custo_novo

    return melhor

def GRASP(iteracoes):
    melhor_solucao = None
    melhor_custo = float("inf") # Valor muito alto
                                # para iniciar a comparação.

    for i in range(iteracoes):
        solucao = construcao()
        solucao = buscaLocal(solucao)
        custo = avaliar(solucao)
        print(f"Iteração {i+1}: Custo = {melhor_custo}")
        if custo < melhor_custo:
            melhor_solucao = solucao
            melhor_custo = custo

    return melhor_solucao, melhor_custo


if __name__ == "__main__":
    solucao, custo = GRASP(iteracoes)

    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex"]
    horarios = ["08h", "10h", "13h", "D15h"]

    print("\nSolução final:")
    print(f"Custo = {custo}")
    for idx, sala in enumerate(solucao):
        print(f"\nSala {idx + 1}:")

        header = "        " + "  ".join(f"{dia:^10}" for dia in dias_semana)
        print(header)
        print("        " + "-" * (len(dias_semana) * 12))

        for i, linha in enumerate(sala):
            linha_formatada = f"{horarios[i]:<5} | " + "  ".join(f"{prof if prof else '':^10}" for prof in linha)
            print(linha_formatada)
