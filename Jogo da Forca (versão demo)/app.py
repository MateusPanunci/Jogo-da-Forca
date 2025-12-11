import flet as ft
import time
import threading
import math
from Agente import Agente
from Ambiente import Ambiente

# --- COMPONENTE VISUAL DA FORCA (GRÁFICO) ---
def criar_forca_grafica():
    cor_madeira = "brown"
    cor_corpo = "black"
    cor_corda = "orange"
    
    base = ft.Container(width=150, height=5, bgcolor=cor_madeira, bottom=0, left=25)
    poste = ft.Container(width=5, height=200, bgcolor=cor_madeira, bottom=0, left=50)
    topo = ft.Container(width=100, height=5, bgcolor=cor_madeira, bottom=200, left=50)
    corda = ft.Container(width=2, height=30, bgcolor=cor_corda, top=0, left=140)
    
    cabeca = ft.Container(
        width=40, height=40, border=ft.border.all(3, cor_corpo), border_radius=20,
        top=30, left=121, opacity=0, animate_opacity=300
    )
    tronco = ft.Container(
        width=3, height=60, bgcolor=cor_corpo, top=70, left=140, 
        opacity=0, animate_opacity=300
    )
    braco_esq = ft.Container(
        width=40, height=3, bgcolor=cor_corpo, top=90, left=102, 
        rotate=ft.Rotate(math.pi / 4), opacity=0, animate_opacity=300
    )
    braco_dir = ft.Container(
        width=40, height=3, bgcolor=cor_corpo, top=90, left=141, 
        rotate=ft.Rotate(-math.pi / 4), opacity=0, animate_opacity=300
    )
    perna_esq = ft.Container(
        width=40, height=3, bgcolor=cor_corpo, top=145, left=102, 
        rotate=ft.Rotate(-math.pi / 4), opacity=0, animate_opacity=300
    )
    perna_dir = ft.Container(
        width=40, height=3, bgcolor=cor_corpo, top=145, left=141, 
        rotate=ft.Rotate(math.pi / 4), opacity=0, animate_opacity=300
    )

    cenario = ft.Stack(
        controls=[base, poste, topo, corda, perna_esq, perna_dir, braco_esq, braco_dir, tronco, cabeca],
        width=200, height=220
    )
    partes_corpo = [cabeca, tronco, braco_esq, braco_dir, perna_esq, perna_dir]
    return cenario, partes_corpo

# --- LOGGING ---
class AppLogger:
    def __init__(self, text_control, scroll_container, page):
        self.text_control = text_control
        self.scroll_container = scroll_container
        self.page = page

    def log(self, message):
        self.text_control.value += f"{message}\n"
        self.page.update()
        try:
            self.scroll_container.scroll_to(offset=-1, duration=300)
        except:
            pass

