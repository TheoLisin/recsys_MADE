## Этапы решения задачи

Напомним артефакты:
- Модель кластеризации
- Модель классификации
- Альтернативные модели `Topic modelling`

Пойдём последовательно:

1) В качестве моделей кластеризации были испытаны `LSA` ([ссылка на ноутбук](../../src/topic_modelling/LSA%20.ipynb))  и `LDA` ([ссылка на ноутбук](../../src/topic_modelling/lda_1_(15.10.2022).ipynb), [ссылка на модель и сопутствующие данные](https://disk.yandex.ru/d/U3XM8g4hrHNlAg)). Метрики качества моделей (в основном `Coherence (UMASS)`) имеются, но отметим, что они ни в коем случае не играют решающей роли при выборе модели, это лучше проверять "глазами" ([ссылка](https://stackoverflow.com/questions/54762690/evaluation-of-topic-modeling-how-to-understand-a-coherence-value-c-v-of-0-4)). Перед подачей данных к моделям проводилась предобработка (лемматизация/стемминг/удаление стоп-слов/нормализация/прочее).
2) Для классификации использовался `Human-in-the-loop ML` подход. В качестве финального классификатора использовался классификатор из `contextualized-topic-models` - `Kitty classifier` ([ссылка на ноутбук](../../src/topic_modelling/Kitty.ipynb), [ссылка на модель и сопутствующие данные](https://disk.yandex.ru/d/m947Vj5NCkFX-Q), [документация](https://contextualized-topic-models.readthedocs.io/en/latest/kitty.html)). Этот классификатор предварительно решает задачу `Topic modelling` с помощью `ZeroShotTM`, о котором будет сказано в следующем пункте.
3) В качестве альтернативных моделей были рассмотрены `BERTopic` ([ссылка на ноутбук](../../src/topic_modelling/BERTopic.ipynb), [документация](https://maartengr.github.io/BERTopic/)) и модели из `contextualized-topic-models` - `CombinedTM` ([ссылка на ноутбук](../../src/topic_modelling/CombinedTM.ipynb), [ссылка на модель](https://disk.yandex.ru/d/-PAzwC3Issq9oA), [документация](https://contextualized-topic-models.readthedocs.io/en/latest/combined.html)) и `ZeroShotTM` ([документация](https://contextualized-topic-models.readthedocs.io/en/latest/zeroshot.html)). Эти модели показали очень хорошие результаты на просмотренных данных, поэтому топики получались именно с помощью них.

P.S. К сожалению, интерактивные визуализации в ноутбуках не сохранились в репозитории. По этим визуализациям, в частности, делались выводы о качестве моделей.
