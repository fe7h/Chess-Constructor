
# Шахматы

---
**!!!** Это всё ещё далеко от завершения и этот ридми скорее монолог с самим собой что бы 
не забыть что я тут вообще делаю **!!!**
---
По сути это шахматный конструктор которой должен предоставлять набор 
методов для упрощения создания шахмат любого вида. Хотя если подумать 
это не совсем так 

## Структура
На данный момент корневой директорией является constructor.

### Модуль figures
<details> 
<summary>figures</summary>
Нужно переименовать в pieces 
</details>

Реализует абстрактный класс для фигур, данный класс хранит и обрабатывает информацию о фигуре.

Так же содержит ряд абстрактный дочерних классов реализующих базовые шахматные механики такие 
как рокировка взятие на проходе и удар не равный ходу (как у пешки)  

### Модуль board 
Предоставляет класс Board который хранит в себе данные обо всех фигурах и реализует методы управляющие ими.

Board для удобства и возможности масштабируемости разбит на классы микисины объединенные единой логикой. 

## Как это должно работать
В задумке это всё безобразие должно реализовывать патерн MVC. Но до этого пока ещё далеко.

### MVC
В роли **модели** в даном случаи выступает класс Board, на данный момент боорд имеет 
почти все необходимые методы, однако большинство из них ещё нужно весьма сильно причесать, 
как минимум рокировка не имеет своего полноценного метода.

Как **контролер** должен выступать класс Game, которого ещё не существует. В объект этого класса должен 
поступать текстовый запрос, затем этот запрос должен парситься после чего в соответствии с запросом будут 
вызваны необходимые методы у борд. В конце концов на выход гейм должен выплёвывать ответ. 
который уже будет обрабатывать и отрисовывать вью.

Собственно говоря что до **вью** то им может выступать что угодно, по задумки создавая контролер будет 
можно задать ему формат выдаваемого ответа, а вью уже будет необходимо создавать с нуля 
под самый удобный формат ответа.

### Структура пользовательских шахмат
С этого момента уже начинается подлинная шиза. 

По своей сути всё это в некоторой, а может и в полной, степени будет являться фремворком.
Так как все эти идеи предполагают определённую архитектуру. 

Так что до этой архитектуры. На данный момент задумка такая:

```
ChessName/
├── __init__.py
├── config.py
├── game.py
├── board.py
└── figures.py
```
Вся эта директория с вложенными фалами будет создаваться автоматически на подобии того как делает джанго. 
А что до самих модулей то суть такая:
- В **figures.py** пишутся реализации для всех фигур что будут доступны в этой версии.
- В **board.py** пишутся либо переопределяются микисны из которых состоит итоговый объект доски. Идея в том что
итоговый объект доски приоритетно будет подтягивать микисны от сюда.
- **game.py** тут сложно пока сказать как именно будет всё происходить, но похоже что на подобие того как и в боорд.
- **config.py** должен представлять собой набор констант таких как патерн координат, базовая 
зона превращения пешек, патерн для стартового расположение фигур.
- **init.py** тут будет происходить вся магия сборки ... и возвращаться через пакет класс игры
для именно этого набора.

Идея в том что бы после всех этих манипуляций итоговое использование созданных человеком шахмат выглядело как то так:
```python
from ChessName import Game

game = Game()

while True:
    response = game(requests)
    view(response)

```
