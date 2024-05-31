from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
import time
import random
import string
from smsactivate.api import SMSActivateAPI


class YandexMap:

    def __init__(self):
        self.activated = False
        self.browser = None
        self.establishment_name = None

    def activate(self):
        try:
            if not self.activated:
                self.activated = True
                options = Options()
                options.add_argument('--ignore-certificate-errors')
                service = Service('D:/kazak_python_project/msedgedriver.exe')
                self.browser = webdriver.Edge(service=service, options=options)
        except Exception as e:
            print(f"Ошибка при активации: {e}")


    def deactivate(self):
        try:
            self.activated = False
            if self.browser:
                self.browser.quit()
        except Exception as e:
            print(f"Ошибка при деактивации: {e}")

    def fullscreen(self):
        self.browser.maximize_window()

    def open_mail(self):
        time.sleep(60)
        # открываем новую вкладку с картами
        self.browser.execute_script("window.open();")
        handles = self.browser.window_handles
        self.browser.switch_to.window(handles[-1])
        self.browser.get('https://yandex.ru/maps')
        print("Открыли КАРТЫ")

    def reg(self):
        WebDriverWait(self.browser, 10)
        try:
            reg = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'registration__block')))
            print("нужно зарегестрироваться, заполняем поля регестрации")
            if reg:
                # Если элемент найден, находим ссылку внутри списка и нажимаем на нее

                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'login')))

                login = "alien"

                # Добавляем к логину строке 6 случайных символов (цифр и букв)
                for _ in range(6):
                    # Случайный выбор цифры или буквы
                    random_char = random.choice(string.ascii_letters + string.digits)
                    # Добавление выбранного символа к логину
                    login += random_char

                # Находим поле для ввода логина
                login_field = self.browser.find_element(By.ID, 'login')

                # Очищаем поле, если оно уже содержит какой-то текст
                login_field.clear()

                # Вводим сгенерированный логин в поле для логина
                login_field.send_keys(login)
                time.sleep(3)

                password = "aliennn"

                # Добавляем к паролю строке 6 случайных символов (цифр и букв)
                for _ in range(6):
                    # Случайный выбор цифры или буквы
                    random_char = random.choice(string.ascii_letters + string.digits)
                    # Добавление выбранного символа к логину
                    password += random_char

                # Находим поле для ввода пароля и повтор
                password_field = self.browser.find_element(By.ID, 'password')

                # Очищаем поле, если оно уже содержит какой-то текст
                password_field.clear()

                # Вводим сгенерированный пароль в поле для логина
                password_field.send_keys(password)
                time.sleep(3)

                password_confirm_field = self.browser.find_element(By.ID, 'password_confirm')

                # Очищаем поле, если оно уже содержит какой-то текст
                password_confirm_field.clear()

                # Вводим сгенерированный логин в поле для логина
                password_confirm_field.send_keys(password)
                time.sleep(3)

                print("ввели логин и пароль")
                buttond = self.browser.find_element(By.CSS_SELECTOR, 'button[data-t="button:action"]')
                buttond.click()
                print("нажали кнопку далее")
                time.sleep(2)
                buttonaccept = self.browser.find_element(By.XPATH,
                                                         '/html/body/div/div/div[2]/div/main/div/form/div[3]/div/div/div[2]/div/button')
                buttonaccept.click()
                print("нажали на кнопку принимаю")
                WebDriverWait(self.browser, 30)
        except TimeoutException:
            WebDriverWait(self.browser, 30)
        print("Заполнили поля с логином паролем и подтверждением + приняли условия")
        self.open_mail()

    def loginSMS_after_purchase(self):
        flag = True
        while flag:

            sa = SMSActivateAPI('YOUR_API_KEY')  # ввод ключа
            # проверяем есть ли номера
            count = sa.getNumbersStatus(country=0, operator='any')
            while count['ya_0'] == 0:
                count = sa.getNumbersStatus(country=0, operator='any')
            print('Количество доступных номеров: ' + count['ya_0'])
            main_answer = sa.getNumberV2(service='ya', country=0,
                                         operator='any')  # получение номера русского для яндекса тут хранится номер

            print('Получили номер: ' + str(main_answer['phoneNumber']))
            # main_answer['activationId'] ключевое слово для получения номера ордера на телефон
            # main_answer['phoneNumber'] ключевое слово для получения самого номера

            # Открываем яндекс почту
            self.browser.get('https://360.yandex.ru/mail/')
            login_button = self.browser.find_element(By.ID, "header-login-button")

            # Нажимаем на кнопку
            login_button.click()
            login_field = self.browser.find_element(By.ID, "passp-field-login")

            # Вставляем текст в поле ввода
            login_field.send_keys(main_answer['phoneNumber'])
            login_field.send_keys(Keys.RETURN)
            print("Вставили номер")
            time.sleep(5)
            print('Ждём код')

            time.sleep(100)
            answer = sa.getStatus(id=main_answer[
                'activationId'])  # функция для получения статуса, также сюда передаётся полученный код, вводиться номер ордера

            if answer == 'STATUS_WAIT_CODE':
                time.sleep(20)
                sa.setStatus(id=main_answer['activationId'],
                             status=3)  # функция для установки статуса, по номеру ордера
                self.deactivate()
                self.activate()
                self.fullscreen()
                continue
            else:
                flag = False

        answer = answer[-6:]
        print('Получили код: ' + str(answer))

        # статус 1 - отправляется после отправки кода на номер
        # статус 6 - код успешно принят, закрывает ордер и отзывает доступ к номеру
        # статус 8 - код для отмены, в случае если аккаунт уже зарегестрирован

        # вставляем полученный код
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'passp-field-phoneCode')))
        password_input = self.browser.find_element(By.ID, 'passp-field-phoneCode')
        password_input.send_keys(answer)
        print('вставили код')
        # sa.setStatus(id=main_answer['activationId'], status=6)  # функция для установки статуса, по номеру ордера
        WebDriverWait(self.browser, 10)

        #  вариации дальнейших событий
        try:
            #   1)   аккаунт уже существует и мы выбираем его из списка + поле регестрации(вряд ли будет)
            account_list = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Accounts-list')))
            print("аккаунт сушествует, мы выбираем его списка")
            try:
                account_link = account_list.find_element(By.XPATH, '//a[contains(@href, "/auth?login=")]')
                account_link.click()
                try:
                    # нажимаем на кнопку "СОЗДАТЬ АККАУНТ"
                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:default:accounts: createIDBtn"]'))
                    )
                    button_element = self.browser.find_element(By.CSS_SELECTOR,
                                                               'button[data-t="button:default:accounts: createIDBtn"]')
                    button_element.click()
                    print('нажали на кнопку "СОЗДАТЬ АККАУНТ"')
                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:action"]'))
                    )
                    button_element11 = self.browser.find_element(By.CSS_SELECTOR, '[data-t="button:action"]')
                    # Нажимаем на кнопку "НЕ СЕЙЧАС"
                    button_element11.click()
                    print('Нажали на кнопку "Не сейчас"')
                    WebDriverWait(self.browser, 10)
                    self.reg()
                except:
                    self.reg()

            except:
                # нажимаем на кнопку "СОЗДАТЬ АККАУНТ"
                WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:default:accounts: createIDBtn"]'))
                )
                button_element = self.browser.find_element(By.CSS_SELECTOR,
                                                           'button[data-t="button:default:accounts: createIDBtn"]')
                button_element.click()
                print('нажали на кнопку "СОЗДАТЬ АККАУНТ"')
                WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:action"]'))
                )
                button_element11 = self.browser.find_element(By.CSS_SELECTOR, '[data-t="button:action"]')
                # Нажимаем на кнопку "НЕ СЕЙЧАС"
                button_element11.click()
                print('Нажали на кнопку "Не сейчас"')
                WebDriverWait(self.browser, 10)
                self.reg()

            try:
                # обрабатываем кнопку "НЕ СЕЙЧАС"
                button_element = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-t="button:pseudo"]'))
                )
                print('Появилась кнопка не сейчас')
                button_element.click()
                print("Нажали на кнопку не сейчас")
                self.reg()
            except:
                print("Кнопка 'Не сейчас' не появилась на экране")
                self.reg()


        except TimeoutException:
            print('Если работает, то повезло')

        #   2)   Сразу после кода появились поля для ввода имени и фамилии
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, 'passp-field-firstname')))
            print('Сразу после кода появились поля для ввода имени и фамилии')
            loggin_input = self.browser.find_element(By.ID, 'passp-field-firstname')
            loggin_input.send_keys('Gleb')

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, 'passp-field-lastname')))
            password_input = self.browser.find_element(By.ID, 'passp-field-lastname')
            password_input.send_keys('Krutoi')
            password_input.send_keys(Keys.RETURN)
            try:
                # нажимаем на кнопку "СОЗДАТЬ АККАУНТ"
                WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:default:accounts: createIDBtn"]'))
                )
                button_element = self.browser.find_element(By.CSS_SELECTOR,
                                                           'button[data-t="button:default:accounts: createIDBtn"]')
                button_element.click()
                print('нажали на кнопку "СОЗДАТЬ АККАУНТ"')
                WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:action"]'))
                )
                button_element11 = self.browser.find_element(By.CSS_SELECTOR, '[data-t="button:action"]')
                # Нажимаем на кнопку "НЕ СЕЙЧАС"
                button_element11.click()
                print('Нажали на кнопку "Не сейчас"')
                WebDriverWait(self.browser, 10)
                self.reg()
            except:
                WebDriverWait(self.browser, 10)

            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-t='button:action']"))
            )
            button111 = self.browser.find_element(By.CSS_SELECTOR, "button[data-t='button:action']")
            button111.click()
            print('Нажали на кнопку ДАЛЕЕ')

            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:default:accounts: createIDBtn"]'))
            )
            button_element = self.browser.find_element(By.CSS_SELECTOR,
                                                       'button[data-t="button:default:accounts: createIDBtn"]')
            button_element.click()
            print('нажали на кнопку "СОЗДАТЬ АККАУНТ"')

            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-t="button:action"]'))
            )
            button_element11 = self.browser.find_element(By.CSS_SELECTOR, '[data-t="button:action"]')
            button_element11.click()
            print('Нажали на кнопку "НЕ СЕЙЧАС"')

            WebDriverWait(self.browser, 10)
            self.reg()

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except TimeoutException as e:
            print(f"Ошибка: время ожидания истекло. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def enter_coordinates(self, latitude, longitude):
        if not self.activated:
            print("Браузер не активирован.")
            return

        try:
            print("Ожидание элемента для ввода поискового запроса...")
            search_input = WebDriverWait(self.browser, 60).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск мест и адресов"]'))
            )
            print("Элемент для ввода поискового запроса найден.")

            # Очистка поля ввода перед вводом нового запроса
            print("Очистка поля ввода...")
            self.browser.execute_script("arguments[0].value = '';", search_input)
            search_input.clear()
            search_input.send_keys(Keys.BACKSPACE * 100)
            print("Поле ввода очищено.")

            print(f"Ввод координат: {latitude}, {longitude}")
            search_input.send_keys(f'{latitude}, {longitude}')
            search_input.send_keys(Keys.RETURN)

            # Ожидание появления точки на карте (например, проверяем наличие элемента с адресом)
            print("Ожидание появления точки на карте...")
            time.sleep(6)
            print("Координаты введены и точка на карте отображена.")

            # Задержка, чтобы убедиться, что страница полностью загрузилась
            time.sleep(5)

            # Эмуляция нажатия клавиши Backspace для удаления символов
            print("Удаление введенных координат из поля ввода...")
            search_input.send_keys(Keys.BACKSPACE * len(f'{latitude}, {longitude}'))
            print("Поле ввода очищено.")

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except TimeoutException as e:
            print(f"Ошибка: время ожидания истекло. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def search_niche(self, niche):
        if not self.activated:
            print("Браузер не активирован.")
            return

        try:
            print("Поиск текстового поля...")
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск мест и адресов"]')))
            search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Поиск мест и адресов"]')

            print("Очистка поля ввода...")
            search_input.clear()
            search_input.send_keys(Keys.BACKSPACE * 100)  # Удаление всех возможных символов

            print(f"Ввод ниши: {niche}")
            search_input.send_keys(niche)

            print("Нажатие на кнопку 'Найти'...")
            WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Найти"]')))
            search_button = self.browser.find_element(By.XPATH, '//button[@aria-label="Найти"]')
            search_button.click()

            print("Ожидание результатов поиска...")
            time.sleep(5)
            print("Поиск выполнен и результаты отображены.")

            # print("Нажатие на кнопку приближения...")
            # zoom_in_button = self.browser.find_element(By.XPATH,'//button[contains(@class, "button _view_air _size_medium _pin-bottom")]')
            # zoom_in_button.click()
            # time.sleep(5)
            # print("Приближение выполнено.")

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except TimeoutException as e:
            print(f"Ошибка: время ожидания истекло. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def browse_establishments(self):
        if not self.activated:
            print("Браузер не активирован.")
            return

        matching_establishment_data_id = None

        try:
            print("Поиск заведений...")
            scroll_origin = ScrollOrigin.from_viewport(100, 200)
            scroll_container = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "scroll__container"))
            )
            scroll_height = 0
            for _ in range(3):  # Цикл для трёх полных прокруток
                scroll_height = self.browser.execute_script(
                    "return arguments[0].scrollHeight", scroll_container
                )
                while True:
                    ActionChains(self.browser).scroll_from_origin(scroll_origin, 0, 5000).perform()
                    time.sleep(0.9)
                    new_scroll_height = self.browser.execute_script(
                        "return arguments[0].scrollHeight", scroll_container
                    )
                    if new_scroll_height == scroll_height:
                        break
                    scroll_height = new_scroll_height

                # Прокрутка до начала
                self.browser.execute_script("arguments[0].scrollTop = 0;", scroll_container)
                time.sleep(2)  # Небольшая задержка перед новой итерацией

            # Теперь получаем количество элементов
            establishments = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view'))
            )
            print(f"Найдено {len(establishments)} заведений.")

            # Ищем интересующий элемент
            target_index = -1
            for index, establishment in enumerate(establishments):
                try:
                    print(f"Проверка заведения {index + 1}...")
                    name = establishment.find_element(By.CSS_SELECTOR, '.search-business-snippet-view__title').text
                    print(f"Название заведения: {name}")
                    if name == self.establishment_name:
                        target_index = index
                        print(f"Интересующий элемент найден на позиции {target_index + 1}.")
                        break
                except StaleElementReferenceException:
                    establishments = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view'))
                    )

            if target_index == -1:
                print("Интересующий элемент не найден.")
                return

            # Дополнительные итерации для первого и последнего элемента
            extra_iterations = 3
            if target_index == 0:
                print("Интересующий элемент находится в начале списка.")
                indices = range(target_index, min(target_index + extra_iterations, len(establishments)))
            elif target_index == len(establishments) - 1:
                print("Интересующий элемент находится в конце списка.")
                indices = range(target_index, max(target_index - extra_iterations, -1), -1)
            else:
                # Определяем направление итерации в зависимости от позиции целевого элемента
                num_establishments = len(establishments)
                if target_index < num_establishments / 2:
                    indices = range(target_index, -1, -1)  # от целевого элемента до начала
                else:
                    indices = range(target_index, num_establishments)  # от целевого элемента до конца

            if target_index == 0:

                print("Интересующий элемент находится в начале списка. Прокручиваем вниз на два элемента.")
                ActionChains(self.browser).scroll_from_origin(scroll_origin, 0,
                                                              2 * scroll_height // len(establishments)).perform()
                time.sleep(2)
            elif target_index == len(establishments) - 1:
                print("Интересующий элемент находится в конце списка. Прокручиваем вверх на два элемента.")
                ActionChains(self.browser).scroll_from_origin(scroll_origin, 0,
                                                              -2 * scroll_height // len(establishments)).perform()
                time.sleep(2)

            for index in indices:
                for attempt in range(3):  # Повторяем до трех раз в случае возникновения исключения
                    try:
                        establishments = WebDriverWait(self.browser, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view'))
                        )
                        if index >= len(establishments) or index < 0:
                            print("Прокрутка до появления новых элементов...")
                            for _ in range(3):  # Цикл для трёх полных прокруток
                                scroll_height = self.browser.execute_script(
                                    "return arguments[0].scrollHeight", scroll_container
                                )
                                while True:
                                    ActionChains(self.browser).scroll_from_origin(scroll_origin, 0, 5000).perform()
                                    time.sleep(0.9)
                                    new_scroll_height = self.browser.execute_script(
                                        "return arguments[0].scrollHeight", scroll_container
                                    )
                                    if new_scroll_height == scroll_height:
                                        break
                                    scroll_height = new_scroll_height

                                # Прокрутка до начала
                                self.browser.execute_script("arguments[0].scrollTop = 0;", scroll_container)
                                time.sleep(2)  # Небольшая задержка перед новой итерацией
                        establishment = establishments[index]

                        # Скроллим до элемента
                        self.browser.execute_script("arguments[0].scrollIntoView(true);", establishment)
                        time.sleep(0.5)  # небольшая задержка для завершения анимации скролла

                        print(f"Обработка заведения {index + 1}...")
                        name = establishment.find_element(By.CSS_SELECTOR, '.search-business-snippet-view__title').text
                        data_id = establishment.find_element(By.XPATH,
                                                             ".//ancestor::div[contains(@class, 'search-snippet-view__body')]").get_attribute(
                            'data-id')
                        print(f"Название: {name}, data-id: {data_id}")

                        if name == self.establishment_name:
                            print(f"Совпадение найдено: {name}")
                            matching_establishment_data_id = data_id
                            self.interact_with_matching_establishment(data_id)
                        else:
                            print(f"Совпадение не найдено, взаимодействие с заведением: {name}")
                            self.interact_with_non_matching_establishment(establishment)
                        break  # Если успешное выполнение, выходим из цикла попыток

                    except StaleElementReferenceException as e:
                        print(f"StaleElementReferenceException: {e}. Попытка #{attempt + 1}")
                        time.sleep(1)  # Задержка перед повторной попыткой

                    except IndexError as e:
                        print(f"Ошибка: попытка доступа к несуществующему элементу списка. {e}")
                        break  # Прерываем цикл, если достигнут конец списка
                    except NoSuchElementException as e:
                        print(f"Ошибка: элемент не найден. {e}")
                    except TimeoutException as e:
                        print(f"Ошибка: время ожидания истекло. {e}")
                    except Exception as e:
                        print(f"Неизвестная ошибка: {e}")

            # После обработки всех элементов, возвращаемся к совпавшему заведению
            if matching_establishment_data_id:
                print(
                    f"Возвращение к заведению с data-id: {matching_establishment_data_id} для выполнения случайного действия.")
                self.perform_action(matching_establishment_data_id)

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except TimeoutException as e:
            print(f"Ошибка: время ожидания истекло. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def interact_with_non_matching_establishment(self, establishment):
        try:
            print("Попытка открыть страницу заведения...")
            establishment.click()
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'business-card-view')))
            print("Страница заведения успешно загружена.")
            time.sleep(12)  # Увеличиваем время ожидания

            try:
                print('Прокрутка до фотографий')
                photos_tab = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Фото']"))
                )
                self.browser.execute_script("arguments[0].scrollIntoView();", photos_tab)
                time.sleep(2)
                photos_tab.click()
                time.sleep(5)  # Пауза для загрузки фотографий
                print('Фотографии открыты')
                # Проверка наличия элемента с фото
                photo_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "media-wrapper"))
                )
                print("Попытка кликнуть на фотографию...")
                photo_element.click()
                time.sleep(12)
                try:
                    button1 = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.photos-player-view__button._type_forward'))
                    )
                    button1.click()
                    time.sleep(5)
                    button2 = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.photos-player-view__button._type_forward'))
                    )
                    button2.click()
                    time.sleep(5)
                except (NoSuchElementException, TimeoutException) as e:
                    print("Фотографии отсутствуют или произошла ошибка при их открытии.")
                time.sleep(5)
                self.browser.back()
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'business-media-list'))
                )
                print("Фотографии открыты.")
                time.sleep(12)

            except (NoSuchElementException, TimeoutException) as e:
                self.browser.refresh()
                time.sleep(5)
                print("Фотографии отсутствуют или произошла ошибка при их открытии. Запускаем обновление страницы")

            time.sleep(10)
            for _ in range(3):
                try:
                    time.sleep(10)
                    reviews_button = WebDriverWait(self.browser, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, 'div._name_reviews > a.tabs-select-view__label'))
                    )
                    print("Попытка открыть отзывы...")
                    self.browser.execute_script("arguments[0].scrollIntoView();", reviews_button)
                    time.sleep(2)
                    self.browser.execute_script("arguments[0].click();", reviews_button)
                    time.sleep(5)

                    print("Попытка открыть сортировку отзывов")
                    element = WebDriverWait(self.browser, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "rating-ranking-view")))
                    time.sleep(5)
                    self.browser.execute_script("arguments[0].scrollIntoView();", element)
                    time.sleep(2)
                    self.browser.execute_script("arguments[0].click();", element)
                    time.sleep(5)

                    print('Подождите, пока появится всплывающее меню')
                    popup = WebDriverWait(self.browser, 15).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "rating-ranking-view__popup")))
                    time.sleep(5)

                    print('Найдите все элементы в всплывающем меню')
                    options = self.browser.find_elements(By.CLASS_NAME, "rating-ranking-view__popup-line")
                    time.sleep(5)

                    print("Выберите случайный элемент, кроме 'По умолчанию'")
                    if len(options) <= 1:
                        raise Exception("Нет доступных опций для выбора, кроме 'По умолчанию'")

                    # Начинаем с индекса 1, чтобы пропустить первый элемент ("По умолчанию")
                    filtered_options = options[1:]

                    random_option = random.choice(filtered_options)
                    time.sleep(3)
                    self.browser.execute_script("arguments[0].click();", random_option)
                    print("Случайный элемент выбран")

                    WebDriverWait(self.browser, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'business-reviews-card-view'))
                    )
                    print("Отзывы открыты.")
                    time.sleep(12)
                    break
                except StaleElementReferenceException:
                    print("Элемент устарел, повторная попытка...")
                # Если элемент не найден, обновляем страницу и пытаемся снова
                self.browser.refresh()
                time.sleep(5)

            print("Возвращение к списку заведений...")
            self.browser.back()
            time.sleep(7)  # Ждем, пока страница загрузится
            self.browser.back()

            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view')))
                print("Возврат к списку заведений выполнен.")
            except TimeoutException:
                print("Не удалось вернуться к списку заведений в течение 10 секунд. Обновление страницы...")
                self.browser.refresh()
                time.sleep(5)
                self.browser.back()
                WebDriverWait(self.browser, 25).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view')))
                print("Страница обновлена и список заведений загружен.")
                time.sleep(5)

            print("Поиск заведений...")
            scroll_origin = ScrollOrigin.from_viewport(100, 200)
            scroll_container = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "scroll__container"))
            )
            scroll_height = 0
            for _ in range(3):  # Цикл для трёх полных прокруток
                scroll_height = self.browser.execute_script(
                    "return arguments[0].scrollHeight", scroll_container
                )
                while True:
                    ActionChains(self.browser).scroll_from_origin(scroll_origin, 0, 5000).perform()
                    time.sleep(0.9)
                    new_scroll_height = self.browser.execute_script(
                        "return arguments[0].scrollHeight", scroll_container
                    )
                    if new_scroll_height == scroll_height:
                        break
                    scroll_height = new_scroll_height

                # Прокрутка до начала
                self.browser.execute_script("arguments[0].scrollTop = 0;", scroll_container)
                time.sleep(2)  # Небольшая задержка перед новой итерацией

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def interact_with_matching_establishment(self, data_id):
        try:
            print(f"Поиск карточки заведения с data-id: {data_id}")
            time.sleep(2)
            establishment_card = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//div[@data-id='{data_id}']"))
            )
            print("Карточка заведения найдена, попытка клика...")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", establishment_card)
            time.sleep(2)
            self.browser.execute_script("arguments[0].click();", establishment_card)
            print("Ожидание загрузки страницы заведения...")
            time.sleep(2)
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'business-card-view')))
            print("Страница заведения успешно загружена.")
            time.sleep(5)

            try:
                photos_button = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div._name_gallery > a.tabs-select-view__label'))
                )
                print("Попытка открыть фотографии...")
                self.browser.execute_script("arguments[0].scrollIntoView();", photos_button)
                time.sleep(2)
                self.browser.execute_script("arguments[0].click();", photos_button)

                # Проверка наличия элемента с фото
                photo_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "media-wrapper"))
                )
                print("Попытка кликнуть на фотографию...")
                photo_element.click()
                time.sleep(12)
                button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.photos-player-view__button._type_forward'))
                )
                button.click()
                time.sleep(5)
                try:
                    button1 = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.photos-player-view__button._type_forward'))
                    )
                    button1.click()
                    time.sleep(5)
                    button2 = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.photos-player-view__button._type_forward'))
                    )
                    button2.click()
                    time.sleep(5)
                except (NoSuchElementException, TimeoutException) as e:
                    print("Фотографии отсутствуют или произошла ошибка при их открытии.")
                self.browser.back()
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'business-media-list'))
                )
                print("Фотографии открыты.")
                time.sleep(12)
            except (NoSuchElementException, TimeoutException) as e:
                print("Фотографии отсутствуют или произошла ошибка при их открытии.")

            time.sleep(10)
            for _ in range(3):
                try:
                    time.sleep(10)
                    reviews_button = WebDriverWait(self.browser, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, 'div._name_reviews > a.tabs-select-view__label'))
                    )
                    print("Попытка открыть отзывы...")
                    self.browser.execute_script("arguments[0].scrollIntoView();", reviews_button)
                    time.sleep(5)
                    self.browser.execute_script("arguments[0].click();", reviews_button)
                    time.sleep(5)

                    print("Попытка открыть сортировку отзывов")
                    element = WebDriverWait(self.browser, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "rating-ranking-view")))
                    time.sleep(5)
                    self.browser.execute_script("arguments[0].scrollIntoView();", element)
                    time.sleep(2)
                    self.browser.execute_script("arguments[0].click();", element)
                    time.sleep(5)

                    print('Подождите, пока появится всплывающее меню')
                    popup = WebDriverWait(self.browser, 15).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "rating-ranking-view__popup")))
                    time.sleep(5)

                    print('Найдите все элементы в всплывающем меню')
                    options = self.browser.find_elements(By.CLASS_NAME, "rating-ranking-view__popup-line")
                    time.sleep(5)

                    print("Выберите случайный элемент, кроме 'По умолчанию'")
                    if len(options) <= 1:
                        raise Exception("Нет доступных опций для выбора, кроме 'По умолчанию'")

                    # Начинаем с индекса 1, чтобы пропустить первый элемент ("По умолчанию")
                    filtered_options = options[1:]

                    random_option = random.choice(filtered_options)
                    time.sleep(3)
                    self.browser.execute_script("arguments[0].click();", random_option)
                    print("Случайный элемент выбран")

                    WebDriverWait(self.browser, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'business-reviews-card-view'))
                    )
                    print("Отзывы открыты.")
                    time.sleep(12)
                    break
                except StaleElementReferenceException:
                    print("Элемент устарел, повторная попытка...")

            print("Возвращение к списку заведений...")
            self.browser.back()
            time.sleep(7)  # Ждем, пока страница загрузится
            self.browser.back()

            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view'))
                )
                print("Возврат к списку заведений выполнен.")
            except TimeoutException:
                print("Не удалось вернуться к списку заведений в течение 10 секунд. Обновление страницы...")
                self.browser.refresh()
                time.sleep(5)
                self.browser.back()
                WebDriverWait(self.browser, 25).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-snippet-view'))
                )
                print("Страница обновлена и список заведений загружен.")
                time.sleep(5)

            print("Поиск заведений...")
            scroll_origin = ScrollOrigin.from_viewport(100, 200)
            scroll_container = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "scroll__container"))
            )
            scroll_height = 0
            for _ in range(3):  # Цикл для трёх полных прокруток
                scroll_height = self.browser.execute_script(
                    "return arguments[0].scrollHeight", scroll_container
                )
                while True:
                    ActionChains(self.browser).scroll_from_origin(scroll_origin, 0, 5000).perform()
                    time.sleep(0.9)
                    new_scroll_height = self.browser.execute_script(
                        "return arguments[0].scrollHeight", scroll_container
                    )
                    if new_scroll_height == scroll_height:
                        break
                    scroll_height = new_scroll_height

                # Прокрутка до начала
                self.browser.execute_script("arguments[0].scrollTop = 0;", scroll_container)
                time.sleep(2)  # Небольшая задержка перед новой итерацией

        except NoSuchElementException as e:
            print(f"Ошибка: элемент не найден. {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def perform_action(self, data_id):
        print(f"Поиск карточки заведения с data-id: {data_id}")
        establishment_card = WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[@data-id='{data_id}']"))
        )
        print("Карточка заведения найдена, попытка клика...")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", establishment_card)
        self.browser.execute_script("arguments[0].click();", establishment_card)
        print("Ожидание загрузки страницы заведения...")
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'business-card-view')))
        print("Страница заведения успешно загружена.")
        time.sleep(5)

        actions = ['telegram', 'website', 'whatsapp']

        for action in actions:
            if action == 'telegram':
                print("Попытка открыть Telegram...")
                try:
                    telegram_button = self.browser.find_element(By.CSS_SELECTOR,
                                                                'div.business-contacts-view__social-button > a[aria-label*="telegram"]')
                    self.browser.execute_script("arguments[0].scrollIntoView();",
                                                telegram_button)  # Прокрутка до кнопки
                    time.sleep(2)  # Даем время на завершение анимаций и прокрутки
                    # Запоминаем текущую вкладку
                    original_window = self.browser.current_window_handle
                    self.browser.execute_script("arguments[0].click();", telegram_button)  # Используем JS для клика
                    # Ждем открытия новой вкладки
                    WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(3))
                    print("Telegram открыт.")
                    # Переключаемся на новую вкладку
                    new_window = self.browser.window_handles[-1]
                    self.browser.switch_to.window(new_window)
                    time.sleep(12)  # Увеличиваем время ожидания
                    # Закрываем новую вкладку и возвращаемся к исходной
                    self.browser.close()
                    self.browser.switch_to.window(original_window)
                    print("Возвращаемся на исходную вкладку.")
                    break
                except:
                    print("Не удалось открыть Telegram. Переход к следующему действию.")

            elif action == 'website':
                print("Поиск кнопки перехода на сайт заведения...")
                try:
                    website_button = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[role='button'][aria-label='Сайт']"))
                    )
                    print("Кнопка сайта найдена, попытка клика...")
                    website_button.click()
                    print("Ожидание перехода на новую вкладку или окно...")
                    WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(3))
                    print("Переход на сайт заведения выполнен.")
                    # Запоминаем текущую вкладку
                    original_window = self.browser.current_window_handle
                    # Находим новую вкладку и переключаемся на неё
                    new_window = self.browser.window_handles[-1]
                    self.browser.switch_to.window(new_window)
                    time.sleep(5)  # Ожидание, чтобы убедиться, что страница загрузилась
                    print("Закрытие вкладки сайта...")
                    self.browser.close()  # Закрытие новой вкладки
                    self.browser.switch_to.window(original_window)  # Возврат к основной вкладке
                    print("Возвращаемся на исходную вкладку.")
                    break
                except:
                    print("Не удалось открыть сайт. Переход к следующему действию.")

            elif action == 'whatsapp':
                print("Попытка открыть WhatsApp...")
                try:
                    whatsapp_button = self.browser.find_element(By.CSS_SELECTOR,
                                                                'div.business-contacts-view__social-button > a[aria-label*="whatsapp"]')
                    self.browser.execute_script("arguments[0].scrollIntoView();",
                                                whatsapp_button)  # Прокрутка до кнопки
                    time.sleep(2)  # Даем время на завершение анимаций и прокрутки
                    # Запоминаем текущую вкладку
                    original_window = self.browser.current_window_handle
                    self.browser.execute_script("arguments[0].click();", whatsapp_button)  # Используем JS для клика
                    # Ждем открытия новой вкладки
                    WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(3))
                    print("WhatsApp открыт.")
                    # Переключаемся на новую вкладку
                    new_window = self.browser.window_handles[-1]
                    self.browser.switch_to.window(new_window)
                    time.sleep(12)  # Увеличиваем время ожидания
                    # Закрываем новую вкладку и возвращаемся к исходной
                    self.browser.close()
                    self.browser.switch_to.window(original_window)
                    print("Возвращаемся на исходную вкладку.")
                    break
                except:
                    print("Не удалось открыть WhatsApp. Все действия выполнены.")

    def run_workflow_for_establishments(self, establishments_info):
        self.loginSMS_after_purchase()
        counter = 0
        for establishment_info in establishments_info:
            try:
                coordinates = establishment_info['coordinates']
                time.sleep(5)
                self.enter_coordinates(coordinates['latitude'], coordinates['longitude'])
                time.sleep(5)
                self.search_niche(establishment_info['niche'])
                time.sleep(5)
                self.establishment_name = establishment_info['name']
                time.sleep(5)

                # Проверка, найдено ли заведение
                if self.browse_establishments():
                    counter += 1
                    print("Для списка компаний накручено" + " " + str(counter) + " " + "ПОВЕДЕНЧЕСКОГО ФАКТОРА")


            except Exception as e:
                print(f"Произошла ошибка при обработке заведения: {e}")

            finally:
                # Обновление страницы после выполнения всех методов или в случае ошибки
                self.browser.refresh()
                time.sleep(5)


