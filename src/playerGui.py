import tkinter as tk
import commands

class DragDropListbox(tk.Listbox):
    def __init__(self, master, update_callback=None, **kw):
        super().__init__(master, kw)
        self.update_callback = update_callback
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
        self.cur_index = None

    def set_current(self, event):
        self.cur_index = self.nearest(event.y)

    def shift_selection(self, event):
        new_index = self.nearest(event.y)
        if new_index != self.cur_index and self.cur_index is not None:
            items = list(self.get(0, tk.END))
            items.insert(new_index, items.pop(self.cur_index))
            self.delete(0, tk.END)
            for item in items:
                self.insert(tk.END, item)
            self.cur_index = new_index
            if self.update_callback:
                self.update_callback()

class GroupFrame(tk.Frame):
    def __init__(self, master, group_idx, update_callback, filas):
        super().__init__(master)
        self.group_idx = group_idx
        self.update_callback = update_callback
        self.filas = filas
        
        # Header with dynamic label
        self.header_var = tk.StringVar()
        self.header = tk.Label(self, textvariable=self.header_var)
        self.header.pack()
        self.update_header()

        # Name Listbox
        self.name_listbox = DragDropListbox(
            self, 
            width=20,
            update_callback=self.on_list_change
        )
        self.name_listbox.pack(side=tk.LEFT)
        
        # Status Listbox
        self.status_listbox = tk.Listbox(self, width=10)
        self.status_listbox.pack(side=tk.LEFT)
        
        # Transfer Button
        self.transfer_btn = tk.Button(
            self, 
            text="→", 
            command=self.transfer_player
        )
        self.transfer_btn.pack(side=tk.LEFT, padx=5)
        self.status_listbox.bind("<Double-Button-1>", self.toggle_status)

    def update_header(self):
        """Update list number and lock status"""
        lock_status = " 🔒" if self.filas.isGroupListLocked else ""
        self.header_var.set(f"Lista {self.group_idx + 1}{lock_status}")
        self.header.config(
            fg="#896279" if self.filas.isGroupListLocked else "black"
        )

    def toggle_status(self, event):
        """Toggle fighting status on double-click"""
        idx = self.status_listbox.nearest(event.y)
        player = self.filas.groupList[self.group_idx][idx]
        player.lutando = not player.lutando
        commands.manageListTxtFile(self.filas)
        self.filas.notify_listeners()

    def update_contents(self, players):
        self.update_header()
        """Update both listboxes with current player data"""
        self.name_listbox.delete(0, tk.END)
        self.status_listbox.delete(0, tk.END)
        
        for player in players:
            self.name_listbox.insert(tk.END, player.nome)
            status = "🥊" if player.lutando else "🛌"
            self.status_listbox.insert(tk.END, status)

    def on_list_change(self):
        """Handle reordering within the group"""
        self.update_callback(self.group_idx)

    def transfer_player(self):
        """Move selected player to next group"""
        if not self.name_listbox.curselection():
            return
            
        # Get selected player
        idx = self.name_listbox.curselection()[0]
        player = self.filas.groupList[self.group_idx][idx]
        
        # Determine target group
        target_group = (self.group_idx + 1) % len(self.filas.groupList)
        
        # Update model
        self.filas.groupList[self.group_idx].remove(player)
        self.filas.groupList[target_group].append(player)
        commands.manageListTxtFile(self.filas)
        self.filas.notify_listeners()


class PlayerManagerGUI:
    def __init__(self, filas_mantenedor):
        self.root = tk.Tk()
        self.root.title("Gerenciador lista")
        self.root.configure(background='#507255')

        self.filas = filas_mantenedor
        self.group_frames = []
        
        self.rebuild_gui()
        # Registra essa classe como um observer
        self.filas.add_listener(self.on_data_change)
        
    def rebuild_gui(self):
        """Recreate all group frames"""
        # Clear existing frames
        for frame in self.group_frames:
            frame.destroy()
        self.group_frames = []
        
        # Create new frames for each group
        for idx, group in enumerate(self.filas.groupList):
            frame = GroupFrame(
                self.root,
                group_idx=idx,
                update_callback=self.handle_group_update,
                filas=self.filas
            )
            frame.pack(side=tk.LEFT, padx=10)
            self.group_frames.append(frame)
            frame.update_contents(group)

    def handle_group_update(self, group_idx):
        """Update model after GUI changes"""
        current_names = self.group_frames[group_idx].name_listbox.get(0, tk.END)
        original_players = self.filas.groupList[group_idx]
        
        # Preserve player objects while updating order
        name_to_player = {p.nome: p for p in original_players}
        new_order = [name_to_player[name] for name in current_names]
        self.filas.groupList[group_idx] = new_order
        commands.manageListTxtFile(self.filas)
        self.filas.notify_listeners()

    def on_data_change(self):
        """Full refresh when groups or statuses change"""
        if len(self.filas.groupList) != len(self.group_frames):
            self.rebuild_gui()
        else:
            for frame, group in zip(self.group_frames, self.filas.groupList):
                frame.update_contents(group)

    def run(self):
        self.root.mainloop()
