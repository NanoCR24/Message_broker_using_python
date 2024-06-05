# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import message_broker_pb2 as message__broker__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in message_broker_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class MessageBrokerStub(object):
    """Servicio del Broker de Mensajes
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Publish = channel.unary_unary(
                '/message_broker.MessageBroker/Publish',
                request_serializer=message__broker__pb2.PublishRequest.SerializeToString,
                response_deserializer=message__broker__pb2.PublishResponse.FromString,
                _registered_method=True)
        self.Subscribe = channel.unary_stream(
                '/message_broker.MessageBroker/Subscribe',
                request_serializer=message__broker__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=message__broker__pb2.Message.FromString,
                _registered_method=True)
        self.GetTopics = channel.unary_unary(
                '/message_broker.MessageBroker/GetTopics',
                request_serializer=message__broker__pb2.Empty.SerializeToString,
                response_deserializer=message__broker__pb2.TopicsResponse.FromString,
                _registered_method=True)


class MessageBrokerServicer(object):
    """Servicio del Broker de Mensajes
    """

    def Publish(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTopics(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MessageBrokerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Publish': grpc.unary_unary_rpc_method_handler(
                    servicer.Publish,
                    request_deserializer=message__broker__pb2.PublishRequest.FromString,
                    response_serializer=message__broker__pb2.PublishResponse.SerializeToString,
            ),
            'Subscribe': grpc.unary_stream_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=message__broker__pb2.SubscribeRequest.FromString,
                    response_serializer=message__broker__pb2.Message.SerializeToString,
            ),
            'GetTopics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTopics,
                    request_deserializer=message__broker__pb2.Empty.FromString,
                    response_serializer=message__broker__pb2.TopicsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'message_broker.MessageBroker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('message_broker.MessageBroker', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MessageBroker(object):
    """Servicio del Broker de Mensajes
    """

    @staticmethod
    def Publish(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/message_broker.MessageBroker/Publish',
            message__broker__pb2.PublishRequest.SerializeToString,
            message__broker__pb2.PublishResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/message_broker.MessageBroker/Subscribe',
            message__broker__pb2.SubscribeRequest.SerializeToString,
            message__broker__pb2.Message.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTopics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/message_broker.MessageBroker/GetTopics',
            message__broker__pb2.Empty.SerializeToString,
            message__broker__pb2.TopicsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
