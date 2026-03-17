import flet as ft
import requests
import threading
import time

def main(page: ft.Page):
    # إعدادات الصفحة الأساسية
    page.title = "Joker Pro v2.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.window_width = 380
    page.window_height = 700
    
    # متغيرات حالة الاتصال
    status_data = {
        "active_name": "",
        "is_ok": False
    }

    # دالة إرسال الأمر للـ ESP32/ESP8266
    def send_command(mode, name):
        try:
            # مهلة 2 ثانية فقط للرد لتجنب الانتظار الطويل
            url = f"http://192.168.4.1/set?m={mode}"
            response = requests.get(url, timeout=2.0)
            status_data["is_ok"] = True if response.status_code == 200 else False
        except Exception:
            status_data["is_ok"] = False
        
        status_data["active_name"] = name
        # الانتقال لصفحة النتيجة بعد الانتهاء
        page.go("/status")

    # دالة لبدء عملية الاتصال في الخلفية
    def start_connection(mode, name):
        page.go("/loading")
        # تشغيل في مسار منفصل (Thread) لمنع الشاشة البيضاء
        threading.Thread(target=send_command, args=(mode, name), daemon=True).start()

    def route_change(e):
        page.views.clear()
        
        # --- 1. الشاشة الافتتاحية (Splash) ---
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    ft.Container(
                        content=ft.Column([
                            # استدعاء الصورة من مجلد assets
                            ft.Image(src="logo.png", width=220, height=220, fit=ft.ImageFit.CONTAIN),
                            ft.Text("JOKER PRO", size=32, weight="bold", color="#CC0000"),
                            ft.Text("Automotive Systems", size=14, color="grey"),
                            ft.Container(height=40),
                            ft.ElevatedButton(
                                content=ft.Text("START DASHBOARD", size=16, weight="bold"),
                                bgcolor="#CC0000", color="white",
                                width=250, height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                on_click=lambda _: page.go("/dashboard")
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center, bgcolor="white"
                    )
                ])
            )

        # --- 2. لوحة التحكم (الأنظمة) ---
        elif page.route == "/dashboard":
            page.views.append(
                ft.View("/dashboard", [
                    ft.AppBar(title=ft.Text("SELECT SYSTEM"), bgcolor="#CC0000", color="white", center_title=True),
                    ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.Text("Choose Gas System:", size=18, weight="bold"),
                            ft.Divider(height=20),
                            # أزرار الأنظمة
                            ft.ElevatedButton("LANDI RENZO", width=350, height=75, color="#CC0000", bgcolor="white", 
                                             on_click=lambda _: start_connection(0, "LANDI RENZO")),
                            ft.ElevatedButton("ZENIT T-FLASH", width=350, height=75, color="#CC0000", bgcolor="white", 
                                             on_click=lambda _: start_connection(1, "ZENIT T-FLASH")),
                            ft.ElevatedButton("ZENIT BLUE BOX", width=350, height=75, color="#CC0000", bgcolor="white", 
                                             on_click=lambda _: start_connection(2, "ZENIT BLUE BOX")),
                            ft.Container(height=20),
                            ft.Text("Note: Ensure Wi-Fi is connected to JOKER_ESP", size=12, italic=True, color="grey")
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="#F8F8F8")
            )

        # --- 3. شاشة الانتظار ---
        elif page.route == "/loading":
            page.views.append(
                ft.View("/loading", [
                    ft.Container(
                        content=ft.Column([
                            ft.ProgressRing(width=60, height=60, stroke_width=6, color="#CC0000"),
                            ft.Container(height=20),
                            ft.Text("Communicating with ESP...", size=18, weight="500")
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="white")
            )

        # --- 4. شاشة النتيجة (الحالة) ---
        elif page.route == "/status":
            is_ok = status_data["is_ok"]
            page.views.append(
                ft.View("/status", [
                    ft.AppBar(title=ft.Text("Connection Status"), bgcolor="#CC0000", color="white"),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(
                                name=ft.icons.CHECK_CIRCLE if is_ok else ft.icons.CANCEL,
                                color="green" if is_ok else "red",
                                size=150
                            ),
                            ft.Text("SUCCESS" if is_ok else "FAILED", size=35, weight="bold", color="green" if is_ok else "red"),
                            ft.Container(height=10),
                            ft.Text(f"System: {status_data['active_name']}", size=20, weight="500"),
                            ft.Container(height=50),
                            ft.ElevatedButton(
                                "BACK TO MENU", 
                                icon=ft.icons.ARROW_BACK,
                                width=250, height=55, 
                                bgcolor="#CC0000", color="white",
                                on_click=lambda _: page.go("/dashboard")
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True, alignment=ft.alignment.center
                    )
                ], bgcolor="white")
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# تشغيل التطبيق مع ربط مجلد الصور
ft.app(target=main, assets_dir="assets")
