import os
import random
import ctypes
import keyboard
import pystray
from PIL import Image
import configparser
from tkinter import Tk, Entry, Label, Button, END, filedialog

# Получаем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к папке с обоями
img_folder = f"{current_dir}\\Wallpapers"

# Читаем настройки из файла конфигурации
config = configparser.ConfigParser()
config.read(f'{current_dir}\\settings.ini')

# Получаем сочетание клавиш для смены обоев
hotkey = config.get('Settings', 'hotkey', fallback='ctrl+alt+w')

# Получаем путь к папке с обоями из конфигурации
wallpaper_folder = config.get('Settings', 'wallpaper_folder', fallback=img_folder)

def change_wallpaper():
    # Получаем список файлов в папке с обоями
    files = os.listdir(wallpaper_folder)
    
    # Проверяем, что список файлов не пуст
    if not files:
        print("Папка с обоями пуста!")
        return
    
    # Выбираем случайный файл
    random_file = random.choice(files)
    
    # Полный путь к выбранному файлу
    wallpaper_path = os.path.join(wallpaper_folder, random_file)
    
    # Устанавливаем обои
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)
    icon.notify("Wallpaper changed!")

def on_right_click(icon, item):
    if item == exit_item:
        icon.stop()
    elif item == change_wallpaper_item:
        change_wallpaper()
    elif item == settings_item:
        show_settings_window()

def show_settings_window():
    root = Tk()
    root.title("Settings")
    
    label = Label(root, text="Hotkey for changing wallpaper:")
    label.pack(pady=10)
    
    hotkey_entry = Entry(root)
    hotkey_entry.insert(0, hotkey)
    hotkey_entry.pack(pady=10)
    
    label = Label(root, text="Wallpaper folder:")
    label.pack(pady=10)
    
    folder_entry = Entry(root)
    folder_entry.insert(0, wallpaper_folder)
    folder_entry.pack(pady=10)
    
    def select_folder():
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_entry.delete(0, END)
            folder_entry.insert(0, selected_folder)
    
    select_folder_button = Button(root, text="Select Folder", command=select_folder)
    select_folder_button.pack(pady=10)
    
    def save_settings():
        new_hotkey = hotkey_entry.get()
        new_wallpaper_folder = folder_entry.get()
        
        config.set('Settings', 'hotkey', new_hotkey)
        config.set('Settings', 'wallpaper_folder', new_wallpaper_folder)
        with open(f'{current_dir}\\settings.ini', 'w') as configfile:
            config.write(configfile)
        
        hotkey_entry.delete(0, END)
        hotkey_entry.insert(0, new_hotkey)
        folder_entry.delete(0, END)
        folder_entry.insert(0, new_wallpaper_folder)
        
        keyboard.remove_hotkey(hotkey)
        keyboard.add_hotkey(new_hotkey, change_wallpaper)
        
        global wallpaper_folder
        wallpaper_folder = new_wallpaper_folder
        
        print(f"Hotkey changed to '{new_hotkey}'")
        print(f"Wallpaper folder changed to '{new_wallpaper_folder}'")
    
    save_button = Button(root, text="Save", command=save_settings)
    save_button.pack(pady=10)
    
    root.mainloop()

# Создаем иконку в трее
image = Image.open(os.path.join(current_dir, "icon.png"))
icon = pystray.Icon("Wallpaper Changer", image, "Wallpaper Changer")
icon.title = "Wallpaper Changer"

change_wallpaper_item = pystray.MenuItem("Change Wallpaper", change_wallpaper)
settings_item = pystray.MenuItem("Settings", on_right_click)
exit_item = pystray.MenuItem("Exit", on_right_click)
menu_items = [change_wallpaper_item, settings_item, exit_item]
icon.menu = pystray.Menu(*menu_items)

# Определяем сочетание клавиш для смены обоев
keyboard.add_hotkey(hotkey, change_wallpaper)

print(f"Press {hotkey} to change the wallpaper.")

# Запускаем иконку в трее
icon.run_detached()