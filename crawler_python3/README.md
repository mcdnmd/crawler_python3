# crawler 
Version: 0.1

Автор: Полтораднев Кирилл

## Описание
Утилита краулер позволяет скачивать веб-сайт по URL в выбранную директорию на диске. 
 
## Состав
* Консольная вресия: `startup.py`
* Модули: `/modules`
* Тесты: `/tests`

### Управление
`python3 startup.py [start_utl] [dir_to_upload] [depth]`

Для работы утилиты нужно задать параметры

* Url веб-сайта `start-url`
* Директорию, куда выгрузим страницы `dir_to_upload`
* Глубину поиска `depth`, по дефолту стоит 5


## Подробности реализации
Модули, отвечающие за логику краулера расположены в пакете modules. В основе лежaт: 
* `modules.Crawler` - класс, формирующий цикл обработки данных
* `modules.Page`- класс, реализующий обработку данных со страницы
* `modules.Request` - класс для обработки HTTP/HTTPS запросов.