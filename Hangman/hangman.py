if __name__ != '__main__':
    quit()

import sys
from select import select

import colorama
from colorama import Fore, Style

import create_database
from database_funcs import *
from music import *

colorama.init(autoreset=True)

USER_STREAK = 0
USER_MODE = 1
TIMEOUT = 8
display_mode = 'Classic'

def spacer():
    print('__________________________________________________________________________________\n')

def title_screen():
    spacer()
    if USER_STREAK >= 1:
        print(Fore.RED+Style.BRIGHT+"Don't stop now! Keep up your streak of",Fore.RED+Style.BRIGHT+str(USER_STREAK)+'!\n')
    print(Fore.RED+Style.BRIGHT+'''
           ██╗░░██╗░█████╗░███╗░░██╗░██████╗░███╗░░░███╗░█████╗░███╗░░██╗
           ██║░░██║██╔══██╗████╗░██║██╔════╝░████╗░████║██╔══██╗████╗░██║
           ███████║███████║██╔██╗██║██║░░██╗░██╔████╔██║███████║██╔██╗██║
           ██╔══██║██╔══██║██║╚████║██║░░╚██╗██║╚██╔╝██║██╔══██║██║╚████║
           ██║░░██║██║░░██║██║░╚███║╚██████╔╝██║░╚═╝░██║██║░░██║██║░╚███║
           ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝
    ''')
    spacer()
    print()
    print('''                                     =========
                                       +---+
                                       |   |
                                       O   |
                                      /|\  |
                                      / \  |
                                           |
                                     =========
                                 '''+Fore.RED+Style.BRIGHT+'By: Preston Cook')
    spacer()
    print('To Play Game: Select 1\nTo Add Word: Select 2\nTo Read Rules: Select 3\nTo View Leaderboard: Select 4\nTo Change Mode: Select 5\nTo Quit Game: Select 6')
    spacer()

