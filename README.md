# qa_guru_python_advanced_1_2_2_db

# ДЗ #2
1. Запустить проект с postgresql в докере
2. Расширить тестовое покрытие:
- Тест на post: создание. Предусловия: подготовленные тестовые данные
- Тест на delete: удаление. Предусловия: созданный пользователь
- Тест на patch: изменение. Предусловия: созданный пользователь

- Get после создания, изменения
- Тест на 405 ошибку: Предусловия: ничего не нужно
- 404 422 ошибки на delete patch
- 404 на удаленного пользователя
- user flow: создаем, читаем, обновляем, удаляем
- валидность тестовых данных (емейл, урл)
- отправить модель без поля на создание

=====================================================
# Продвинутые техники автоматизации REST API. Александр Котляр

1. Создать класс с методами на каждую ручку собственного микросервиса, который писали на прошлых уроках.
2. Класс должен принимать переменную окружения и создавать сессию с вшитым baseurl для выбранного окружения.
3. Окружение должно прокидываться через опции и возвращаться фикстурой.


### Запуск приложения
В терминале выполнить <br>
docker compose up

В файле main.py запустить приложение