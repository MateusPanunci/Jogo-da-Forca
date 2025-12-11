from Ambiente import Ambiente
import random
import time 


class Agente:
    def __init__(self, ambiente: Ambiente, max_vidas=6):
        self.banco_palavras = []
        self.banco_filtrado = []
        self.letrasCertas = []
        self.letrasErradas = []
        self.Objetivo = False
        self.ambiente = ambiente
        self.letras = list("AÁÀÂÃBCÇDEÉÊFGHIÍJKLMNOÓÔÕPQRSTUÚVWXYZ")
        self.max_vidas = max_vidas
        
        # Carregar banco de palavras (começa vazio e cresce)
        self.carregar_banco_palavras()
        
        # Verifica que banco_agente.txt ta atualizado
        try:
            with open('banco_agente.txt', 'r', encoding='utf-8') as f:
                palavras_salvas = len([linha.strip() for linha in f if linha.strip()])
                print(f"Banco salvo tem {palavras_salvas} palavras.")
        except FileNotFoundError:
            print("banco_agente.txt ainda não existe, será criado quando salvar.")
    
    def carregar_banco_palavras(self):
        """Carrega o banco de palavras do arquivo externo e salva no interno"""
        try:
            # Le do banco_externo.txt
            with open('banco_externo.txt', 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    palavra_limpa = linha.strip().upper()
                    if palavra_limpa and len(palavra_limpa) >= 3:
                        self.banco_palavras.append(palavra_limpa)
            
            print(f"Banco do Agente: {len(self.banco_palavras)} palavras carregadas do banco_externo.txt")
            
            # Salva no banco_agente.txt
            self.salvar_banco_palavras()
                
        except FileNotFoundError:
            print("Arquivo banco_externo.txt não encontrado. Criando novo banco inicial...")
            self.banco_palavras = ["PYTHON", "JAVA", "FORCA", "PROGRAMA", "COMPUTADOR", 
                                "JOGO", "DADOS", "ALGORITMO", "INTELIGENCIA", "ARTIFICIAL"]
            self.salvar_banco_palavras()
    
    def salvar_banco_palavras(self):
        """Salva o banco de palavras atualizado"""

        try:
            with open('banco_agente.txt', 'w', encoding='utf-8') as arquivo:
                for palavra in sorted(set(self.banco_palavras)):  # Remove duplicatas
                    arquivo.write(palavra + '\n')
        except Exception as e:
            print(f"Erro ao salvar banco: {e}")
    
    def adicionar_palavra_ao_banco(self, palavra):
        """Adiciona uma nova palavra ao banco se não existir"""
        palavra = palavra.upper()
        if palavra not in self.banco_palavras and len(palavra) >= 3:
            self.banco_palavras.append(palavra)
            print(f"Palavra '{palavra}' adicionada ao banco do agente!")
            self.salvar_banco_palavras()
    
    def filtrar(self):
        if not self.banco_filtrado:
            # Filtragem de palavras com mesmo tamanho
            self.banco_filtrado = [
                palavra for palavra in self.banco_palavras
                if len(palavra) == self.ambiente.tam_palavra
            ]
        else:
            # Filtragem nas letras certas e erradas
            filtro = self.ambiente.palavraMontada
            
            self.banco_filtrado = [
                palavra for palavra in self.banco_filtrado
                if all(
                    (filtro[i] == '_' or palavra[i] == filtro[i]) and 
                    palavra[i] not in self.letrasErradas
                    for i in range(len(palavra))
                )
            ]
    
    def conta_freq_letras(self):
        freq_letras = {}

        for letra in self.letras:
            if letra in self.letrasCertas or letra in self.letrasErradas: 
                continue

            contador = 0 
            for palavra in self.banco_filtrado:  
                if letra in palavra: 
                    contador += 1
            
            if len(self.banco_filtrado) > 0:
                freq_letras[letra] = contador/len(self.banco_filtrado)

        return freq_letras

    def agir(self):
        self.filtrar()
        
        # Se nao tem palavras no banco filtrado, tenta letras comuns
        if len(self.banco_filtrado) == 0:
            print("Agente: Não conheço palavras assim... Tentando letras comuns")
            
            # Ordem de frequencia de letras em portugues
            ordem_letras = ['E', 'A', 'O', 'S', 'I', 'R', 'N', 'D', 'M', 'U', 
                        'T', 'C', 'L', 'P', 'V', 'G', 'H', 'Q', 'B', 'F', 
                        'Z', 'J', 'X', 'K', 'W', 'Y']
            
            for letra in ordem_letras:
                if (letra not in self.letrasCertas and 
                    letra not in self.letrasErradas and 
                    letra in self.letras):
                    print(f"Agente: A letra {letra} está na palavra?")
                    return letra, ""
            
            # Se todas as letras comuns foram tentadas, tentar qualquer uma
            for letra in self.letras:
                if letra not in self.letrasCertas and letra not in self.letrasErradas:
                    print(f"Agente: A letra {letra} está na palavra?")
                    return letra, ""
            
            return None, None
        
        print(f"Palavras possíveis no banco: {len(self.banco_filtrado)}")
        
        # Mostrar as palavras quando são poucas
        if len(self.banco_filtrado) <= 5:
            print(f"(Palavras possíveis: {', '.join(self.banco_filtrado)})")
        
        # Chutar se tem 1-3 palavras e estamos com poucas vidas
        if len(self.banco_filtrado) <= 3 and self.ambiente.vidas_restantes > 0:
            # Se só tem UMA palavra é certeza
            if len(self.banco_filtrado) <= 3 and self.ambiente.vidas_restantes > 0:
                # Escolhe uma palavra ALEATÓRIA da lista
                palavra_chute = random.choice(self.banco_filtrado)
                
                if len(self.banco_filtrado) == 1:
                    print(f"Agente: Deve ser '{palavra_chute}'!")
                else:
                    print(f"Agente: Talvez seja '{palavra_chute}'?")
                return None, palavra_chute
            else:
                # Se tem 2-3 palavras, tentar a primeira
                palavra_chute = self.banco_filtrado[0]
                print(f"Agente: Talvez seja '{palavra_chute}'?")
                return None, palavra_chute
        
        # Escolhe a melhor letra baseada na frequência
        freq_letras = self.conta_freq_letras()
        if freq_letras:
            melhor_letra = max(freq_letras, key=freq_letras.get)
            print(f"Agente: A letra {melhor_letra} está na palavra?")
            return melhor_letra, ""
        
        return None, None

    def perceber(self, tam_palavra):
        self.tam_palavra = tam_palavra

        while not self.Objetivo and self.ambiente.vidas_restantes > 0:
            self.ambiente.mostrar_estado_jogo()
            
            letra_chute, palavra_chute = self.agir()
            
            if letra_chute is None and palavra_chute is None:
                print("Agente: Não sei mais o que tentar!")
                break
            
            time.sleep(1.5)

            resultado = self.ambiente.verificarLetra(letra_chute, palavra_chute)
            
            if resultado == True:
                self.letrasCertas.append(letra_chute)
            elif resultado == False:
                self.letrasErradas.append(letra_chute)
            elif resultado == "Acertou":
                self.Objetivo = True
                # Se acertou a palavra, adiciona ao banco
                self.adicionar_palavra_ao_banco(palavra_chute)
                break
            elif resultado == "Errou":
                if palavra_chute:
                    self.letrasErradas.extend([l for l in palavra_chute if l not in self.letrasErradas])
            
            # Ve se completou a palavra com letras
            flg_acertou_palavra = self.ambiente.mostrarPalavra(resultado == True, letra_chute if letra_chute else "")
            if flg_acertou_palavra:
                self.Objetivo = True
                # Se descobriu a palavra letra por letra, adiciona ao banco
                self.adicionar_palavra_ao_banco(self.ambiente.palavraObj)
                break
            
            time.sleep(1)
        
        # resultado final
        self.ambiente.mostrar_estado_jogo()
        if self.Objetivo:
            print("\n🎉 AGENTE VENCEU! 🎉")
        else:
            print(f"\n💀 AGENTE PERDEU! A palavra era: {self.ambiente.palavraObj}")
            # adiciona a palavra ao banco para aprender
            self.adicionar_palavra_ao_banco(self.ambiente.palavraObj)