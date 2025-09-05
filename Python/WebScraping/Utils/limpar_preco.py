import re
def limpar_preco(preco_str):
    try:
        if isinstance(preco_str, (int, float)):
            return float(preco_str)

        valores = re.findall(r'R\$ ?\d+,\d+', preco_str)
        if valores:
            valor = valores[1] if len(valores) > 1 else valores[0]
            valor = valor.replace("R$", "").replace(",", ".").strip()
            return float(valor)
        else:
            preco_str = preco_str.replace(",", ".").strip()
            return float(preco_str) if preco_str else 0.0
    except Exception:
        return 0.0