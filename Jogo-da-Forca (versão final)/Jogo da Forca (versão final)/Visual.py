# visual.py
import os

class Visual:
    @staticmethod
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def mostrar_forca(erros, max_erros=6):
        """Mostra o desenho da forca baseado no número de erros"""
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
        
        # Ajusta para o número máximo de erros
        if max_erros != 6:
            idx = int((erros / max_erros) * 6)
            idx = min(idx, 6)
        else:
            idx = min(erros, 6)
        
        print(estagios[idx])
    
    @staticmethod
    def mostrar_palavra_oculta(palavra_montada):
        """Mostra a palavra com as letras descobertas"""
        print("\n" + " " * 15 + " ".join(palavra_montada) + "\n")
    
    @staticmethod
    def mostrar_letras_tentadas(certas, erradas):
        """Mostra as letras já tentadas"""
        print("Letras certas: " + " ".join(sorted(certas)) if certas else "Letras certas: Nenhuma")
        print("Letras erradas: " + " ".join(sorted(erradas)) if erradas else "Letras erradas: Nenhuma")
    
    @staticmethod
    def mostrar_status(tentativas_restantes, max_tentativas):
        """Mostra o status das tentativas"""
        print(f"\nTentativas restantes: {tentativas_restantes}/{max_tentativas}")
    
    @staticmethod
    def mostrar_titulo(titulo):
        """Mostra um título formatado"""
        print("=" * 50)
        print(f"{titulo:^50}")
        print("=" * 50)