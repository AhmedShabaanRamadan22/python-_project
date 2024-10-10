import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Modern look
import schedule
import time
from threading import Thread
from backup import backup_files
from email_notification import send_email
from download_files import download_file
import os

class SchedulerGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Download and Backup Scheduler")
        master.geometry("500x450")

        # Set custom style
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12), foreground="#333333")
        style.configure("TButton", font=("Helvetica", 12), foreground="#000000", background="#007BFF")
        style.map("TButton", background=[("active", "#45A049")])

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # File URL
        ttk.Label(self.master, text="File URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.file_url = ttk.Entry(self.master, width=50)
        self.file_url.grid(row=0, column=1, padx=5, pady=5)

        # Download Directory
        ttk.Label(self.master, text="Download Directory:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.download_dir = ttk.Entry(self.master, width=50)
        self.download_dir.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_download_dir).grid(row=1, column=2, padx=5, pady=5)

        # Backup Source
        ttk.Label(self.master, text="Backup Source:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.backup_source = ttk.Entry(self.master, width=50)
        self.backup_source.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_backup_source).grid(row=2, column=2, padx=5, pady=5)

        # Backup Destination
        ttk.Label(self.master, text="Backup Destination:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.backup_dest = ttk.Entry(self.master, width=50)
        self.backup_dest.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_backup_dest).grid(row=3, column=2, padx=5, pady=5)

        # Email Subject
        ttk.Label(self.master, text="Email Subject:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.email_subject = ttk.Entry(self.master, width=50)
        self.email_subject.grid(row=4, column=1, padx=5, pady=5)

        # Email Body
        ttk.Label(self.master, text="Email Body:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.email_body = tk.Text(self.master, width=50, height=3, font=("Helvetica", 10))
        self.email_body.grid(row=5, column=1, padx=5, pady=5)

        # Email Recipient
        ttk.Label(self.master, text="Email Recipient:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.email_recipient = ttk.Entry(self.master, width=50)
        self.email_recipient.grid(row=6, column=1, padx=5, pady=5)

        # Schedule Time
        ttk.Label(self.master, text="Schedule Time (HH:MM):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.schedule_time = ttk.Entry(self.master, width=50)
        self.schedule_time.grid(row=7, column=1, padx=5, pady=5)

        # Schedule Button
        ttk.Button(self.master, text="Schedule Job", command=self.schedule_job).grid(row=8, column=1, pady=20)

    def browse_download_dir(self):
        self.download_dir.delete(0, tk.END)
        self.download_dir.insert(0, filedialog.askdirectory())

    def browse_backup_source(self):
        self.backup_source.delete(0, tk.END)
        self.backup_source.insert(0, filedialog.askdirectory())

    def browse_backup_dest(self):
        self.backup_dest.delete(0, tk.END)
        self.backup_dest.insert(0, filedialog.askdirectory())

    def schedule_job(self):
        file_url = self.file_url.get()
        download_directory = self.download_dir.get()
        backup_source = self.backup_source.get()
        backup_destination = self.backup_dest.get()
        email_subject = self.email_subject.get()
        email_body = self.email_body.get("1.0", tk.END).strip()
        email_recipient = self.email_recipient.get()
        schedule_time = self.schedule_time.get()

        if not all([file_url, download_directory, backup_source, backup_destination, 
                    email_subject, email_body, email_recipient, schedule_time]):
            messagebox.showerror("Error", "All fields are required!")
            return

        schedule.every().day.at(schedule_time).do(self.job, file_url, download_directory, 
                                                  backup_source, backup_destination, 
                                                  email_subject, email_body, email_recipient)

        messagebox.showinfo("Success", f"Job scheduled daily at {schedule_time}")
        
        # Start the scheduler in a separate thread
        Thread(target=self.run_scheduler, daemon=True).start()

    def job(self, file_url, download_directory, backup_source, backup_destination, 
            email_subject, email_body, email_recipient):
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        try:
            download_file(file_url, download_directory)
            print("File downloaded successfully.")

            backup_files(backup_source, backup_destination)
            print("Backup completed successfully.")

            send_email(email_subject, email_body, email_recipient)
            print("Email sent successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
