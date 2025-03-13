import tkinter as tk

class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        super().__init__(master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i

def create_gui(player_groups):
    root = tk.Tk()
    root.title("Player Manager")

    # Create frames for each group
    for idx, group in enumerate(player_groups):
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        label = tk.Label(frame, text=f"Group {idx + 1}")
        label.pack()

        listbox = DragDropListbox(frame, height=len(group), width=20)
        listbox.pack()

        # Populate the listbox with players
        for player in group:
            listbox.insert(tk.END, player)

    root.mainloop()

# Example data: groups of players
player_groups = [
    ["Player A", "Player B", "Player C"],
    ["Player D", "Player E", "Player F"],
    ["Player G", "Player H", "Player I"]
]

create_gui(player_groups)
