import tkinter as tk
from tkinter import ttk, messagebox
import json
import api_client

BG = "#181a1f"
BG_PANEL = "#20232b"
FG = "#e6e6e6"
FG_MUTED = "#9aa0ab"
ACCENT = "#4f8cff"
SUCCESS = "#3ecf8e"
DANGER = "#ff5d5d"
FONT = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 11, "bold")
FONT_MONO = ("Consolas", 10)

ventana = tk.Tk()
ventana.title("Cliente API REST")
ventana.geometry("780x620")
ventana.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=BG)
style.configure("Panel.TFrame", background=BG_PANEL)
style.configure("TLabel", background=BG, foreground=FG, font=FONT)
style.configure("Panel.TLabel", background=BG_PANEL, foreground=FG, font=FONT)
style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=FONT_TITLE)
style.configure("Muted.TLabel", background=BG_PANEL, foreground=FG_MUTED, font=FONT)

style.configure("TButton", font=FONT, padding=8, background=BG_PANEL, foreground=FG, borderwidth=0)
style.map("TButton", background=[("active", ACCENT)], foreground=[("active", "#ffffff")])

style.configure("Danger.TButton", font=FONT, padding=8, background=BG_PANEL, foreground=DANGER, borderwidth=0)
style.map("Danger.TButton", background=[("active", DANGER)], foreground=[("active", "#ffffff")])

style.configure("TEntry", fieldbackground="#2a2e38", foreground=FG, insertcolor=FG, borderwidth=0, padding=6)

style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=BG_PANEL, foreground=FG_MUTED, padding=(16, 8), font=FONT)
style.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "#ffffff")])

style.configure("Treeview", background="#22252d", fieldbackground="#22252d", foreground=FG, rowheight=26, borderwidth=0, font=FONT)
style.configure("Treeview.Heading", background=BG_PANEL, foreground=ACCENT, font=FONT_TITLE, borderwidth=0)
style.map("Treeview", background=[("selected", ACCENT)])

# --- Layout principal ---
ttk.Label(ventana, text="Cliente API REST", style="Title.TLabel").pack(anchor="w", padx=20, pady=(16, 8))

notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 12))

# --- Barra de estado inferior ---
status_var = tk.StringVar(value="Listo.")
status_bar = ttk.Label(ventana, textvariable=status_var, style="Muted.TLabel", anchor="w")
status_bar.pack(fill=tk.X, padx=20, pady=(0, 12))


def set_status(texto, color=FG_MUTED):
    status_var.set(texto)
    status_bar.configure(foreground=color)


def manejar_generico(response, on_success_text="Operación exitosa.", avisar=False):
    if response is None:
        set_status("No se pudo conectar al servidor.", DANGER)
        if avisar:
            messagebox.showerror("Sin conexión", "No se pudo conectar al servidor.")
        return None
    if response.status_code in (200, 201):
        set_status(f"Status {response.status_code} — {on_success_text}", SUCCESS)
        if avisar:
            messagebox.showinfo("Éxito", on_success_text)
        try:
            return response.json()
        except Exception:
            return None
    if response.status_code == 204:
        set_status(f"Status {response.status_code} — {on_success_text}", SUCCESS)
        if avisar:
            messagebox.showinfo("Éxito", on_success_text)
        return None
    if response.status_code == 404:
        set_status("Status 404 — Recurso no encontrado.", DANGER)
        if avisar:
            messagebox.showerror("No encontrado", "El usuario no existe.")
        return None
    if response.status_code == 400:
        try:
            msg = response.json().get("Error", "Solicitud inválida.")
        except Exception:
            msg = "Solicitud inválida."
        set_status(f"Status 400 — {msg}", DANGER)
        if avisar:
            messagebox.showerror("Solicitud inválida", msg)
        return None
    set_status(f"Status {response.status_code} — Error no esperado.", DANGER)
    if avisar:
        messagebox.showerror("Error", f"Status {response.status_code} — error no esperado.")
    return None


