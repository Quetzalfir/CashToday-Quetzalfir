from aws_cdk import (
    aws_opensearchservice as opensearch,
    aws_kinesisfirehose as firehose,
    aws_iam as iam,
    aws_s3 as s3
)


class ElasticsearchStack:

    def __init__(self, stack, database_stack) -> None:

        # Obtener el valor del ambiente del contexto
        env = stack.node.try_get_context('env')

        # bucket de S3 para Firehose Backup
        backup_bucket = s3.Bucket(stack, f"FirehoseBackupBucket-{env.capitalize()}", versioned=True)

        # dominio de Elasticsearch
        self.domain = opensearch.Domain(
            stack, f"CashTodayStack-DOMAIN-{env.capitalize()}",
            version=opensearch.EngineVersion.OPENSEARCH_1_0,  # Especifica la versión de Elasticsearch
            capacity={
                "master_nodes": 3,
                "data_nodes": 6,
            },
            ebs={
                "volume_size": 10,
            },
            zone_awareness={
                "enabled": True,
                "availability_zone_count": 2,
            },
            enforce_https=True,
            node_to_node_encryption=True,
            fine_grained_access_control={
               "master_user_name": "master-user",
            },
            encryption_at_rest={
                "enabled": True,
            },
        )

        # rol de IAM para Kinesis Data Firehose con la política necesaria para interactuar con DynamoDB y Elasticsearch
        firehose_role = iam.Role(
            stack, "FirehoseToElasticsearchRole",
            assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
            )

        firehose_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:ListStreams"
            ],
            resources=[database_stack.table.table_stream_arn],
        ))

        firehose_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "opensearch:ESHttpPost",
                "opensearch:ESHttpPut",
                "opensearch:ESHttpGet"
            ],
            resources=[self.domain.domain_arn + "/*"],
        ))

        # Configuración de S3 para Firehose
        s3_config = firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
            bucket_arn=backup_bucket.bucket_arn,
            buffering_hints=firehose.CfnDeliveryStream.BufferingHintsProperty(
                interval_in_seconds=300,
                size_in_m_bs=5
            ),
            compression_format="UNCOMPRESSED",
            role_arn=firehose_role.role_arn
        )

        # Kinesis Data Firehose Delivery Stream
        self.firehose_delivery_stream = firehose.CfnDeliveryStream(
            stack, f"CashTodayStack-Firehose-{env.capitalize()}",
            delivery_stream_type="KinesisStreamAsSource",
            elasticsearch_destination_configuration=firehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty(
                domain_arn=self.domain.domain_arn,
                index_name="clients",
                role_arn=firehose_role.role_arn,
                s3_configuration=s3_config
            ),
            kinesis_stream_source_configuration={
                "kinesisStreamArn": database_stack.table.table_stream_arn,
                "roleArn": firehose_role.role_arn
            }
            )

        backup_bucket.grant_write(firehose_role)

