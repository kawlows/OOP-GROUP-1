import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .classes import Deck, TextFlashcard, MultipleChoiceFlashcard, TrueFalseFlashcard
import random


class FlashcardStudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Study App")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        self.decks = []  
        self.current_deck = None 

        self.setup_ui()

    def setup_ui(self):
        # Styling
        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        style.configure("TButton", font=("Roboto", 12), padding=(20, 10))

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)

        # Welcome Frame
        welcome_frame = tk.Frame(main_frame, bg="#f0f0f0")
        welcome_frame.pack(pady=20, padx=20)

        welcome_label = tk.Label(welcome_frame, text="WELCOME !", font=("Arial", 24, "bold"), bg="#f0f0f0")
        welcome_label.pack(pady=20)

        # Buttons for Deck Management, Card Management, Study
        buttons_frame = tk.Frame(welcome_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=20)

        buttons = [
            ("Deck Management", self.show_deck_management),
            ("Card Management", self.show_card_management),
            ("Study", self.show_study),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            btn = ttk.Button(buttons_frame, text=text, command=command, width=20)
            btn.pack(pady=10)

    def show_deck_management(self):
        # Clear the current screen and show deck management
        for widget in self.root.winfo_children():
            widget.destroy()

        center_frame = tk.Frame(self.root, bg="#f0f0f0")
        center_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            center_frame,
            text="Manage Your Decks",
            bg="#f0f0f0",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        title_label.pack(pady=20)

        deck_frame = tk.Frame(center_frame, bg="#f0f0f0")
        deck_frame.pack(pady=20)

        deck_buttons = [
            ("Create Deck", self.create_deck),
            ("Select Deck", self.select_deck),
            ("Edit Deck", self.edit_deck),
            ("Delete Deck", self.delete_deck),
            ("View All Decks", self.view_all_decks),
            ("Back to Menu", self.show_welcome_screen)
        ]

        for i, (text, command) in enumerate(deck_buttons):
            row, col = divmod(i, 2) 
            btn = ttk.Button(deck_frame, text=text, command=command, width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for col in range(2):  
            deck_frame.grid_columnconfigure(col, weight=1)

    def show_card_management(self):
        # Clear the current screen and show card management
        for widget in self.root.winfo_children():
            widget.destroy()

        center_frame = tk.Frame(self.root, bg="#f0f0f0")
        center_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            center_frame,
            text="Manage Your Cards",
            bg="#f0f0f0",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        title_label.pack(pady=20)

        card_frame = tk.Frame(center_frame, bg="#f0f0f0")
        card_frame.pack(pady=20)

        card_buttons = [
            ("Add Text Card", lambda: self.add_card("text")),
            ("Multiple Choice", lambda: self.add_card("mc")),
            ("True or False", lambda: self.add_card("tf")),
            ("Edit Card", self.edit_card),
            ("Delete Card", self.delete_card),
            ("Back to Menu", self.show_welcome_screen)
        ]

        for i, (text, command) in enumerate(card_buttons):
            row, col = divmod(i, 2)  
            btn = ttk.Button(card_frame, text=text, command=command, width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for col in range(2):  
            card_frame.grid_columnconfigure(col, weight=1)

    def show_study(self):
        # Clear the current screen and show study options
        for widget in self.root.winfo_children():
            widget.destroy()

        center_frame = tk.Frame(self.root, bg="#f0f0f0")
        center_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            center_frame,
            text="Study Your Decks",
            bg="#f0f0f0",
            font=("Arial", 24, "bold"),
            anchor="center"
        )
        title_label.pack(pady=20)

        button_frame = tk.Frame(center_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        study_buttons = [
            ("Practice Deck", self.practice_deck),
            ("View Deck Stats", self.view_deck_stats),
            ("View Card Stats", self.view_card_stats),
            ("Back to Menu", self.show_welcome_screen)
        ]

        for text, command in study_buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.pack(pady=10)

    def show_welcome_screen(self):
        # Go back to the welcome screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.setup_ui()

    def create_deck(self):
        name = simpledialog.askstring("Create Deck", "Enter deck name:")
        if name:
            # Check if the name is only numbers
            if name.isdigit():
                messagebox.showwarning("Warning", "Deck name cannot be only numbers. Please enter a valid name.")
                return

            new_deck = Deck(name)
            self.decks.append(new_deck)
            messagebox.showinfo("Success", f"Deck '{name}' created!")

    def select_deck(self):
        if not self.decks:
            messagebox.showwarning("Warning", "No decks available!")
            return

        # Create a selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Select a Deck")
        select_window.geometry("400x300")

        # Create a treeview to display deck information
        tree = ttk.Treeview(select_window, columns=("Name", "Cards"), show="headings")
        tree.heading("Name", text="Deck Name")
        tree.heading("Cards", text="Number of Cards")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate the treeview with deck information
        for deck in self.decks:
            tree.insert("", "end", values=(deck.name, deck.get_card_count()), tags=(deck.name,))

        # Define confirm selection as a method
        def confirm_selection():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a deck!")
                return

            # Get the deck name from the selected item
            selected_deck_name = tree.item(selected_item[0])['values'][0]

            # Find and set the current deck
            self.current_deck = next((deck for deck in self.decks if deck.name == selected_deck_name), None)

            if self.current_deck:
                messagebox.showinfo("Success", f"Selected deck: {selected_deck_name}")
                select_window.destroy()

        # Bind double-click to selection
        def on_double_click(event):
            confirm_selection()

        tree.bind('<Double-1>', on_double_click)

        # Confirmation button
        confirm_btn = ttk.Button(select_window, text="Select Deck", command=confirm_selection)
        confirm_btn.pack(pady=10)

    def edit_deck(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "No deck selected!")
            return

        new_name = simpledialog.askstring("Edit Deck", "Enter new deck name:", initialvalue=self.current_deck.name)
        if new_name:
            self.current_deck.name = new_name
            messagebox.showinfo("Success", "Deck renamed!")

    def delete_deck(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "No deck selected!")
            return

        if messagebox.askyesno("Confirm", f"Delete deck '{self.current_deck.name}'?"):
            self.decks.remove(self.current_deck)
            self.current_deck = None
            messagebox.showinfo("Success", "Deck deleted!")

    def view_all_decks(self):
        if not self.decks:
            messagebox.showwarning("Warning", "No decks available!")
            return

        deck_list = "\n".join([deck.name for deck in self.decks])
        messagebox.showinfo("All Decks", f"Available decks:\n{deck_list}")

    def add_card(self, card_type):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Select a deck first!")
            return

        question = simpledialog.askstring("Question", "Enter the question:")
        if not question:
            return

        if card_type == "text":
            answer = simpledialog.askstring("Answer", "Enter the answer:")
            card = TextFlashcard(question, answer)
        elif card_type == "mc":
            answer = simpledialog.askstring("Correct Answer", "Enter the correct answer:")
            options = [answer]
            for i in range(2):
                option = simpledialog.askstring("Option", f"Enter option {i+2}:")
                if option:
                    options.append(option)
            card = MultipleChoiceFlashcard(question, answer, options)
        elif card_type == "tf":
            answer = messagebox.askyesno("True/False", f"Is this statement true?")
            card = TrueFalseFlashcard(question, answer)

        self.current_deck.add_card(card)
        messagebox.showinfo("Success", "Card added!")

    def edit_card(self):
        if not self.current_deck or not self.current_deck.cards:
            messagebox.showwarning("Warning", "No cards available in the selected deck!")
            return

        # Create a selection window for editing cards
        select_window = tk.Toplevel(self.root)
        select_window.title("Edit Card")
        select_window.geometry("400x300")

        # Create a treeview to display cards in the deck
        tree = ttk.Treeview(select_window, columns=("Question",), show="headings")
        tree.heading("Question", text="Question")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate the treeview with card questions
        for card in self.current_deck.cards:
            tree.insert("", "end", values=(card.question,))

        def on_double_click(event):
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a card!")
                return

            selected_question = tree.item(selected_item[0])['values'][0]
            card_to_edit = next(card for card in self.current_deck.cards if card.question == selected_question)

            new_question = simpledialog.askstring("Edit Question", "Edit question:", initialvalue=card_to_edit.question)
            if new_question:
                card_to_edit.question = new_question
                messagebox.showinfo("Success", "Card question updated!")

        tree.bind('<Double-1>', on_double_click)

    def delete_card(self):
        if not self.current_deck or not self.current_deck.cards:
            messagebox.showwarning("Warning", "No cards available in the selected deck!")
            return

        select_window = tk.Toplevel(self.root)
        select_window.title("Delete Card")
        select_window.geometry("400x300")

        tree = ttk.Treeview(select_window, columns=("Question",), show="headings")
        tree.heading("Question", text="Question")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for card in self.current_deck.cards:
            tree.insert("", "end", values=(card.question,))

        def on_double_click(event):
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a card!")
                return

            selected_question = tree.item(selected_item[0])['values'][0]
            card_to_delete = next(card for card in self.current_deck.cards if card.question == selected_question)

            if messagebox.askyesno("Confirm", f"Delete card: {card_to_delete.question}?"):
                self.current_deck.cards.remove(card_to_delete)
                messagebox.showinfo("Success", "Card deleted!")

        tree.bind('<Double-1>', on_double_click)

    def practice_deck(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "No deck selected!")
            return

        for card in self.current_deck.cards:
            if isinstance(card, TextFlashcard):
                answer = simpledialog.askstring("Practice", f"{card.question}")
                if answer == card.answer:
                    messagebox.showinfo("Correct!", "Well done!")
                else:
                    messagebox.showinfo("Incorrect!", f"The correct answer is {card.answer}.")
            elif isinstance(card, MultipleChoiceFlashcard):
                answer = simpledialog.askstring("Practice", f"{card.question}\n{card.options}")
                if answer == card.answer:
                    messagebox.showinfo("Correct!", "Well done!")
                else:
                    messagebox.showinfo("Incorrect!", f"The correct answer is {card.answer}.")
            elif isinstance(card, TrueFalseFlashcard):
                answer = messagebox.askyesno("Practice", f"{card.question}")
                if answer == card.answer:
                    messagebox.showinfo("Correct!", "Well done!")
                else:
                    messagebox.showinfo("Incorrect!", f"The correct answer is {'True' if card.answer else 'False'}.")
            else:
                answer = simpledialog.askstring("Practice", f"{card.question}")
                if answer == card.answer:
                    messagebox.showinfo("Correct!", "Well done!")
                else:
                    messagebox.showinfo("Incorrect!", f"The correct answer is {card.answer}.")

    def view_deck_stats(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Select a deck first!")
            return

        stats = f"Deck '{self.current_deck.name}' has {len(self.current_deck.cards)} cards."
        messagebox.showinfo("Deck Stats", stats)

    def view_card_stats(self):
        if not self.current_deck or not self.current_deck.cards:
            messagebox.showwarning("Warning", "No cards in deck!")
            return

        stats = ""
        for card in self.current_deck.cards:
            stats += f"Question: {card.question}\nAnswer: {card.answer}\n\n"

        messagebox.showinfo("Card Stats", stats)
