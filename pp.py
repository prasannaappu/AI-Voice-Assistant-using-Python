import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3 as pt
import pywhatkit as pw
import pyautogui as pa
import webbrowser as wb
import os
import speech_recognition as sr
import threading

# Voice Engine Initialization
engine = pt.init()
engine.setProperty("rate", 135)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def handle_command(event=None):
    query = entry.get().lower().strip()
    if not query:
        messagebox.showinfo("Hey!", "Please enter a command.")
        return

    log.insert(tk.END, f"You: {query}\n")

    if "quit" in query:
        speak("Are you sure you want to quit?")
        if messagebox.askyesno("Exit", "Do you want to close the assistant?"):
            speak("Goodbye!")
            root.destroy()

    elif "search" in query:
        question = query.replace("search", "").strip()
        speak("Searching your question")
        wb.open(f"https://www.google.com/search?q={question}")
        log.insert(tk.END, f"Assistant: Searching for {question}\n")

    elif "play" in query:
        video = query.replace("play", "").strip()
        speak("Playing " + video)
        pw.playonyt(video)
        log.insert(tk.END, f"Assistant: Playing {video} on YouTube\n")

    elif "screenshot" in query:
        path = r'C:\screenshot'
        os.makedirs(path, exist_ok=True)
        img = pa.screenshot()
        img.save(os.path.join(path, 'screenshot.png'))
        speak("Screenshot taken and saved.")
        log.insert(tk.END, f"Assistant: Screenshot saved to {path}\n")

    elif "open" in query:
        app_name = query.replace("open", "").strip()
        speak("Opening " + app_name)
        pa.press("super")
        pa.typewrite(app_name)
        pa.press("enter")
        log.insert(tk.END, f"Assistant: Opened {app_name}\n")

    elif "zomato" in query:
        speak("Opening Zomato")
        wb.open("https://www.zomato.com/india")

    elif "swiggy" in query:
        speak("Opening Swiggy")
        wb.open("https://www.swiggy.com")

    elif "amazon" in query:
        speak("Opening Amazon")
        wb.open("https://www.amazon.in")

    elif "flipkart" in query:
        speak("Opening Flipkart")
        wb.open("https://www.flipkart.com")

    elif "whatsapp" in query:
        speak("Opening WhatsApp")
        wb.open("https://web.whatsapp.com/")

    elif "bmsce" in query:
        speak("Opening BMS College Website")
        wb.open("https://www.bmsce.ac.in/")

    elif "email" in query:
        speak("Opening Gmail")
        wb.open("https://mail.google.com/mail/u/0/")

    elif "youtube" in query:
        speak("Opening YouTube")
        wb.open("https://www.youtube.com/")

    elif "restart" in query:
        if messagebox.askyesno("Restart", "Do you want to restart the system?"):
            speak("Restarting your system")
            os.system("shutdown /r /t 1")

    elif "shutdown" in query:
        if messagebox.askyesno("Shutdown", "Do you want to shut down the system?"):
            speak("Shutting down your system")
            os.system("shutdown /s /t 1")

    else:
        speak("Sorry, I didn't understand.")
        messagebox.showinfo("Try Again", "Try: search AI, play music, screenshot, open notepad")
        log.insert(tk.END, f"Assistant: Command not recognized.\n")

    entry.delete(0, tk.END)
    log.see(tk.END)

# Voice input from microphone
def listen_command():
    threading.Thread(target=voice_input).start()

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        log.insert(tk.END, "🎙 Listening...\n")
        log.see(tk.END)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            query = recognizer.recognize_google(audio).lower()
            log.insert(tk.END, f"You (via mic): {query}\n")
            entry.delete(0, tk.END)
            entry.insert(0, query)
            handle_command()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            log.insert(tk.END, "Assistant: Timeout. No speech detected.\n")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
            log.insert(tk.END, "Assistant: Couldn't recognize speech.\n")
        except sr.RequestError:
            speak("Sorry, there seems to be a network issue.")
            log.insert(tk.END, "Assistant: Speech recognition service failed.\n")

# Dark mode toggle
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    if dark_mode:
        root.configure(bg="#0f172a")
        container.configure(style="DarkCard.TFrame")
        title.configure(bg="#1e293b", fg="#e2e8f0")
        footer.configure(bg="#1e293b", fg="#cbd5e1")
        log.configure(bg="#1e293b", fg="#e2e8f0", insertbackground="white")
        style.configure("TEntry", fieldbackground="#334155", foreground="#e2e8f0")
    else:
        root.configure(bg="#e0f2fe")
        container.configure(style="LightCard.TFrame")
        title.configure(bg="#f1f5f9", fg="#1e293b")
        footer.configure(bg="#f1f5f9", fg="#475569")
        log.configure(bg="#f8fafc", fg="#0f172a", insertbackground="black")
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#0f172a")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("✨ AI Voice Assistant")
root.geometry("670x500")
root.minsize(500, 420)
root.configure(bg="#e0f2fe")

style = ttk.Style()
style.theme_use("clam")
style.configure("LightCard.TFrame", background="#f1f5f9", relief="flat", borderwidth=0)
style.configure("DarkCard.TFrame", background="#1e293b", relief="flat", borderwidth=0)
style.configure("TButton", font=("Segoe UI Semibold", 12), padding=8, relief="flat")
style.map("TButton",
          background=[("active", "#1d4ed8")],
          foreground=[("active", "#ffffff")])
style.configure("TEntry", padding=8, font=("Segoe UI", 12))

dark_mode = False

container = ttk.Frame(root, padding=25, style="LightCard.TFrame")
container.place(relx=0.5, rely=0.45, anchor="center")

title = tk.Label(container, text="🔊 Your Smart Voice Assistant", font=("Segoe UI Semibold", 20), bg="#f1f5f9", fg="#1e293b")
title.pack(pady=(0, 15))

entry = ttk.Entry(container, width=45)
entry.pack(pady=12)
entry.bind("<Return>", handle_command)

run_btn = ttk.Button(container, text="🚀 Run Command", command=handle_command)
run_btn.pack(pady=6)

voice_btn = ttk.Button(container, text="🎙 Speak Now", command=listen_command)
voice_btn.pack(pady=6)

log = tk.Text(root, height=9, width=80, bg="#f8fafc", fg="#0f172a", font=("Segoe UI", 10))
log.pack(padx=15, pady=(5, 10))
log.insert(tk.END, "Assistant: Hello Prasanna! I'm ready to help.\n")
log.configure(state='normal')

footer = tk.Label(container, text="Try: search AI, play music, screenshot, open notepad", font=("Segoe UI", 10), bg="#f1f5f9", fg="#64748b")
footer.pack(pady=(10, 0))

theme_btn = ttk.Button(root, text="🌗 Toggle Theme", command=toggle_theme)
theme_btn.place(relx=1.0, y=12, anchor="ne", x=-12)

speak("Hi Prasanna! I'm ready to help you.")
apply_theme()
root.mainloop()
