# Changelog

## 3.0.0 — 2026-09-05

### Breaking changes

- Навык стал гибридным решателем: ядро ТРИЗ + смежные методики.
- Схема результата: противоречия теперь типизированы (`anyOf` — достаточно одного из `technical`/`physical`/`dilemma`), `triz_tool` в концепции опционален.
- `validate_output.py` добавлены смысловые проверки (механизм не равен названию инструмента, статус evidence, enum-значения домена/природы/выхода).

### Added

- Входной смыслообразующий маршрутизатор Cynefin + честные выходы («обычная оптимизация», «сначала измерить», «данных недостаточно», «решения нет»).
- Диагностика природы задачи: ТП / ФП / ложная дилемма / сеть проблем / неопределённость / невыполнимость / многокритериальный выбор.
- Полный алгоритм ARIZ-85C (9 частей / 3 блока) в `references/ariz-85c.md`.
- 16 модулей смежных методик: TOC Evaporating Cloud, OTSM, C-K, морфологический анализ+CCA, Axiomatic Design, Decision Analysis (NASA/Pugh/Taguchi), Cynefin, SSM/CATWOE, Kepner-Tregoe, SIT, биомимикрия, синектика, латеральное мышление/6 шляп, Double Diamond, DOE, STPA.
- Расширены eval-наборы: кейсы на новые методики и отрицательные случаи.

### Changed

- `methodology-map.md` — полная карта маршрутизации по домену и природе задачи.
- `sources.md` — добавлены первоисточники смежных методик.

## 2.0.0 — 2026-07-11

### Breaking changes

- Удалён обязательный линейный конвейер «40 приёмов → веполь → АРИЗ».
- Пятишаговый маршрут переименован и заменён triage-моделью.
- Авторская короткая таблица больше не называется матрицей Альтшуллера.
- Интеграции TCE/NC777 стали опциональными.

### Added

- Problem identification: границы, функция, поток, CECA, ключевая задача.
- Physical contradiction separation principles.
- Correct Su-Field routing and 76 SIS overview.
- ARIZ-85C escalation route.
- Resources, trimming, feature transfer, FOS, scientific effects.
- S-curve and TESE overview.
- Reviewer protocol, evals, schema and validation scripts.
- Evidence and uncertainty ledger.

### Fixed

- Исправлены битые относительные ссылки.
- Исправлена трактовка поля в Su-Field.
- Убрано дублирование полного списка 40 приёмов из основного файла.
- Числовые software-пороги помечены как контекстные, а не универсальные.
