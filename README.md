# Intro to Data Analysis Portfolio

Учебный портфолио-репозиторий с лабораторными работами по анализу, качеству и визуализации данных на Python.

This repository is a compact academic portfolio with data analysis, data quality, and data visualization labs completed in Python.

## О проекте

Репозиторий объединяет пять отдельных лабораторных работ из курса по методам визуализации и анализу данных. Каждая работа сохранена в отдельной папке и разделена на две части: `assignment` с исходным заданием из основной ветки учебного репозитория и `solution` с выполненной работой из ветки `feedback`.

Код решений внутри лабораторных не редактировался при переносе. Структура репозитория приведена к портфолио-формату: каждая лабораторная лежит в своей директории, а этот README служит общей навигацией.

## About

The repository combines five separate course labs focused on data manipulation, data quality, visualization, exploratory analysis, and dashboarding. Each lab is stored in its own folder and split into two parts: `assignment` with the original task files from the source repository's main branch, and `solution` with the completed work from the `feedback` branch.

The lab solution files were not modified during consolidation. The repository structure was organized for portfolio review and easy navigation.

## Содержание / Contents

| Папка | Тема | Что внутри | Навыки |
| --- | --- | --- | --- |
| [`lab-01-data-manipulation`](./lab-01-data-manipulation) | Манипуляция данными | `assignment/` и `solution/` с Python-скриптом, тестами и CSV-датасетом | `pandas`, фильтрация, группировки, агрегации, работа с табличными данными |
| [`lab-02-data-quality`](./lab-02-data-quality) | Качество данных | `assignment/` и `solution/` с Jupyter Notebook по обеспечению качества данных | проверка данных, очистка, анализ пропусков и ошибок |
| [`lab-03-basic-dataviz`](./lab-03-basic-dataviz) | Базовая визуализация | `assignment/` и `solution/` с ноутбуками по визуализации | базовые графики, визуальный анализ, оформление результатов |
| [`lab-04-exploratory-data-analysis`](./lab-04-exploratory-data-analysis) | Разведочный анализ данных | `assignment/` с заданием и `solution/` с EDA-ноутбуком и ссылкой на документ | формулирование гипотез, проверка гипотез, визуализация, интерпретация результатов |
| [`lab-05-dashboards`](./lab-05-dashboards) | Дашборды | `assignment/` и `solution/` с Dash-приложением, HTML-шаблоном, CSV-данными и материалами DataLens | Plotly Dash, интерактивные графики, дашборды, презентация результатов |

## Технологии / Technologies

- Python
- pandas
- Jupyter Notebook
- Plotly Dash
- HTML templates
- CSV datasets
- DataLens materials

## Структура репозитория / Repository Structure

```text
IntroToDataAnalysis/
├── lab-01-data-manipulation/
│   ├── assignment/
│   └── solution/
├── lab-02-data-quality/
│   ├── assignment/
│   └── solution/
├── lab-03-basic-dataviz/
│   ├── assignment/
│   └── solution/
├── lab-04-exploratory-data-analysis/
│   ├── assignment/
│   └── solution/
├── lab-05-dashboards/
│   ├── assignment/
│   └── solution/
├── .gitignore
└── README.md
```

## Для просмотра работ

1. Откройте интересующую папку лабораторной работы.
2. Перейдите в `assignment`, если хотите посмотреть постановку задания, или в `solution`, если хотите посмотреть выполненную работу.
3. Для ноутбуков используйте Jupyter Notebook, JupyterLab, VS Code или Google Colab.
4. Для Dash-проекта перейдите в [`lab-05-dashboards/solution`](./lab-05-dashboards/solution) и установите зависимости из `PlotlyDash/requirements.txt`, если хотите запустить интерактивный дашборд локально.

## Notes for Reviewers

This repository is intended as an academic portfolio for a data analyst application. It demonstrates work with tabular data, data cleaning, exploratory analysis, static and interactive visualization, and dashboard development.
