import flet as ft
import time
import threading
import math
from Agente import Agente
from Ambiente import Ambiente

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

class AppLogger:
    def __init__(self, list_view_control, page):
        self.list_view = list_view_control
        self.page = page

    def log(self, message):
        cor_texto = "#333333"
        icone = "•"
        
        if "VITÓRIA" in message: cor_texto = "green"
        elif "DERROTA" in message: cor_texto = "red"
        elif "Certeza" in message: cor_texto = "blue"
        elif "Arriscando" in message: cor_texto = "#E65100"

        item = ft.Container(
            content=ft.Row([
                ft.Text(icone, color="#9E9E9E", size=10),
                ft.Text(message, color=cor_texto, font_family="Consolas, monospace", size=13, selectable=True)
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.only(bottom=5)
        )
        
        self.list_view.controls.append(item)
        self.page.update()

def main(page: ft.Page):
    page.title = "Jogo da Forca - IA vs Humano"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000 
    page.window_height = 700
    page.padding = 20
    page.bgcolor = "#F5F7FA"
    
    
    titulo = ft.Container(
        content=ft.Row([
            ft.Icon("psychology", color="white", size=28),
            ft.Text("Configuração", size=20, weight="bold", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="#2196F3",
        padding=15,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=5, color="#00000020")
    )
    
    txt_palavra = ft.TextField(
        label="Palavra Secreta", 
        password=True, 
        can_reveal_password=True,
        border_color="#2196F3",
        text_size=14,
        dense=True
    )
    
    dd_dificuldade = ft.Dropdown(
        label="Dificuldade",
        options=[
            ft.dropdown.Option("1", "Fácil (8 vidas)"),
            ft.dropdown.Option("2", "Médio (6 vidas)"),
            ft.dropdown.Option("3", "Difícil (4 vidas)"),
        ],
        value="2",
        border_color="#2196F3",
        text_size=14,
        dense=True
    )

    btn_iniciar = ft.Container(
        content=ft.Text("INICIAR / REINICIAR", size=14, weight="bold", color="white"),
        bgcolor="#4CAF50",
        padding=12,
        border_radius=8,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=5, color="#00000020"),
        animate=ft.Animation(300, "easeOut"),
        on_click=None
    )

    lbl_vidas = ft.Text("Vidas: --", size=18, weight="bold", color="#FF5722")
    
    lbl_palavra = ft.Text(
        "_ _ _ _ _", 
        size=32, 
        weight="bold", 
        font_family="monospace",
        color="#2196F3",
        text_align=ft.TextAlign.CENTER
    )
    
    visual_forca, partes_forca = criar_forca_grafica()
    
    area_visual_jogo = ft.Container(
        content=ft.Column([
            lbl_vidas,
            ft.Container(height=10),
            visual_forca,
            ft.Container(height=10),
            lbl_palavra
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        border_radius=15,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
        alignment=ft.alignment.center
    )


    lista_log = ft.ListView(
        expand=True,
        spacing=2,
        padding=10,
        auto_scroll=True,
    )

    area_cerebro = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon("terminal", color="#424242", size=20),
                    ft.Text("RACIOCÍNIO DO AGENTE", color="#424242", weight="bold", size=14),
                    ft.Container(expand=True),
                    ft.Icon("memory", color="#2196F3", size=20)
                ]),
                padding=ft.padding.only(bottom=10),
                border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0"))
            ),
            lista_log
        ]),
        border_radius=15,
        bgcolor="white",
        padding=15,
        shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
        expand=True
    )


    coluna_esquerda = ft.Column(
        controls=[
            titulo,
            ft.Container(height=10),
            txt_palavra,
            dd_dificuldade,
            btn_iniciar,
            ft.Divider(),
            area_visual_jogo
        ],
        width=300,
        scroll=ft.ScrollMode.AUTO
    )

    layout_principal = ft.Row(
        controls=[
            coluna_esquerda,
            ft.VerticalDivider(width=20, color="transparent"),
            area_cerebro
        ],
        expand=True
    )

    def jogar_thread(palavra_secreta, max_vidas):
        logger = AppLogger(lista_log, page)
        
        def app_print(texto="", end="\n"):
            logger.log(str(texto))

        for parte in partes_forca:
            parte.opacity = 0
        page.update()

        try:
            ambiente = Ambiente(palavra_secreta, max_vidas)
            agente = Agente(ambiente, max_vidas)
        except Exception as e:
            app_print(f"Erro Crítico: {e}")
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
        app_print(f"--- NOVA PARTIDA INICIADA ---")
        app_print(f"Alvo: Palavra de {len(palavra_secreta)} letras")
        app_print(f"Conhecimento: {len(agente.banco_palavras)} palavras no banco.")
        
        while not agente.Objetivo and ambiente.vidas_restantes > 0:
            ambiente.mostrar_estado_jogo()
            app_print("Processando...")
            time.sleep(1.0)
            
            letra_chute, palavra_chute = agente.agir()
            
            if palavra_chute:
                if len(agente.banco_filtrado) <= 2:
                    app_print(f"💡 ALTA CONFIANÇA: Chute '{palavra_chute}'")
                else:
                    app_print(f"🎲 TENTATIVA DE RISCO: '{palavra_chute}'")
            elif letra_chute:
                app_print(f"🔎 Analisando letra: [{letra_chute}]")
            else:
                app_print("⚠️ Falha lógica: Sem opções viáveis.")
                break
            
            resultado = ambiente.verificarLetra(letra_chute, palavra_chute)
            
            if resultado == True:
                agente.letrasCertas.append(letra_chute)
                app_print(f"✅ Sucesso! A letra '{letra_chute}' existe.")
            elif resultado == False:
                agente.letrasErradas.append(letra_chute)
                app_print(f"❌ Falha. A letra '{letra_chute}' não existe.")
            elif resultado == "Acertou":
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(palavra_chute)
                break
            elif resultado == "Errou":
                if palavra_chute:
                    agente.palavrasErradas.append(palavra_chute)
                    app_print(f"🚫 A palavra '{palavra_chute}' está incorreta.")
            
            flg_acertou = ambiente.mostrarPalavra(resultado == True, letra_chute if letra_chute else "")
            if flg_acertou:
                agente.Objetivo = True
                agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
                break
            
            time.sleep(0.3)

        ambiente.mostrar_estado_jogo()
        if agente.Objetivo:
            app_print(f"🎉 VITÓRIA! Palavra descoberta: {palavra_secreta}")
            lbl_palavra.color = "#4CAF50"
            lbl_palavra.value = palavra_secreta
        else:
            app_print(f"💀 DERROTA. A palavra era: {palavra_secreta}")
            lbl_palavra.color = "#F44336"
            lbl_palavra.value = palavra_secreta
            agente.adicionar_palavra_ao_banco(ambiente.palavraObj)
            
        btn_iniciar.disabled = False
        btn_iniciar.opacity = 1
        page.update()

    def on_click_iniciar(e):
        palavra = txt_palavra.value.strip().upper()
        if len(palavra) < 3:
            item_erro = ft.Text("⚠️ Digite uma palavra válida (min 3 letras)!", color="red")
            lista_log.controls.append(item_erro)
            page.update()
            return
            
        max_vidas = {"1": 8, "2": 6, "3": 4}[dd_dificuldade.value]

        btn_iniciar.disabled = True
        btn_iniciar.opacity = 0.5
        
        lista_log.controls.clear()
        
        lbl_palavra.color = "#2196F3"
        lbl_palavra.value = "_ " * len(palavra)
        page.update()

        threading.Thread(target=jogar_thread, args=(palavra, max_vidas)).start()

    btn_iniciar.on_click = on_click_iniciar

    page.add(layout_principal)

ft.app(target=main)