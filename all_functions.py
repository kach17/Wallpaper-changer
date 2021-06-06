from requests import get
import os
import ctypes
import sys
import json
from bs4 import BeautifulSoup
from random import choice

with open('config.json') as config_file:
    data = json.load(config_file)

base_path = os.getcwd()
unsplash_url = data['unsplash_url']
file_name = data['file_name'] + ".jpg"
keyword_default = data['keyword_default']
sleep_time = data['sleep_time']
saved_pic_number = data["saved_pic_number"]
custom_link = data["custom_link"]
source = data["source_default"]


def update_json(setting_for='config_loading'):
    # update json file every time we make SETTING changes
    # the parameter is not necessary but is kept to see what's going on
    with open("config.JSON", "w") as setting_for:
        json.dump(data, setting_for)


def is_64bit():
    # 'SystemParametersInfoW' works on newer systems
    # 'SystemParametersInfoA' works on older systems
    return sys.maxsize > 2 ** 32


def download(link, file_name, keywords):
    # downloading the file and saving it (for Unsplash)
    full_url = link + keywords
    with open(file_name, "wb") as file:
        response = get(full_url)
        file.write(response.content)


def setup(path_to_file):
    # setting up the wallpaper
    name_of_file = path_to_file
    path_to_file = os.path.join(os.getcwd(), name_of_file)
    SPI_SETDESKWALLPAPER = 20
    if is_64bit():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path_to_file, 0)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path_to_file, 0)


def run():
    # changing wallpaper according to source
    if source == '1':
        # change wallpaper from Unsplash
        with open('config.json') as config_file:
            json.load(config_file)
        try:
            download(unsplash_url, file_name, keyword_default)
            setup(file_name)
        except Exception as e:
            print(f"Error {e}")
            raise NotImplementedError
    elif source == '2':
        # change wallpaper from local wallpapers
        try:
            set_random('Wallpaper Folder')
        except IndexError:
            print('Th Wallpaper Folder seems to be empty!')
            print('Try adding more Wallpapers to it first or change the Source from settings.')
    elif source == '3':
        # Change wallpapers from provided link
        try:
            set_random("Wallpapers From Link")
        except IndexError:
            print('This feature does not guarantee you will get High quality wallpapers.')
            get_from_link("Wallpapers From Link")


def change_source():  # sourcery skip
    # SETTING to change the source of the wallpapers
    while True:
        print('''----------------------
[1] From Unsplash
[2] From Wallpapers Folder
[3] From custom link
----------------------''')
        new_source = input('> ')
        if new_source == '1' or '2' or '3':
            break
        else:
            print('Please choose from the given options.')
            continue
    data['source_default'] = new_source
    with open("config.JSON", "w") as new_source_setting:
        json.dump(data, new_source_setting)
    print('Source type updated!')
    return source


def make_folder(folder_name, remove_existing=False):
    # make a folder 'folder_name' if not already made.
    # remove_existing if True will existing data in the mentioned folder
    # NOTE 'remove_existing' will not work on nested directories
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f'New folder {folder_name} created!')
    if remove_existing:
        for file in os.scandir(base_path + "\\" + folder_name + "\\"):
            os.remove(file.path)
        print(f'A folder named {folder_name} found!')


def change_time():
    # SETTING to change the time interval
    print(f'---Current delay is {sleep_time} seconds---')
    while True:
        try:
            new_time = int(input('New sleep time: ') or sleep_time)
            break
        except ValueError:
            print("Please input time delay in numerical form.")

    data["sleep_time"] = new_time
    update_json('new_time_setting')
    print('Time settings updated!')
    return sleep_time


def change_keywords():
    # SETTING to change the query
    new_keyword = input('New keywords: ').lower().replace(' ', ',')
    if new_keyword == '':
        new_keyword = keyword_default
    data['keyword_default'] = new_keyword
    update_json('new_keyword_setting')
    print('Keywords updated!')
    return keyword_default


def change_custom_link():
    # SETTING to update the custom link
    new_custom_link = input(':: New custom link ::\n> ')
    if new_custom_link == '':
        new_custom_link = custom_link
        print('Continuing with older link.')
    data['custom_link'] = new_custom_link
    update_json('new_custom_link')
    print('Link updated!')
    get_from_link("Wallpapers From Link")


def move_to_folder(folder_name, new_file_name=file_name):
    # move saved wallpapers to their respective folders with their respective file names
    make_folder(folder_name)
    try:
        os.rename(f'{base_path}/{file_name}', f'{base_path}/{folder_name}/{new_file_name}')
        print(f"Picture saved as '{new_file_name}' in the '{folder_name}' folder")
    except FileExistsError:
        print(f"[ERROR] A file with the name of {new_file_name} already exists in the folder, try changing its name "
              f"first.")
    except FileNotFoundError:
        print(f"File with the name {new_file_name} does not exist. It may have already been moved.")


def save_picture():
    # move the picture to saved wallpapers folder and update file name index in json
    move_to_folder('Saved wallpapers')
    data['file_name'] = "Wallpaper " + str(data["saved_pic_number"])
    data["saved_pic_number"] += 1
    update_json('new_saved_picture')


def save_as():
    # move the picture to saved wallpapers folder with a new name (no json updating is required)
    new_name = input('Save the picture as?\n> ')
    move_to_folder('Saved wallpapers', new_name + '.jpg')


def set_random(from_folder):
    # set random wallpapers from their respective folders
    make_folder(from_folder)
    file = choice(os.listdir(f"{base_path}\\{from_folder}"))
    file = base_path + f"\\{from_folder}\\" + file
    setup(file)


def get_from_link(save_to="Wallpapers From Link"):
    # getting pictures from custom link
    # this is to download every image from the given url
    # as images are generally displayed as thumbnails, it does not imply good quality wallpapers.
    # Also sites with heavy JavaScript would be difficult to scrape
    new_link = data["custom_link"]
    r = get(new_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    print(f"Total {len(images)} Image Found!")
    make_folder(save_to, remove_existing=True)
    if len(images) != 0:
        count = 0
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL
            try:
                image_link = image["data-srcset"]
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]

                        # if no Source URL found
                        except:
                            pass
            try:
                r = get(image_link).content
                try:
                    # possibility of decode
                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    # After checking above condition, Image Download start
                    with open(f"{save_to}/images{i + 1}.jpg", "wb+") as f:
                        f.write(r)
                    count += 1
            except:
                pass
        print(f"Total {count} Images Downloaded Out of {len(images)}")
        print("Wallpapers updated! Go to Settings to if source is not already set to 'From custom link'.")
    else:
        print("No images found.")
