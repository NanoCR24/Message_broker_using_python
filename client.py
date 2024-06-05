import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import grpc
import message_broker_pb2
import message_broker_pb2_grpc
import threading
import time
import os

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.transient(parent)
        self.title("Conectando al servidor...")
        self.geometry("300x100")
        self.message_label = tk.Label(self, text=message)
        self.message_label.pack(pady=20)

class ChatClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Cliente")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.condition = threading.Condition()
        self.is_connected = False
        self.custom_dialog = CustomDialog(self.root, "Conectando al servidor...")
        self.channel = grpc.insecure_channel('localhost:32000')
        self.stub = message_broker_pb2_grpc.MessageBrokerStub(self.channel)
        self.connect_to_server()

    def wait_for_connection(self):
        with self.condition:
            while not self.is_connected:
                self.condition.wait()

    def set_connected(self, connected):
        with self.condition:
            self.is_connected = connected
            if connected:
                self.condition.notify_all()

    def connect_to_server(self):
        def try_connect():
            start_time = time.time()
            while not self.is_connected:
                try:
                    self.available_topics = self.get_available_topics()
                    self.root.after(0, self.setup_gui)
                    self.set_connected(True)
                except grpc.RpcError:
                    time.sleep(1)
                    if time.time() - start_time > 60:
                        self.root.after(0, self.show_connection_error)
                        break
        threading.Thread(target=try_connect).start()

    def show_connection_error(self):
        messagebox.showerror("Error", "El servidor está apagado. Por favor, inténtelo de nuevo más tarde.")
        self.on_closing()

    def setup_gui(self):
        self.custom_dialog.destroy()
        self.topics = self.select_topics()

        self.tab_control = ttk.Notebook(self.root)
        self.tabs = {}

        for topic in self.topics:
            self.create_tab(topic)

        self.tab_control.pack(expand=1, fill='both')

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X)

        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.sub_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opciones", menu=self.sub_menu)
        self.sub_menu.add_command(label="Suscribirse a nuevos tópicos", command=self.add_new_topics)

        for topic in self.topics:
            threading.Thread(target=self.subscribe_to_topic, args=(topic,)).start()

    def create_tab(self, topic):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=topic)
        self.tabs[topic] = {
            "frame": tab,
            "text_area": tk.Text(tab, wrap=tk.WORD, state=tk.DISABLED)
        }
        self.tabs[topic]["text_area"].pack(fill=tk.BOTH, expand=True)

    def select_topics(self):
        if not self.available_topics:
            messagebox.showinfo("No hay temas disponibles.")
            self.on_closing()

        topic_list_str = "\n".join([f"{index}. {topic}" for index, topic in enumerate(self.available_topics, start=1)])
        topic_indices_str = simpledialog.askstring("Selección de Temas", f"{topic_list_str}\n\nSeleccione los números de los temas a los que desea suscribirse (separados por comas):")

        if topic_indices_str is None:
            self.on_closing()

        try:
            topic_indices = [int(i) for i in topic_indices_str.split(',')]
            for index in topic_indices:
                if index < 1 or index > len(self.available_topics):
                    raise ValueError("Número fuera de rango")
            return [self.available_topics[i - 1] for i in topic_indices]
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Por favor, introduzca números separados por comas.")
            return self.select_topics()

    def get_available_topics(self):
        response = self.stub.GetTopics(message_broker_pb2.Empty())
        return response.topics

    def subscribe_to_topic(self, topic):
        while True:
            self.wait_for_connection()
            if not self.check_connection():
                self.root.after(0, self.show_connection_error)
                return
            try:
                responses = self.stub.Subscribe(message_broker_pb2.SubscribeRequest(topic=topic))
                for response in responses:
                    self.display_message(topic, response.sender, response.message)
            except grpc.RpcError:
                self.root.after(0, self.show_connection_error)
                return

    def display_message(self, topic, sender, message):
        text_area = self.tabs[topic]["text_area"]
        text_area.configure(state=tk.NORMAL)
        text_area.insert(tk.END, f"\n{sender} ({topic}): {message}")
        text_area.see(tk.END)
        text_area.configure(state=tk.DISABLED)

    def add_new_topics(self):
        new_topics = self.select_topics()
        for new_topic in new_topics:
            if new_topic not in self.topics:
                self.topics.append(new_topic)
                self.create_tab(new_topic)
                threading.Thread(target=self.subscribe_to_topic, args=(new_topic,)).start()
            else:
                messagebox.showinfo("Info", f"Ya está suscrito a este tópico: {new_topic}")

    def send_message(self):
        message = self.input_entry.get()
        selected_tab = self.tab_control.tab(self.tab_control.select(), "text")
        if message:
            if not self.check_connection():
                self.show_connection_error()
                return
            threading.Thread(target=self._send_message, args=(selected_tab, message)).start()

    def _send_message(self, topic, message):
        try:
            self.stub.Publish(message_broker_pb2.PublishRequest(topic=topic, message=message))
            self.root.after(0, self.input_entry.delete, 0, tk.END)
        except grpc.RpcError:
            self.root.after(0, self.show_connection_error)

    def check_connection(self):
        try:
            self.stub.GetTopics(message_broker_pb2.Empty())
            return True
        except grpc.RpcError:
            return False

    def on_closing(self):
        self.root.quit()
        os._exit(0)

def main():
    root = tk.Tk()
    app = ChatClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
