import pandas as pd
from collections import Counter
import inquirer
import os
from colorama import init, Fore, Style

data_folder = "data"
saved_folder = "saved"
os.makedirs(data_folder, exist_ok=True)
os.makedirs(saved_folder, exist_ok=True)

init(autoreset=True)

# These will be the colors
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
GREEN = Fore.GREEN
RED = Fore.RED

class StatTable:
    def __init__(self, data_list, precision=2, stat_mode="Sample"):
        self.data_list = data_list
        self.precision = precision  # Just in case the user wants to set the precision in decimals
        self.stat_mode = stat_mode
        self.n = len(data_list)
        self.mean = sum(data_list) / self.n
        self.freq = Counter(data_list)
        self.df = None
        self.f_df = None
        self.sorted = sorted(self.data_list)
        self._set_sym()

        """
        I don't know, but I want to define these special math expressions using Unicode.
        Maybe because it's cool?

        I did think of assigning these variables inside a separate file, but nope.
        For the sake of compactness, I did this instead.
        """

    def _set_sym(self):
        if self.stat_mode == "Population":
            self.mean_sym = "\u03BC"
            self.var_sym = "\u03C3\u00B2"
            self.std_sym = "\u03C3"
            self.diff_sym = "x - \u03BC"
            self.diff2_sym = "(x - \u03BC)\u00B2"
        else: # stat_mode == "Sample"
            self.mean_sym = "x\u0304"
            self.var_sym = "s\u00B2"
            self.std_sym = "s"
            self.diff_sym = "x - x\u0304"
            self.diff2_sym = "(x - x\u0304)\u00B2"

    def build_table(self):
        """
        I know there is a better way of doing what I did with xmm and xmm_s.
        This works best for me because I can reuse it in solving the Variance and Std_Dev.
        I don't know. Maybe I'll update this next time
        """
        xmm_raw = [x - self.mean for x in self.data_list]
        xmm = [round(x, self.precision) for x in xmm_raw]
        xmm_s = [round((x - self.mean)**2, self.precision) for x in self.data_list]

        """
        I only chose x, x - mean, (x - mean)^2, and frequency for the columns.
        Maybe I'll update this next time and add more columns? LOL
        """

        self.df = pd.DataFrame({
            "x" : self.data_list,
            self.diff_sym : xmm,
            self.diff2_sym : xmm_s,
            "f" : [self.freq[x] for x in self.data_list]
        })

        row_sums = pd.Series({
            "x": round(sum(self.data_list), self.precision),
            self.diff_sym: round(sum(xmm), self.precision),
            self.diff2_sym: round(sum(xmm_s), self.precision),
            "f": ""
        })
        self.df.loc["\u03A3"] = row_sums

        mid = self.n // 2
        if self.n % 2 == 0:
            median = round((self.sorted[mid - 1] + self.sorted[mid]) / 2, self.precision)
        else:
            median = round(self.sorted[mid], self.precision)

        max_freq = max(self.freq.values())
        modes = [x for x, f in self.freq.items() if f == max_freq]
        if max_freq == 1:
            mode = "None"
        elif len(modes) == 1:
            mode = modes[0]
        else:
            mode = ', '.join(map(str, modes))

        min_val = min(self.data_list)
        max_val = max(self.data_list)
        range_val = round(max_val - min_val, self.precision)

        if self.stat_mode == "Population":
            variance = round(sum(xmm_s) / self.n, self.precision)
        else: # stat_mode = "Sample"
            variance = round(sum(xmm_s) / (self.n - 1), self.precision)


        std_dev = round(variance**(1/2), self.precision)
        # Yeah, I didn't use math.sqrt() because this works just fine

        """
        This DataFrame only has two columns: the statistics symbols and their corresponding values.
        In the Statistics Symbol Columns includes:
        - Mean
        - Median 
        - Mode
        - Min
        - Max
        - Range
        - Variance
        - Std Dev
        """

        self.f_df = pd.DataFrame(
            {
                "Value" : [
                    round(self.mean, self.precision),
                    median,
                    mode,
                    min_val,
                    max_val,
                    range_val,
                    variance,
                    std_dev
                ]
            },
            index = [
                f"Mean ({self.mean_sym})",
                "Median",
                "Mode",
                "Min",
                "Max",
                "Range",
                f"Variance ({self.var_sym})",
                f"Std Dev ({self.std_sym})"
            ]
        )

    # The two functions are just there to return the data

    def show(self):
        return self.df

    def show_stats(self):
        return self.f_df

def cprint(color, text, print_type=0):
    """
    At first, I thought of using the just print() to do the job but figured out that
    it is better to make another function to handle the colors and printing
    """
    if print_type == 0:
        print("[" + CYAN + "+" + Style.RESET_ALL + "] " + color + text + Style.RESET_ALL)
    elif print_type == 1:
        print(color + text + Style.RESET_ALL)


def intro():
    print(CYAN + """
       _____________ __________  _________   ___  __   ____
      / __/_  __/ _ /_  __/ __/ /_  __/ _ | / _ )/ /  / __/
     _\ \  / / / __ |/ / _\ \    / / / __ |/ _  / /__/ _/  
    /___/ /_/ /_/ |_/_/ /___/   /_/ /_/ |_/____/____/___/
    """)
    print(GREEN + "-"*64)
    cprint(YELLOW, "Stats Table Generator CLI")
    cprint(YELLOW, "Version 1.0 | Author: Ros N.")
    cprint(MAGENTA, "You can load a dataset from 'data/' or enter data manually.")
    cprint(MAGENTA, "All generated tables will be saved in the 'saved/' folder.")
    print(GREEN + "-"*64 + "\n")

