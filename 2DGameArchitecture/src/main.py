from src.Game import Game
from src.Settings import *
from datetime import datetime


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

    now = datetime.now()  # get the time now : datetime()
    record_log = open('../dev/record.log', 'a')  # create a record log to record activities

    # this is welcoming page and developer description
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

    # for recording and log
    # ---------------------
    # dd/mm/YY H:M:S
    date_string = now.strftime('%d-%m-%Y %H:%M:%S')
    # record
    # format date :: status :: status description :: written
    record_status = 'NORMAL'  # status of the application : str
    record_description = 'Normal behaviour of the software'  # description for the application : str
    record_written_activities = ''  # str(input('Record: '))  # user can record the activities : str
    if record_written_activities is '':
        written_activities = 'No activities record'  # if no input just write this
    try:
        record_log.writelines('\n')
        record_log.writelines(date_string)  # record date
        record_log.writelines(' :: ')
        record_log.writelines(record_status)  # record status
        record_log.writelines(' :: ')
        record_log.writelines(record_description)  # record description
        record_log.writelines(' :: ')
        record_log.writelines(record_written_activities)  # recored input activities
    finally:
        record_log.close()  # close the record log file

    quit()  # quit the application


# process the main
main()
