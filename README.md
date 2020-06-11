# 2D Python Game Engine 2019
name    : Cbit-py

version : 1.0.1
## TODO
- ui class
- read xml file
- sprite animation
- fix collider
- tilemap class
- physic class
## main class
### main function
- creating the game  
  ```python
   game = Game(TITLE, WIDTH, HEIGHT, False)
   ```
- start the game
  ```python
   game.start()
   ```
- game loop, using while loop to loop all the function inside the game
  ```python
   while game.is_running is True:
        game.handle_events()  
        game.update()  
        game.render()  
        game.clear()  
    ```
- quit the game if loop is end
    ``` python
    game.quit()
    ```

## Game class
### function init
- parameter of the game class init function is title, width, height, fullscreen
### Game attributes
- title is the title of the game : string
- width is the screen size width : integer
- height is the screen size height: integer
- fullscreen check if the game screen is full screen: boolean
- is_running check if the game loop is still running : boolean
- clock will use pygame clock to start the timer of the game : float
- delta