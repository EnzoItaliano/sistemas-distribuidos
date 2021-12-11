# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import service_pb2 as service__pb2


class ControleNotasStub(object):
  """interface de serviço
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AdicionarMatricula = channel.unary_unary(
        '/ControleNotas/AdicionarMatricula',
        request_serializer=service__pb2.MatriculaRequest.SerializeToString,
        response_deserializer=service__pb2.MatriculaResponse.FromString,
        )
    self.AlterarNota = channel.unary_unary(
        '/ControleNotas/AlterarNota',
        request_serializer=service__pb2.MatriculaRequest.SerializeToString,
        response_deserializer=service__pb2.MatriculaResponse.FromString,
        )
    self.AlterarFaltas = channel.unary_unary(
        '/ControleNotas/AlterarFaltas',
        request_serializer=service__pb2.MatriculaRequest.SerializeToString,
        response_deserializer=service__pb2.MatriculaResponse.FromString,
        )
    self.ListarAlunos = channel.unary_unary(
        '/ControleNotas/ListarAlunos',
        request_serializer=service__pb2.ListarAlunosRequest.SerializeToString,
        response_deserializer=service__pb2.ListarAlunosResponse.FromString,
        )
    self.ListarDisciplinasAluno = channel.unary_unary(
        '/ControleNotas/ListarDisciplinasAluno',
        request_serializer=service__pb2.BoletimRequest.SerializeToString,
        response_deserializer=service__pb2.BoletimResponse.FromString,
        )
    self.ListarDisciplinasCurso = channel.unary_unary(
        '/ControleNotas/ListarDisciplinasCurso',
        request_serializer=service__pb2.ListarDisciplinasCursoRequest.SerializeToString,
        response_deserializer=service__pb2.ListarDisciplinasCursoResponse.FromString,
        )


class ControleNotasServicer(object):
  """interface de serviço
  """

  def AdicionarMatricula(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AlterarNota(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AlterarFaltas(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListarAlunos(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListarDisciplinasAluno(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListarDisciplinasCurso(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ControleNotasServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AdicionarMatricula': grpc.unary_unary_rpc_method_handler(
          servicer.AdicionarMatricula,
          request_deserializer=service__pb2.MatriculaRequest.FromString,
          response_serializer=service__pb2.MatriculaResponse.SerializeToString,
      ),
      'AlterarNota': grpc.unary_unary_rpc_method_handler(
          servicer.AlterarNota,
          request_deserializer=service__pb2.MatriculaRequest.FromString,
          response_serializer=service__pb2.MatriculaResponse.SerializeToString,
      ),
      'AlterarFaltas': grpc.unary_unary_rpc_method_handler(
          servicer.AlterarFaltas,
          request_deserializer=service__pb2.MatriculaRequest.FromString,
          response_serializer=service__pb2.MatriculaResponse.SerializeToString,
      ),
      'ListarAlunos': grpc.unary_unary_rpc_method_handler(
          servicer.ListarAlunos,
          request_deserializer=service__pb2.ListarAlunosRequest.FromString,
          response_serializer=service__pb2.ListarAlunosResponse.SerializeToString,
      ),
      'ListarDisciplinasAluno': grpc.unary_unary_rpc_method_handler(
          servicer.ListarDisciplinasAluno,
          request_deserializer=service__pb2.BoletimRequest.FromString,
          response_serializer=service__pb2.BoletimResponse.SerializeToString,
      ),
      'ListarDisciplinasCurso': grpc.unary_unary_rpc_method_handler(
          servicer.ListarDisciplinasCurso,
          request_deserializer=service__pb2.ListarDisciplinasCursoRequest.FromString,
          response_serializer=service__pb2.ListarDisciplinasCursoResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ControleNotas', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))