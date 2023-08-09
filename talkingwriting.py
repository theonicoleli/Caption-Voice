import threading
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk

# Initialize the speech recognizer
rec = sr.Recognizer()
is_recording = False  # Variable to control recording

# Toggle recording function
def toggle_recording():
    global is_recording
    is_recording = not is_recording # Making the sentence true
    if is_recording:
        update_button.config(text="Pausar gravação")
        start_recording_thread()
    else:
        update_button.config(text="Continuar gravação")

# Start recording thread
def start_recording_thread():
    threading.Thread(target=start_recording).start()

# Start recording
def start_recording():
    while is_recording:
        selection_indice = combo.current()
        opcao_selecionada = combo["values"][selection_indice]
        print(opcao_selecionada.split()[0])
        mic_text = int(opcao_selecionada.split()[0]) - 1

        with sr.Microphone(mic_text) as mic:
            rec.adjust_for_ambient_noise(mic)
            print("Você pode falar agora, eu vou gravar:")
            audio = rec.listen(mic)
            texto = rec.recognize_google(audio, language="pt-BR")
            print(texto)

            # Insert the recognized text into the Text widget
            final_box.delete(1.0, tk.END)  # Clear previous content
            final_box.insert(tk.END, texto)

# Create a window with dimensions 500x340 and a black background
window = tk.Tk()
window.geometry('500x340')
window.configure(bg="black")

mic_selection = tk.StringVar()

# Create a combo box to select the microphone
combo = ttk.Combobox(window, textvariable=mic_selection, values=[
    f"{n+1} - {sr.Microphone().list_microphone_names()[n]}"
    for n in range(len(sr.Microphone().list_microphone_names()))
])
combo.grid(row=0, column=0, padx=10, pady=10)

# Create a button to initiate speech recognition
update_button = tk.Button(window, text="Start Recording", command=toggle_recording)
update_button.grid(row=1, column=0, padx=10, pady=5)

# Create a Text widget to display the recognized text
final_box = tk.Text(window)
final_box.grid(row=2, column=0, padx=10, pady=10)

# Run the Tkinter main loop
window.mainloop()