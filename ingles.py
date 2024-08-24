import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import signal
import sys

# Configura el motor TTS
engine = pyttsx3.init()

# Configura el reconocimiento de voz
recognizer = sr.Recognizer()

# Archivo de almacenamiento de palabras
WORDS_FILE = 'words.txt'

# Variable global para controlar la escucha
listening = True

def speak(text):
    """Función para hablar texto"""
    engine.say(text)
    engine.runAndWait()

def listen_for_command(callback):
    """Función para escuchar y reconocer voz usando un hilo separado"""
    global listening
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)  # Ajusta el reconocimiento al ruido ambiental
        while listening:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                print(f"Has dicho: {command}")
                callback(command)
                break  # Salir del bucle después de recibir el comando
            except sr.UnknownValueError:
                print("No entendí lo que dijiste.")
                speak("No entendí lo que dijiste.")
                callback(None)
                break  # Salir del bucle después de un error
            except sr.RequestError:
                print("No se pudo conectar al servicio de reconocimiento.")
                speak("No se pudo conectar al servicio de reconocimiento.")
                callback(None)
                break  # Salir del bucle después de un error
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                speak(f"Ocurrió un error: {e}")
                callback(None)
                break  # Salir del bucle después de un error

def start_quiz():
    """Función para manejar el flujo de tarjetas"""
    cards = load_words()
    if not cards:
        speak("No hay palabras para el cuestionario.")
        return

    def ask_question(english_word, spanish_word):
        """Pregunta la traducción de una palabra y espera la respuesta"""
        def on_command_received(command):
            if command and command.lower() == spanish_word.lower():
                speak("¡Correcto!")
            else:
                speak(f"Incorrecto. La respuesta correcta es {spanish_word}.")
            next_question()

        speak(f"¿Cómo se dice {english_word} en español?")
        global listening
        listening = True
        threading.Thread(target=listen_for_command, args=(on_command_received,)).start()

    def next_question():
        """Avanza a la siguiente pregunta"""
        if cards:
            english_word, spanish_word = cards.pop(0)
            ask_question(english_word, spanish_word)
        else:
            speak("Has terminado el cuestionario.")
            global listening
            listening = False

    next_question()

def load_words():
    """Función para cargar las palabras desde el archivo"""
    try:
        with open(WORDS_FILE, 'r') as file:
            return [tuple(line.strip().split(',')) for line in file if len(line.strip().split(',')) == 2]
    except FileNotFoundError:
        return []

def add_word():
    """Función para agregar palabras al archivo"""
    english_word = simpledialog.askstring("Agregar Palabra", "Introduce la palabra en inglés:")
    if english_word:
        spanish_word = simpledialog.askstring("Agregar Palabra", "Introduce la traducción en español:")
        if spanish_word:
            try:
                with open(WORDS_FILE, 'a') as file:
                    file.write(f"{english_word},{spanish_word}\n")
                messagebox.showinfo("Éxito", "Palabra añadida con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

def exit_app():
    """Función para cerrar la aplicación"""
    global listening
    listening = False
    root.destroy()

def create_app():
    """Configura la interfaz gráfica"""
    global root
    root = tk.Tk()
    root.title("Aplicación de Vocabulario")

    start_button = tk.Button(root, text="Iniciar", command=start_quiz)
    start_button.pack(pady=10)

    add_button = tk.Button(root, text="Agregar Palabra", command=add_word)
    add_button.pack(pady=10)

    exit_button = tk.Button(root, text="Salir", command=exit_app)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()