import os
import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox

CAMINHO_DB = "yugioh.db"  # Altere para o caminho real se necessário

TABELAS_EXPORTAR = [
    "carta", "venda", "produto", "venda_produto",
    "colecao", "qualidade", "raridade", "historico_precos"
]

def exportar_banco_completo():
    pasta_destino = filedialog.askdirectory(title="Escolha a pasta para exportar")
    if not pasta_destino:
        return

    try:
        conn = sqlite3.connect(CAMINHO_DB)

        caminho_xlsx = os.path.join(pasta_destino, "exportacao_completa.xlsx")
        with pd.ExcelWriter(caminho_xlsx, engine="openpyxl") as writer:
            for tabela in TABELAS_EXPORTAR:
                df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
                nome_sheet = tabela[:31]  # nome do sheet no Excel tem limite de 31 caracteres
                df.to_excel(writer, sheet_name=nome_sheet, index=False)

        # Copiar o arquivo .db
        caminho_db_destino = os.path.join(pasta_destino, "backup_banco.sqlite")
        with open(CAMINHO_DB, "rb") as f_origem, open(caminho_db_destino, "wb") as f_dest:
            f_dest.write(f_origem.read())

        messagebox.showinfo("Sucesso", f"Exportado com sucesso para:\n{pasta_destino}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar: {e}")

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    exportar_banco_completo()