if __name__ == "__main__":
    yandex_map = YandexMap()
    yandex_map.activate()
    establishments_info = [
        {
            'name': 'Старый город',
            'niche': 'ресторан, банкетный зал',
            'coordinates': {'latitude': '55.772722', 'longitude': '37.661169'}
        },
        {
            'name': 'Мобил Сервис',
            'niche': 'Ремонт телефонов, компьютерный ремонт и услуги',
            'coordinates': {'latitude': '44.596874', 'longitude': '132.818735'}
        },
        {
            'name': 'Монро',
            'niche': 'Парикмахерские, Маникюр',
            'coordinates': {'latitude': '55.764260', 'longitude': '37.830530'}
        },
        {
            'name': 'Крокус',
            'niche': 'Клининг',
            'coordinates': {'latitude': '55.890590', 'longitude': '37.442303'}
        },
        {
            'name': 'Krokus',
            'niche': 'Клининговые услуги',
            'coordinates': {'latitude': '55.907189', 'longitude': '37.731509'}
        },
        {
            'name': 'Студия штор Ирины Бурдиной',
            'niche': 'Шторы, карнизы',
            'coordinates': {'latitude': '55.088715', 'longitude': '38.763609'}
        },
        {
            'name': 'Lash Room',
            'niche': 'Салоны бровей и ресниц',
            'coordinates': {'latitude': '55.615315', 'longitude': '37.747260'}
        },
        {
            'name': 'ОлДент',
            'niche': 'Стоматологии',
            'coordinates': {'latitude': '55.776046', 'longitude': '37.693965'}
        },
        {
            'name': 'Лазер-Экспресс',
            'niche': 'Эпиляция',
            'coordinates': {'latitude': '55.684026', 'longitude': '37.853172'}
        }
    ]
    while True:
        yandex_map.fullscreen()
        yandex_map.activate()
        yandex_map.run_workflow_for_establishments(establishments_info)
        yandex_map.deactivate()
        yandex_map.activate()
# При переходе на карту возникает capthca
