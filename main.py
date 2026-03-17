import flet as ft
import requests
import threading

def main(page: ft.Page):
    page.title = "Joker Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F5F5"
    page.padding = 20

    state = {"system": "", "connected": False}

    def check_connection(mode, name):
        try:
            # محاولة الاتصال بالـ ESP
            res = requests.get(f"http://192.168.4.1/set?m={mode}", timeout=1.5)
            state["connected"] = True if res.status_code == 200 else False
        except:
            state["connected"] = False
        state["system"] = name
        page.go("/status")

    def start_process(mode, name):
        page.go("/loading")
        threading.Thread(target=check_connection, args=(mode, name), daemon=True).start()

    def route_change(route):
        page.views.clear()
        
        # 1. شاشة الافتتاحية
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    ft.Container(
                        content=ft.Column([
                            ft.Image(src="logo.png", width=250, height=250),
                            ft.Container(height=40),
                            ft.ElevatedButton("ENTER SYSTEM", bgcolor="red", color="white", width=280, height=60, on_click=lambda _: page.go("/dashboard"))
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ])
            )

        # 2. لوحة التحكم
        elif page.route == "/dashboard":
            page.views.append(
                ft.View("/dashboard", [
                    ft.AppBar(title=ft.Text("SELECT SYSTEM"), bgcolor="red", color="white", center_title=True),
                    ft.Container(
                        content=ft.Column([
                            ft.ElevatedButton("LANDI RENZO", width=300, height=80, on_click=lambda _: start_process(0, "LANDI RENZO")),
                            ft.ElevatedButton("ZENIT T-FLASH", width=300, height=80, on_click=lambda _: start_process(1, "ZENIT T-FLASH")),
                            ft.ElevatedButton("ZENIT BLUE BOX", width=300, height=80, on_click=lambda _: start_process(2, "ZENIT BLUE BOX")),
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                        expand=True, alignment=ft.alignment.center
                    )
                ])
            )

        # 3. شاشة التحميل
        elif page.route == "/loading":
            page.views.append(
                ft.View("/loading", [
                    ft.Container(
                        content=ft.Column([
                            ft.ProgressRing(color="red"),
                            ft.Text("SENDING...")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ])
            )

        # 4. شاشة الحالة
        elif page.route == "/status":
            color = "green" if state["connected"] else "red"
            page.views.append(
                ft.View("/status", [
                    ft.AppBar(title=ft.Text("RESULT"), bgcolor="red", color="white"),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.CIRCLE, color=color, size=150),
                            ft.Text("CONNECTED" if state["connected"] else "FAILED", size=30, color=color, weight="bold"),
                            ft.Text(f"System: {state['system']}"),
                            ft.ElevatedButton("BACK", on_click=lambda _: page.go("/dashboard"))
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ])
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# هنا السر: flet سيقوم بالبحث عن مجلد assets تلقائياً
ft.app(target=main, assets_dir="assets")
