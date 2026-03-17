import flet as ft
import requests
import threading

def main(page: ft.Page):
    page.title = "Joker Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 400
    page.window_height = 700
    
    # متغيرات الحالة
    state = {
        "system": "",
        "connected": False
    }

    # دالة فحص الاتصال في الخلفية
    def check_esp(mode, name):
        try:
            # إرسال الطلب مع مهلة زمنية قصيرة
            response = requests.get(f"http://192.168.4.1/set?m={mode}", timeout=2)
            state["connected"] = True if response.status_code == 200 else False
        except:
            state["connected"] = False
        
        state["system"] = name
        page.go("/status")

    def nav_to_loading(mode, name):
        page.go("/loading")
        # تشغيل الفحص في Thread منفصل لمنع تجمد التطبيق
        threading.Thread(target=check_esp, args=(mode, name), daemon=True).start()

    def route_change(route):
        page.views.clear()
        
        # --- الشاشة الافتتاحية ---
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    ft.Container(
                        content=ft.Column([
                            ft.Image(src="logo.png", width=220, height=220, fit=ft.ImageFit.CONTAIN),
                            ft.Container(height=40),
                            ft.ElevatedButton(
                                "ENTER SYSTEM", 
                                bgcolor="#FF0000", color="white",
                                width=250, height=60,
                                on_click=lambda _: page.go("/dashboard"),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="white")
            )

        # --- لوحة التحكم (Dashboard) ---
        elif page.route == "/dashboard":
            page.views.append(
                ft.View("/dashboard", [
                    ft.AppBar(title=ft.Text("JOKER PRO SYSTEMS", weight="bold"), bgcolor="#FF0000", color="white", center_title=True),
                    ft.Container(
                        content=ft.Column([
                            ft.ElevatedButton("LANDI RENZO", width=320, height=75, color="#FF0000", bgcolor="white", on_click=lambda _: nav_to_loading(0, "LANDI RENZO")),
                            ft.ElevatedButton("ALL ZENIT - T-FLASH", width=320, height=75, color="#FF0000", bgcolor="white", on_click=lambda _: nav_to_loading(1, "ZENIT T-FLASH")),
                            ft.ElevatedButton("ZENIT BLUE BOX", width=320, height=75, color="#FF0000", bgcolor="white", on_click=lambda _: nav_to_loading(2, "ZENIT BLUE BOX")),
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="#F5F5F5")
            )

        # --- شاشة التحميل ---
        elif page.route == "/loading":
            page.views.append(
                ft.View("/loading", [
                    ft.Container(
                        content=ft.Column([
                            ft.ProgressRing(width=50, height=50, stroke_width=5, color="#FF0000"),
                            ft.Container(height=20),
                            ft.Text("SENDING COMMAND...", size=18, weight="bold")
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="white")
            )

        # --- شاشة الحالة (خضراء/حمراء) ---
        elif page.route == "/status":
            res_color = ft.colors.GREEN if state["connected"] else ft.colors.RED
            res_icon = ft.icons.CHECK_CIRCLE if state["connected"] else ft.icons.CANCEL
            res_text = "CONNECTED" if state["connected"] else "FAILED"
            
            page.views.append(
                ft.View("/status", [
                    ft.AppBar(title=ft.Text("SYSTEM STATUS"), bgcolor="#FF0000", color="white", leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard"))),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(res_icon, color=res_color, size=120),
                            ft.Text(res_text, color=res_color, size=30, weight="bold"),
                            ft.Divider(height=40, color="transparent"),
                            ft.Text("SELECTED:", color="grey", size=16),
                            ft.Text(state["system"], size=22, weight="bold"),
                            ft.Container(height=40),
                            ft.ElevatedButton("BACK TO MENU", width=250, height=55, bgcolor="#FF0000", color="white", on_click=lambda _: page.go("/dashboard"))
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="white")
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# تشغيل مع تحديد مجلد الصور
ft.app(target=main, assets_dir="assets")
