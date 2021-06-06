import all_functions

option_message = '''----------------------
[1] Change wallpaper
[2] Save picture
[3] Save picture as-
[4] Settings
[5] Help Message
[0] Exit
----------------------'''

setting_message = '''----------------------
:: SETTINGS ::
[1] Change keywords
[2] Change time limit
[3] Change custom link
[4] Change source of wallpapers
[5] Option Message
[0] Back
----------------------'''


def setting_inputs():
    while True:
        print(':: OPTIONS ::')
        print(option_message)
        option = input('> ')
        if option == '1':
            all_functions.run()
        elif option == '2':
            all_functions.save_picture()
        elif option == '3':
            all_functions.save_as()
        elif option == '4':
            while True:
                print(setting_message)
                setting = input('> ')
                if setting == '1':
                    all_functions.change_keywords()
                elif setting == '2':
                    all_functions.change_time()
                elif setting == '3':
                    all_functions.change_custom_link()
                elif setting == '4':
                    all_functions.change_source()
                elif setting == '5':
                    continue
                elif setting == '0':
                    break
        elif option == '5':
            continue
        elif option == '0':
            print('Exiting')
            print('Okay see you!')
            break
        else:
            print('Please choose from the option indexes.')
            continue


if __name__ == '__main__':
    setting_inputs()
