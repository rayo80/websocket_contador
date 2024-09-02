import documents as dc


# class Device:
#     def __init__(self, db):
#         self.estado: int = 0
#         self.db = db
#         self.contadores = self.db["contadores"]
#         self.trackers = self.db["trackers"]
#
#     def aumentar(self, value):
#         self.estado += value
#
#     async def conectar(self, request):
#         params = request.params
#         print('headers', request.headers)
#         print('params', request.params)
#         pk = int(params['id'][0])
#         if pk in range(100):
#
#             if result := await self.contadores.find_one({'id': pk}):
#                 print(result)
#                 self.estado = int(result["estado"])
#             else:
#                 self.estado = int(params['estado'][0])
#                 print("ionseting")
#                 self.contadores.insert_one(
#                     {'id': pk,
#                      'estado': self.estado
#                      },
#                 )
#                 print("insertado")
#         else:
#             raise SystemError("Este contador no es valido")

class Contador:

    def __init__(self):
        # el estado no esta dentro del objeto en db
        self.estado: int = 0
        self.contador = None

    def aumentar(self, value):
        self.estado += value

    async def conectar(self, request):
        params = request.params
        pk = int(params['id'][0])
        if pk in range(100):
            if result := await dc.Contador.find_one(dc.Contador.id == pk):
                print(result)
                self.estado = result.estado
                self.contador = result
            else:
                self.estado = int(params['estado'][0])
                print("insertando")
                contador = dc.Contador(id=pk, estado=self.estado)
                # And can be inserted into the database
                self.contador = contador
                await contador.insert()
                print("insertado")
        else:
            raise SystemError("Este contador no es valido")

    async def set_estado(self, payload):
        number = int(payload.decode('utf8'))
        self.estado += number
        self.contador.estado = self.estado
        self.contador.save()
        return self.estado


