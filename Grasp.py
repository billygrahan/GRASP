import random

capacidade = 20
pesos = [7, 3, 4, 1, 8, 10, 9, 2, 6, 4]
precos = [5, 15, 22, 37, 14, 2, 1, 100, 22, 2]
iteracoes = 100

def avaliar(itens):
    peso = 0
    preco =0
    for i in range(0, len(itens)):
        if itens[i] == 1:
            peso = peso + pesos[i]
            preco = preco + precos[i]
    if peso <= capacidade:
        return preco
    else:
        return -1
    

def construcao():
    itens = []
    for i in range(len(pesos)):
        itens.append(0)
    LC = ["inicio"]
    auxcapacidade = 0
    while len(LC) > 0:
        soma = 0
        LC = []
        for i in range(len(itens)):
            if itens[i] == 0:
                if auxcapacidade + pesos[i] <= capacidade:
                    LC.append((i, auxcapacidade + pesos[i]))
                    soma += auxcapacidade + pesos[i]
        if len(LC) > 0:
            posicao = int(random.random()*soma)
            cont = 0
            id = 0
            for i in range(len(LC)):
                cont = cont + LC[i][1]
                if posicao <= cont:
                    id = i
                    break
            itens[LC[id][0]] = 1
            auxcapacidade += LC[id][1]
    return itens

def buscaLocal(itens):
    melhorSolucao = itens[:]
    melhorValor = avaliar(itens)

    for i in range(len(itens)):
        if itens[i] == 1:
            for j in range(len(itens)):
                if i == j:
                    continue
                else:
                    if itens[j] == 0:
                        solucao = itens[:]
                        solucao[i] = 0
                        solucao[j] = 1
                        valor = avaliar(solucao)
                        if valor > melhorValor:
                            melhorValor = valor
                            melhorSolucao = solucao[:]
    return melhorSolucao


def GRASP(iteracoes):
    melhor = []
    valor = 0
    cont = 0

    while cont < iteracoes:
        solucao = construcao()
        solucao = buscaLocal(solucao)
        novoValor = avaliar(solucao)

        if novoValor > valor:
            valor = novoValor
            melhor = solucao[:]

        cont += 1
        print("n: {} valor: {}".format(cont, valor))
    return melhor

if __name__ == "__main__":
    solucao = GRASP(iteracoes)

    print(solucao)
    print("avaliacao: {}".format(avaliar(solucao)))