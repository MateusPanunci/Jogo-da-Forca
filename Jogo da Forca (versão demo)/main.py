import os
from Agente import Agente
from Ambiente import Ambiente

def limpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("\n" + "="*50)
    print("        JOGO DA FORCA - AGENTE INTELIGENTE")
    print("="*50)
    
    # Escolher dificuldade
    print("\nEscolha a dificuldade:")
    print("1. Fácil (8 vidas)")
    print("2. Médio (6 vidas)")
    print("3. Difícil (4 vidas)")
    
    while True:
        try:
            opcao = input("\nOpção (1-3): ").strip()
            if opcao == '1':
                max_vidas = 8
                break
            elif opcao == '2':
                max_vidas = 6
                break
            elif opcao == '3':
                max_vidas = 4
                break
            else:
                print("Digite 1, 2 ou 3")
        except:
            print("Entrada inválida!")
    
    # Entrada da palavra
    print("\n" + "="*50)
    palavra = input("Insira a palavra escolhida: ").strip().upper()
    
    # Verifica se é uma palavra válida
    while len(palavra) < 3 or not all(c.isalpha() or c in "ÁÀÂÃÇÉÊÍÓÔÕÚ" for c in palavra):
        print("Por favor, digite uma palavra válida (mínimo 3 letras):")
        palavra = input("Insira a palavra escolhida: ").strip().upper()
    
    # Cria ambiente e agente
    ambiente = Ambiente(palavra, max_vidas)
    agente = Agente(ambiente, max_vidas)
    
    # Inicia jogo
    print(f"\nO agente começa com {len(agente.banco_palavras)} palavras no banco.")
    print("Ele vai aprender novas palavras durante o jogo!")
    
    tam_palavra = len(palavra)
    agente.perceber(tam_palavra)
    
    print("\n" + "="*50)
    print("         FIM DE JOGO")
    print("="*50)
    
    # Pergunta se quer jogar novamente
    while True:
        try:
            jogar_novamente = input("\nJogar novamente? (S/N): ").strip().upper()
            if jogar_novamente == 'S':
                limpaTela()
                main()
                break
            elif jogar_novamente == 'N':
                print("\nO agente agora tem {} palavras no banco.".format(len(agente.banco_palavras)))
                print("Obrigado por jogar!")
                break
            else:
                print("Digite S para Sim ou N para Não")
        except:
            print("Entrada inválida!")

if __name__ == "__main__":
    main()