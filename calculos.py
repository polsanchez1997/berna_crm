import pandas as pd


def obtener_coste_procedimiento(nombre_procedimiento, productos, materiales):
    try:
        materiales_proc = materiales[materiales["procedimiento"] == nombre_procedimiento]
        total = 0.0
        for _, row in materiales_proc.iterrows():
            producto = productos[productos["nombre"] == row["producto"]]
            if not producto.empty:
                total += float(producto.iloc[0]["coste_unitario"]) * float(row["cantidad"])
        return round(total, 2)
    except Exception:
        return 0


def desglose_costes_procedimiento(nombre_procedimiento, productos, materiales):
    try:
        materiales_proc = materiales[materiales["procedimiento"] == nombre_procedimiento]
        detalle = []
        total = 0.0
        for _, row in materiales_proc.iterrows():
            producto = productos[productos["nombre"] == row["producto"]]
            if not producto.empty:
                coste_unitario = float(producto.iloc[0]["coste_unitario"])
                cantidad       = float(row["cantidad"])
                subtotal       = coste_unitario * cantidad
                total         += subtotal
                detalle.append({
                    "Producto":       row["producto"],
                    "Cantidad usada": cantidad,
                    "Coste unitario": round(coste_unitario, 2),
                    "Subtotal":       round(subtotal, 2),
                })
        return pd.DataFrame(detalle), round(total, 2)
    except Exception:
        return pd.DataFrame(), 0
