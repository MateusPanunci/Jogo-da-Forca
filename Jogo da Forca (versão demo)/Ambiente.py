import time

class Ambiente:
    def __init__(self, palavraObj, max_vidas=6):
        self.palavraObj = palavraObj
        self.tam_palavra = len(palavraObj)
        self.vidas_restantes = max_vidas
        self.max_vidas = max_vidas
        self.palavraMontada = ['_' for _ in range(len(palavraObj))]
        self.letras_erradas = []

    def mostrar_estado_jogo(self):
        """Mostra o estado atual do jogo"""
        print("\n" + "="*40)
        print(f"VIDAS: {self.vidas_restantes}/{self.max_vidas}")
        
        # Desenho da forca
        estagios = [
            """
               ------
               |    |
               |
               |
               |
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |
               |
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |    |
               |
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |   /|
               |
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |   /|\\
               |
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |   /|\\
               |   /
               |
            ----------
            """,
            """
               ------
               |    |
               |    O
               |   /|\\
               |   / \\
               |
            ----------
            """
        ]
        
        erros = self.max_vidas - self.vidas_restantes
        idx = min(erros, 6)
        print(estagios[idx])
        
        print("Palavra: " + " ".join(self.palavraMontada))
        
        if self.letras_erradas:
            print(f"Letras erradas: {', '.join(self.letras_erradas)}")
        
        print("="*40 + "\n")

    def mostrarPalavra(self, flg_acertou_letra, letra_chutada):
        print("Palavra:", end=" ")

        palavraObj = self.palavraObj
        for i in range(self.tam_palavra):
            if (letra_chutada == palavraObj[i] and flg_acertou_letra == True):
                self.palavraMontada[i] = letra_chutada

        str_palavraMontada = "".join(self.palavraMontada) 

        if (str_palavraMontada == self.palavraObj):
            print(self.palavraObj)
            return True 
        else:
            print(str_palavraMontada)
            return False

    def verificarLetra(self, letra, palavra_chute):
        if (palavra_chute != ""):
            if (palavra_chute == self.palavraObj):
                print("\n--- Sim você acertou, parabéns! ---")
                return "Acertou"
            else:
                print("Não, você errou!")
                self.vidas_restantes -= 1
                return "Errou"
            
        elif (letra in self.palavraObj):
            print(f"Ambiente: A letra {letra} ESTÁ na palavra!\n")
            return True 
        else:
            print(f"Ambiente: A letra {letra} NÃO está na palavra!\n")
            self.letras_erradas.append(letra)
            self.vidas_restantes -= 1
            return False