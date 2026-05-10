
import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from google.oauth2.service_account import Credentials
import gspread
from estilo import aplicar_estilo

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BERNA",
    page_icon="💅",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo()

# =========================================================
# AUTENTICACIÓN
# =========================================================

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("## 💅 BERNA")
        st.caption("Estetica Bernardita Driollet")
        st.markdown("<br>", unsafe_allow_html=True)
        clave = st.text_input("Contraseña", type="password", placeholder="••••••••")
        if st.button("Entrar", use_container_width=True, type="primary"):
            if clave == st.secrets.get("auth", {}).get("password", ""):
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================
# GOOGLE SHEETS
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def conectar_gsheets():
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES,
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(st.secrets["sheet_id"])


# =========================================================
# CARGA DE DATOS
# =========================================================

@st.cache_data(ttl=300)
def _listar_titulos(_hoja):
    # Retorna {title_lower: title_original} — solo strings, serializable por cache_data
    return {w.title.strip().lower(): w.title for w in _hoja.worksheets()}


@st.cache_data(ttl=300)
def cargar(_hoja, nombre_ws):
    try:
        titulos = _listar_titulos(_hoja)
        titulo_real = titulos.get(nombre_ws.strip().lower())
        if titulo_real is None:
            return pd.DataFrame()
        ws = _hoja.worksheet(titulo_real)
        datos = ws.get_all_records()
        df = pd.DataFrame(datos)
        if not df.empty:
            df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error cargando '{nombre_ws}': {e}")
        return pd.DataFrame()


@st.cache_data(ttl=600)
def listar_hojas(_hoja):
    try:
        return list(_listar_titulos(_hoja).values())
    except Exception:
        return []


def recargar():
    st.cache_data.clear()
    st.rerun()


# ─── Cargar todo ──────────────────────────────────────────
hoja           = conectar_gsheets()
servicios_raw  = cargar(hoja, "servicios")
procedimientos = cargar(hoja, "procedimientos")
clientes       = cargar(hoja, "clientes")
ingresos       = cargar(hoja, "ingresos")
gastos         = cargar(hoja, "gastos")
materiales     = cargar(hoja, "materiales")
costos_proc    = cargar(hoja, "costos_procedimiento")

# ─── Unificar servicios + procedimientos (left join) ─────
if not procedimientos.empty and not servicios_raw.empty:
    cols_add = [c for c in servicios_raw.columns if c not in procedimientos.columns]
    servicios = pd.merge(
        procedimientos,
        servicios_raw[["nombre"] + cols_add],
        on="nombre", how="left",
    )
elif not procedimientos.empty:
    servicios = procedimientos.copy()
elif not servicios_raw.empty:
    servicios = servicios_raw.copy()
else:
    servicios = pd.DataFrame()

# ─── Normalizar numéricos ─────────────────────────────────
def _to_float(val):
    """Convierte a float tolerando coma decimal europea (1.349,39 o 1349,39)."""
    if pd.isna(val):
        return float("nan")
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(" ", "").replace("\xa0", "")
    if "," in s and "." in s:          # 1.349,39 → 1349.39
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:                     # 1349,39  → 1349.39
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return float("nan")

for df_name, df_obj, col in [
    ("ingresos",   ingresos,   "monto"),
    ("gastos",     gastos,     "importe"),
    ("materiales", materiales, "coste_unitario"),
    ("materiales", materiales, "cantidad"),
    ("materiales", materiales, "precio_compra"),
    ("costos_proc", costos_proc, "cantidad"),
]:
    if not df_obj.empty and col in df_obj.columns:
        df_obj[col] = df_obj[col].apply(_to_float)


# =========================================================
# HELPERS
# =========================================================

def normalizar_margen(val):
    """Convierte 65 o 0.65 siempre a decimal (0.65)."""
    try:
        m = float(val)
        return m / 100 if m > 1 else m
    except (TypeError, ValueError):
        return 0.65


def buscar_fila_sheets(ws, col_header, valor):
    """Retorna nro de fila en Sheets (1-indexed) donde col_header == valor. None si no existe."""
    try:
        all_vals = ws.get_all_values()
        if len(all_vals) < 2:
            return None
        headers = [h.strip() for h in all_vals[0]]
        if col_header not in headers:
            return None
        col_idx = headers.index(col_header)
        for i, row in enumerate(all_vals[1:], start=2):
            if len(row) > col_idx and str(row[col_idx]).strip() == str(valor).strip():
                return i
        return None
    except Exception:
        return None


def descontar_stock(procedimiento_nombre):
    """Deduce del stock los materiales usados en un procedimiento."""
    if costos_proc.empty or materiales.empty:
        return []
    if "procedimiento" not in costos_proc.columns or "material" not in costos_proc.columns:
        return []

    mats_usados = costos_proc[costos_proc["procedimiento"] == procedimiento_nombre]
    if mats_usados.empty:
        return []

    try:
        ws_mat   = hoja.worksheet("materiales")
        all_vals = ws_mat.get_all_values()
        if len(all_vals) < 2:
            return []
        headers  = [h.strip() for h in all_vals[0]]
        if "nombre" not in headers or "cantidad" not in headers:
            return []

        col_nom  = headers.index("nombre")
        col_cant = headers.index("cantidad")
        ajustes  = []

        for _, uso in mats_usados.iterrows():
            mat_nombre = str(uso["material"]).strip()
            cant_usar  = float(uso["cantidad"]) if uso["cantidad"] else 0

            fila = next(
                (i for i, r in enumerate(all_vals[1:], start=2)
                 if len(r) > col_nom and r[col_nom].strip() == mat_nombre),
                None,
            )
            if fila:
                actual = _to_float(all_vals[fila - 1][col_cant] or 0)
                nuevo  = max(0.0, actual - cant_usar)
                ws_mat.update_cell(fila, col_cant + 1, round(nuevo, 4))
                ajustes.append({"material": mat_nombre, "usado": cant_usar, "restante": nuevo})

        return ajustes
    except Exception as e:
        st.warning(f"No se pudo actualizar el stock: {e}")
        return []


def validar_duplicado(df, campo, valor, excluir=None):
    """True si valor ya existe en df[campo] (ignorando excluir)."""
    if df.empty or campo not in df.columns:
        return False
    series_lower = df[campo].astype(str).str.strip().str.lower()
    val_lower    = str(valor).strip().lower()
    if excluir:
        excluir_lower = str(excluir).strip().lower()
        series_lower  = series_lower[series_lower != excluir_lower]
    return val_lower in series_lower.values


