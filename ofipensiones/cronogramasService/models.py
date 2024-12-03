from mongoengine import Document, fields, EmbeddedDocument

class DetalleCobroCurso(EmbeddedDocument):
    id = fields.ObjectIdField(primary_key=True, editable=False)
    mes = fields.StringField(max_length=20)
    valor = fields.DecimalField(max_digits=10, decimal_places=2)
    fechaCausacion = fields.DateTimeField()
    fechaLimite = fields.DateTimeField()
    frecuencia = fields.StringField(max_length=50)

    def __str__(self):
        return f"Cobro de {self.mes} - Valor {self.valor}"

class CronogramaBase(Document):
    institucionId = fields.ObjectIdField(editable=False)
    nombreInstitucion = fields.StringField(max_length=100)
    cursoId = fields.ObjectIdField(editable=False)
    grado = fields.StringField(max_length=50)

    codigo = fields.StringField(max_length=50)
    nombre = fields.StringField(max_length=100)
    detalle_cobro = fields.ListField(fields.EmbeddedDocumentField(DetalleCobroCurso))

    def __str__(self):
        return self.nombre