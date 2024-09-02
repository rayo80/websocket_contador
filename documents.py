from beanie import Document, Indexed, init_beanie


class Contador(Document):
    id: int
    estado: int

    class Settings:
        # Establecer el nombre de la colección existente
        name = "contadores"

