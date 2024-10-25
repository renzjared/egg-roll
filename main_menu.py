"""
Copyright 2024 Renz Jared Rolle.

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
"""

import sys
import time

def display_main_menu():
    """Displays the main menu and processes user input to start the game, 
    view instructions, or exit.
    """
    while True:
        from egg_roll import clear_screen       # Use local import to avoid circular imports
        clear_screen()
        header = """


       ███████╗ ██████╗  ██████╗     ██████╗  ██████╗ ██╗     ██╗         
       ██╔════╝██╔════╝ ██╔════╝     ██╔══██╗██╔═══██╗██║     ██║         
       █████╗  ██║  ███╗██║  ███╗    ██████╔╝██║   ██║██║     ██║         
       ██╔══╝  ██║   ██║██║   ██║    ██╔══██╗██║   ██║██║     ██║         
       ███████╗╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝███████╗███████╗    
       ╚══════╝ ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    



        """
        print(header)
        print("Welcome to Egg Roll!")
        print("1. Start Game")
        print("2. Instructions")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")

        if choice.strip() == '1':
            filename = input("Enter the level filename: ")
            from egg_roll import main           # Use local import to avoid circular imports
            main(filename)                      # Start the game
        elif choice.strip() == '2':
            display_instructions()              # Show instructions
        elif choice.strip() == '3':
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

def display_instructions():
    """Displays the game instructions to the player."""
    from egg_roll import clear_screen           # Use local import to avoid circular imports
    clear_screen()
    print("Instructions:")
    print("1. You will be asked to enter a series of moves.")
    print("2. Valid moves are: F (forward), B (backward), L (left), R (right).")
    print("3. Type 'restart' at any time to start over.")
    print("4. Try to collect as many points as you can before your moves run out.")
    input("Press Enter to return to the main menu...")