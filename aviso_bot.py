from playwright.sync_api import sync_playwright
import time

LOGIN = "meresen"
PASSWORD = "Neserem1.Z"
SURF_URL = "https://aviso.bz/tasks-surf"

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Переход на страницу логина
        page.goto("https://aviso.bz/login")
        page.wait_for_selector("input[name='login']", timeout=15000)

        # Вывод содержимого страницы (для отладки)
        html = page.content()
        print("=== HTML контент страницы логина ===")
        print(html)

        # Ввод логина и пароля
        page.fill("input[name='login']", LOGIN)
        page.fill("input[name='password']", PASSWORD)
        page.keyboard.press("Enter")
        page.wait_for_url("https://aviso.bz/account", timeout=15000)
        print("Авторизация успешна")

        while True:
            page.goto(SURF_URL)
            page.wait_for_selector(".task_surf_table", timeout=15000)

            tasks = page.query_selector_all(".task_surf_table a.task_surf_button")
            if not tasks:
                print("Нет заданий. Ждём 60 секунд...")
                time.sleep(60)
                continue

            for task in tasks:
                try:
                    task.click()
                    page.wait_for_selector("button.btn-success", timeout=10000)
                    page.click("button.btn-success")  # Приступить к просмотру
                    print("Просмотр запущен. Ждём 16 секунд...")
                    time.sleep(16)

                    page.wait_for_selector("button.confirm_task", timeout=10000)
                    page.click("button.confirm_task")  # Подтвердить просмотр
                    print("Просмотр подтверждён")
                    time.sleep(3)
                    break

                except Exception as e:
                    print(f"Ошибка при выполнении задания: {e}")
                    break

        browser.close()

if __name__ == "__main__":
    run_bot()
