from requests import get
import os
import ctypes
import sys
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from random import choice, sample, randint

user32 = ctypes.windll.user32
# get width and height of desktop
(size) = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

with open('config.json') as config_file:
    data = json.load(config_file)

base_path = os.getcwd()
unsplash_url = data["using"]['unsplash_url']
file_name = data["using"]['file_name'] + ".jpg"
keywords = data["using"]['keywords']
sleep_time = data["using"]['sleep_time']
saved_pic_number = data["using"]["saved_pic_number"]
custom_link = data["using"]["custom_link"]
source = data["using"]["source"]
fit_type = data["using"]["fit_type"]
quote_bg = data["using"]["quote_settings"]["quote_bg"]
quote_text = data["using"]["quote_settings"]["quote_text"]
quote_randomize = data["using"]["quote_settings"]["quote_randomize"]
quote_bg_type = data["using"]["quote_settings"]["quote_bg_type"]


def is_64bit():
    # 'SystemParametersInfoW' works on newer systems
    # 'SystemParametersInfoA' works on older systems
    return sys.maxsize > 2 ** 32


def download(link, keywords):
    # downloading the file and saving it (for Unsplash)
    full_url = link + keywords
    with open('Wallpaper.jpg', "wb") as file:
        response = get(full_url)
        file.write(response.content)


def setup(path_to_file):
    # setting up the wallpaper
    fit_to_screen(path_to_file)
    path_to_file = os.path.join(os.getcwd(), 'Wallpaper.jpg')
    SPI_SETDESKWALLPAPER = 20
    if is_64bit():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path_to_file, 0)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path_to_file, 0)


def set_random(from_folder):
    # set random wallpapers from their respective folders
    make_folder(from_folder)
    file = choice(os.listdir(f"{base_path}\\{from_folder}"))
    file = base_path + f"\\{from_folder}\\" + file
    setup(file)


def run():
    # changing wallpaper according to source
    if source == 1:
        # change wallpaper from Unsplash
        with open('config.json') as config_file:
            json.load(config_file)
        try:
            download(unsplash_url, keywords)
            setup('Wallpaper.jpg')
        except Exception as e:
            print(f"Error {e}")
            raise NotImplementedError
    elif source == 2:
        # change wallpaper from local wallpapers
        try:
            set_random('Wallpaper Folder')
        except IndexError:
            print('The Wallpaper Folder seems to be empty!')
            print('Try adding more Wallpapers to it first or change the Source from settings.')
    elif source == 3:
        # Change wallpapers from provided link
        try:
            set_random("Wallpapers From Link")
        except IndexError:
            print('This feature does not guarantee you will get High quality wallpapers.')
            get_from_link("Wallpapers From Link")
    elif source == 4:
        quote_wallpaper_index()
    elif source == 5:
        random_gradient()
    print('==================\nWallpaper updated!\n==================')


def setting_function(*options, name, updating=True, auto_back_key=True, key='Back'):
    # A function maker for updating settings
    # PARAMETERS:
    # options = (*args) Names of options provided for a particular setting
    # name = Name of the setting
    # updating = If we want to update the json of the GIVEN NAME.
    # auto_back_key = False if we want to customize the 'back' key
    # key = Name of the back key (used when customizing

    msg = []
    # Make the prompt options format from given options arguments and add it to 'msg' list
    for i, selections in enumerate(options, 1):
        selection = f'[{i}] {selections}\n'
        msg.append(selection)
    # Make the 'msg' list a string
    msg = ''.join([str(elem) for elem in msg])
    # Add the lines and 'Back' option as final touches
    msg = f':: {name.upper().replace("_", " ")} ::\n----------------------\n{msg}[0] {key}\n----------------------'

    while True:
        print(msg)
        try:
            option = int(input('> '))
        except ValueError:
            print('Please choose from the given numbers.')
            continue
        if option in range(0, len(options) + 1):
            if auto_back_key and option == 0:
                break
            if updating:
                update_json(name, option)
                break
        else:
            print('Option not in range.')
            continue
        return option


