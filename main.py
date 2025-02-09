import sys

from gui import Gui as GUI  

class MainApp:
    def __init__(self):
        self.gui = GUI()

    def run(self):
        try:
            self.gui.start()
        except Exception as e:
            print(f"Vyskytl se problém: {e}", file=sys.stderr)

if __name__ == "__main__":
    app = MainApp()
    app.run()