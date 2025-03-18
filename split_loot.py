import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import math

class PaymentInstructionsWindow(tk.Toplevel):
    def __init__(self, parent, instructions_list, player_names):
        super().__init__(parent)
        self.title("Instruções de Pagamento")
        self.transient(parent)
        self.grab_set()

        self.players_label_title = ttk.Label(self, text="Jogadores:")
        self.players_label_title.pack(pady=(10, 0))

        self.players_frame = ttk.Frame(self)
        self.players_frame.pack(padx=10, pady=(0, 10), fill="x")
        for name in player_names:
            player_name_label = ttk.Label(self.players_frame, text=name, anchor="w")
            player_name_label.pack(pady=2, fill="x")

        self.instructions_label_title = ttk.Label(self, text="Instruções de Pagamento:")
        self.instructions_label_title.pack(pady=(10, 0))

        self.instructions_frame = ttk.Frame(self)
        self.instructions_frame.pack(padx=10, pady=(0, 10), fill="x")
        self.instruction_labels = []
        max_instruction_width = 0
        for instruction in instructions_list:
            instruction_label = ttk.Label(self.instructions_frame, text=instruction, anchor="w")
            self.instruction_labels.append(instruction_label)
            instruction_label.pack(pady=2, fill="x")
            instruction_width = instruction_label.winfo_reqwidth()
            if instruction_width > max_instruction_width:
                max_instruction_width = instruction_width

        window_width = max(400, max_instruction_width + 40)
        window_height = 150 + len(player_names) * 25 + len(instructions_list) * 25
        self.geometry(f"{window_width}x{window_height}")

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.button_close = ttk.Button(self.button_frame, text="Fechar", command=self.destroy)
        self.button_close.pack(side=tk.LEFT, padx=10)

        self.copy_all_button = ttk.Button(self.button_frame, text="Copiar Tudo", command=self.copy_instructions)
        self.copy_all_button.pack(side=tk.LEFT)

        parent.wait_window(self)

    def copy_instructions(self):
        all_instructions = "\n".join([label.cget("text") for label in self.instruction_labels])
        self.clipboard_clear()
        self.clipboard_append(all_instructions)
        self.update()
        messagebox.showinfo("Copiado", "As instruções de pagamento foram copiadas para a área de transferência.")

class SplitLootWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root  
        self.title("Split Loot Calculator")

        self.label_instructions = ttk.Label(self, text="Cole o texto do loot aqui:")
        self.label_instructions.pack(pady=10)

        self.text_loot = scrolledtext.ScrolledText(self, height=15, width=60)
        self.text_loot.pack(pady=10)

        self.frame_controls = ttk.Frame(self)
        self.frame_controls.pack(pady=20)

        self.button_calculate = ttk.Button(self.frame_controls, text="Calcular Split", command=self.calculate_split)
        self.button_calculate.pack(side=tk.LEFT, padx=10)

        self.add_adjustment_var = tk.BooleanVar()
        self.check_add_adjustment = ttk.Checkbutton(self.frame_controls, text="Adicionar Gasto/Lucro", variable=self.add_adjustment_var)
        self.check_add_adjustment.pack(side=tk.LEFT)

    def calculate_split(self):
        loot_text = self.text_loot.get("1.0", tk.END)
        add_adjustment = self.add_adjustment_var.get()

        players_data = []
        current_player = None
        for line in loot_text.splitlines():
            if line and not line.startswith("Session data:") and not line.startswith("Session:") and not line.startswith("Loot Type:") and not line.startswith("Loot:") and not line.startswith("Supplies:") and not line.startswith("Balance:"):
                if not line.startswith("\t"):
                    player_name = line
                    if " (Leader)" in player_name:
                        player_name = player_name.replace(" (Leader)", "")
                    current_player = {"name": player_name, "balance": None}
                    players_data.append(current_player)
                elif current_player is not None and line.startswith("\tBalance:"):
                    try:
                        balance_str = line.split(":")[1].replace(",", "")
                        balance = float(balance_str)
                        current_player["balance"] = balance
                    except ValueError:
                        messagebox.showerror("Erro", f"Não foi possível ler o balance de {current_player['name']}.")
                        return

        valid_players_data = [p for p in players_data if p["balance"] is not None]

        if not valid_players_data:
            messagebox.showinfo("Informação", "Nenhum jogador com informações de balance encontradas.")
            return

        player_names = [player["name"] for player in valid_players_data]
        total_balance = sum(player["balance"] for player in valid_players_data)
        num_players = len(valid_players_data)

        if num_players > 0:
            split_amount = total_balance / num_players
            rounded_split_amount = math.floor(split_amount)

            instructions_list = [f"Valor da divisão por jogador: {rounded_split_amount:,}"]
            instructions_list.append("")
            instructions_list.append("Instruções de Pagamento:")

            payers = sorted([p for p in valid_players_data if p["balance"] > rounded_split_amount], key=lambda x: x["balance"], reverse=True)
            receivers = sorted([p for p in valid_players_data if p["balance"] < rounded_split_amount], key=lambda x: x["balance"])

            for payer in payers:
                remaining_to_pay = math.floor(payer["balance"] - rounded_split_amount)
                for receiver in receivers:
                    remaining_to_receive = math.ceil(rounded_split_amount - receiver["balance"])
                    transfer_amount = min(remaining_to_pay, remaining_to_receive)
                    if transfer_amount > 0:
                        instructions_list.append(f"{payer['name']} to pay {transfer_amount:,} to {receiver['name']} (Bank: transfer {transfer_amount:,} to {receiver['name']})")
                        remaining_to_pay -= transfer_amount
                        receiver["balance"] += transfer_amount
                        if remaining_to_pay == 0:
                            break

            PaymentInstructionsWindow(self, instructions_list, player_names) # Usando 'self' como o parent
        else:
            messagebox.showinfo("Informação", "Nenhum jogador válido encontrado.")