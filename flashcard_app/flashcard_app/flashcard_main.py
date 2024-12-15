import tkinter as tk
from flashcard_app import FlashcardStudyApp

def main():
    root = tk.Tk()
    app = FlashcardStudyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()