def tabla(df, key=None):
    """Muestra DataFrame ocultando columnas internas."""
    cols = [c for c in df.columns if not c.startswith("_")]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)


def csv_btn(df, filename, label="📥 Exportar CSV"):
    cols = [c for c in df.columns if not c.startswith("_")]
    csv  = df[cols].to_csv(index=False).encode("utf-8")
    st.download_button(label, csv, filename, "text/csv")


def formatear_servicios(df):
    """Retorna tabla de servicios con columnas legibles."""
    d = df[[c for c in df.columns if not c.startswith("_")]].copy()
    if "margen_objetivo" in d.columns:
        d["margen_objetivo"] = pd.to_numeric(d["margen_objetivo"], errors="coerce").apply(
            lambda x: f"{normalizar_margen(x)*100:.0f}%" if pd.notna(x) else ""
        )
    if "precio" in d.columns:
        d["precio"] = pd.to_numeric(d["precio"], errors="coerce").apply(
            lambda x: f"${x:,.0f}" if pd.notna(x) else ""
        )
    d = d.rename(columns={
        "nombre": "Nombre", "categoria": "Categoría", "precio": "Precio",
        "duracion_min": "Duración (min)", "margen_objetivo": "Margen",
    })
    return d


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 💅 BERNA")
    st.caption("Estetica Bernardita Driollet")
    st.divider()

    # Resumen del mes actual
    mes_actual = date.today().strftime("%Y-%m")
    if not ingresos.empty and "monto" in ingresos.columns and "fecha" in ingresos.columns:
        ing_c = ingresos.copy()
        ing_c["fecha"] = pd.to_datetime(ing_c["fecha"], errors="coerce")
        ing_mes_actual = ing_c[ing_c["fecha"].dt.to_period("M").astype(str) == mes_actual]["monto"].sum()
        st.metric("Ingresos este mes", f"${ing_mes_actual:,.0f}")

    hojas_disponibles = listar_hojas(hoja)
    hojas_set = {h.strip().lower() for h in hojas_disponibles}

    with st.expander("📡 Estado de conexión"):
        dfs = {
            "servicios":            servicios_raw,
            "clientes":             clientes,
            "ingresos":             ingresos,
            "gastos":               gastos,
            "materiales":           materiales,
            "procedimientos":       procedimientos,
            "costos_procedimiento": costos_proc,
        }
        for nombre, df_obj in dfs.items():
            existe = nombre.lower() in hojas_set
            tiene_datos = not df_obj.empty
            if not existe:
                icono = "❌"
                estado_txt = "hoja no encontrada"
            elif not tiene_datos:
                icono = "⚠️"
                estado_txt = "sin datos"
            else:
                icono = "✅"
                estado_txt = f"{len(df_obj)} filas"
            st.caption(f"{icono} {nombre} — {estado_txt}")

    st.divider()

    # Alertas de stock bajo
    if (
        not materiales.empty
        and "stock_minimo" in materiales.columns
        and "cantidad" in materiales.columns
    ):
        stock_num = pd.to_numeric(materiales["cantidad"],     errors="coerce")
        min_num   = pd.to_numeric(materiales["stock_minimo"], errors="coerce")
        bajo = materiales[stock_num.lt(min_num) & stock_num.notna() & min_num.notna()]
        if not bajo.empty:
            st.warning(f"⚠️ {len(bajo)} material(es) con stock bajo")
            for _, row in bajo.iterrows():
                st.caption(f"• {row['nombre']}: {row['cantidad']} {row.get('unidad','')}")

    st.divider()
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# =========================================================
# TABS
# =========================================================

tabs = st.tabs([
    "📊 Dashboard",
    "✨ Servicios",
    "👥 Clientes",
    "📦 Materiales",
    "💰 Costos por servicio",
    "📈 Ingresos",
    "💸 Gastos",
])

# =========================================================
# DASHBOARD
# =========================================================

with tabs[0]:
    st.title("Dashboard")

    tiene_ing  = not ingresos.empty  and "monto"   in ingresos.columns
    tiene_gast = not gastos.empty    and "importe" in gastos.columns

    total_ing  = ingresos["monto"].sum()   if tiene_ing  else 0
    total_gast = gastos["importe"].sum()   if tiene_gast else 0
    balance    = total_ing - total_gast

    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos totales",  f"${total_ing:,.0f}")
    c2.metric("Gastos totales",    f"${total_gast:,.0f}")
    c3.metric("Balance",           f"${balance:,.0f}",
              delta=f"${balance:+,.0f}",
              delta_color="normal")
    c4, c5 = st.columns(2)
    c4.metric("Clientes",  len(clientes))
    c5.metric("Servicios", len(servicios))

    st.divider()

    # ── Gráfico combinado ingresos vs gastos ──────────────
    if tiene_ing or tiene_gast:
        st.subheader("Ingresos vs Gastos por mes")
        frames = []
        if tiene_ing and "fecha" in ingresos.columns:
            ing_c = ingresos.copy()
            ing_c["fecha"] = pd.to_datetime(ing_c["fecha"], errors="coerce")
            ing_c = ing_c.dropna(subset=["fecha"])
            ing_c["mes"] = ing_c["fecha"].dt.to_period("M").astype(str)
            ing_mes = ing_c.groupby("mes")["monto"].sum().reset_index()
            ing_mes.columns = ["mes", "importe"]
            ing_mes["tipo"] = "Ingresos"
            frames.append(ing_mes)
        if tiene_gast and "fecha" in gastos.columns:
            gast_c = gastos.copy()
            gast_c["fecha"] = pd.to_datetime(gast_c["fecha"], errors="coerce")
            gast_c = gast_c.dropna(subset=["fecha"])
            gast_c["mes"] = gast_c["fecha"].dt.to_period("M").astype(str)
            gast_mes = gast_c.groupby("mes")["importe"].sum().reset_index()
            gast_mes["tipo"] = "Gastos"
            frames.append(gast_mes)

        if frames:
            combined = pd.concat(frames, ignore_index=True)
            chart = (
                alt.Chart(combined)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X("mes:O", title="Mes", axis=alt.Axis(labelAngle=-30)),
                    y=alt.Y("importe:Q", title="$", axis=alt.Axis(format="$,.0f")),
                    color=alt.Color(
                        "tipo:N",
                        scale=alt.Scale(domain=["Ingresos","Gastos"], range=["#8C5E58","#D4B5B0"]),
                        legend=alt.Legend(title=""),
                    ),
                    xOffset="tipo:N",
                    tooltip=["mes:O", "tipo:N", alt.Tooltip("importe:Q", format="$,.0f")],
                )
                .properties(height=280)
            )
            st.altair_chart(chart, use_container_width=True)

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Top 5 clientes")
        if tiene_ing and "cliente" in ingresos.columns:
            ing_norm = ingresos.copy()
            ing_norm["cliente"] = ing_norm["cliente"].astype(str).str.strip()
            top_cli = (
                ing_norm.groupby("cliente")["monto"]
                .agg(total="sum", visitas="count")
                .sort_values("total", ascending=False)
                .head(5)
                .reset_index()
            )
            top_cli["total"] = top_cli["total"].apply(lambda x: f"${x:,.0f}")
            top_cli.columns = ["Cliente", "Total gastado", "Visitas"]
            st.dataframe(top_cli, use_container_width=True, hide_index=True)
        else:
            st.info("Sin datos de ingresos aún.")

    with col_b:
        st.subheader("Top 5 servicios")
        if tiene_ing and "servicio" in ingresos.columns:
            ing_norm2 = ingresos.copy()
            ing_norm2["servicio"] = ing_norm2["servicio"].astype(str).str.strip()
            top_srv = (
                ing_norm2.groupby("servicio")["monto"]
                .agg(total="sum", realizados="count")
                .sort_values("total", ascending=False)
                .head(5)
                .reset_index()
            )
            top_srv["total"] = top_srv["total"].apply(lambda x: f"${x:,.0f}")
            top_srv.columns = ["Servicio", "Ingresos generados", "Realizados"]
            st.dataframe(top_srv, use_container_width=True, hide_index=True)
        else:
            st.info("Sin datos de ingresos aún.")

    st.divider()
    st.subheader("Últimos 10 ingresos")
    if not ingresos.empty:
        tabla(ingresos.tail(10))
    else:
        st.info("Sin ingresos registrados.")

