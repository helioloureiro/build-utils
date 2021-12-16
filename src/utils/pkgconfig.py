# -*- coding: utf-8 -*-
#
#   pkgconfig utils
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



try:
    import commands
except ModuleNotFoundError:
    import subprocess
    class CommandInterface(object):
        def __init__(self): None

        def runShell(self, command):
            # this just go avoid unfriendly subprocess errors
            def exception_handler(type, value, traceback):
                if type == subprocess.CalledProcessError:
                    return
                else:
                    print("ERROR:", value)

            # this just go avoid unfriendly subprocess errors
            sys.excepthook = exception_handler

            try:
                response = subprocess.check_output(command.split())
            except subprocess.CalledProcessError:
                raise Exception("The following command failed:", command)
            return response
        
        def getoutput(self, command):
            response =  self.runShell(command)
            return response.decode('utf-8')

    commands = CommandInterface()
import sys

version = int(sys.version_info.major)
version += int(sys.version_info.minor) / 10.
if version < 3.6:
    raise Exception("Unsupported Python version.  Please use 3.6 or higher.")

def get_pkg_version(pkg_name):
    return commands.getoutput(f"pkg-config --modversion {pkg_name}").strip()


def get_pkg_includes(pkg_names):
    includes = []
    for item in pkg_names:
        output = commands.getoutput(f"pkg-config --cflags-only-I {item}")
        names = output.replace('-I', '').strip().split(' ')
        for name in names:
            if name not in includes:
                includes.append(name)
    return includes


def get_pkg_libs(pkg_names):
    libs = []
    for item in pkg_names:
        output = commands.getoutput(f"pkg-config --libs-only-l {item}")
        names = output.replace('-l', '').strip().split(' ')
        for name in names:
            if name not in libs:
                libs.append(name)
    return libs


def get_pkg_cflags(pkg_names):
    flags = []
    for item in pkg_names:
        output = commands.getoutput(f"pkg-config --cflags-only-other {item}")
        names = output.strip().split(' ')
        for name in names:
            if name not in flags:
                flags.append(name)
    return flags
