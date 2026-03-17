import flet as ft
import requests
import threading

def main(page: ft.Page):
    page.title = "Joker Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F5F5"
    
    current_system = ""
    is_connected = False

    def check_connection(mode):
        nonlocal is_connected
        try:
            # إرسال الأمر للـ ESP
            res = requests.get(f"http://192.168.4.1/set?m={mode}", timeout=1.5)
            is_connected = True if res.status_code == 200 else False
        except:
            is_connected = False
        
        page.go("/status")

    def on_system_click(mode, name):
        nonlocal current_system
        current_system = name
        page.go("/loading")
        threading.Thread(target=check_connection, args=(mode,)).start()

    def route_change(route):
        page.views.clear()
        
        # 1. شاشة الافتتاحية (Splash Screen)
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src="logo.png", width=250, height=250, fit=ft.ImageFit.CONTAIN),
                                ft.Container(height=40),
                                ft.ElevatedButton("ENTER SYSTEM", bgcolor="#FF0000", color="white", width=280, height=65, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)), on_click=lambda _: page.go("/dashboard"))
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center, expand=True
                        )
                    ], bgcolor="white"
                )
            )
            
        # 2. شاشة الداشبورد (اختيار الأنظمة)
        elif page.route == "/dashboard":
            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        ft.AppBar(title=ft.Text("JOKER PRO SYSTEMS", weight="bold"), bgcolor="#FF0000", color="white", center_title=True),
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton("LANDI RENZO", width=320, height=80, bgcolor="white", color="#FF0000", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=lambda _: on_system_click(0, "LANDI RENZO")),
                                ft.ElevatedButton("ALL ZENIT - T-FLASH", width=320, height=80, bgcolor="white", color="#FF0000", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=lambda _: on_system_click(1, "ALL ZENIT - T-FLASH")),
                                ft.ElevatedButton("ZENIT BLUE BOX", width=320, height=80, bgcolor="white", color="#FF0000", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=lambda _: on_system_click(2, "ZENIT BLUE BOX")),
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                            alignment=ft.alignment.center, expand=True
                        )
                    ], bgcolor="#F5F5F5"
                )
            )
            
        # 3. شاشة التحميل
        elif page.route == "/loading":
            page.views.append(
                ft.View(
                    "/loading",
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.ProgressRing(color="#FF0000", stroke_width=6),
                                ft.Container(height=20),
                                ft.Text("CONNECTING...", size=20, weight="bold", color="black")
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center, expand=True
                        )
                    ], bgcolor="white"
                )
            )
            
        # 4. شاشة حالة الاتصال
        elif page.route == "/status":
            status_color = ft.colors.GREEN if is_connected else ft.colors.RED
            status_text = "CONNECTED" if is_connected else "DISCONNECTED"
            status_icon = ft.icons.CHECK_CIRCLE if is_connected else ft.icons.CANCEL
            
            page.views.append(
                ft.View(
                    "/status",
                    [
                        ft.AppBar(title=ft.Text("STATUS"), bgcolor="#FF0000", color="white", center_title=True, leading=ft.IconButton(ft.icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/dashboard"))),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(status_icon, color=status_color, size=160),
                                ft.Text(status_text, size=35, weight="bold", color=status_color),
                                ft.Container(height=30),
                                ft.Text("ACTIVE SYSTEM:", size=18, color="grey"),
                                ft.Text(current_system, size=28, weight="bold", color="black"),
                                ft.Container(height=60),
                                ft.ElevatedButton("BACK TO DASHBOARD", bgcolor="#FF0000", color="white", width=280, height=60, on_click=lambda _: page.go("/dashboard"))
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center, expand=True
                        )
                    ], bgcolor="white"
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# تحديد مجلد الصور لتفادي الشاشة البيضاء
ft.app(target=main, assets_dir="assets")
