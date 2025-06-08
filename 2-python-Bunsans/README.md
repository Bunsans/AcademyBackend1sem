# Generator labirints
## Start game
To start game press `sh bin/labirints.sh`

## Using
At the beginig of the game you will see the menu. You can pass the size of labirinth, select the surface, select want you see the progress of generation, choose the algoritm of generation. After generation you can pass the begin and final point, and you will see the result of finding path.

### About size of labirinth
Due to implementation of labirinth you can pass only odd numbers in range from 5 to 49.

### Abount surfaces
If you choose `yes` at menu of surface you will see the surface of labirinth.

```black``` - is basic road

```purple``` "🟪" - is booster of speed, you should to collect it

```brown``` "🟫" -  is sand, you shoud to avoi it

🔻 - is begin point 

✅ - is final point

🟩 - is path

🟦 - is border

⬜️ - is walls

# Realisation
## Algorithm of generation
### Prima

### Kruskal

## Algorithm of finding path
### BFS

### Dijkstra

# Structure of code
```main.py``` - main file

```generate_maze.py``` - file with algoritm of generation

```structure_graph.py``` - file with data structure using to generate labirinth and finding path

```visual.py``` - file with visualisation of labirinth

```symbols.py``` - file with symbols of labirinth