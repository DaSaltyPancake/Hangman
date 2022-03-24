from playsound import playsound

def play_theme(bool_arg):
    playsound('mp3_files/theme.mp3',bool_arg)

def play_navigation(bool_arg):
    playsound('mp3_files/navigation.wav',bool_arg)

def play_lose(bool_arg):
    playsound('mp3_files/lose.wav',bool_arg)

def play_win(bool_arg):
    playsound('mp3_files/win.wav',bool_arg)

def play_wrong_guess(bool_arg):
    playsound('mp3_files/wrong_guess.wav',bool_arg)

def play_correct_guess(bool_arg):
    playsound('mp3_files/correct_guess.wav',bool_arg)