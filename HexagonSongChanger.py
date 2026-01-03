# python 3.14.2
import subprocess
from pathlib import Path
import shutil
import os

def check_dependences():
    result_ff = subprocess.run('ffmpeg -version', capture_output=True, shell=True, text=True)
    if result_ff.returncode != 0:
        print("ffmpeg is not installed, install it now? (y/n): ")
        choice = input().lower()
        if choice == 'y':
            result_install_ff = subprocess.run('winget install ffmpeg', shell=True)
            if result_install_ff.returncode != 0:
                print("Failed to install ffmpeg. Please install it manually.")
                exit()
        else:
            exit()

    result_yt = subprocess.run('yt-dlp --version', capture_output=True, shell=True, text=True)
    if result_yt.returncode != 0:
        print("yt-dlp is not installed, install it now? (y/n): ")
        choice = input().lower()
        if choice == 'y':
            result_install_yt = subprocess.run('python -m pip install yt-dlp', shell=True)
            if result_install_yt.returncode != 0:
                result_install_yt = subprocess.run('python3 -m pip install yt-dlp', shell=True)
                if result_install_yt.returncode != 0:
                    result_install_yt = subprocess.run('py -m pip install yt-dlp', shell=True)
                    if result_install_yt.returncode != 0:
                        print("Failed to install yt-dlp. Please install it manually.")
                        exit()
        else:
            exit()

def get_path():
    script_path = Path(__file__).parent

    if Path(script_path / "gamepath.txt").exists():
        with open (script_path / "gamepath.txt", "r") as f:
            game_path = f.read().strip()
    else:
        with open (script_path / "gamepath.txt", "w") as f:
            game_path = input("Enter path to game: ")
            f.write(game_path)
            print("Path saved to gamepath.txt as " + game_path + ".\n")

    return game_path
    

def backup_files(game_path):
    music1 = Path(game_path) / "data" / "music" / "music1.dat"
    music2 = Path(game_path) / "data" / "music" / "music2.dat"
    music3 = Path(game_path) / "data" / "music" / "music3.dat"

    if music1.with_suffix('.bak').exists() and music2.with_suffix('.bak').exists() and music3.with_suffix('.bak').exists():
        return
    else:
        shutil.copy(music1, music1.with_suffix('.bak'))
        shutil.copy(music2, music2.with_suffix('.bak'))
        shutil.copy(music3, music3.with_suffix('.bak'))

        print("Backup of original music files created.")

def restore(game_path):
    music1 = Path(game_path) / "data" / "music" / "music1.bak"
    music2 = Path(game_path) / "data" / "music" / "music2.bak"
    music3 = Path(game_path) / "data" / "music" / "music3.bak"

    if music1.exists():
        shutil.copy(music1, Path(game_path) / "data" / "music" / "music1.dat")
    if music2.exists():
        shutil.copy(music2, Path(game_path) / "data" / "music" / "music2.dat")
    if music3.exists():
        shutil.copy(music3, Path(game_path) / "data" / "music" / "music3.dat")
    print("Restored original music files.")
    exit()

def get_song(game_path):
    print("Pick song to replace: (1) Hexagon 130BPM, (2) Hexagoner 135BPM, (3) Hexagonest 175BPM, (4) Default")
    song = int(input())

    if song == 1:
        name = "music1.dat"
    elif song == 2:
        name = "music2.dat"
    elif song == 3:
        name = "music3.dat"
    elif song == 4:
        restore(game_path)
    else:
        print("Invalid choice.")
        exit()
    
    link = input("\nPaste Link: ")

    print("\nDownloading...\n--------------")
    subprocess.run('yt-dlp -x --audio-format wav -o songfile.wav ' + link, shell=True)

    print("\nConverting...\n-------------")
    subprocess.run('ffmpeg -i songfile.wav -c:a libvorbis -b:a 224k -ar 44100 -ac 2 songfile.ogg', shell=True)

    file = Path("songfile.ogg")
    shutil.move(file, Path(f"{game_path}\\data\\music\\{name}"))
    
    if Path("songfile.wav").exists():
        os.remove("songfile.wav")

    print(f"Replaced {name} with the downloaded song.")

if __name__ == "__main__":
    os.chdir(Path.home())

    check_dependences()
    backup_files(get_path())
    get_song(get_path())

    print("\nCompleted successfully.\n")
    input()
