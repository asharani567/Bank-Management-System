import tkinter as tk
from customer_management import welcomeScreen

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')  # Full-screen mode
    root.title("Bank Management System")
    
    app = welcomeScreen(root)

    root.mainloop()
