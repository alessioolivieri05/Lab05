import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- GUI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    input_tipo= ft.TextField("Tipo")
    input_marca = ft.TextField("Marca")
    input_anno = ft.TextField("Anno acquisto")
    text_prezzo = ft.TextField(value=0, width=70, disabled=True, text_size=20, text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def handler_minus(e):
        v = int(text_prezzo.value)
        v -= 1
        text_prezzo.value = v
        text_prezzo.update()

    def handler_plus(e):
        v = int(text_prezzo.value)
        v += 1
        text_prezzo.value = v
        text_prezzo.update()


    def on_click_aggiungi(e):
        if not (input_tipo.value and input_marca.value and input_anno.value):
            alert.show_alert("❌ Compila tutti i campi")
            return
        try:
            deposito.aggiungi_strumento(
            input_tipo.value,
            input_marca.value,
            int(input_anno.value),
            float(text_prezzo.value),
            )

        except ValueError:
            alert.show_alert("❌ L'anno deve essere un numero intero")
            return

        aggiorna_lista_strumenti()
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        text_prezzo.value = "0"
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    my_button_plus = ft.IconButton(icon=ft.Icons.ADD, icon_size=20, icon_color="green", on_click=handler_plus)
    my_button_minus = ft.IconButton(icon=ft.Icons.REMOVE, icon_size=20, icon_color="red", on_click=handler_minus)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi Strumento", on_click=on_click_aggiungi)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Modifica Strumenti", size=20),
        ft.Row(spacing=20,
               controls=[input_tipo, input_marca, input_anno, my_button_minus, text_prezzo, my_button_plus],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
