# flashcard_classes.py

from datetime import datetime

# Base Flashcard Class
class Flashcard:
    def __init__(self, question, answer, category="Uncategorized"):
        self.id = id(self)  # Unique identifier
        self.question = question
        self.answer = answer
        self.category = category
        self.attempts = 0
        self.correct_attempts = 0
        self.last_practiced = None

    def practice(self, user_answer):
        self.attempts += 1
        self.last_practiced = datetime.now()
        is_correct = self._validate_answer(user_answer)
        
        if is_correct:
            self.correct_attempts += 1
        
        return is_correct

    def _validate_answer(self, user_answer):
        raise NotImplementedError("Subclasses must implement this method")

    def get_stats(self):
        accuracy = (self.correct_attempts / self.attempts * 100) if self.attempts > 0 else 0
        return {
            "Question": self.question,
            "Total Attempts": self.attempts,
            "Correct Attempts": self.correct_attempts,
            "Accuracy": f"{accuracy:.2f}%",
            "Category": self.category,
            "Type": self.__class__.__name__
        }

# Text Flashcard
class TextFlashcard(Flashcard):
    def _validate_answer(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()

# Multiple Choice Flashcard
class MultipleChoiceFlashcard(Flashcard):
    def __init__(self, question, answer, options, category="Uncategorized"):
        super().__init__(question, answer, category)
        self.options = options

    def _validate_answer(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()

    def get_stats(self):
        stats = super().get_stats()
        stats["Options"] = ", ".join(self.options)
        return stats

# True or False Flashcard
class TrueFalseFlashcard(Flashcard):
    def __init__(self, question, answer, category="Uncategorized"):
        super().__init__(question, str(answer).lower(), category)

    def _validate_answer(self, user_answer):
        return user_answer.lower() in ['true', 'false', '1', '0', 'yes', 'no'] and \
               user_answer.lower() == self.answer.lower()

# Deck Class
class Deck:
    def __init__(self, name):
        self.id = id(self)
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card_id):
        self.cards = [card for card in self.cards if card.id != card_id]

    def get_card_count(self):
        return len(self.cards)