# =========================================================
# SERVICIOS
# =========================================================

with tabs[1]:
    st.title("Servicios")

    # ── Crear ─────────────────────────────────────────────
    with st.expander("➕ Crear servicio"):
        with st.form("form_servicio", clear_on_submit=True):
            nombre_srv    = st.text_input("Nombre del servicio")
            categoria_srv = st.text_input("Categoría")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                precio_srv   = st.number_input("Precio ($)", min_value=0.0, step=100.0)
                duracion_srv = st.number_input("Duración (min)", min_value=0, step=5)
            with col_f2:
                margen_pct = st.slider("Margen objetivo (%)", 10, 500, 65, step=5)

            if st.form_submit_button("Crear servicio", type="primary"):
                if not nombre_srv.strip():
                    st.error("El nombre es obligatorio.")
                elif not categoria_srv.strip():
                    st.error("La categoría es obligatoria.")
                elif validar_duplicado(servicios, "nombre", nombre_srv.strip()):
                    st.error(f"Ya existe un servicio llamado '{nombre_srv.strip()}'.")
                else:
                    try:
                        n, c = nombre_srv.strip(), categoria_srv.strip()
                        hoja.worksheet("procedimientos").append_row([n, c, margen_pct])
                        hoja.worksheet("servicios").append_row([n, c, precio_srv, int(duracion_srv)])
                        st.success(f"✅ Servicio '{n}' creado.")
                        recargar()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

    # ── Editar ────────────────────────────────────────────
    if not servicios.empty and "nombre" in servicios.columns:
        nombres_srv = servicios["nombre"].dropna().tolist()
        with st.expander("✏️ Editar servicio"):
            srv_edit  = st.selectbox("Seleccionar", nombres_srv, key="sel_edit_srv")
            srv_actual = servicios[servicios["nombre"] == srv_edit].iloc[0]
            margen_actual = normalizar_margen(srv_actual.get("margen_objetivo", 0.65))

            # Clave de form y widgets incluye srv_edit para refrescar al cambiar selección
            with st.form(f"form_edit_srv_{srv_edit}", clear_on_submit=False):
                e_nombre   = st.text_input("Nombre",    value=str(srv_actual.get("nombre", "")),    key=f"e_srv_nombre_{srv_edit}")
                e_cat      = st.text_input("Categoría", value=str(srv_actual.get("categoria", "")), key=f"e_srv_cat_{srv_edit}")
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    precio_raw = srv_actual.get("precio", 0)
                    e_precio   = st.number_input("Precio ($)", min_value=0.0, step=100.0,
                                                  value=float(precio_raw) if pd.notna(precio_raw) and str(precio_raw).strip() != "" else 0.0,
                                                  key=f"e_srv_precio_{srv_edit}")
                    dur_raw    = srv_actual.get("duracion_min", 0)
                    e_dur      = st.number_input("Duración (min)", min_value=0, step=5,
                                                  value=int(float(dur_raw)) if pd.notna(dur_raw) and str(dur_raw).strip() != "" else 0,
                                                  key=f"e_srv_dur_{srv_edit}")
                with col_e2:
                    e_margen   = st.slider("Margen (%)", 10, 500, int(margen_actual * 100), step=5,
                                           key=f"e_srv_margen_{srv_edit}")

                if st.form_submit_button("Guardar cambios", type="primary"):
                    if not e_nombre.strip():
                        st.error("El nombre es obligatorio.")
                    else:
                        try:
                            todo_ok = True
                            for ws_name, campos in [
                                ("procedimientos", {"nombre": e_nombre.strip(), "categoria": e_cat.strip(), "margen_objetivo": e_margen}),
                                ("servicios",      {"nombre": e_nombre.strip(), "categoria": e_cat.strip(), "precio": e_precio, "duracion_min": int(e_dur)}),
                            ]:
                                ws  = hoja.worksheet(ws_name)
                                hds = ws.row_values(1)
                                fil = buscar_fila_sheets(ws, "nombre", srv_edit)
                                if fil:
                                    for campo, valor in campos.items():
                                        if campo in hds:
                                            ws.update_cell(fil, hds.index(campo) + 1, valor)
                                else:
                                    st.error(f"No se encontró '{srv_edit}' en la hoja '{ws_name}'.")
                                    todo_ok = False
                            if todo_ok:
                                st.success("✅ Servicio actualizado.")
                                recargar()
                        except Exception as e:
                            st.error(f"Error: {e}")

    st.divider()

    if servicios.empty:
        st.info("No hay servicios registrados.")
    else:
        busq_s = st.text_input("🔍 Buscar servicio", key="busq_srv")
        df_s = servicios if not busq_s else servicios[
            servicios.apply(lambda c: c.astype(str).str.contains(busq_s, case=False, na=False)).any(axis=1)
        ]
        st.dataframe(formatear_servicios(df_s), use_container_width=True, hide_index=True)
        csv_btn(servicios, "servicios.csv")

        # ── Eliminar ──────────────────────────────────────
        with st.expander("🗑️ Eliminar servicio"):
            srv_borrar    = st.selectbox("Seleccionar", servicios["nombre"].dropna().tolist(), key="sel_del_srv")
            confirmar_srv = st.checkbox("Confirmar eliminación", key="confirm_del_srv")
            if st.button("Eliminar servicio", disabled=not confirmar_srv, key="btn_del_srv"):
                try:
                    for ws_name in ["procedimientos", "servicios"]:
                        try:
                            ws  = hoja.worksheet(ws_name)
                            fil = buscar_fila_sheets(ws, "nombre", srv_borrar)
                            if fil:
                                ws.delete_rows(fil)
                        except Exception:
                            pass
                    # Limpiar costos_procedimiento huérfanos
                    try:
                        ws_cp    = hoja.worksheet("costos_procedimiento")
                        all_rows = ws_cp.get_all_values()
                        headers  = all_rows[0] if all_rows else []
                        if "procedimiento" in headers:
                            col_p = headers.index("procedimiento")
                            filas_borrar = [
                                i for i, r in enumerate(all_rows[1:], start=2)
                                if len(r) > col_p and r[col_p].strip() == srv_borrar
                            ]
                            for f in reversed(filas_borrar):
                                ws_cp.delete_rows(f)
                    except Exception:
                        pass
                    st.success(f"'{srv_borrar}' eliminado.")
                    recargar()
                except Exception as e:
                    st.error(f"Error: {e}")

