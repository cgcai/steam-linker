Steam Linker
============

Many Steam apps/games can be launched independently without using the Steam launcher by running them from their hiding spot at `~/Application Support/Steam/SteamApps/common`

This script automatically creates or removes symlinks for installed Steam apps/games in `~/Applications`. 

##Usage

    $ ./steamlinker.py -h
    usage: steamlinker.py [-h] [-ad APPS_DIRECTORY] [-sd STEAM_APPS_DIR] [-c] [-s]

    optional arguments:
      -h, --help            show this help message and exit
      -ad APPS_DIRECTORY, --apps-directory APPS_DIRECTORY
                            Specify if linking to a directory different from
                            '~/Applications'
      -sd STEAM_APPS_DIR, --steam-apps-dir STEAM_APPS_DIR
                            Specify the path to 'Steam/SteamApps/common/'
      -c, --cleanup         Specify to cleanup generated symlinks
      -s, --simulation      Lists the actions to be taken, but does not perform
                            them