hangman_phases=['''  +---+
  |   |
      |
      |
      |
      |
=========''','''  +---+
  |   |
  O   |
      |
      |
      |
=========''','''  +---+
  |   |
  O   |
  |   |
      |
      |
=========''','''  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''','''  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''','''  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''','''  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

play_theme(False)

while True:
    title_screen()
    if USER_MODE==1:
            display_mode='Classic'
    else:
        display_mode=Fore.RED+Style.BRIGHT+'HARDCORE'
    user_input=input('Enter a Selection: ')
    play_navigation(False)
    while user_input not in ['1','2','3','4','5','6']:
        print('ERROR: Invalid Input')
        user_input=input('Enter a Selection: ')
        play_navigation(False)
    if user_input=='6':
        spacer()
        print(Fore.RED+Style.BRIGHT+'                             ...QUITTING PROGRAM...')
        spacer()
        quit()
    elif user_input=='5':
        spacer()
        print(Fore.RED+Style.BRIGHT+'                                  MODE SELECTION')
        spacer()
        print('You are currently in',display_mode,'Mode\n')
        print('To Play Classic Mode: Select 1')
        print('To Play '+Fore.RED+Style.BRIGHT+'HARDCORE','Mode: Select 2')
        spacer()
        user_selection = input('Select a Mode: ')
        play_navigation(False)
        while user_selection not in ['1','2']:
            print('ERROR: Invalid Input')
            user_selection = input('Select a Mode: ')
            play_navigation(False)
        if user_selection == '1':
            confirmation=input('Are You Sure that You Want to Play in Classic Mode? Y or N?: ')
            play_navigation(False)
            while confirmation.lower() not in ['y','n']:
                print('ERROR: Invalid Input')
                confirmation=input('Are You Sure that You Want to Play in Classic Mode? Y or N?: ')
                play_navigation(False)
            if confirmation.lower() == 'y':
                USER_MODE = 1
        elif user_selection == '2':
            confirmation=input('Are You Sure that You Want to Play in'+Fore.RED+Style.BRIGHT+' HARDCORE'+Fore.RESET+Style.NORMAL+' Mode? Y or N?: ')
            play_navigation(False)
            while confirmation.lower() not in ['y','n']:
                print('ERROR: Invalid Input')
                confirmation=input('Are You Sure that You Want to Play in'+Fore.RED+Style.BRIGHT+' HARDCORE'+Fore.RESET+Style.NORMAL+' Mode? Y or N?: ')
                play_navigation(False)
            if confirmation.lower() == 'y':   
                USER_MODE = 2
    elif user_input == '4':
        spacer()
        print(Fore.RED+Style.BRIGHT+'                                  THE LEADERBOARD')
        spacer()
        print()
        top_five_leaderboard()
        spacer()
        input('Enter any character to continue:' )
        play_navigation(False)
    elif user_input == '3':
        spacer()
        print(Fore.RED+Style.BRIGHT+'                                THE RULES OF HANGMAN')
        spacer()
        print()
        print('1) The computer will randomly select a word\n2) You try to guess the word one letter at a time\n3) If you guess an incorrect letter 6 times, you lose\n4) If you guess the correct word, you win!')
        spacer()
        input('Enter any character to continue: ')
        play_navigation(False)
    elif user_input == '2':
        spacer()
        print(Fore.RED+Style.BRIGHT+'                                   ADDING WORDS')
        spacer()
        print()
        print('Enter Words to Add Them to the Wordbank')
        print('Enter "STOP" when Done')
        spacer()
        while True:
            added_word = input('Enter a Word: ')
            play_navigation(False)
            if added_word.lower() in ['stop']:
                break
            add_word(added_word)
    elif user_input == '1':
        correct_word = rand_word()
        user_lives = 6
        failed_letters = []
        spacer()
        print(Fore.RED+Style.BRIGHT+'                                     HANGMAN')
        spacer()
        print()
        print(display_mode.upper(),'MODE\n')
        dashes='_ '*len(correct_word)
        whitespace=' '*len(dashes)
        while True:
            print(hangman_phases[-(user_lives+1)]+'                     ',whitespace)
            print('                              ',Fore.RED+Style.BRIGHT+dashes+'\n')
            print('FAILED LETTERS:',failed_letters,'\n')
            spacer()
            if user_lives == 0:
                print(Fore.RED+Style.BRIGHT+'                         THE CORRECT WORD WAS',Fore.RED+Style.BRIGHT+correct_word.upper())
                spacer()
                print(Fore.RED+Style.BRIGHT+'''
     ░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
     ██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
     ██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
     ██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
     ╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
     ░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝''')
                play_lose(True)
                if USER_STREAK > top_five_min():
                    spacer()
                    print(Fore.RED+Style.BRIGHT+'           CONGRATULATIONS! YOU MADE THE LEADERBOARD!')
                    spacer()
                    user_name = input('Enter your name: ')
                    play_navigation(False)
                    add_leaderboard(user_name,USER_STREAK)
                USER_STREAK = 0
                break
            if len(set(correct_word))+1==len(set(whitespace)):
                print(Fore.RED+Style.BRIGHT+'''
            ██╗░░░██╗░█████╗░██╗░░░██╗  ░██╗░░░░░░░██╗██╗███╗░░██╗██╗
            ╚██╗░██╔╝██╔══██╗██║░░░██║  ░██║░░██╗░░██║██║████╗░██║██║
            ░╚████╔╝░██║░░██║██║░░░██║  ░╚██╗████╗██╔╝██║██╔██╗██║██║
            ░░╚██╔╝░░██║░░██║██║░░░██║  ░░████╔═████║░██║██║╚████║╚═╝
            ░░░██║░░░╚█████╔╝╚██████╔╝  ░░╚██╔╝░╚██╔╝░██║██║░╚███║██╗
            ░░░╚═╝░░░░╚════╝░░╚═════╝░  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝''')
                play_win(True)
                USER_STREAK += 1
                break
            if USER_MODE == 1:
                while True:
                    indx_lst=[]
                    user_guess=input('Enter a Letter: ')
                    try:
                        int(user_guess)
                        print('ERROR: Invalid Input')
                        continue
                    except:
                        if len(user_guess)>1:
                            print('ERROR: Invalid Input')
                            continue
                        elif user_guess.upper() in failed_letters:
                            print('ERROR: Invalid Input')
                            continue
                        elif user_guess.upper() in whitespace:
                            print('ERROR: Invalid Input')
                            continue
                    spacer()
                    if user_guess.lower() in correct_word:
                        for i in range(len(correct_word)):
                            if correct_word[i]==user_guess.lower():
                                indx_lst.append(i)
                        for index in indx_lst:
                            whitespace=whitespace[:index*2]+user_guess.upper()+whitespace[index*2+1:]
                        play_correct_guess(False)
                        break
                    elif user_guess.lower() not in correct_word:
                        failed_letters.append(user_guess.upper())
                        user_lives-=1
                        play_wrong_guess(False)
                        break
            elif USER_MODE == 2:
                while True:
                    indx_lst=[]
                    print('Enter a Letter: ')
                    rlist, _, _=select([sys.stdin], [], [], TIMEOUT)
                    if rlist:
                        user_guess = sys.stdin.readline().strip()
                        try:
                            int(user_guess)
                            print('ERROR: Invalid Input')
                            continue
                        except:
                            if len(user_guess) > 1:
                                print('ERROR: Invalid Input')
                                continue
                            elif user_guess.upper() in failed_letters:
                                print('ERROR: Invalid Input')
                                continue
                            elif user_guess.upper() in whitespace:
                                print('ERROR: Invalid Input')
                                continue
                        spacer()
                        if user_guess.lower() in correct_word:
                            for i in range(len(correct_word)):
                                if correct_word[i]==user_guess.lower():
                                    indx_lst.append(i)
                            for index in indx_lst:
                                whitespace=whitespace[:index*2]+user_guess.upper()+whitespace[index*2+1:]
                            play_correct_guess(False)
                            break
                        elif user_guess.lower() not in correct_word:
                            failed_letters.append(user_guess.upper())
                            user_lives-=1
                            play_wrong_guess(False)
                            break
                    else:
                        print(Fore.RED+Style.BRIGHT+'TOO SLOW!')
                        spacer()
                        user_lives-=1
                        play_wrong_guess(False)
                        break