# =========================================================
# CLIENTES
# =========================================================

with tabs[2]:
    st.title("Clientes")

    # ── Agregar ───────────────────────────────────────────
    with st.expander("➕ Agregar cliente"):
        with st.form("form_cliente", clear_on_submit=True):
            col_cl1, col_cl2 = st.columns(2)
            with col_cl1:
                nombre_cli    = st.text_input("Nombre completo")
                telefono_cli  = st.text_input("Teléfono")
            with col_cl2:
                email_cli     = st.text_input("Email")
                instagram_cli = st.text_input("Instagram")
            if st.form_submit_button("Guardar cliente", type="primary"):
                if not nombre_cli.strip():
                    st.error("El nombre es obligatorio.")
                elif validar_duplicado(clientes, "nombre", nombre_cli.strip()):
                    st.error(f"Ya existe un cliente llamado '{nombre_cli.strip()}'.")
                else:
                    try:
                        hoja.worksheet("clientes").append_row([
                            nombre_cli.strip(), telefono_cli.strip(),
                            email_cli.strip(),  instagram_cli.strip(),
                        ])
                        st.success(f"✅ Cliente '{nombre_cli.strip()}' agregado.")
                        recargar()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

    # ── Editar ────────────────────────────────────────────
    if not clientes.empty and "nombre" in clientes.columns:
        with st.expander("✏️ Editar cliente"):
            cli_edit  = st.selectbox("Seleccionar", clientes["nombre"].tolist(), key="sel_edit_cli")
            cli_actual = clientes[clientes["nombre"] == cli_edit].iloc[0]
            with st.form(f"form_edit_cli_{cli_edit}", clear_on_submit=False):
                e_nombre_c = st.text_input("Nombre",    value=str(cli_actual.get("nombre", "")),    key=f"e_cli_nombre_{cli_edit}")
                e_tel      = st.text_input("Teléfono",  value=str(cli_actual.get("telefono", "")),  key=f"e_cli_tel_{cli_edit}")
                e_email    = st.text_input("Email",     value=str(cli_actual.get("email", "")),     key=f"e_cli_email_{cli_edit}")
                e_ig       = st.text_input("Instagram", value=str(cli_actual.get("instagram", "")), key=f"e_cli_ig_{cli_edit}")
                if st.form_submit_button("Guardar cambios", type="primary"):
                    if not e_nombre_c.strip():
                        st.error("El nombre es obligatorio.")
                    else:
                        try:
                            ws  = hoja.worksheet("clientes")
                            hds = ws.row_values(1)
                            fil = buscar_fila_sheets(ws, "nombre", cli_edit)
                            if fil:
                                for campo, valor in {
                                    "nombre": e_nombre_c.strip(), "telefono": e_tel.strip(),
                                    "email":  e_email.strip(),    "instagram": e_ig.strip(),
                                }.items():
                                    if campo in hds:
                                        ws.update_cell(fil, hds.index(campo) + 1, valor)
                                st.success("✅ Cliente actualizado.")
                                recargar()
                            else:
                                st.error(f"No se encontró '{cli_edit}' en la hoja de clientes.")
                        except Exception as e:
                            st.error(f"Error: {e}")

    st.divider()

    if clientes.empty:
        st.info("No hay clientes registrados.")
    else:
        busq_c = st.text_input("🔍 Buscar cliente", key="busq_cli")
        df_c = clientes if not busq_c else clientes[
            clientes.apply(lambda c: c.astype(str).str.contains(busq_c, case=False, na=False)).any(axis=1)
        ]
        tabla(df_c)
        csv_btn(clientes, "clientes.csv")

# =========================================================
# MATERIALES
# =========================================================