def update_json(name, new_setting, print_updates=True, for_quotes=False):
    # update json file every time we make SETTING changes
    # PARAMETERS:
    # name = the exact name of json object inside 'data["using"]'
    # for quotes = moves saving to 'data["using"]['quotes']'
    # new_setting = New value of the key 'name'
    # print_updates = False if we don't want updates after updating json file

    if for_quotes:
        data["using"]["quote_settings"][name] = new_setting
    else:
        data["using"][name] = new_setting
    with open("config.JSON", "w") as setting_for:
        json.dump(data, setting_for)
    if print_updates:
        print(f'{name.capitalize().replace("_", " ")} updated!')


def make_folder(folder_name, remove_existing=False):
    # make a folder 'folder_name' if not already made.
    # PARAMETERS:
    # folder_name = name of folder to be made
    # remove_existing = if True will delete existing data in the mentioned folder
    # NOTE 'remove_existing' will not work on nested directories
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f'New folder {folder_name} created!')
    if remove_existing:
        for file in os.scandir(base_path + "\\" + folder_name + "\\"):
            os.remove(file.path)
        print(f'A folder named {folder_name} found!')


def move_to_folder(folder_name, new_file_name, update_number=False):
    # move saved wallpapers to their respective folders with their respective file names
    # made for error handling while saving pictures
    # PARAMETERS:
    # folder name = name of the folder where you want ot move the files
    # new_file_name = name of file after moving
    # update_number = if True will update 'saved_pic_number' in Json, used for simple Save picture function
    make_folder(folder_name)
    try:
        os.rename(f'{base_path}/Wallpaper.jpg', f'{base_path}/{folder_name}/{new_file_name}')
        print(f"Picture saved as '{new_file_name}' in the '{folder_name}' folder")
        if update_number:
            data["using"]['file_name'] = "Wallpaper " + str(data["using"]["saved_pic_number"])
            data["using"]["saved_pic_number"] += 1
            update_json('saved_pic_number', data["using"]["saved_pic_number"], print_updates=False)
    except FileExistsError:
        print(f"[ERROR] A file with the name of {new_file_name} already exists in the folder, try changing its name "
              f"first.")
    except FileNotFoundError:
        print(f"File not found. It may have already been moved.")


def save_picture():
    # move the picture to saved wallpapers folder and update file name index in json
    with open('config.json') as config_file:
        new_data = json.load(config_file)
    file_name = new_data["using"]['file_name'] + ".jpg"
    move_to_folder('Saved wallpapers', file_name, update_number=True)


def save_as():
    # move the picture to saved wallpapers folder with a new name (no json updating is required)
    new_name = input('Save the picture as?\n> ')
    move_to_folder('Saved wallpapers', new_name + '.jpg')


def change_time():
    # SETTING to change the time interval
    print(f'---Current delay is {sleep_time} seconds---')
    while True:
        try:
            new_time = int(input('New sleep time: ') or sleep_time)
            break
        except ValueError:
            print("Please input time delay in numerical form.")
    update_json('sleep_time', new_time)


def change_keywords():
    # SETTING to change the query
    new_keyword = (input(':: New keywords ::\n> ').lower().replace(' ', ',') or keywords)
    update_json('keywords', new_keyword)


def change_custom_link():
    # SETTING to update the custom link
    new_custom_link = input(':: New custom link ::\n> ')
    if new_custom_link == '':
        new_custom_link = custom_link
        print('Continuing with older link.')
    update_json('custom_link', new_custom_link)
    get_from_link("Wallpapers From Link")


def get_from_link(save_to="Wallpapers From Link"):
    # getting pictures from custom link
    # this is to download every image from the given url
    # as images are generally displayed as thumbnails, it does not imply good quality wallpapers.
    # Also sites with heavy JavaScript would be difficult to scrape
    new_link = data["using"]["custom_link"]
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


