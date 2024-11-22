import tkinter as tk
from tkinter import ttk, messagebox
import locale

class KonverterMataUang:
    def __init__(self):  
        self.nilai_tukar = {
            "IDR": 1,
            "MYR": 3400,
            "SGD": 11500,
            "THB": 440,
            "PHP": 270,
            "JPY": 120,
            "USD": 15000,
            "EUR": 17000
        }

    def konversi(self, jumlah, dari_mata_uang, ke_mata_uang):
        if dari_mata_uang not in self.nilai_tukar or ke_mata_uang not in self.nilai_tukar:
            return None

        jumlah_dalam_idr = jumlah * self.nilai_tukar[dari_mata_uang]
        hasil = jumlah_dalam_idr / self.nilai_tukar[ke_mata_uang]
        return hasil


class AplikasiKonversiMataUang:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Aplikasi Konversi Mata Uang")
        self.root.configure(bg="#90EE90") 

        self.konverter = KonverterMataUang()
        self.riwayat = []
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
        self.font = ("Helvetica", 12)
        self.tampilan_awal()

    def tampilan_awal(self):
        self.clear_window()

        tk.Label(self.root, text="Selamat Datang di Sistem Konversi Mata Uang",
                 font=("Helvetica", 18, "bold"), bg="#e5e5e5").pack(pady=20)
        tk.Label(self.root, text="Masukkan nama Anda", font=self.font, bg="#e5e5e5").pack(pady=10)

        tk.Label(self.root, text="Nama:", font=self.font, bg="#e5e5e5").pack(pady=5)
        self.nama_entry = tk.Entry(self.root, font=self.font)
        self.nama_entry.pack(pady=20)

        tk.Button(self.root, text="Next", font=self.font, bg="red", fg="white",
                  command=self.tampilan_layar_konversi).pack(pady=20)

    def tampilan_layar_konversi(self):
        nama = self.nama_entry.get()

        if not nama:
            messagebox.showerror("Error", "Nama harus diisi.")
            return

        self.clear_window()

        tk.Label(self.root, text=f"Selamat datang, {nama}!",
                 font=("Helvetica", 12, "italic"), bg="#e5e5e5").pack(pady=10)
        tk.Label(self.root, text="Konversi Mata Uang", font=("Helvetica", 16, "bold"), bg="#e5e5e5").pack(pady=10)

        tk.Label(self.root, text="Masukkan Jumlah Uang:", font=self.font, bg="#e5e5e5").pack(pady=5)
        self.jumlah_entry = tk.Entry(self.root, font=self.font)
        self.jumlah_entry.pack(pady=5)
        self.jumlah_entry.bind("<KeyRelease>", self.format_input_jumlah)

        tk.Label(self.root, text="Dari Mata Uang:", font=self.font, bg="#e5e5e5").pack(pady=5)
        self.dari_mata_uang_var = tk.StringVar(self.root)
        self.dari_mata_uang_menu = ttk.Combobox(self.root, textvariable=self.dari_mata_uang_var, font=self.font)
        self.dari_mata_uang_menu['values'] = list(self.konverter.nilai_tukar.keys())
        self.dari_mata_uang_menu.pack(pady=5)
        self.dari_mata_uang_menu.bind("<<ComboboxSelected>>", self.update_kurs)

        tk.Label(self.root, text="Ke Mata Uang:", font=self.font, bg="#e5e5e5").pack(pady=5)
        self.ke_mata_uang_var = tk.StringVar(self.root)
        self.ke_mata_uang_menu = ttk.Combobox(self.root, textvariable=self.ke_mata_uang_var, font=self.font)
        self.ke_mata_uang_menu['values'] = list(self.konverter.nilai_tukar.keys())
        self.ke_mata_uang_menu.pack(pady=5)
        self.ke_mata_uang_menu.bind("<<ComboboxSelected>>", self.update_kurs)

        self.kurs_label = tk.Label(self.root, text="", font=("Helvetica", 10, "italic"), bg="#90EE90")
        self.kurs_label.pack(pady=5)

        tk.Button(self.root, text="Konversi", font=self.font, bg="blue", fg="white",
                  command=self.konversi_uang).pack(pady=15)
        self.hasil_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"), fg="green", bg="#90EE90")
        self.hasil_label.pack(pady=10)

        tk.Label(self.root, text="Riwayat Konversi", font=("Helvetica", 12, "bold"), bg="#e5e5e5").pack(pady=10)
        self.history_listbox = tk.Listbox(self.root, width=60, height=10, font=("Helvetica", 10))
        self.history_listbox.pack(pady=10)

        tk.Button(self.root, text="Hapus Riwayat", font=self.font, bg="red", fg="white",
                  command=self.hapus_history).pack(pady=5)
        tk.Button(self.root, text="Keluar", font=self.font, bg="gray", fg="white",
                  command=self.keluar_program).pack(pady=5)

        self.update_kurs()

    def update_kurs(self, event=None):
        dari_mata_uang = self.dari_mata_uang_var.get()
        ke_mata_uang = self.ke_mata_uang_var.get()
        if dari_mata_uang and ke_mata_uang:
            kurs = self.konverter.nilai_tukar[dari_mata_uang] / self.konverter.nilai_tukar[ke_mata_uang]
            self.kurs_label.config(text=f"Kurs: 1 {dari_mata_uang} = {kurs:.4f} {ke_mata_uang}")

    def format_input_jumlah(self, event):
        input_text = self.jumlah_entry.get().replace(".", "").strip()
        if input_text.isdigit():
            formatted_text = f"{int(input_text):,}".replace(",", ".")
            self.jumlah_entry.delete(0, tk.END)
            self.jumlah_entry.insert(0, formatted_text)

    def konversi_uang(self):
        try:
            jumlah = float(self.jumlah_entry.get().replace(".", ""))
            dari_mata_uang = self.dari_mata_uang_var.get()
            ke_mata_uang = self.ke_mata_uang_var.get()

            if not dari_mata_uang or not ke_mata_uang:
                raise ValueError("Mata uang harus dipilih.")
            if jumlah <= 0:
                raise ValueError("Jumlah harus lebih dari nol.")

            hasil = self.konverter.konversi(jumlah, dari_mata_uang, ke_mata_uang)
            if hasil is not None:
                hasil_text = f"{jumlah:,.2f} {dari_mata_uang} = {hasil:,.2f} {ke_mata_uang}".replace(",", ".")
                self.hasil_label.config(text=hasil_text)
                self.riwayat.append(hasil_text)
                self.update_history()
            else:
                messagebox.showerror("Error", "Konversi tidak valid.")
        except ValueError as e:
            messagebox.showerror("Error", "Jumlah Mata Uang Harus Diisi")

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.riwayat:
            self.history_listbox.insert(tk.END, item)

    def hapus_history(self):
        if messagebox.askyesno("Konfirmasi", "Hapus semua riwayat?"):
            self.riwayat.clear()
            self.update_history()

    def keluar_program(self):
        if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.root.quit()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiKonversiMataUang(root)
    root.mainloop()
