import tkinter as tk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import wikipediaapi

# ------------------ Setup ML ChatBot ------------------
chatbot = ChatBot("TourismBot")

# Train using the built-in English corpus (no custom arrays)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Wikipedia API for Assam & Arunachal queries
wiki = wikipediaapi.Wikipedia('en')

# ------------------ GUI ------------------
class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Tourism ChatBot - Assam & Arunachal Pradesh")

        # Chat display
        self.chat_display = tk.Text(master, state=tk.DISABLED, bg="lightcyan", fg="black", font=("Arial", 14))
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Input field
        self.user_input = tk.Entry(master, bg="white", fg="black", font=("Arial", 14))
        self.user_input.pack(fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        user_msg = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)

        if user_msg:
            self.display_message(user_msg, "You")
            response = self.get_response(user_msg)
            self.display_message(response, "Bot")

    def display_message(self, message, sender):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def get_response(self, message):
        msg_lower = message.lower()
        if "assam" in msg_lower or "arunachal" in msg_lower:
            # Query Wikipedia dynamically
            page = wiki.page(message)
            if page.exists():
                return page.summary[:500] + ("..." if len(page.summary) > 500 else "")
            else:
                return "Sorry, I couldn’t find details on that topic in Wikipedia."
        else:
            return str(chatbot.get_response(message))

# ------------------ Main ------------------
def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
