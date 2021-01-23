from src.game import Game
from src.settings import *
from datetime import datetime
import logging
import logging.config
import datetime


# main function
def main():
    # application information and attributes
    author = 'Nur Akmal arcmole007'  # author name : str
    start_date = '24-08-2019'  # start date : str
    company_name = 'OHWOW Game Studio est. 2019'  # game company name : str
    build = 1  # version number build : int
    major_change_no = 10  # version major changes no : int
    minor_change_no = 74  # version minor changes no : int
    version = str(build) + '.' + str(major_change_no) + '.' + str(minor_change_no)  # version : str

    current_time = datetime.datetime.now()
    logging_filename = f'{current_time.year}-{current_time.month}-{current_time.day}-{current_time.timestamp()}.log'

    # this is welcoming page and developer description
    logging.basicConfig(filename=f'../log/{logging_filename}',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    # logger = logging.getLogger(__name__)

    # logger.debug('This is a debug message')
    print('welcome to Cbit-Python game engine')
    print('Author :', author)  # show author name
    print('Software version :', version)  # show application version
    print('Company :', company_name)  # show company name

    # game main function
    # -----------------
    # create the game
    game = Game(TITLE, WIDTH, HEIGHT, False)  # game : Game()

    # init the game
    game.start()
    # game loop
    while game.is_running is True:
        game.handle_events()  # handle the event of the game
        game.update()  # update process in the game
        game.render()  # render or draw all images in the game
        game.clear()  # clear all the image in the game
    game.quit()  # quit the game
    # -----------------

    quit()  # quit the application


# process the main
if __name__ == '__main__':
    main()
