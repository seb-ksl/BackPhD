#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  backphd.py
#  
#  Copyright 2014 seb-ksl <seb@gelis.ch>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#  
#

import os
import subprocess
import sys


def ask(question, valid_answers):
    answer = ''
    while answer not in valid_answers:
        try:
            answer = input(question + ' ' + str(valid_answers) + ' ')
            return answer
        except KeyboardInterrupt:
            print('\nKeyboard interruption: leaving program.')
            sys.exit(0)


def get_backup_folder():
    folders_dic = {}

    media_folder = os.listdir('/media')
    for subfolder in media_folder:
        if subfolder.startswith('sd'):
            if 'PhD_backup' in os.listdir('/media/' + subfolder):
                folders_dic[subfolder] = True
            else:
                folders_dic[subfolder] = False
    return folders_dic


def create_folder(folders):
    folder_to_create = ask('Where to create backup folder?', list(folders.keys()))
    os.mkdir('/media/' + folder_to_create + '/PhD_backup')


def backup(folder):
    if os.access('/media/' + folder + '/PhD_backup', os.W_OK):
        subprocess.call(['/usr/bin/rsync', '-taurv', '--delete', '/home/seb/PhD/',
                 '/media/' + folder + '/PhD_backup/'])
    else:
        print('Not allowed to write to backup disk ' + folder + '.\nBackup not done.')


def main():
    # Test if rsync and pumount are available before doing anything else
    if os.access('/usr/bin/rsync', os.F_OK) and os.access('/usr/bin/pumount', os.F_OK):
        folders = get_backup_folder()

        if folders:

            # If at least one backup folder is found, look for it (or them) and backup
            if True in folders.values():
                for folder in folders:

                    if folders[folder]:
                        backup(folder)
                        do_unmount = ask('Unmount backup disk?', ['y', 'n'])

                        if do_unmount == 'y':
                            subprocess.call(['/usr/bin/pumount', folder])

            else:
                do_create = ask('Create backup folder?', ['y', 'n'])

                if do_create == 'y':
                    create_folder(folders)
                    main()

        else:
            print('No USB drive detected.')

    else:
        print('This script requires rsync and pumount to be installed.')


if __name__ == '__main__':
    main()