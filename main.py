import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    proxy_choice = int(input("Выберите прокси сервер (1-7): "))
    proxy_url = proxy_servers.get(proxy_choice)

    twitch_username = input("Введите название канала Twitch: ")
    proxy_count = int(input("Сколько вкладок открыть? "))

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')  # Новый headless-режим
    chrome_options.add_argument("--mute-audio")  # Отключаем звук
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=320,240")  # Минимальное разрешение
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Отключаем изображения
    chrome_options.add_argument("--disable-webrtc")  # Отключаем WebRTC
    chrome_options.add_argument("--disable-accelerated-2d-canvas")  # Отключаем анимации
    chrome_options.add_argument("--disable-gpu")  # Отключаем GPU
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-software-rasterizer")

    drivers = []
    
    for _ in range(proxy_count):
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(proxy_url)

        try:
            # Вводим Twitch-адрес
            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)

            time.sleep(5)  # Ждем загрузку

            # Отключаем чат и рекомендации
            driver.execute_script("""
                try {
                    document.querySelector('.chat-room__container').remove();
                    document.querySelector('.recommended-channels').remove();
                } catch (e) {}
            """)

            # Принудительно ставим минимальное качество видео
            driver.execute_script("""
                var settingsButton = document.querySelector('[data-a-target="player-settings-button"]');
                if (settingsButton) {
                    settingsButton.click();
                    setTimeout(() => {
                        var qualityMenu = document.querySelector('[data-a-target="player-settings-menu"]');
                        if (qualityMenu) {
                            var lowestQuality = qualityMenu.querySelectorAll('[data-a-target="player-settings-menu-item"]');
                            if (lowestQuality.length > 0) {
                                lowestQuality[lowestQuality.length - 1].click(); // Выбираем последнее (обычно 160p)
                            }
                        }
                    }, 2000);
                }
            """)

        except Exception as e:
            print(f"Ошибка: {e}")

        drivers.append(driver)  # Сохраняем драйвер, чтобы вкладка не закрылась

    input("Все вкладки открыты. Нажмите Enter для завершения.")

    for driver in drivers:
        driver.quit()  # Закрываем все браузеры

if __name__ == '__main__':
    main()
