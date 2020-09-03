# crawler 
Version: 1.0

Автор: Полтораднев Кирилл
Дата: 03.09.2020

## Описание
Утилита краулер позволяет скачивать контент с выбранного сайта.Зная глубину погружения и стартовую ссылку, робот начинает скачивать все ссылки в пределах глубины. Все ссылки сохраняются, соглсасно изначальной кодировке, в выбранной папке.


## Состав
* Файл запуска утилиты: `startup.py`
* Модули: `/modules`
* Тесты: `/tests`

### Управление
`python3 startup.py [web_url] -f [folder] -s [chunk_size] -d [depth] -ef [simple_filter]`

Для работы утилита использует параметры:

* Url или IP веб-сайта `web-url`
* Директорию для выгрузки страницы `-f <folder>`
* Размер чанка для загрузки страницы `-s <chunk_size>`, по умолчанию 512
* Глубина поиска `-d <depth>`, по умолчанию 5
* Фильтры на расширение файлов в ссылках `-ef <simple_filter>`

## Подробности реализации
Модули, отвечающие за логику краулера расположены в пакете modules. 
* `modules.Crawler` - класс, формирующий цикл обработки данных
* `modules.PageParser`- класс, реализующий обрабоку страницы и верификацию ссылок
* `modules.LinkParser`- класс-потомок `html.parse.HTMLParser`, реализующий обработку данных из HTML файла
