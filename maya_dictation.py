import time

time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")


def readDictation():
    try:
        file = open('dictation.txt', 'r').read()
        if file == "":
            print('Dictation Section is empty')
        else:
            print(file)
    except FileNotFoundError:
        print('Dictation file not found')


def clearDictation():
    sure = input('Are you sure you want to clear the dictation? This step can be destructive!!!(y/n)? ')
    if sure == 'y':
        file = open('dictation.txt', 'w')
        clear_file = ""
        file.write(clear_file)
        file.close()
        print('The dictation has been cleared')
    else:
        print('No changes done in the dictation')


def writeDictation():
    file = open('dictation.txt', 'r')
    read_file = file.read()
    file.close()
    if read_file != "":
        permission = input('''The file already contains previous dictation, do you want to continue in previous 
        existing file or you want to clear the previous dictation?(continue/clear/read)? ''')
        if permission == 'clear':
            clearDictation()
            file_write = open('dictation.txt', 'a')
            dictate_on = True
            file_write.write(time_stamp + '\n\n')
            while dictate_on:
                dictate_maya = input('What you want to write?\n')
                file_write.write(dictate_maya + '\n')
                print('Added to the dictation')
                per = input('Do you want to dictate_maya more?(y/n) ')
                if per == 'n':
                    dictate_on = False
                else:
                    dictate_on = True
            print('Your dictation has been added.')
            file_write.close()
        elif permission == 'continue':
            file_append = open('dictation.txt', 'a')
            file_append.write("\n\n")
            file_append.write(time_stamp + '\n\n')
            dictate_on = True
            while dictate_on:
                dictate_maya = input('What you want to write?\n')
                file_append.write(dictate_maya + '\n')
                print('Added to the dictation')
                per = input('Do you want to dictate_maya more?(y/n) ')
                if per == 'n':
                    dictate_on = False
                else:
                    dictate_on = True
            print('Your dictation has been added.')
            file_append.close()
        else:
            readDictation()
            writeDictation()
    else:
        file_write = open('dictation.txt', 'w')
        dictate_on = True
        file_write.write(time_stamp + '\n\n')
        while dictate_on:
            dictate_maya = input('What you want to write?\n')
            file_write.write(dictate_maya + '\n')
            print('Added to the dictation')
            per = input('Do you want to dictate_maya more?(y/n) ')
            if per == 'n':
                dictate_on = False
            else:
                dictate_on = True
        print('Your dictation has been added.')
        file_write.close()


if __name__ == '__main__':
    dictate = input('''Do you want to:
                        1. Write the dictation(w). 
                        2. Read your previous dictation(r).
                        3. Clear your previous dictation(c). 
                        ======================================\n ''')
    if dictate == 'w':
        writeDictation()
    elif dictate == 'r':
        readDictation()
    elif dictate == 'c':
        clearDictation()
    else:
        print('Wrong Entry!! Please choose between w (write) ,r (read) or c (clear)')
