# -*- coding: utf-8 -*-
#
#   Localization utils
#
# 	Copyleft  (L) 2021 by Helio Loureiro
# 	Copyright (C) 2018 by Ihor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
from . import fsutils

version = int(sys.version_info.major)
version += int(sys.version_info.minor) / 10.
if version < 3.6:
    raise Exception("Unsupported Python version.  Please use 3.6 or higher.")

def build_pot(paths, po_file='messages.po', error_logs=False):
    ret = 0
    files = []
    error_logs = 'warnings.log' if error_logs else '/dev/null'
    file_list = 'locale.in'
    for path in paths:
        files += fsutils.get_files_tree(path, 'py')
    with open(file_list, 'w') as target:
        target.write('\n'.join(files))
    ret += os.system(f'xgettext -f {file_list} -L Python -o {po_file} 2>{error_logs}')
    if ret:
        print('Error while POT file update')
    ret += os.system(f'rm -f {file_list}')
    if not ret:
        print('POT file updated')


def build_locales(src_path, dest_path, textdomain):
    print('Building locales')
    for item in fsutils.get_filenames(src_path, 'po'):
        lang = item.split('.')[0]
        po_file = os.path.join(src_path, item)
        mo_dir = os.path.join(dest_path, lang, 'LC_MESSAGES')
        mo_file = os.path.join(mo_dir, textdomain + '.mo')
        if not os.path.lexists(mo_dir):
            os.makedirs(mo_dir)
        print(po_file, '==>', mo_file)
        os.system(f'msgfmt -o {mo_file} {po_file}')