with tabs[3]:
    st.title("Materiales")

    # ── Alerta de stock bajo ───────────────────────────────
    if (
        not materiales.empty
        and "stock_minimo" in materiales.columns
        and "cantidad" in materiales.columns
    ):
        stock_num = pd.to_numeric(materiales["cantidad"],     errors="coerce")
        min_num   = pd.to_numeric(materiales["stock_minimo"], errors="coerce")
        bajo = materiales[stock_num.lt(min_num) & stock_num.notna() & min_num.notna()]
        if not bajo.empty:
            st.error(f"⚠️ {len(bajo)} material(es) con stock bajo")
            cols_show = [c for c in ["nombre", "cantidad", "unidad", "stock_minimo"] if c in bajo.columns]
            st.dataframe(bajo[cols_show], use_container_width=True, hide_index=True)
            st.divider()

    # ── Añadir ────────────────────────────────────────────
    with st.expander("➕ Añadir material"):
        with st.form("form_material", clear_on_submit=True):
            nombre_mat = st.text_input("Nombre del material")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                precio_compra = st.number_input("Precio de compra ($)", min_value=0.0, step=100.0)
                cantidad_mat  = st.number_input("Cantidad / stock actual", min_value=0.0, step=1.0)
            with col_m2:
                unidad_mat    = st.text_input("Unidad (ml, g, unidad…)")
                stock_min_mat = st.number_input("Stock mínimo para alerta", min_value=0.0, step=1.0, value=2.0)
            if st.form_submit_button("Guardar material", type="primary"):
                if not nombre_mat.strip():
                    st.error("El nombre es obligatorio.")
                elif precio_compra <= 0:
                    st.error("El precio debe ser mayor a $0.")
                elif cantidad_mat <= 0:
                    st.error("La cantidad debe ser mayor a 0.")
                elif validar_duplicado(materiales, "nombre", nombre_mat.strip()):
                    st.error(f"Ya existe un material llamado '{nombre_mat.strip()}'.")
                else:
                    coste_unit = round(precio_compra / cantidad_mat, 4)
                    try:
                        hoja.worksheet("materiales").append_row([
                            nombre_mat.strip(), precio_compra,
                            cantidad_mat, unidad_mat.strip(), coste_unit, stock_min_mat,
                        ])
                        st.success(f"✅ '{nombre_mat.strip()}' guardado · Costo unitario: ${coste_unit:,.4f}")
                        recargar()
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ── Editar ────────────────────────────────────────────
    if not materiales.empty and "nombre" in materiales.columns:
        with st.expander("✏️ Editar material"):
            mat_edit   = st.selectbox("Seleccionar", materiales["nombre"].tolist(), key="sel_edit_mat")
            mat_actual = materiales[materiales["nombre"] == mat_edit].iloc[0]
            with st.form(f"form_edit_mat_{mat_edit}", clear_on_submit=False):
                e_nom_m   = st.text_input("Nombre", value=str(mat_actual.get("nombre", "")), key=f"e_mat_nombre_{mat_edit}")
                col_em1, col_em2 = st.columns(2)
                with col_em1:
                    e_precio_c = st.number_input("Precio de compra ($)", min_value=0.0, step=100.0,
                                                  value=float(mat_actual.get("precio_compra", 0) or 0),
                                                  key=f"e_mat_precio_{mat_edit}")
                    e_cant_m   = st.number_input("Cantidad / stock", min_value=0.0, step=1.0,
                                                  value=float(mat_actual.get("cantidad", 0) or 0),
                                                  key=f"e_mat_cant_{mat_edit}")
                with col_em2:
                    e_unidad   = st.text_input("Unidad", value=str(mat_actual.get("unidad", "")), key=f"e_mat_unidad_{mat_edit}")
                if st.form_submit_button("Guardar cambios", type="primary"):
                    if not e_nom_m.strip():
                        st.error("El nombre es obligatorio.")
                    elif e_cant_m <= 0:
                        st.error("La cantidad debe ser mayor a 0.")
                    else:
                        nuevo_coste = round(e_precio_c / e_cant_m, 4) if e_cant_m > 0 else 0
                        try:
                            ws  = hoja.worksheet("materiales")
                            hds = ws.row_values(1)
                            fil = buscar_fila_sheets(ws, "nombre", mat_edit)
                            if fil:
                                for campo, valor in {
                                    "nombre": e_nom_m.strip(), "precio_compra": e_precio_c,
                                    "cantidad": e_cant_m, "unidad": e_unidad.strip(),
                                    "coste_unitario": nuevo_coste,
                                }.items():
                                    if campo in hds:
                                        ws.update_cell(fil, hds.index(campo) + 1, valor)
                                st.success(f"✅ Material actualizado · Costo unitario: ${nuevo_coste:,.4f}")
                                recargar()
                            else:
                                st.error(f"No se encontró '{mat_edit}' en la hoja de materiales.")
                        except Exception as e:
                            st.error(f"Error: {e}")

    # ── Reponer stock ─────────────────────────────────────
    with st.expander("🔄 Reponer stock"):
        with st.form("form_reponer", clear_on_submit=True):
            if not materiales.empty and "nombre" in materiales.columns:
                mat_reponer  = st.selectbox("Material", materiales["nombre"].tolist())
                cant_reponer = st.number_input("Cantidad a añadir", min_value=0.0, step=1.0)
                precio_nuevo = st.number_input("Precio de este lote ($, opcional para recalcular costo)", min_value=0.0, step=100.0)
                if st.form_submit_button("Reponer", type="primary"):
                    if cant_reponer <= 0:
                        st.error("La cantidad debe ser mayor a 0.")
                    else:
                        try:
                            ws       = hoja.worksheet("materiales")
                            all_vals = ws.get_all_values()
                            headers  = [h.strip() for h in all_vals[0]]
                            if "nombre" not in headers or "cantidad" not in headers:
                                st.error("La hoja 'materiales' no tiene las columnas esperadas.")
                                st.stop()
                            col_nom = headers.index("nombre")
                            fil      = next(
                                (i for i, r in enumerate(all_vals[1:], start=2)
                                 if len(r) > col_nom and r[col_nom].strip() == mat_reponer),
                                None,
                            )
                            if fil:
                                col_cant = headers.index("cantidad") + 1
                                actual   = _to_float(all_vals[fil - 1][headers.index("cantidad")] or 0)
                                nuevo    = actual + cant_reponer
                                ws.update_cell(fil, col_cant, nuevo)

                                if precio_nuevo > 0 and "coste_unitario" in headers and "precio_compra" in headers:
                                    old_coste    = _to_float(all_vals[fil - 1][headers.index("coste_unitario")] or 0)
                                    old_total    = actual * old_coste
                                    nuevo_coste  = round((old_total + precio_nuevo) / nuevo, 4)
                                    ws.update_cell(fil, headers.index("coste_unitario") + 1, nuevo_coste)
                                    ws.update_cell(fil, headers.index("precio_compra")   + 1, precio_nuevo)
                                    st.success(f"✅ Stock: {nuevo} · Nuevo costo unitario: ${nuevo_coste:,.4f}")
                                else:
                                    st.success(f"✅ Stock de '{mat_reponer}' actualizado a {nuevo}.")
                                recargar()
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.info("No hay materiales cargados.")

    st.divider()

    if materiales.empty:
        st.info("No hay materiales registrados.")
    else:
        busq_m = st.text_input("🔍 Buscar material", key="busq_mat")
        df_m = materiales if not busq_m else materiales[
            materiales.apply(lambda c: c.astype(str).str.contains(busq_m, case=False, na=False)).any(axis=1)
        ]
        tabla(df_m)
        csv_btn(materiales, "materiales.csv")

        with st.expander("🗑️ Eliminar material"):
            mat_borrar    = st.selectbox("Seleccionar", materiales["nombre"].tolist(), key="sel_del_mat")
            # Verificar si está en uso
            en_uso = (
                not costos_proc.empty
                and "material" in costos_proc.columns
                and mat_borrar in costos_proc["material"].tolist()
            )
            if en_uso:
                st.warning(f"⚠️ '{mat_borrar}' está asignado a uno o más servicios en costos_procedimiento.")
            confirmar_mat = st.checkbox("Confirmar eliminación igualmente", key="confirm_del_mat")
            if st.button("Eliminar material", disabled=not confirmar_mat, key="btn_del_mat"):
                try:
                    ws  = hoja.worksheet("materiales")
                    fil = buscar_fila_sheets(ws, "nombre", mat_borrar)
                    if fil:
                        ws.delete_rows(fil)
                        st.success(f"'{mat_borrar}' eliminado.")
                        recargar()
                except Exception as e:
                    st.error(f"Error: {e}")