def load_data():
    while True:
        cprint(YELLOW, "Enter dataset filename (CSV, inside 'data/' folder):")
        filename = input(" > ").strip()
        """
        Although I can use the normal input for this and put the prompt and '>' inside, 
        I did this because I think this is way better.
        Just look at it LOL.
        """
        filepath = os.path.join(data_folder, f"{filename}.csv")
        if not os.path.exists(filepath):
            cprint(RED, f"File {filepath} not found. Please try again.", print_type=1)
            continue
        try:
            df = pd.read_csv(filepath, header=None)
            data_list = df.values.flatten().tolist()
            data_list = [float(x) for x in data_list]
            return data_list
        except Exception as e:
            cprint(RED, f"Failed to load numbers from '{filename}'. Error: {e}", print_type=1)

def get_data():
    data_list = []
    index = 1
    cprint(YELLOW, "Enter the data one by one. Type 'done' when finished.\n")
    while True:
        val = input("[" + CYAN + f"{index}" + Style.RESET_ALL + "] Data > ")
        if val.strip().lower() == "done":
            break
        try:
            data_list.append(float(val))
            index += 1
        except ValueError:
            cprint(RED, "Invalid input! Only numbers are allowed.", print_type=1)
    if not data_list:
        cprint(RED, "No data found.", print_type=1)
    return data_list

def save_results(df, f_df):
    def save(filename):
        df.to_csv(filename, index=False)
        with open(filename, 'a') as f:
            f.write("\n")
        f_df.to_csv(file, mode='a', index=True)

    while True:
        cprint(YELLOW, "Enter filename to save (will be saved in 'saved/' folder):")
        name = input(" > ")
        if not name:
            name = "stats_table"
        file = os.path.join(saved_folder, f"{name}.csv")

        if os.path.exists(file):
            cprint(RED, f"File '{name}' already exists.", print_type=1)
            print()

            """
            The normal input looks lame. 
            Like I mean why would the user want to type 'Override" or 'o', 'Skip' or 's', and
            'Rename' or 'r' if they can just navigate through the three choices using their arrow keys LOL.
            """

            choices = [
                inquirer.List(
                    'action',
                    message="- Choose what to do",
                    choices=['Override', 'Skip', 'Rename'],
                    carousel=True # Yeah, turn this on
                )
            ]
            choice = inquirer.prompt(choices)['action']

            if choice == 'Override':
                save(file)

                cprint(GREEN, f"Tables overridden and saved as '{file}.csv.", print_type=1)
                break
            elif choice == 'Skip':
                cprint(YELLOW, f"Skipped saving the tables.", print_type=1)
                break
            elif choice == 'Rename':
                cprint(CYAN, "Enter a new filename.", print_type=1)
                continue
        else:
            print()
            save(file)

            cprint(GREEN, f"Tables saved as '{file}.csv.", print_type=1)
            break

def main():
    intro()
    data_list = []
    while True:

        choices = [
            inquirer.List(
                'method',
                message="- Choose data input method",
                choices=['Load dataset', 'Manual', 'Cancel / Exit'],
                carousel=True  # I like turning this part on or True
            )
        ]
        choice = inquirer.prompt(choices)['method']

        if choice == 'Load dataset':
            data_list = load_data()
        elif choice == 'Manual':
            data_list = get_data()
        elif choice == 'Cancel / Exit':
            print("[" + CYAN + "+" + Style.RESET_ALL + "] " + Style.DIM + "Exiting..." + Style.RESET_ALL)
            break

        stat_mode = "Population"

        def gen_table(mode, dec=2):
            tables = StatTable(data_list, precision=dec, stat_mode=mode)
            tables.build_table()
            print()
            cprint(CYAN, "Raw data table:")
            print(tables.show())
            print()
            cprint(CYAN, "Summary statistics:")
            print(tables.show_stats())
            print()
            return tables

        table = gen_table(stat_mode)

        while True:
            options = [
                inquirer.List(
                    'action',
                    message="- Choose what to do",
                    choices=['Precision', 'Stat Type', 'Save'],
                    carousel=True
                )
            ]
            option = inquirer.prompt(options)['action']

            if option == 'Precision':
                cprint(YELLOW, "Enter the precision(0-8):")
                try:
                    pre = int(input(" > "))
                    if 0 <= pre <= 8:
                        table = gen_table(stat_mode, dec=pre)
                    else:
                        raise ValueError
                except ValueError:
                    cprint(RED, "Precision must be between 0 and 8.", print_type=1)
                    continue
            elif option == 'Stat Type':
                stat_modes = [
                    inquirer.List(
                        'mode',
                        message="- Choose statistics type",
                        choices=['Population', 'Sample'],
                        carousel=True
                    )
                ]

                stat_mode = inquirer.prompt(stat_modes)['mode']
                table = gen_table(stat_mode, dec=table.precision)
            elif option == 'Save':
                save_results(table.df, table.f_df)
                print()
                break

        cprint(CYAN, "Done!")
        cprint(CYAN, "Summary rows includes:")
        cprint(CYAN, "- Mean")
        cprint(CYAN, "- Variance")
        cprint(CYAN, "- Standard Deviation")
        print(GREEN + "-" * 64 + "\n")

if __name__ == "__main__":
    main()