def change_quote_settings():
    # SETTINGS change settings related to quotes
    if quote_randomize == 1:
        print('----------------------\nRandom is "ON"\n----------------------')
    else:
        print('----------------------\nRandom is "OFF"\n----------------------')
    new_quote_settings = setting_function('Change background color', 'Change text color', 'Random colors',
                                          name='quotes', updating=False)
    msg = '----------------------\n' \
          'Give hex color of new {} color:\n(Try looking at ' \
          '"https://colorhunt.co/" for good combinations!)\n' \
          '----------------------'

    def quote_color_settings(element, json_name):
        # our very own quotes settings defining function like settings function above
        print(msg.format(element))
        new_option = input('> ')
        if new_option == '':
            pass
            print('Old colors kept!')
        else:
            if not new_option.startswith('#'):
                new_option = '#' + new_option
            update_json(json_name, new_option, for_quotes=True)
        print('----------------------')

    if new_quote_settings == 1:
        quote_color_settings('background', 'quote_bg')
    elif new_quote_settings == 2:
        quote_color_settings('text', 'quote_text')
    elif new_quote_settings == 3:
        # TOGGLE randomization
        new_quote_randomize = not quote_randomize
        update_json("quote_randomize", new_quote_randomize, print_updates=False, for_quotes=True)
        print('Random is "ON"' if new_quote_randomize else 'Random is "OFF"')


def quote_settings():
    while True:
        option = setting_function('Quote colours', 'Background type',
                                  name='quotes_settings', updating=False, auto_back_key=False)
        if option == 1:
            change_quote_settings()
        elif option == 2:
            bg_type_option = setting_function('Solid colors', 'Gradient colors', name='quote_bg_type', updating=False)
            # add to wallpaper
            update_json('quote_bg_type', bg_type_option, for_quotes=True)
        elif option == 0:
            break


def fit_to_screen(file):
    # image is resized to size of the screen
    # PARAMETERS:
    # file = the image to be resized
    if fit_type == 1:
        pass
    elif fit_type == 2:
        im = Image.open(file)
        # resizing requires width and height in tuples
        im.resize(size).convert("RGB").save(file)


def randomize_color():
    # get random pairs of pre-defined colors and shuffling to interchange between bg and text color
    colors = list(choice([('#FAF1E6', '#FFC074'), ('#7952B3', '#343A40'),
                          ('#DDDDDD', '#125D98'), ('#346751', '#C84B31')]))
    color = sample(colors, len(colors))
    return color[0], color[1]


def random_gradient():
    # make gradient images
    img = Image.new("RGB", (1920, 1080), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    dr = (randint(0, 255) - r) / 1000.
    dg = (randint(0, 255) - g) / 1000.
    db = (randint(0, 255) - b) / 1000.
    for i in range(1920):
        r, g, b = r + dr, g + dg, b + db
        draw.line((i, 0, i, 1080), fill=(int(r), int(g), int(b)))
    if source == 5:
        img.save('Wallpaper.jpg')
        setup('Wallpaper.jpg')
    return img


def quote_wallpaper_index():
    # Make wallpaper with quotes
    global quote_bg, quote_text
    # if not quote_toggle:
    #     pass
    if quote_randomize:
        quote_bg, quote_text = randomize_color()

    if quote_bg_type == 1:
        img = Image.new('RGB', (1920, 1080), color=quote_bg)
    # elif quote_bg_type == 2:
    #     img = Image.open(file_name)
    else:
        img = random_gradient()
    set_quote_wallpaper(img)


def set_quote_wallpaper(image):
    # PARAMETERS:
    # image = the image on which we want the quote to be printed upon

    # Generating Wallpaper
    # https://github.com/arfin97/Quote-wallpaper-generator-and-setter-Python

    # get quotes from zen quotes API and adjusting to screen size
    r = get('https://zenquotes.io/api/random')
    json_data = json.loads(r.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    text = textwrap.fill(quote, width=35)

    fnt = ImageFont.truetype('fonts/Rubik-Black.ttf', 72)
    d = ImageDraw.Draw(image)
    d.text((350, 400), text, font=fnt, fill=quote_text)
    image.save('Wallpaper.jpg')
    setup('Wallpaper.jpg')


def reset():
    # resets settings to default
    confirmation = setting_function('Yes', 'No', name='reset', updating=False)
    if confirmation == 1:
        for setting in data["using"]:
            update_json(setting, data["default"][setting], print_updates=False) and update_json(setting, data["default"]["quote_settings"][setting])
        print('Settings now set to default!')
    elif confirmation == 2:
        print('Old settings kept!')
