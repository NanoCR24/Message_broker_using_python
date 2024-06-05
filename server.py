from concurrent import futures
import threading
import time
import logging
import queue
from collections import defaultdict

import grpc
import message_broker_pb2
import message_broker_pb2_grpc

MAX_QUEUE_SIZE = 100

# Configuración del logging para escribir solo en archivo
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='server.log', filemode='a')

class MessageBrokerServicer(message_broker_pb2_grpc.MessageBrokerServicer):
    def __init__(self):
        self.topics = {"noticias": queue.Queue(MAX_QUEUE_SIZE), "deportes": queue.Queue(MAX_QUEUE_SIZE), "tecnología": queue.Queue(MAX_QUEUE_SIZE)}
        self.subscribers = {"noticias": [], "deportes": [], "tecnología": []}
        self.locks = {topic: threading.Lock() for topic in self.topics}
        self.clients_by_topic = defaultdict(list)

    def Publish(self, request, context):
        with self.locks[request.topic]:
            if not self.topics[request.topic].full():
                self.topics[request.topic].put((request.message, context.peer()))
                logging.info(f"Mensaje publicado en {request.topic}: {request.message} por {context.peer()}")
                return message_broker_pb2.PublishResponse(success=True)
            else:
                logging.warning(f"Cola llena en {request.topic}. No se pudo publicar el mensaje: {request.message}")
                return message_broker_pb2.PublishResponse(success=False)

    def Subscribe(self, request, context):
        logging.info(f"Cliente {context.peer()} suscrito a {request.topic}")
        subscriber_queue = queue.Queue()

        with self.locks[request.topic]:
            self.subscribers[request.topic].append((context, subscriber_queue))
            self.clients_by_topic[request.topic].append((context, subscriber_queue))

        try:
            while True:
                try:
                    message, sender = subscriber_queue.get(timeout=1)
                    if sender != context.peer():
                        logging.info(f"Enviando mensaje a {context.peer()} desde {sender}: {message}")
                        yield message_broker_pb2.Message(topic=request.topic, message=message, sender=sender)
                except queue.Empty:
                    continue
        finally:
            with self.locks[request.topic]:
                self.subscribers[request.topic] = [(peer, q) for peer, q in self.subscribers[request.topic] if peer != context]
                self.clients_by_topic[request.topic] = [(peer, q) for peer, q in self.clients_by_topic[request.topic] if peer != context]

    def GetTopics(self, request, context):
        logging.info("Lista de temas solicitada")
        return message_broker_pb2.TopicsResponse(topics=list(self.topics.keys()))

def distribute_messages(servicer):
    while True:
        for topic, q in servicer.topics.items():
            if not q.empty():
                message, sender = q.get()
                with servicer.locks[topic]:
                    for context, subscriber_queue in servicer.subscribers[topic]:
                        subscriber_queue.put((message, sender))
        time.sleep(0.1)

def serve():
    logging.info("Servidor gRPC iniciando...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = MessageBrokerServicer()
    message_broker_pb2_grpc.add_MessageBrokerServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:32000')
    server.start()

    distributor_thread = threading.Thread(target=distribute_messages, args=(servicer,))
    distributor_thread.daemon = True
    distributor_thread.start()

    logging.info("Servidor gRPC iniciado en el puerto 32000")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