# --- MAIN APP ---
def main(page: ft.Page):
    page.title = "Jogo da Forca - IA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 850
    page.scroll = "auto"
    
    titulo = ft.Text("🤖 Agente da Forca", size=30, weight="bold", color="blue")
    subtitulo = ft.Text("Defina uma palavra e veja a IA jogar", size=16, color="grey")

    txt_palavra = ft.TextField(label="Palavra Secreta", password=True, can_reveal_password=True)
    dd_dificuldade = ft.Dropdown(
        label="Dificuldade",
        options=[
            ft.dropdown.Option("1", "Fácil (8 vidas)"),
            ft.dropdown.Option("2", "Médio (6 vidas)"),
            ft.dropdown.Option("3", "Difícil (4 vidas)"),
        ],
        value="2"
    )

    lbl_vidas = ft.Text("Vidas: --/--", size=20, weight="bold")
    lbl_palavra = ft.Text("_ _ _ _ _", size=30, weight="bold", font_family="monospace")
    
    visual_forca, partes_forca = criar_forca_grafica()
    
    txt_log = ft.Text("", size=12, selectable=True)
    container_log = ft.Column(
        [ft.Text("🧠 Pensamentos do Agente:", weight="bold"), txt_log],
        scroll=ft.ScrollMode.AUTO,
        height=200, 
    )

    btn_iniciar = ft.ElevatedButton("Iniciar Jogo", icon="play_arrow")

    def jogar_thread(palavra_secreta, max_vidas):
        logger = AppLogger(txt_log, container_log, page)
        def app_print(texto="", end="\n"):
            logger.log(str(texto))

        for parte in partes_forca:
            parte.opacity = 0
        page.update()

        try:
            ambiente = Ambiente(palavra_secreta, max_vidas)
            agente = Agente(ambiente, max_vidas)
        except Exception as e:
            app_print(f"Erro ao inicializar: {e}")
            return

        def atualizar_interface_visual():
            lbl_vidas.value = f"Vidas: {ambiente.vidas_restantes}/{ambiente.max_vidas}"
            lbl_palavra.value = " ".join(ambiente.palavraMontada)
            erros = ambiente.max_vidas - ambiente.vidas_restantes
            erros_visiveis = min(erros, 6)
            for i in range(erros_visiveis):
                partes_forca[i].opacity = 1
            page.update()

        ambiente.mostrar_estado_jogo = atualizar_interface_visual
        
        agente.tam_palavra = len(palavra_secreta)
        app_print(f"--- Iniciando: Palavra com {len(palavra_secreta)} letras ---")
        
        while not agente.Objetivo and ambiente.vidas_restantes > 0:
            ambiente.mostrar_estado_jogo()
            app_print("Agente está pensando...")
            time.sleep(1.0)
            
            letra_chute, palavra_chute = agente.agir()
            
            if palavra_chute:
                if len(agente.banco_filtrado) == 1:
                    app_print(f"💡 Agente: Só pode ser '{palavra_chute}'!")
                else:
                    app_print(f"🎲 Agente arriscou a palavra: {palavra_chute}")
            elif letra_chute:
                app_print(f"Agente escolheu a letra: {letra_chute}")
            else:
                app_print("Agente desistiu (sem opções).")
                break
            
            resultado = ambiente.verificarLetra(letra_chute, palavra_chute)
            
            if resultado == True:
                agente.letrasCertas.append(letra_chute)
            elif resultado == False:
                agente.letrasErradas.append(letra_chute)
            elif resultado == "Acertou":
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(palavra_chute)
                break
            elif resultado == "Errou":
                if palavra_chute:
                    # CORREÇÃO CRUCIAL: Adiciona a palavra errada à lista negra do agente
                    agente.palavrasErradas.append(palavra_chute) 
                    app_print(f"❌ '{palavra_chute}' não é a palavra. Agente aprendeu isso.")
            
            flg_acertou = ambiente.mostrarPalavra(resultado == True, letra_chute if letra_chute else "")
            if flg_acertou:
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
                break
            
            time.sleep(0.5)

        ambiente.mostrar_estado_jogo()
        if agente.Objetivo:
            app_print("\n🎉 VITÓRIA! O Agente acertou! 🎉")
            lbl_palavra.color = "green"
            lbl_palavra.value = palavra_secreta
        else:
            app_print(f"\n💀 DERROTA! A palavra era: {ambiente.palavraObj}")
            lbl_palavra.color = "red"
            lbl_palavra.value = palavra_secreta
            agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
            
        btn_iniciar.disabled = False
        page.update()

    def on_click_iniciar(e):
        palavra = txt_palavra.value.strip().upper()
        if len(palavra) < 3:
            txt_log.value = "❌ Erro: Digite uma palavra válida (min 3 letras)!"
            page.update()
            return
        max_vidas = {"1": 8, "2": 6, "3": 4}[dd_dificuldade.value]
        btn_iniciar.disabled = True
        txt_log.value = "Iniciando...\n"
        lbl_palavra.color = "black"
        lbl_palavra.value = "_ " * len(palavra)
        page.update()
        threading.Thread(target=jogar_thread, args=(palavra, max_vidas)).start()

    btn_iniciar.on_click = on_click_iniciar

    page.add(
        titulo, subtitulo, ft.Divider(),
        txt_palavra, dd_dificuldade, btn_iniciar, ft.Divider(),
        ft.Container(
            content=ft.Column([
                lbl_vidas, ft.Container(height=20), 
                visual_forca, ft.Container(height=20), 
                lbl_palavra
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, border=ft.border.all(1, "grey"), border_radius=10, bgcolor="#E3F2FD"
        ),
        ft.Divider(), container_log
    )

ft.app(target=main)