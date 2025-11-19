import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from Interface.app_state import app_state
from classes.login import user_login

from utils.Validate_CPF import validate_cpf
from auth.validateAcess import authorize_access


def openMainPage(root):
    acessValidator = authorize_access()

    if acessValidator == False:
        messagebox.showerror("Error", "Licença não encontrada. Execução não autorizada, fale com o seu administrador.")
        return

    # --------------------------------------- #
    # FUNÇÕES
    # --------------------------------------- #

    def save_and_close():
        """Captura os valores e salva no app_state."""

        user = User_entry.get()
        password = Password_entry.get()
        user_login.set_data(user, password)

        inscricao_estadual = Ie_entry.get()
        mes = Month_entry.get()
        ano = Year_entry.get()
        tipo = tipo_var.get()  # "CFE" ou "NFCE"

        # Salvar no estado global (app_state já adaptado com tipo)
        app_state.set_data(inscricao_estadual, mes, ano, tipo)
        app_state.autorizationNext(True)

        root.destroy()

    def check_and_save():

        cpf = User_entry.get()
        year = Year_entry.get()
        month = Month_entry.get()
        companyCode = Ie_entry.get()
        password = Password_entry.get()

        if not validate_cpf(cpf):
            messagebox.showerror("Error", "CPF Inválido. Por favor, digite um CPF válido.")
            return

        if len(year) != 4:
            messagebox.showerror("Error", "Ano Inválido. O ano deve ter um padrão de 4 dígitos.")
            return

        if len(month) == 0:
            messagebox.showerror("Error", "Mês Inválido. Informe o mês.")
            return

        try:
            month_int = int(month)
        except ValueError:
            messagebox.showerror("Error", "Mês Inválido. Use apenas números.")
            return

        if month_int < 1 or month_int > 12:
            messagebox.showerror("Error", "Mês Inválido. O mês deve estar entre 1 e 12.")
            return

        if len(companyCode) != 9:
            messagebox.showerror("Error", "Inscrição da Empresa Inválida. O código deve ter 9 dígitos.")
            return

        if not password:
            messagebox.showerror("Error", "Por favor, digite a senha.")
            return

        if tipo_var.get() not in ("CFE", "NFCE"):
            messagebox.showerror("Error", "Selecione o tipo de cupom (CFE ou NFC-e).")
            return

        save_and_close()

    # --------------------------------------- #
    # CONFIGURAÇÃO DA JANELA ROOT
    # --------------------------------------- #

    root.title("Main Page")
    root.state("zoomed")
    root.configure(fg_color="#25412D")

    # limpa tudo antes de montar
    for widget in root.winfo_children():
        widget.destroy()

    # ==========================
    #  FRAME PRINCIPAL (duas colunas)
    # ==========================
    mainPage_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
    mainPage_frame.pack(fill="both", expand=True)

    # ==========================
    #  LADO ESQUERDO (com scroll)
    # ==========================
    left_scroll = ctk.CTkScrollableFrame(
        mainPage_frame,
        fg_color="transparent",
        width=500  # largura fixa para NÃO estourar layout
    )
    left_scroll.pack(side="left", fill="y", padx=30, pady=20)

    MainLeft_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
    MainLeft_frame.pack(fill="both", expand=True)

    # ==========================
    #  LADO DIREITO (LOGO)
    # ==========================
    MainRight_frame = ctk.CTkFrame(
        mainPage_frame,
        fg_color="transparent",
        width=900   # largura boa para o logo
    )
    MainRight_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    logo_frame = ctk.CTkFrame(
        MainRight_frame,
        width=900,
        height=700,
        corner_radius=60,
        fg_color="white"
    )
    logo_frame.pack(fill="both", expand=True)
    logo_frame.pack_propagate(False)

    try:
        logo_image = ctk.CTkImage(
            dark_image=Image.open("logo.png"),
            size=(600, 600)
        )
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
        logo_label.pack(expand=True)
    except:
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="BUSINESS PRO\nCONTÁBIL",
            font=("Arial", 40, "bold"),
            text_color="#1e3d2f"
        )
        logo_label.pack(expand=True)


    # ------------------------------------------------------------------ #
    # CAMPOS DO LADO ESQUERDO
    # ------------------------------------------------------------------ #

    # ---------- TÍTULO LOGIN ----------
    IeTitleLabel = ctk.CTkLabel(
        MainLeft_frame,
        text=" LOGIN AMBIENTE SEGURO ",
        font=("Consolas", 30, "bold"),
        text_color="#25412D",
        width=600,
        height=50,
        corner_radius=6,
        fg_color='white'
    )
    IeTitleLabel.pack(anchor='w', pady=(10, 15))

    # ---------- USUÁRIO ----------
    UserLabel = ctk.CTkLabel(
        MainLeft_frame,
        text="CPF DO CONTADOR:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    UserLabel.pack(anchor='w', pady=(10, 5))

    User_entry = ctk.CTkEntry(
        MainLeft_frame,
        text_color='black',
        width=200,
        font=("Consolas", 18, "bold"),
        border_color='white'
    )
    User_entry.pack(anchor='w', pady=5, padx=20)
    User_entry.insert(0, user_login.username)

    # ---------- SENHA ----------
    PasswordLabel = ctk.CTkLabel(
        MainLeft_frame,
        text="SENHA:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    PasswordLabel.pack(anchor='w', pady=(15, 5))

    Password_entry = ctk.CTkEntry(
        MainLeft_frame,
        show="*",
        text_color='black',
        width=200,
        font=("Consolas", 18, "bold"),
        border_color='white'
    )
    Password_entry.pack(anchor='w', pady=5, padx=20)

    # ---------- TÍTULO CONSULTA ----------
    IeTitleLabel2 = ctk.CTkLabel(
        MainLeft_frame,
        text=" DADOS DE CONSULTA ",
        font=("Consolas", 30, "bold"),
        width=600,
        height=50,
        text_color="#25412D",
        corner_radius=6,
        fg_color='white'
    )
    IeTitleLabel2.pack(anchor='w', pady=(30, 10))

    # ---------- INSCRIÇÃO ----------
    IeLabel = ctk.CTkLabel(
        MainLeft_frame,
        text="INSCRIÇÃO:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    IeLabel.pack(anchor='w', pady=(10, 5))

    Ie_entry = ctk.CTkEntry(
        MainLeft_frame,
        text_color='black',
        width=200,
        font=("Consolas", 18, "bold"),
        border_color='white'
    )
    Ie_entry.pack(anchor='w', pady=5, padx=20)

    # ---------- MÊS + ANO ----------
    date_frame = ctk.CTkFrame(MainLeft_frame, fg_color="transparent")
    date_frame.pack(anchor='w', pady=(20, 10))

    # ----- MÊS -----
    month_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
    month_frame.pack(side="left", padx=10)

    MonthLabel = ctk.CTkLabel(
        month_frame,
        text="MÊS:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    MonthLabel.pack(anchor='w')

    Month_entry = ctk.CTkEntry(
        month_frame,
        text_color='black',
        width=100,
        font=("Consolas", 18, "bold"),
        border_color='white'
    )
    Month_entry.pack(anchor='w', pady=5, padx=5)

    # ----- ANO -----
    year_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
    year_frame.pack(side="left", padx=10)

    YearLabel = ctk.CTkLabel(
        year_frame,
        text="ANO:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    YearLabel.pack(anchor='w')

    Year_entry = ctk.CTkEntry(
        year_frame,
        text_color='black',
        width=100,
        font=("Consolas", 18, "bold"),
        border_color='white'
    )
    Year_entry.pack(anchor='w', pady=5, padx=5)
    Year_entry.insert(0, '2025')

    # ------------------------------------------------------ #
    # 🔳 QUADRADOS — TIPO DE CUPOM (CFE / NFC-e)
    # ------------------------------------------------------ #

    tipo_frame = ctk.CTkFrame(MainLeft_frame, fg_color="transparent")
    tipo_frame.pack(anchor="w", pady=(25, 10))

    TipoLabel = ctk.CTkLabel(
        tipo_frame,
        text="TIPO DE CUPOM:",
        font=("Consolas", 20, "bold"),
        text_color="white"
    )
    TipoLabel.pack(anchor="w", pady=(0, 10))

    tipo_var = ctk.StringVar(value="CFE")  # default CFE

    def selecionar_cfe():
        if cupom_cfe.get() == 1:
            cupom_nfce.deselect()
            tipo_var.set("CFE")
        else:
            cupom_cfe.select()
            tipo_var.set("CFE")

    def selecionar_nfce():
        if cupom_nfce.get() == 1:
            cupom_cfe.deselect()
            tipo_var.set("NFCE")
        else:
            cupom_nfce.select()
            tipo_var.set("NFCE")

    cupom_cfe = ctk.CTkCheckBox(
        tipo_frame,
        text="CFE (Cupom Fiscal Eletrônico)",
        font=("Consolas", 16),
        text_color="white",
        onvalue=1,
        offvalue=0,
        command=selecionar_cfe
    )
    cupom_cfe.pack(anchor="w", pady=5, padx=20)
    cupom_cfe.select()  # padrão

    cupom_nfce = ctk.CTkCheckBox(
        tipo_frame,
        text="NFC-e (Nota Fiscal de Consumidor Eletrônica)",
        font=("Consolas", 16),
        text_color="white",
        onvalue=1,
        offvalue=0,
        command=selecionar_nfce
    )
    cupom_nfce.pack(anchor="w", pady=5, padx=20)

    # ---------- BOTÃO EXECUTAR ----------
    MainexitButton = ctk.CTkButton(
        MainLeft_frame,
        font=("Consolas", 20, "bold"),
        text_color='black',
        text="EXECUTAR",
        fg_color='white',
        width=250,
        height=50,
        corner_radius=10,
        command=check_and_save
    )
    MainexitButton.pack(pady=30, anchor="w")

    # IMPORTANTE: o mainloop fica fora daqui (no front / index)
