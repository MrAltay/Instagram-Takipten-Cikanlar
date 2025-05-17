from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
from datetime import datetime

def parse_instagram_html(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            usernames = []
            for link in soup.find_all('a'):
                username = link.text.strip()
                if username and username not in usernames:
                    usernames.append(username)
            return usernames
    except Exception as e:
        print(f"Hata: {html_file} dosyası okunurken bir sorun oluştu: {str(e)}")
        return []

def find_non_followers(followers_file, following_file):
    followers = parse_instagram_html(followers_file)
    following = parse_instagram_html(following_file)
    
    if not followers or not following:
        return None
    
    non_followers = [user for user in following if user not in followers]
    
    return non_followers

class InstagramCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Takipten Çıkanları Bul")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f2f5')
        
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', padding=10, font=('Segoe UI', 10))
        self.style.configure('Custom.TLabel', font=('Segoe UI', 10), background='#f0f2f5')
        
        self.followers_file = None
        self.following_file = None
        self.non_followers = None

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_font = Font(family='Segoe UI', size=16, weight='bold')
        title_label = ttk.Label(main_frame, text="Instagram Takipten Çıkanları Bul", 
                              font=title_font, style='Custom.TLabel')
        title_label.pack(pady=20)

        followers_frame = ttk.LabelFrame(main_frame, text="Takipçiler", padding="10")
        followers_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(followers_frame, text="Takipçiler (followers) dosyasını seçin:", 
                 style='Custom.TLabel').pack(pady=5)
        ttk.Button(followers_frame, text="Takipçiler Dosyası Seç", 
                  command=self.select_followers_file, style='Custom.TButton').pack(pady=5)
        self.followers_label = ttk.Label(followers_frame, text="Henüz dosya seçilmedi.", 
                                       style='Custom.TLabel')
        self.followers_label.pack(pady=2)

        following_frame = ttk.LabelFrame(main_frame, text="Takip Edilenler", padding="10")
        following_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(following_frame, text="Takip Edilenler (following) dosyasını seçin:", 
                 style='Custom.TLabel').pack(pady=5)
        ttk.Button(following_frame, text="Takip Edilenler Dosyası Seç", 
                  command=self.select_following_file, style='Custom.TButton').pack(pady=5)
        self.following_label = ttk.Label(following_frame, text="Henüz dosya seçilmedi.", 
                                       style='Custom.TLabel')
        self.following_label.pack(pady=2)

        result_frame = ttk.LabelFrame(main_frame, text="Sonuçlar", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Takipten Çıkanları Göster", 
                  command=self.show_non_followers, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Sonuçları Kaydet", 
                                    command=self.save_results, style='Custom.TButton', state='disabled')
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=60, height=15, 
                                                   font=('Segoe UI', 10), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)

        footer_label = tk.Label(root, 
                              text="emrullahaltay.com",
                              font=('Segoe UI', 10, 'bold'),
                              fg='blue',
                              cursor='hand2')
        footer_label.pack(side=tk.BOTTOM, pady=10)
        footer_label.bind('<Button-1>', lambda e: self.open_website())
        footer_label.bind('<Enter>', lambda e: footer_label.configure(fg='darkblue'))
        footer_label.bind('<Leave>', lambda e: footer_label.configure(fg='blue'))

    def open_website(self):
        import webbrowser
        webbrowser.open('https://emrullahaltay.com')

    def save_results(self):
        if not self.non_followers:
            messagebox.showwarning("Uyarı", "Kaydedilecek sonuç bulunamadı!")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"takipten_cikanlar_{timestamp}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Metin Dosyası", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("Sizi takip etmeyen kullanıcılar:\n")
                    file.write("─" * 38 + "\n")
                    for i, username in enumerate(self.non_followers, 1):
                        file.write(f"{i}. {username}\n")
                    file.write(f"\nToplam {len(self.non_followers)} kişi sizi takip etmiyor.\n")
                    file.write(f"\nOluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                    file.write("emrullahaltay.com")
                messagebox.showinfo("Başarılı", "Sonuçlar başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {str(e)}")

    def select_followers_file(self):
        file_path = filedialog.askopenfilename(title="Takipçiler dosyasını seçin", 
                                             filetypes=[("HTML Dosyası", "*.html")])
        if file_path:
            self.followers_file = file_path
            self.followers_label.config(text=os.path.basename(file_path))

    def select_following_file(self):
        file_path = filedialog.askopenfilename(title="Takip Edilenler dosyasını seçin", 
                                             filetypes=[("HTML Dosyası", "*.html")])
        if file_path:
            self.following_file = file_path
            self.following_label.config(text=os.path.basename(file_path))

    def show_non_followers(self):
        self.result_text.delete(1.0, tk.END)
        if not self.followers_file or not self.following_file:
            messagebox.showerror("Hata", "Lütfen iki dosyayı da seçin!")
            return
        self.non_followers = find_non_followers(self.followers_file, self.following_file)
        if self.non_followers is None:
            self.result_text.insert(tk.END, "Kullanıcı listeleri oluşturulamadı veya dosya formatı hatalı!\n")
            self.save_button.configure(state='disabled')
            return
        if not self.non_followers:
            self.result_text.insert(tk.END, "Hiç takipten çıkan kullanıcı bulunamadı!\n")
            self.save_button.configure(state='disabled')
            return
        self.result_text.insert(tk.END, "Sizi takip etmeyen kullanıcılar:\n")
        self.result_text.insert(tk.END, "─" * 40 + "\n")
        for i, username in enumerate(self.non_followers, 1):
            self.result_text.insert(tk.END, f"{i}. {username}\n")
        self.result_text.insert(tk.END, f"\nToplam {len(self.non_followers)} kişi sizi takip etmiyor.\n")
        self.save_button.configure(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    messagebox.showinfo("Bilgilendirme", "Bu dosya tamamen açık kaynak ve ücretsiz olarak paylaşılmıştır. Ücret talebinde bulunulması yasaktır.")
    app = InstagramCheckerApp(root)
    root.mainloop()