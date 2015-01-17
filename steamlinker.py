#!/usr/bin/env python
import argparse
import os
import os.path


# OS_X=10.10.1;Steam=1416954800
STEAM_APPS_DIR = '~/Library/Application Support/Steam/SteamApps/common/'
APPS_DIR = '~/Applications/'


def main(args):
    apps_dir = canonicalize_dir(args.apps_directory)
    steam_dir = canonicalize_dir(args.steam_apps_dir)

    steam_apps = get_installed_apps(steam_dir)
    modified = sync_links(steam_apps, apps_dir, args.cleanup, args.simulation)
    if args.simulation:
        print('Proposed actions:')
    if args.cleanup:
        print('Remove {} links'.format(len(modified)))
    else:
        print('Create {} links'.format(len(modified)))
    for app_name in modified:
        print('- ' + app_name)


def canonicalize_path(path):
    expanded = os.path.expanduser(path)
    return os.path.expandvars(expanded)


def canonicalize_dir(path):
    expanded = canonicalize_path(path)
    if not os.path.isdir(expanded):
        raise IOError('Supplied path does not refer to a directory')
    if expanded[:1] != '/':
        expanded += '/'
    return expanded


def get_subdirectories(path):
    return [path + subdir + '/' for subdir in os.listdir(path)
            if os.path.isdir(path + subdir)]


def get_installed_apps(steam_dir):
    installed = []
    app_dirs = get_subdirectories(steam_dir)
    for ad in app_dirs:
        apps = [(name, ad + name) for name in os.listdir(ad)
                if name.endswith('.app')]
        installed += apps
    return installed


def sync_links(steam_apps, apps_dir, delete=False, simulation=True):
    modified = []
    existing_apps = os.listdir(apps_dir)
    for app in steam_apps:
        if delete and app[0] in existing_apps:
            if simulation:
                print('rm {}'.format(apps_dir + app[0]))
            else:
                os.remove(apps_dir + app[0])
            modified.append(app[0])
        elif app[0] not in existing_apps:
            if simulation:
                print('{} => {}'.format(app[1], apps_dir + app[0]))
            else:
                os.symlink(app[1], apps_dir + app[0])
            modified.append(app[0])
    return modified


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-ad', '--apps-directory', type=str,
                        default=APPS_DIR, help='Specify if linking to a '
                        'directory different from \'~/Applications\'')
    parser.add_argument('-sd', '--steam-apps-dir', type=str,
                        default=STEAM_APPS_DIR, help='Specify the path to '
                        '\'Steam/SteamApps/common/\'')
    parser.add_argument('-c', '--cleanup', action='store_true', help='Specify '
                        'to cleanup generated symlinks')
    parser.add_argument('-s', '--simulation', action='store_true', help='Lists'
                        ' the actions to be taken, but does not perform them')

    main(parser.parse_args())
