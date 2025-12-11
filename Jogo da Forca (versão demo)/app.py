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
        # Adiciona quebra de linha visual para separar pensamentos
        self.text_control.value += f"• {message}\n\n"
        self.page.update()
        try:
            self.scroll_container.scroll_to(offset=-1, duration=300)
        except:
            pass

# --- MAIN APP ---
def main(page: ft.Page):
    page.title = "Jogo da Forca - IA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000  # Janela mais larga para caber tudo
    page.window_height = 700
    page.padding = 20
    
    # --- LADO ESQUERDO: CONTROLES E JOGO ---
    
    titulo = ft.Text("🤖 Forca IA", size=30, weight="bold", color="blue")
    
    txt_palavra = ft.TextField(
        label="Palavra Secreta", 
        password=True, 
        can_reveal_password=True,
        width=250
    )
    
    dd_dificuldade = ft.Dropdown(
        label="Dificuldade",
        options=[
            ft.dropdown.Option("1", "Fácil (8 vidas)"),
            ft.dropdown.Option("2", "Médio (6 vidas)"),
            ft.dropdown.Option("3", "Difícil (4 vidas)"),
        ],
        value="2",
        width=150
    )

    btn_iniciar = ft.ElevatedButton(
        "INICIAR JOGO", 
        icon="play_arrow", 
        style=ft.ButtonStyle(
            color="white", 
            bgcolor="green", 
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        height=50,
        width=400
    )

    lbl_vidas = ft.Text("Vidas: --/--", size=20, weight="bold")
    lbl_palavra = ft.Text(
        "_ _ _ _ _", 
        size=35, 
        weight="bold", 
        font_family="monospace",
        color="blue"
    )
    
    visual_forca, partes_forca = criar_forca_grafica()
    
    # Container do visual do jogo (Fundo azulado claro)
    area_jogo = ft.Container(
        content=ft.Column([
            lbl_vidas,
            ft.Container(height=10),
            visual_forca,
            ft.Container(height=30),
            lbl_palavra
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30,
        border=ft.border.all(1, "grey"),
        border_radius=15,
        bgcolor="#F0F4F8",
        alignment=ft.alignment.center
    )

    coluna_esquerda = ft.Column(
        controls=[
            titulo,
            ft.Row([txt_palavra, dd_dificuldade], alignment="spaceBetween"),
            ft.Container(height=10),
            btn_iniciar,
            ft.Container(height=20),
            area_jogo
        ],
        width=450,
        scroll="auto"
    )

    # --- LADO DIREITO: CÉREBRO DA IA ---
    
    txt_log = ft.Text(
        "", 
        size=16,          # Letra maior
        font_family="Consolas, monospace", 
        color="#333333",
        selectable=True
    )
    
    container_log = ft.Column(
        [txt_log],
        scroll=ft.ScrollMode.ALWAYS, # Sempre permite scroll
        auto_scroll=True,
    )

    # Container estilo "Terminal" ou "Log Card"
    area_cerebro = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon("psychology", color="white"),
                    ft.Text("PENSAMENTOS DO AGENTE", color="white", weight="bold")
                ]),
                bgcolor="blue",
                padding=10,
                border_radius=ft.border_radius.only(top_left=10, top_right=10)
            ),
            ft.Container(
                content=container_log,
                padding=15,
                expand=True # Ocupa todo o espaço restante vertical
            )
        ]),
        border=ft.border.all(1, "grey"),
        border_radius=10,
        bgcolor="white",
        expand=True # Ocupa todo o espaço restante horizontal
    )

    coluna_direita = ft.Column(
        controls=[area_cerebro],
        expand=True
    )

    # --- LÓGICA DO JOGO ---
    def jogar_thread(palavra_secreta, max_vidas):
        logger = AppLogger(txt_log, container_log, page)
        
        def app_print(texto="", end="\n"):
            logger.log(str(texto))

        # Reset visual
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
        app_print(f"--- NOVA PARTIDA: Palavra de {len(palavra_secreta)} letras ---")
        app_print(f"Memória: {len(agente.banco_palavras)} palavras conhecidas.")
        
        while not agente.Objetivo and ambiente.vidas_restantes > 0:
            ambiente.mostrar_estado_jogo()
            app_print("🤔 Analisando possibilidades...")
            time.sleep(1.2) # Um pouco mais lento para ler os pensamentos
            
            letra_chute, palavra_chute = agente.agir()
            
            if palavra_chute:
                if len(agente.banco_filtrado) == 1:
                    app_print(f"💡 Certeza absoluta: É '{palavra_chute}'!")
                else:
                    app_print(f"🎲 Arriscando tudo na palavra: '{palavra_chute}'")
            elif letra_chute:
                app_print(f"👉 Escolho a letra: {letra_chute}")
            else:
                app_print("😓 Não sei mais o que fazer...")
                break
            
            resultado = ambiente.verificarLetra(letra_chute, palavra_chute)
            
            if resultado == True:
                agente.letrasCertas.append(letra_chute)
                app_print("✅ Acertei a letra!")
            elif resultado == False:
                agente.letrasErradas.append(letra_chute)
                app_print("❌ Errei a letra...")
            elif resultado == "Acertou":
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(palavra_chute)
                break
            elif resultado == "Errou":
                if palavra_chute:
                    agente.palavrasErradas.append(palavra_chute)
                    app_print(f"🚫 '{palavra_chute}' não é a palavra.")
            
            flg_acertou = ambiente.mostrarPalavra(resultado == True, letra_chute if letra_chute else "")
            if flg_acertou:
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
                break
            
            time.sleep(0.5)

        ambiente.mostrar_estado_jogo()
        if agente.Objetivo:
            app_print(f"\n🎉 VITÓRIA! A palavra era {palavra_secreta} 🎉")
            lbl_palavra.color = "green"
            lbl_palavra.value = palavra_secreta
        else:
            app_print(f"\n💀 DERROTA... A palavra era {palavra_secreta}")
            lbl_palavra.color = "red"
            lbl_palavra.value = palavra_secreta
            agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
            
        btn_iniciar.disabled = False
        btn_iniciar.text = "JOGAR NOVAMENTE"
        page.update()

    def on_click_iniciar(e):
        palavra = txt_palavra.value.strip().upper()
        if len(palavra) < 3:
            txt_log.value = "⚠️ Digite uma palavra válida (min 3 letras)!"
            page.update()
            return
            
        max_vidas = {"1": 8, "2": 6, "3": 4}[dd_dificuldade.value]

        btn_iniciar.disabled = True
        txt_log.value = "" # Limpa o log antigo
        lbl_palavra.color = "blue"
        lbl_palavra.value = "_ " * len(palavra)
        page.update()

        threading.Thread(target=jogar_thread, args=(palavra, max_vidas)).start()

    btn_iniciar.on_click = on_click_iniciar

    # MONTAGEM FINAL DO LAYOUT (Lado a Lado)
    layout_principal = ft.Row(
        controls=[coluna_esquerda, coluna_direita],
        expand=True, # Ocupa toda a tela
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.add(layout_principal)

ft.app(target=main)