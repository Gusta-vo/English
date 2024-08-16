import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox

# Configura el motor TTS
engine = pyttsx3.init()

# Función para hablar texto
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Configura el reconocimiento de voz
recognizer = sr.Recognizer()

# Función para escuchar y reconocer voz
def listen_for_command():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Has dicho: {command}")
            return command
        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            return None
        except sr.RequestError:
            print("No se pudo conectar al servicio de reconocimiento.")
            return None

# Función para manejar el flujo de tarjetas
def start_quiz():
    cards = [("Hola", "Hi"), ("Adiós", "Goodbye")]
    for question, answer in cards:
        speak(f"¿Cómo se dice {question}?")
        response = listen_for_command()
        if response and response.lower() == answer.lower():
            messagebox.showinfo("Resultado", "¡Correcto!")
        else:
            messagebox.showinfo("Resultado", f"Incorrecto. La respuesta correcta es {answer}.")

# Configura la interfaz gráfica
def create_app():
    root = tk.Tk()
    root.title("Aplicación de Vocabulario")

    start_button = tk.Button(root, text="Iniciar", command=start_quiz)
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_app()