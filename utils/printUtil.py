colors = {'HEADER': "\033[95m",
          'OKBLUE': "\033[94m",
          'RED': "\033[91m",
          'OKYELLOW': "\033[93m",
          'GREEN': "\033[92m",
          'LIGHTBLUE': "\033[96m",
          'WARNING': "\033[93m",
                 'FAIL': "\033[91m",
                 'ENDC': "\033[0m",
                 'BOLD': "\033[1m",
                 'UNDERLINE': "\033[4m",
          }

class Printer:
    def __init__(self):
        pass
    def green(self, string_):
        print(colors['GREEN']+string_+colors['ENDC'])

    def red(self, string_):
        print(colors['RED']+string_+colors['ENDC'])

    def yellow(self, string_):
        print(colors['OKYELLOW']+string_+colors['ENDC'])

    def functionCall(self, string_):
        print()
        self.green(f" = ) {string_}")