# =========================================================
# COSTOS POR SERVICIO
# =========================================================

with tabs[4]:
    st.title("Costos por servicio")

    if servicios.empty:
        st.warning("No hay servicios cargados.")
    else:
        srv_col  = "nombre" if "nombre" in servicios.columns else servicios.columns[0]
        nombres_validos = servicios[srv_col].dropna().tolist()
        proc_sel = st.selectbox("Seleccionar servicio", nombres_validos)
        srv_info = servicios[servicios[srv_col] == proc_sel].iloc[0]

        # ── Agregar material ──────────────────────────────
        if not materiales.empty and "nombre" in materiales.columns:
            with st.expander("➕ Agregar material a este servicio"):
                with st.form("form_costo_proc", clear_on_submit=True):
                    mat_elegido = st.selectbox("Material", materiales["nombre"].tolist())
                    cant_uso    = st.number_input(
                        "Cantidad usada por procedimiento",
                        min_value=0.0, step=0.1, format="%.3f",
                    )
                    mat_prev = materiales[materiales["nombre"] == mat_elegido]
                    if not mat_prev.empty and "coste_unitario" in mat_prev.columns:
                        coste_p  = float(mat_prev.iloc[0]["coste_unitario"] or 0)
                        unidad_p = str(mat_prev.iloc[0].get("unidad", ""))
                        st.caption(
                            f"Unidad: **{unidad_p}** · Costo/unidad: **${coste_p:,.4f}**"
                            f" · Subtotal estimado: **${cant_uso * coste_p:,.2f}**"
                        )
                    if st.form_submit_button("Agregar", type="primary"):
                        if cant_uso <= 0:
                            st.error("La cantidad debe ser mayor a 0.")
                        else:
                            try:
                                hoja.worksheet("costos_procedimiento").append_row([proc_sel, mat_elegido, cant_uso])
                                st.success(f"✅ '{mat_elegido}' agregado a '{proc_sel}'.")
                                recargar()
                            except Exception as e:
                                st.error(f"Error: {e}")

        # ── Materiales asignados ──────────────────────────
        costo_materiales = 0.0
        detalle_costos   = []
        mats_del_proc = (
            costos_proc[costos_proc["procedimiento"] == proc_sel]
            if not costos_proc.empty and "procedimiento" in costos_proc.columns
            else pd.DataFrame()
        )

        if mats_del_proc.empty:
            st.info("Este servicio no tiene materiales asignados. Usá el formulario de arriba para agregar.")
        else:
            st.subheader("Materiales asignados")
            if not materiales.empty and "nombre" in materiales.columns:
                for _, uso in mats_del_proc.iterrows():
                    mat_nombre = str(uso["material"]).strip()
                    cant       = float(uso["cantidad"]) if uso["cantidad"] else 0
                    mat_row    = materiales[materiales["nombre"] == mat_nombre]
                    if not mat_row.empty:
                        coste_u  = float(mat_row.iloc[0]["coste_unitario"] or 0)
                        subtotal = cant * coste_u
                        costo_materiales += subtotal
                        detalle_costos.append({
                            "Material":       mat_nombre,
                            "Cantidad":       f"{cant} {mat_row.iloc[0].get('unidad', '')}".strip(),
                            "Costo unitario": f"${coste_u:,.4f}",
                            "Subtotal":       f"${subtotal:,.0f}",
                        })
                    else:
                        st.warning(f"'{mat_nombre}' no encontrado en materiales.")
            if detalle_costos:
                st.dataframe(pd.DataFrame(detalle_costos), use_container_width=True, hide_index=True)

            with st.expander("🗑️ Quitar material de este servicio"):
                mat_quitar  = st.selectbox("Material a quitar", mats_del_proc["material"].tolist(), key="sel_quitar_mat")
                confirmar_q = st.checkbox("Confirmar", key="confirm_quitar_mat")
                if st.button("Quitar material", disabled=not confirmar_q, key="btn_quitar_mat"):
                    try:
                        ws_cp    = hoja.worksheet("costos_procedimiento")
                        all_rows = ws_cp.get_all_values()
                        headers  = all_rows[0] if all_rows else []
                        if "procedimiento" not in headers or "material" not in headers:
                            st.error("La hoja 'costos_procedimiento' no tiene las columnas esperadas.")
                            st.stop()
                        col_p, col_m = headers.index("procedimiento"), headers.index("material")
                        fila_del = next(
                            (i for i, r in enumerate(all_rows[1:], start=2)
                             if r[col_p] == proc_sel and r[col_m] == mat_quitar),
                            None,
                        )
                        if fila_del:
                            ws_cp.delete_rows(fila_del)
                            st.success(f"'{mat_quitar}' quitado de '{proc_sel}'.")
                            recargar()
                        else:
                            st.error("No se encontró esa combinación en la hoja.")
                    except Exception as e:
                        st.error(f"Error: {e}")

        # ── Costos operativos ─────────────────────────────
        st.divider()
        st.subheader("Costos operativos")
        oc1, oc2 = st.columns(2)
        with oc1:
            costo_prof = st.number_input("Tiempo profesional ($)", min_value=0.0, step=500.0, key="op_prof")
            costo_cab  = st.number_input("Cabina ($)", min_value=0.0, step=500.0, key="op_cab")
        with oc2:
            costo_cons = st.number_input("Consumibles ($)", min_value=0.0, step=500.0, key="op_cons")

        costo_operativo = costo_prof + costo_cab + costo_cons
        costo_total     = costo_materiales + costo_operativo
        margen          = normalizar_margen(srv_info.get("margen_objetivo", 0.65))
        if 0 < margen < 1:
            precio_rec = costo_total / (1 - margen)   # margen clásico (ej. 65% → precio = costo/0.35)
        elif margen >= 1:
            precio_rec = costo_total * margen          # multiplicador (ej. 300% → precio = 3x costo)
        else:
            precio_rec = costo_total
        beneficio       = precio_rec - costo_total

        precio_raw = srv_info.get("precio", None)
        try:
            precio_act = float(precio_raw) if pd.notna(precio_raw) and str(precio_raw).strip() not in ("", "0") else None
        except (TypeError, ValueError):
            precio_act = None

        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Costo materiales",   f"${costo_materiales:,.0f}")
        m2.metric("Costo operativo",    f"${costo_operativo:,.0f}")
        m3.metric("Costo total",        f"${costo_total:,.0f}")
        m4.metric("Precio recomendado", f"${precio_rec:,.0f}")

        if precio_act:
            diferencia = precio_act - precio_rec
            st.metric(
                "Precio actual en agenda", f"${precio_act:,.0f}",
                delta=f"${diferencia:+,.0f} vs recomendado",
                delta_color="normal",
            )

        st.metric(
            "Beneficio estimado", f"${beneficio:,.0f}",
            delta=f"{margen*100:.0f}% margen objetivo",
        )

