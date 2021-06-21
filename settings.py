import all_functions
from importlib import reload


def options():
    while True:
        # OPTIONS
        option = all_functions.setting_function('Change wallpaper', 'Save picture',
                                                'Save picture as-', 'Settings',
                                                'Reset settings to default',
                                                name='OPTIONS', updating=False,
                                                auto_back_key=False, key='Exit')

        if option == 1:
            # Change wallpaper
            all_functions.run()
        elif option == 2:
            # Save picture
            all_functions.save_picture()
        elif option == 3:
            # Save picture as-
            all_functions.save_as()
        elif option == 4:
            # SETTINGS
            while True:
                setting = all_functions.setting_function('Change keywords', 'Change time delay',
                                                         'Change custom link', 'Change source of wallpapers',
                                                         'Change fit type', 'Quotes settings', name='SETTINGS',
                                                         updating=False, auto_back_key=False)
                if setting == 1:
                    # Change keywords
                    all_functions.change_keywords()
                elif setting == 2:
                    # Change time delay
                    all_functions.change_time()
                elif setting == 3:
                    # Change custom link
                    all_functions.change_custom_link()
                elif setting == 4:
                    # Change source of wallpapers
                    all_functions.setting_function('From Unsplash', 'From Wallpapers Folder',
                                                   'From custom link', 'Quotes', 'Gradient colors', name='source')
                elif setting == 5:
                    # Change fit type
                    all_functions.setting_function('Original size', 'Fit to screen', name='fit_type')
                elif setting == 6:
                    # Quotes settings
                    all_functions.quote_settings()
                elif setting == 0:
                    options()
                    break
                reload(all_functions)
                continue
            break
        elif option == 5:
            all_functions.reset()
        elif option == 0:
            print('Exiting...')
            print('Okay see you!')
            break


if __name__ == '__main__':
    options()
