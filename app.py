from pyamaze import maze, agent
from queue import PriorityQueue

destino = (1, 1)

def h_score(celula, destino):
    linhac = celula[0]
    colunac = celula[1]
    linhad = destino[0]
    colunad = destino[1]
    return abs(colunac - colunad) + abs(linhac - linhad)

def aestrela(labirinto):
    #Criar tabuleiro com valores infinitos:
    f_score = {celula: float("inf") for celula in labirinto.grid}
    #Criar Dicionário g_score:
    g_score = {}
    #Calcular célula inicial:
    celula_inicial = (labirinto.rows, labirinto.cols)
    g_score[celula_inicial] = 0
    f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial, destino)

    #Criando a Fila:
    fila = PriorityQueue()
    #Adicionando item na Fila:
    item = (f_score[celula_inicial], h_score(celula_inicial, destino), celula_inicial)
    fila.put(item)

    caminho = {}
    #Caminhando utilizando a Fila:
    while not fila.empty():
        celula = fila.get()[2]

        #Se a celula for o destino final, interrompe o loop:
        if celula == destino:
            break

        #Verficando as Direções Possíveis:
        for direcao in "NSEW":
            if labirinto.maze_map[celula][direcao] == 1:
                #Posição da célula atual:
                linha_celula = celula[0]
                coluna_celula = celula[1]
                #Calculando a Posição da Próxima Célula:
                if direcao == "N":
                    proxima_celula = (linha_celula - 1, coluna_celula)
                elif direcao == "S":
                    proxima_celula = (linha_celula + 1, coluna_celula)
                elif direcao == "W":
                    proxima_celula = (linha_celula, coluna_celula - 1)
                elif direcao == "E":
                    proxima_celula = (linha_celula, coluna_celula + 1)
                #Calculando o g_score da próxima célula:
                novo_g_score = g_score[celula] + 1
                #Calculando o f_score para a próxima célula:
                novo_f_score = novo_g_score + h_score(proxima_celula, destino)

                #Verificando o f_score e atualizando os valores:
                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    #atualizando a fila:
                    item = (novo_f_score, h_score(proxima_celula, destino), proxima_celula)
                    fila.put(item)
                    caminho[proxima_celula] = celula

    #Criando o caminho final, a rota perfeita:
    caminho_final = {}
    celula_analisada = destino
    print("Celulas analisadas", len(caminho.keys()))
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    return caminho_final

labirinto = maze(50, 50)
labirinto.CreateMaze()

agente = agent(labirinto, filled=True, footprints=True)
caminho = aestrela(labirinto)
labirinto.tracePath({agente: caminho}, delay=100)

print("Total de celulas", len(labirinto.maze_map.keys()))

labirinto.run()
