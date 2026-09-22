"""
Skript:  gui_main.py
Autor:   Ihor Demenkov
Datum:   22.09.2026
Zweck:   Grafische Oberflaeche (Flet 1.0) fuer die DCMS Backend Engine.
         Nutzt dieselben Module wie main.py (server_modell, storage,
         network, logger) - nur die Bedienung ist jetzt ein Fenster
         statt ein Text-Menue im Terminal.
"""

import flet as ft

import logger
import network
import storage
from server_modell import DatenbankServer, Server, Webserver


def main(page: ft.Page):
    page.title = "DCMS Backend Engine - GUI"
    page.window.width = 900
    page.window.height = 820
    page.appbar = ft.AppBar(title=ft.Text("DCMS Backend Engine"))

    logger.schreibe_log("INFO", "GUI gestartet")
    server_liste = storage.daten_laden()

    # ---------------------------------------------------------------
    # Anzeige-Elemente, die spaeter aktualisiert werden
    # ---------------------------------------------------------------
    server_spalte = ft.Column(controls=[], spacing=12)
    status_text = ft.Text("", size=14)
    log_text = ft.Text("", size=14)
    dialog_fehler = ft.Text("", color=ft.Colors.RED, size=13)

    # ---------------------------------------------------------------
    # Hilfsfunktionen
    # ---------------------------------------------------------------
    def speichern_und_neu_zeichnen():
        storage.daten_speichern(server_liste)
        liste_neu_zeichnen()

    def liste_neu_zeichnen():
        if not server_liste:
            server_spalte.controls = [
                ft.Text("Noch keine Server angelegt.", italic=True, color=ft.Colors.GREY_600)
            ]
        else:
            server_spalte.controls = [server_karte(s) for s in server_liste]
        page.update()

    def server_karte(server: Server):
        ist_online = server.status == "online"
        farbe = ft.Colors.GREEN_100 if ist_online else ft.Colors.RED_100

        zeilen = [
            ft.Text(server.name, size=18, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[ft.Text("IP:", weight=ft.FontWeight.BOLD), ft.Text(server.ip)]),
            ft.Row(controls=[ft.Text("OS:", weight=ft.FontWeight.BOLD), ft.Text(server.os)]),
            ft.Row(controls=[ft.Text("Status:", weight=ft.FontWeight.BOLD), ft.Text(server.status)]),
        ]

        if isinstance(server, Webserver):
            zeilen.append(ft.Row(controls=[ft.Text("Typ:", weight=ft.FontWeight.BOLD), ft.Text("Webserver")]))
            zeilen.append(ft.Row(controls=[ft.Text("Domain:", weight=ft.FontWeight.BOLD), ft.Text(server.domain)]))
            zeilen.append(ft.Row(controls=[ft.Text("SSL:", weight=ft.FontWeight.BOLD), ft.Text(server.ssl_aktiv)]))
        elif isinstance(server, DatenbankServer):
            zeilen.append(ft.Row(controls=[ft.Text("Typ:", weight=ft.FontWeight.BOLD), ft.Text("Datenbankserver")]))
            zeilen.append(ft.Row(controls=[ft.Text("DB-Typ:", weight=ft.FontWeight.BOLD), ft.Text(server.db_typ)]))
            zeilen.append(ft.Row(controls=[ft.Text("Port:", weight=ft.FontWeight.BOLD), ft.Text(str(server.port))]))
        else:
            zeilen.append(ft.Row(controls=[ft.Text("Typ:", weight=ft.FontWeight.BOLD), ft.Text("Generisch")]))

        zeilen.append(
            ft.Row(controls=[
                ft.Button("Online/Offline", on_click=lambda e, s=server: status_umschalten(s)),
                ft.Button("IP bearbeiten", on_click=lambda e, s=server: ip_dialog_oeffnen(s)),
                ft.Button("Loeschen", on_click=lambda e, s=server: loeschen_dialog_oeffnen(s)),
            ])
        )

        return ft.Container(
            content=ft.Column(controls=zeilen, spacing=4),
            bgcolor=farbe,
            padding=14,
            border_radius=8,
        )

    def status_umschalten(server: Server):
        server.status_wechseln()
        logger.schreibe_log("INFO", f"Status von {server.name} geaendert auf {server.status}")
        speichern_und_neu_zeichnen()

    # ---------------------------------------------------------------
    # Dialog: Server hinzufuegen
    # ---------------------------------------------------------------
    name_feld = ft.TextField(label="Name")
    ip_feld = ft.TextField(label="IP-Adresse")
    os_feld = ft.TextField(label="Betriebssystem")

    domain_feld = ft.TextField(label="Domain")
    ssl_checkbox = ft.Checkbox(label="SSL aktiv", value=False)
    web_felder = ft.Column(controls=[domain_feld, ssl_checkbox], visible=False)

    db_typ_feld = ft.TextField(label="DB-Typ (z. B. PostgreSQL)")
    port_feld = ft.TextField(label="Port")
    db_felder = ft.Column(controls=[db_typ_feld, port_feld], visible=False)

    def typ_geaendert(e):
        web_felder.visible = typ_radio.value == "2"
        db_felder.visible = typ_radio.value == "3"
        page.update()

    typ_radio = ft.RadioGroup(
        content=ft.Column(controls=[
            ft.Radio(value="1", label="Generischer Server"),
            ft.Radio(value="2", label="Webserver"),
            ft.Radio(value="3", label="Datenbankserver"),
        ]),
        value="1",
        on_change=typ_geaendert,
    )

    def felder_zuruecksetzen():
        name_feld.value = ""
        ip_feld.value = ""
        os_feld.value = ""
        domain_feld.value = ""
        ssl_checkbox.value = False
        db_typ_feld.value = ""
        port_feld.value = ""
        typ_radio.value = "1"
        web_felder.visible = False
        db_felder.visible = False
        dialog_fehler.value = ""

    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Neuen Server anlegen"),
        content=ft.Column(
            controls=[name_feld, ip_feld, os_feld, typ_radio, web_felder, db_felder, dialog_fehler],
            tight=True,
            width=380,
        ),
        actions=[
            ft.Button("Abbrechen", on_click=lambda e: page.pop_dialog()),
            ft.Button("Hinzufuegen", on_click=lambda e: server_hinzufuegen(e)),
        ],
    )

    def add_dialog_oeffnen(e):
        felder_zuruecksetzen()
        page.show_dialog(add_dialog)

    def server_hinzufuegen(e):
        name = name_feld.value.strip() if name_feld.value else ""
        ip = ip_feld.value.strip() if ip_feld.value else ""
        os_wert = os_feld.value.strip() if os_feld.value else ""

        if not name or not ip:
            dialog_fehler.value = "Name und IP-Adresse sind Pflichtfelder!"
            page.update()
            return

        if typ_radio.value == "2":
            neuer_server = Webserver(
                name, ip, os_wert,
                domain_feld.value or "",
                "ja" if ssl_checkbox.value else "nein",
            )
        elif typ_radio.value == "3":
            neuer_server = DatenbankServer(
                name, ip, os_wert,
                db_typ_feld.value or "",
                port_feld.value or "",
            )
        else:
            neuer_server = Server(name, ip, os_wert)

        server_liste.append(neuer_server)
        logger.schreibe_log("INFO", f"Server {name} hinzugefuegt")
        page.pop_dialog()
        speichern_und_neu_zeichnen()

    # ---------------------------------------------------------------
    # Dialog: IP bearbeiten
    # ---------------------------------------------------------------
    neue_ip_feld = ft.TextField(label="Neue IP-Adresse")
    ip_dialog_fehler = ft.Text("", color=ft.Colors.RED, size=13)
    aktueller_server_fuer_ip = {"server": None}

    def ip_dialog_oeffnen(server: Server):
        aktueller_server_fuer_ip["server"] = server
        neue_ip_feld.value = server.ip
        ip_dialog_fehler.value = ""
        page.show_dialog(ip_dialog)

    def ip_speichern(e):
        server = aktueller_server_fuer_ip["server"]
        neue_ip = neue_ip_feld.value.strip() if neue_ip_feld.value else ""
        if not neue_ip:
            ip_dialog_fehler.value = "IP-Adresse darf nicht leer sein!"
            page.update()
            return
        server.ip = neue_ip
        logger.schreibe_log("INFO", f"IP von Server {server.name} geaendert auf {neue_ip}")
        page.pop_dialog()
        speichern_und_neu_zeichnen()

    ip_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("IP-Adresse bearbeiten"),
        content=ft.Column(controls=[neue_ip_feld, ip_dialog_fehler], tight=True, width=320),
        actions=[
            ft.Button("Abbrechen", on_click=lambda e: page.pop_dialog()),
            ft.Button("Speichern", on_click=ip_speichern),
        ],
    )

    # ---------------------------------------------------------------
    # Dialog: Server loeschen
    # ---------------------------------------------------------------
    loeschen_hinweis = ft.Text("")
    aktueller_server_fuer_loeschen = {"server": None}

    def loeschen_dialog_oeffnen(server: Server):
        aktueller_server_fuer_loeschen["server"] = server
        loeschen_hinweis.value = f"Server '{server.name}' wirklich loeschen?"
        page.show_dialog(loeschen_dialog)

    def server_loeschen(e):
        server = aktueller_server_fuer_loeschen["server"]
        server_liste.remove(server)
        logger.schreibe_log("INFO", f"Server {server.name} geloescht")
        page.pop_dialog()
        speichern_und_neu_zeichnen()

    loeschen_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Server loeschen"),
        content=loeschen_hinweis,
        actions=[
            ft.Button("Abbrechen", on_click=lambda e: page.pop_dialog()),
            ft.Button("Loeschen", on_click=server_loeschen),
        ],
    )

    # ---------------------------------------------------------------
    # System-Status pruefen (Netzwerk) und Log-Report
    # ---------------------------------------------------------------
    def status_pruefen(e):
        status_text.value = "Pruefe Verbindung..."
        status_text.color = ft.Colors.GREY_700
        page.update()  # Zwischenstand manuell anzeigen, bevor die Netzwerk-Anfrage laeuft

        ip = network.hole_externe_ip()
        if ip is None:
            status_text.value = "Keine Internetverbindung verfuegbar."
            status_text.color = ft.Colors.RED
        else:
            standort = network.hole_standort(ip)
            if standort is not None:
                status_text.value = (
                    f"System online. Externe IP: {ip}. "
                    f"Standort: {standort.get('city')}, {standort.get('country')}. "
                    f"Provider: {standort.get('isp')}."
                )
                status_text.color = ft.Colors.GREEN
            else:
                status_text.value = f"System online. Externe IP: {ip}. Standort konnte nicht ermittelt werden."
                status_text.color = ft.Colors.GREEN
        page.update()

    def log_report_anzeigen(e):
        try:
            error_counter = 0
            info_counter = 0
            with open("dcms_audit.log", "r", encoding="utf-8") as datei:
                for zeile in datei:
                    if "[ERROR]" in zeile:
                        error_counter += 1
                    elif "[INFO]" in zeile:
                        info_counter += 1
            log_text.value = f"Log-Report: {info_counter} INFO, {error_counter} ERROR"
        except FileNotFoundError:
            log_text.value = "Noch keine dcms_audit.log vorhanden."
        page.update()

    # ---------------------------------------------------------------
    # Seitenaufbau
    # ---------------------------------------------------------------
    page.add(
        ft.Row(controls=[
            ft.Button("+ Server hinzufuegen", on_click=add_dialog_oeffnen),
            ft.Button("Status pruefen", on_click=status_pruefen),
            ft.Button("Log-Report", on_click=log_report_anzeigen),
        ]),
        status_text,
        log_text,
        ft.Divider(),
        ft.Text("Server-Uebersicht", size=20, weight=ft.FontWeight.BOLD),
        ft.Column(controls=[server_spalte], scroll=ft.ScrollMode.AUTO, height=480),
    )

    liste_neu_zeichnen()


if __name__ == "__main__":
    ft.run(main)