# =========================================================
# INGRESOS
# =========================================================

with tabs[5]:
    st.title("Ingresos")

    # ── Registrar ─────────────────────────────────────────
    with st.expander("➕ Registrar ingreso"):
        # Selectores FUERA del form para que funcionen condicionalmente
        fecha_ing = st.date_input("Fecha", value=date.today(), key="fecha_ing_input")

        if not servicios.empty and "nombre" in servicios.columns:
            opciones_srv = [""] + servicios["nombre"].dropna().tolist()
            sel_srv      = st.selectbox("Servicio (elegí de la lista o escribí abajo)", opciones_srv, key="sel_srv_ing")
            srv_manual   = st.text_input("Servicio (si no está en la lista)", key="srv_manual_ing")
            servicio_ing = srv_manual.strip() if srv_manual.strip() else sel_srv
        else:
            servicio_ing = st.text_input("Servicio", key="srv_ing")

        if not clientes.empty and "nombre" in clientes.columns:
            opciones_cli = [""] + clientes["nombre"].dropna().tolist()
            sel_cli      = st.selectbox("Cliente (elegí de la lista o escribí abajo)", opciones_cli, key="sel_cli_ing")
            cli_manual   = st.text_input("Cliente (si no está en la lista)", key="cli_manual_ing")
            cliente_ing  = cli_manual.strip() if cli_manual.strip() else sel_cli
        else:
            cliente_ing = st.text_input("Cliente", key="cli_ing")

        monto_ing    = st.number_input("Monto ($)", min_value=0.0, step=500.0, key="monto_ing")
        descontar_st = st.checkbox(
            "Descontar materiales del stock automáticamente", value=True,
            help="Deduce del stock los materiales definidos en 'costos_procedimiento'.",
        )

        if st.button("Registrar ingreso", type="primary", key="btn_reg_ing"):
            if monto_ing <= 0:
                st.error("El monto debe ser mayor a $0.")
            elif not cliente_ing:
                st.error("El cliente es obligatorio.")
            else:
                try:
                    hoja.worksheet("ingresos").append_row(
                        [str(fecha_ing), cliente_ing, servicio_ing, float(monto_ing)]
                    )
                    st.success("✅ Ingreso registrado.")
                    if descontar_st and servicio_ing:
                        ajustes = descontar_stock(servicio_ing)
                        if ajustes:
                            st.info(f"Stock actualizado: {len(ajustes)} material(es) descontado(s).")
                        elif not costos_proc.empty:
                            st.caption("No hay materiales definidos para este servicio en costos_procedimiento.")
                    recargar()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()

    if ingresos.empty:
        st.info("No hay ingresos registrados.")
    else:
        # ── Métricas ──────────────────────────────────────
        i1, i2, i3 = st.columns(3)
        i1.metric("Total",         f"${ingresos['monto'].sum():,.0f}")
        i2.metric("Promedio",      f"${ingresos['monto'].mean():,.0f}")
        i3.metric("Mayor ingreso", f"${ingresos['monto'].max():,.0f}")

        # ── Filtro por fecha ──────────────────────────────
        st.divider()
        fc1, fc2 = st.columns(2)
        with fc1:
            desde_ing = st.date_input("Desde", value=date(date.today().year, 1, 1), key="ing_desde")
        with fc2:
            hasta_ing = st.date_input("Hasta", value=date.today(), key="ing_hasta")

        df_i = ingresos.copy()
        if "fecha" in df_i.columns:
            df_i["_fecha_dt"] = pd.to_datetime(df_i["fecha"], errors="coerce")
            df_i = df_i[df_i["_fecha_dt"].dt.date.between(desde_ing, hasta_ing)].drop(columns=["_fecha_dt"])

        busq_i = st.text_input("🔍 Buscar", key="busq_ing")
        if busq_i:
            mask = df_i.apply(lambda c: c.astype(str).str.contains(busq_i, case=False, na=False)).any(axis=1)
            df_i = df_i[mask]

        # ── Gráfico del período ───────────────────────────
        if "fecha" in df_i.columns and not df_i.empty:
            chart_i = df_i.copy()
            chart_i["fecha"] = pd.to_datetime(chart_i["fecha"], errors="coerce")
            chart_i = chart_i.dropna(subset=["fecha"]).sort_values("fecha")
            chart_i["mes"] = chart_i["fecha"].dt.to_period("M").astype(str)
            st.bar_chart(chart_i.groupby("mes")["monto"].sum())

        tabla(df_i)
        csv_btn(df_i, "ingresos.csv")

        # ── Eliminar ──────────────────────────────────────
        with st.expander("🗑️ Eliminar ingreso"):
            opciones_ing = [
                f"{r.get('fecha','')} | {r.get('cliente','')} | {r.get('servicio','')} | ${float(r.get('monto',0) or 0):,.0f}"
                for _, r in ingresos.iterrows()
            ]
            ing_borrar_lbl = st.selectbox("Seleccionar", opciones_ing, key="sel_del_ing")
            confirmar_ing  = st.checkbox("Confirmar eliminación", key="confirm_del_ing")
            if st.button("Eliminar ingreso", disabled=not confirmar_ing, key="btn_del_ing"):
                try:
                    idx          = opciones_ing.index(ing_borrar_lbl)
                    fila_sheets  = idx + 2
                    ws           = hoja.worksheet("ingresos")
                    ws.delete_rows(fila_sheets)
                    st.success("Ingreso eliminado.")
                    recargar()
                except Exception as e:
                    st.error(f"Error: {e}")