# ======================= PESTAÑA: TODOS LOS USUARIOS =======================
tab_todos = ttk.Frame(notebook, style="TFrame", padding=12)
notebook.add(tab_todos, text="Todos los usuarios")

barra_todos = ttk.Frame(tab_todos)
barra_todos.pack(fill=tk.X, pady=(0, 10))

tabla = ttk.Treeview(tab_todos, columns=("id", "name", "age", "phone"), show="headings")
for col, ancho in (("id", 60), ("name", 220), ("age", 80), ("phone", 160)):
    tabla.heading(col, text=col.capitalize())
    tabla.column(col, width=ancho, anchor="w")
tabla.pack(fill=tk.BOTH, expand=True)


def refrescar_tabla():
    response = api_client.all_users()
    data = manejar_generico(response, "Lista actualizada.")
    tabla.delete(*tabla.get_children())
    if data:
        for u in data:
            tabla.insert("", tk.END, values=(u.get("id"), u.get("name"), u.get("age"), u.get("phone")))


ttk.Button(barra_todos, text="Refrescar lista", command=refrescar_tabla).pack(side=tk.LEFT)
ttk.Button(
    barra_todos, text="Eliminar TODOS", style="Danger.TButton",
    command=lambda: (manejar_generico(api_client.delete_all_users(), "Todos los usuarios eliminados."), refrescar_tabla())
).pack(side=tk.RIGHT)

# ======================= PESTAÑA: BUSCAR / ELIMINAR POR ID =======================
tab_id = ttk.Frame(notebook, style="TFrame", padding=20)
notebook.add(tab_id, text="Buscar / eliminar")

ttk.Label(tab_id, text="ID del usuario").pack(anchor="w")
entry_id = ttk.Entry(tab_id, width=20)
entry_id.pack(anchor="w", pady=(4, 12))

fila_botones_id = ttk.Frame(tab_id)
fila_botones_id.pack(anchor="w", pady=(0, 16))

resultado_id = tk.Text(tab_id, height=10, bg="#111318", fg=SUCCESS, insertbackground=FG,
                        font=FONT_MONO, relief=tk.FLAT, padx=10, pady=10)
resultado_id.pack(fill=tk.BOTH, expand=True)


def mostrar_json(widget, data):
    widget.delete("1.0", tk.END)
    if data is not None:
        widget.insert(tk.END, json.dumps(data, indent=2, ensure_ascii=False))


def accion_buscar():
    try:
        id_val = int(entry_id.get())
    except ValueError:
        set_status("El id debe ser un número entero.", DANGER)
        return
    data = manejar_generico(api_client.user(id_val), "Usuario encontrado.")
    mostrar_json(resultado_id, data)


def accion_eliminar_uno():
    try:
        id_val = int(entry_id.get())
    except ValueError:
        set_status("El id debe ser un número entero.", DANGER)
        return
    manejar_generico(api_client.delete_users(id_val), "Usuario eliminado.", avisar=True)
    resultado_id.delete("1.0", tk.END)
    refrescar_tabla()


ttk.Button(fila_botones_id, text="Buscar", command=accion_buscar).pack(side=tk.LEFT, padx=(0, 8))
ttk.Button(fila_botones_id, text="Eliminar", style="Danger.TButton", command=accion_eliminar_uno).pack(side=tk.LEFT)

# ======================= PESTAÑA: CREAR =======================
tab_crear = ttk.Frame(notebook, style="TFrame", padding=20)
notebook.add(tab_crear, text="Crear usuario")

campos_crear = [("Nombre", 22), ("Edad", 10), ("Teléfono", 18)]
entries_crear = {}
for i, (label, ancho) in enumerate(campos_crear):
    ttk.Label(tab_crear, text=label).grid(row=0, column=i, sticky="w", padx=(0, 12))
    e = ttk.Entry(tab_crear, width=ancho)
    e.grid(row=1, column=i, sticky="w", padx=(0, 12), pady=(4, 16))
    entries_crear[label] = e


