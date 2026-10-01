import sys

from app.app import App

def main():
    a = App(sys.argv)
    a.run()

if __name__ == "__main__":
    main()