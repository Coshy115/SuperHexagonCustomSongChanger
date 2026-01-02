# python 3.14.2
import subprocess
from pathlib import Path
import shutil
import os

def backup_files():
    music1 = Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music1.dat")
    music2 = Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music2.dat")
    music3 = Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music3.dat")

    if music1.with_suffix('.bak').exists() and music2.with_suffix('.bak').exists() and music3.with_suffix('.bak').exists():
        return
    else:
        shutil.copy(music1, music1.with_suffix('.bak'))
        shutil.copy(music2, music2.with_suffix('.bak'))
        shutil.copy(music3, music3.with_suffix('.bak'))

        print("Backup of original music files created.")

def restore():
    if Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music1.bak").exists():
        shutil.copy(Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music1.bak"), Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music1.dat"))
    if Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music2.bak").exists():
        shutil.copy(Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music2.bak"), Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music2.dat"))
    if Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music3.bak").exists():
        shutil.copy(Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music3.bak"), Path("D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\music3.dat"))
    print("Restored original music files.")
    exit()

def get_song():
    print("Pick song to replace: (1) Hexagon 130BPM, (2) Hexagoner 135BPM, (3) Hexagonest 175BPM, (4) Default")
    song = int(input())

    if song == 1:
        name = "music1.dat"
    elif song == 2:
        name = "music2.dat"
    elif song == 3:
        name = "music3.dat"
    elif song == 4:
        restore()
    else:
        print("Invalid choice.")
        exit()
    
    link = input("\nPaste Link: ")

    print("\nDownloading...\n--------------")
    subprocess.run([
    'yt-dlp', 
    '-x', 
    '--audio-format', 'wav',
    '-o', 'songfile.wav', 
    link])

    print("\nConverting...\n-------------")
    subprocess.run([
    'ffmpeg',
    '-i', 'songfile.wav',
    '-c:a', 'libvorbis',
    '-b:a', '224k',
    '-ar', '44100',
    '-ac', '2',
    'songfile.ogg'
    ])

    file = Path("songfile.ogg")
    shutil.move(file, Path(f"D:\\SteamLibrary\\steamapps\\common\\Super Hexagon\\data\\music\\{name}"))
    
    if Path("songfile.wav").exists():
        os.remove("songfile.wav")

    print(f"Replaced {name} with the downloaded song.")

if __name__ == "__main__":
    os.chdir(Path.home())
    backup_files()
    get_song()
    print("\nCompleted successfully.\n")
    input()