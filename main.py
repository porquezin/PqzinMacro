import os
import json
import time
import keyboard


class FrasesManager:
    def __init__(self):
        self.file_path = 'text.json'

    def carregar_frases(self):
        try:
            with open(self.file_path, 'r', encoding="utf-8") as arquivo:
                self.frases = json.load(arquivo)
        except FileNotFoundError:
            self.frases = {}
        except json.JSONDecodeError:
            self.frases = {}

    def mostrar_frases(self):
        for key, frase in self.frases.items():
            print(f"Tecla {key}: {frase}")

    def criar_frase(self):
        key = input("Tecla: ").upper()
        keys = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]
        if key not in keys:
            print("Invalid key")
            return
        frase = input(f"Frase <{key}>: ")

        self.frases[key] = frase

        with open(self.file_path, 'w', encoding="utf-8") as arquivo:
            json.dump(self.frases, arquivo)

    def escrever_frase(self, key):
        if key not in self.frases:
            return

        frase = self.frases[key]

        keyboard.press_and_release("shift+enter")
        time.sleep(0.01)
        keyboard.write(frase)
        keyboard.press_and_release('enter')


def main():
    frases_manager = FrasesManager()
    frases_manager.carregar_frases()

    keyboard.on_press_key("F1", lambda _: frases_manager.escrever_frase("F1"))
    keyboard.on_press_key("F2", lambda _: frases_manager.escrever_frase("F2"))
    keyboard.on_press_key("F3", lambda _: frases_manager.escrever_frase("F3"))
    keyboard.on_press_key("F4", lambda _: frases_manager.escrever_frase("F4"))
    keyboard.on_press_key("F5", lambda _: frases_manager.escrever_frase("F5"))
    keyboard.on_press_key("F6", lambda _: frases_manager.escrever_frase("F6"))
    keyboard.on_press_key("F7", lambda _: frases_manager.escrever_frase("F7"))
    keyboard.on_press_key("F8", lambda _: frases_manager.escrever_frase("F8"))

    keyboard.on_press_key("F9", lambda _: frases_manager.mostrar_frases())
    keyboard.on_press_key("F10", lambda _: frases_manager.criar_frase())

    keyboard.wait("F12")
    print("Obrigado por usar!")


if __name__ == "__main__":
    os.system("cls")
    help = """                /-----------------\\
                | <-PQZIN-MACRO-> |
                \-----------------/
================== MENU DE AJUDA ==================
/    - F1-F8: Escrever frase associada à tecla    /
\    - F9:    Mostrar frases cadastradas          \\
/    - F10:   Criar nova frase                    /
\    - F12:   Sair do programa                    \\
===================================================
    """
    try:
        print(help)
        main()
    except KeyboardInterrupt:
        print("Obrigado por usar!")
