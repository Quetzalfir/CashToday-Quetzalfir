from aws_cdk import aws_dynamodb as ddb


class DatabaseStack:
    def __init__(self, stack, env_props):

        # Define the DynamoDB table
        self.table = ddb.Table(
            stack, 'Clients',
            table_name=env_props['dynamodb_table_name'],
            partition_key={'name': 'numeroIdentificacion', 'type': ddb.AttributeType.STRING}
        )

        # Agregar los índices secundarios globales
        self.table.add_global_secondary_index(
            index_name="codigoPostal-index",
            partition_key=ddb.Attribute(name="codigoPostal", type=ddb.AttributeType.STRING)
        )
        self.table.add_global_secondary_index(
            index_name="pais-index",
            partition_key=ddb.Attribute(name="pais", type=ddb.AttributeType.STRING)
        )
        self.table.add_global_secondary_index(
            index_name="ciudad-index",
            partition_key=ddb.Attribute(name="ciudad", type=ddb.AttributeType.STRING)
        )
        self.table.add_global_secondary_index(
            index_name="nombreApellido-index",
            partition_key=ddb.Attribute(name="nombreApellido", type=ddb.AttributeType.STRING)
        )
