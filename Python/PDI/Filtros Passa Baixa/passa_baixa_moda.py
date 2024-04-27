from PIL import Image, ImageFilter, ImageTk
from tkinter import filedialog, Tk, Button, Label, Entry
from matplotlib import pyplot as plt


class ModeFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Moda")

        # Variáveis para armazenar a imagem original e a imagem filtrada
        self.image = None
        self.mode_filtered_image = None

        # Criar um botão para escolher uma imagem
        self.button_choose_image = Button(
            self.root, text="Escolha uma imagem", command=self.choose_image)
        self.button_choose_image.pack(pady=10)

        # Criar um campo de entrada para definir quantas vezes o filtro é aplicado
        self.entry_filter_count = Entry(self.root)
        self.entry_filter_count.insert(0, "1")  # Valor padrão: 1
        self.entry_filter_count.pack()

        # Criar um botão para aplicar o filtro de moda
        self.button_apply_filter = Button(
            self.root, text="Aplicar filtro", command=self.apply_filter)
        self.button_apply_filter.pack(pady=10)

        # Label para exibir a imagem original
        self.label_original_image = Label(self.root)
        self.label_original_image.pack(side='left')

        # Label para exibir a imagem filtrada
        self.label_filtered_image = Label(self.root)
        self.label_filtered_image.pack(side='right')

    def choose_image(self):
        # Solicitar ao usuário para escolher uma imagem
        image_path = filedialog.askopenfilename(title="Escolha uma imagem",
                                                filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])

        if image_path:
            # Carregar a imagem escolhida
            self.load_image(image_path)
        else:
            print("Nenhuma imagem foi selecionada.")

    def load_image(self, image_path):
        # Carregar a imagem do caminho fornecido
        self.image = Image.open(image_path)

        # Exibir a imagem original na label correspondente
        self.display_image(
            self.image, self.label_original_image, "Imagem Original")

    def apply_filter(self):
        # Obter o número de vezes que o filtro deve ser aplicado
        filter_count = self.get_filter_count()

        if self.image is not None and filter_count is not None:
            # Aplicar o filtro de mediana o número de vezes especificado
            mode_filtered_image = self.image
            for _ in range(filter_count):
                mode_filtered_image = mode_filtered_image.filter(
                    ImageFilter.ModeFilter)

            # Exibir a imagem filtrada na label correspondente
            self.display_image(mode_filtered_image, self.label_filtered_image,
                               f"Imagem Filtrada ({filter_count} vezes)")

    def get_filter_count(self):
        # Obter o valor inserido no campo de entrada
        filter_count = self.entry_filter_count.get()
        try:
            filter_count = int(filter_count)
            # Verificar se o valor é válido (positivo)
            if filter_count < 0:
                raise ValueError(
                    "O número de vezes que o filtro é aplicado deve ser positivo.")
            return filter_count
        except ValueError as e:
            # Exibir uma mensagem de erro para o usuário
            tk.messagebox.showerror("Erro", f"Valor inválido: {e}")
            return None

    def display_image(self, image, label, title):
        # Definir tamanho fixo da imagem
        fixed_width = 400
        fixed_height = 400

        # Redimensionar a imagem para o tamanho fixo
        image = image.resize((fixed_width, fixed_height), Image.ANTIALIAS)

        # Converter a imagem para um formato compatível com Tkinter
        img_tk = ImageTk.PhotoImage(image)

        # Atualizar a label com a imagem
        label.config(text=title, image=img_tk,
                     compound='top', font=("Arial", 20))
        label.image = img_tk  # Manter uma referência para evitar garbage collection


def main():
    # Inicializar a interface Tkinter
    root = Tk()

    # Definir a janela para ocupar a tela inteira
    root.state("zoomed")  # Modo de tela cheia

    # Criar a aplicação
    app = ModeFilterApp(root)

    # Iniciar a interface Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