# =========================================================
# GASTOS
# =========================================================

with tabs[6]:
    st.title("Gastos")

    # ── Registrar ─────────────────────────────────────────
    with st.expander("➕ Registrar gasto"):
        fecha_gast   = st.date_input("Fecha", value=date.today(), key="fecha_gast_input")
        cats_gasto   = sorted(gastos["categoria"].dropna().unique().tolist()) if not gastos.empty and "categoria" in gastos.columns else []
        opciones_cat = [""] + cats_gasto
        sel_cat      = st.selectbox("Categoría (elegí o escribí abajo)", opciones_cat, key="sel_cat_gasto")
        cat_manual   = st.text_input("Nueva categoría (si no está en la lista)", key="cat_manual_gasto")
        cat_gasto    = cat_manual.strip() if cat_manual.strip() else sel_cat

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            importe_gast = st.number_input("Importe ($)", min_value=0.0, step=100.0, key="importe_gast")
        with col_g2:
            desc_gast = st.text_input("Descripción", key="desc_gast")

        if st.button("Registrar gasto", type="primary", key="btn_reg_gast"):
            if importe_gast <= 0:
                st.error("El importe debe ser mayor a $0.")
            elif not cat_gasto:
                st.error("La categoría es obligatoria.")
            else:
                try:
                    hoja.worksheet("gastos").append_row(
                        [str(fecha_gast), cat_gasto, float(importe_gast), desc_gast.strip()]
                    )
                    st.success("✅ Gasto registrado.")
                    recargar()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()

    if gastos.empty:
        st.info("No hay gastos registrados.")
    else:
        g1, g2, g3 = st.columns(3)
        g1.metric("Total gastos",    f"${gastos['importe'].sum():,.0f}")
        g2.metric("Promedio",        f"${gastos['importe'].mean():,.0f}")
        g3.metric("Mayor gasto",     f"${gastos['importe'].max():,.0f}")

        # ── Filtro por fecha ──────────────────────────────
        st.divider()
        gc1, gc2 = st.columns(2)
        with gc1:
            desde_gast = st.date_input("Desde", value=date(date.today().year, 1, 1), key="gast_desde")
        with gc2:
            hasta_gast = st.date_input("Hasta", value=date.today(), key="gast_hasta")

        df_g = gastos.copy()
        if "fecha" in df_g.columns:
            df_g["_fecha_dt"] = pd.to_datetime(df_g["fecha"], errors="coerce")
            df_g = df_g[df_g["_fecha_dt"].dt.date.between(desde_gast, hasta_gast)].drop(columns=["_fecha_dt"])

        busq_g = st.text_input("🔍 Buscar", key="busq_gast")
        if busq_g:
            mask = df_g.apply(lambda c: c.astype(str).str.contains(busq_g, case=False, na=False)).any(axis=1)
            df_g = df_g[mask]

        # ── Gráficos ──────────────────────────────────────
        if not df_g.empty:
            col_ga, col_gb = st.columns(2)
            with col_ga:
                if "categoria" in df_g.columns:
                    st.subheader("Por categoría")
                    st.bar_chart(df_g.groupby("categoria")["importe"].sum().sort_values(ascending=False))
            with col_gb:
                if "fecha" in df_g.columns:
                    st.subheader("Evolución mensual")
                    chart_g = df_g.copy()
                    chart_g["fecha"] = pd.to_datetime(chart_g["fecha"], errors="coerce")
                    chart_g = chart_g.dropna(subset=["fecha"]).sort_values("fecha")
                    chart_g["mes"] = chart_g["fecha"].dt.to_period("M").astype(str)
                    st.bar_chart(chart_g.groupby("mes")["importe"].sum())

        tabla(df_g)
        csv_btn(df_g, "gastos.csv")

        # ── Eliminar ──────────────────────────────────────
        with st.expander("🗑️ Eliminar gasto"):
            opciones_gast = [
                f"{r.get('fecha','')} | {r.get('categoria','')} | {r.get('descripcion','')} | ${float(r.get('importe',0) or 0):,.0f}"
                for _, r in gastos.iterrows()
            ]
            gast_borrar_lbl = st.selectbox("Seleccionar", opciones_gast, key="sel_del_gast")
            confirmar_gast  = st.checkbox("Confirmar eliminación", key="confirm_del_gast")
            if st.button("Eliminar gasto", disabled=not confirmar_gast, key="btn_del_gast"):
                try:
                    idx         = opciones_gast.index(gast_borrar_lbl)
                    fila_sheets = idx + 2
                    ws          = hoja.worksheet("gastos")
                    ws.delete_rows(fila_sheets)
                    st.success("Gasto eliminado.")
                    recargar()
                except Exception as e:
                    st.error(f"Error: {e}")
