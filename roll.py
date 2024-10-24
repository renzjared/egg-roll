"""
Copyright 2024 Renz Jared Rolle and Jeremiah Adriel Ocampo.

Licensed under the GNU General Public License, Version 3 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/renzjared/egg-roll/blob/main/LICENSE

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 @author Renz Jared Rolle <rgrolle@up.edu.ph>
 @author Jeremiah Adriel Ocampo <renzjaredrolle@gmail.com>
"""

import sys

def main(filename):
    level = read_level(filename).readlines()
    row = int(level[0].replace("\n",""))
    moves = int(level[1].replace("\n",""))
    print(row, moves)

def read_level(filename):
    # Check if file exists; send error message if the file does not exist
    # We assume that the file is valid (as per MP1 Section 3)
    try:
        level = open(filename, "r") 
        return level
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # check first if the user included a level filename
    if(len(sys.argv) > 1):
        filename = str(sys.argv[1])
        main(filename)
    else:
        print("[Error] Please include a filename argument for a game level.")