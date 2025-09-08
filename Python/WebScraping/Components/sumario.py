# Components/summary_frame.py

from tkinter import ttk

def criar_summary_frame(root, titulo, dados, padding=(10, 5)):
    """
    Cria um frame de resumo customizável.

    Parâmetros:
    - root: widget pai (normalmente a janela ou frame).
    - titulo: título do LabelFrame.
    - dados: lista de dicionários com as chaves:
        - emoji (opcional): string (ex: "💰")
        - texto: string descritiva
        - valor: número float ou string
        - row: linha na grade
        - column: coluna na grade
        - anchor: alinhamento ("w", "e", "center", etc)
    - padding: espaçamento interno do frame.

    Retorna:
    - o frame construído.
    """

    frame = ttk.LabelFrame(root, text=titulo, padding=padding)
    frame.grid(sticky="ew")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    fonte = ("Segoe UI", 10, "bold")

    for item in dados:
        emoji = item.get("emoji", "")
        texto = item["texto"]
        valor = item["valor"]
        row = item["row"]
        column = item["column"]
        anchor = item.get("anchor", "w")

        label_texto = f"{emoji} {texto}: R$ {float(valor):.2f}" if isinstance(valor, (float, int)) else f"{emoji} {texto}: {valor}"

        ttk.Label(frame, text=label_texto, font=fonte).grid(
            row=row,
            column=column,
            padx=5,
            pady=2,
            sticky=anchor
        )

    return frame