def accion_crear():
    name = entries_crear["Nombre"].get().strip()
    age_raw = entries_crear["Edad"].get().strip()
    phone = entries_crear["Teléfono"].get().strip() or None
    if not name:
        set_status("El nombre es obligatorio.", DANGER)
        return
    try:
        age = int(age_raw) if age_raw else None
    except ValueError:
        set_status("La edad debe ser un número entero.", DANGER)
        return
    manejar_generico(api_client.upload_users(name, age, phone), "Usuario creado.", avisar=True)
    for e in entries_crear.values():
        e.delete(0, tk.END)
    refrescar_tabla()


ttk.Button(tab_crear, text="Crear usuario", command=accion_crear).grid(row=2, column=0, sticky="w")

# ======================= PESTAÑA: ACTUALIZAR =======================
tab_actualizar = ttk.Frame(notebook, style="TFrame", padding=20)
notebook.add(tab_actualizar, text="Actualizar")

ttk.Label(tab_actualizar, text="ID del usuario a actualizar").grid(row=0, column=0, sticky="w", columnspan=2)
entry_update_id = ttk.Entry(tab_actualizar, width=15)
entry_update_id.grid(row=1, column=0, sticky="w", pady=(4, 20))

ttk.Label(tab_actualizar, text="Campo").grid(row=2, column=0, sticky="w")
combo_field = ttk.Combobox(tab_actualizar, values=("Nombre", "Edad", "Teléfono"), state="readonly", width=17)
combo_field.grid(row=3, column=0, sticky="w", pady=(4, 12))

ttk.Label(tab_actualizar, text="Nuevo valor").grid(row=2, column=1, sticky="w", padx=(20, 0))
entry_field_value = ttk.Entry(tab_actualizar, width=20)
entry_field_value.grid(row=3, column=1, sticky="w", padx=(20, 0), pady=(4, 12))


def accion_actualizar_campo():
    try:
        id_val = int(entry_update_id.get())
    except ValueError:
        set_status("El id debe ser un número entero.", DANGER)
        return
    field = combo_field.get()
    value = entry_field_value.get()
    if not field:
        set_status("Selecciona un campo a actualizar.", DANGER)
        return
    manejar_generico(api_client.update_user_field(id_val, field, value), "Campo actualizado.", avisar=True)
    refrescar_tabla()


ttk.Button(tab_actualizar, text="Actualizar campo", command=accion_actualizar_campo).grid(row=4, column=0, sticky="w", pady=(0, 24))

ttk.Separator(tab_actualizar, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 20))

ttk.Label(tab_actualizar, text="Actualizar todos los campos").grid(row=6, column=0, sticky="w", columnspan=2, pady=(0, 8))
campos_full = [("Nombre", 18), ("Edad", 8), ("Teléfono", 16)]
entries_full = {}
for i, (label, ancho) in enumerate(campos_full):
    ttk.Label(tab_actualizar, text=label).grid(row=7, column=i, sticky="w", padx=(0, 12))
    e = ttk.Entry(tab_actualizar, width=ancho)
    e.grid(row=8, column=i, sticky="w", padx=(0, 12), pady=(4, 16))
    entries_full[label] = e


def accion_actualizar_full():
    try:
        id_val = int(entry_update_id.get())
        age = int(entries_full["Edad"].get()) if entries_full["Edad"].get() else None
    except ValueError:
        set_status("El id y la edad deben ser números enteros.", DANGER)
        return
    name = entries_full["Nombre"].get().strip()
    phone = entries_full["Teléfono"].get().strip() or None
    if not name:
        set_status("El nombre es obligatorio.", DANGER)
        return
    manejar_generico(api_client.update_user(id_val, name, age, phone), "Usuario actualizado.", avisar=True)
    refrescar_tabla()


ttk.Button(tab_actualizar, text="Actualizar todo", command=accion_actualizar_full).grid(row=9, column=0, sticky="w")

# Carga inicial
refrescar_tabla()

ventana.mainloop()
