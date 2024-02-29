from aws_cdk import (
    aws_apigateway as apigw,
    CfnOutput
)


class ApiGatewayStack:

    def __init__(self, stack, lambda_stack) -> None:

        # Obtener el valor del ambiente del contexto
        env = stack.node.try_get_context('env')

        # Define the API Gateway and connect it to the Lambda functions
        api = apigw.RestApi(
            stack, "user-api",
            rest_api_name="User Service",
            description="This service serves users."
        )

        # Define API Gateway resources and methods
        user_api = api.root.add_resource("users")
        user_api.add_method("POST", apigw.LambdaIntegration(lambda_stack.user_register_lambda))
        user_api.add_method("GET", apigw.LambdaIntegration(lambda_stack.user_search_lambda))
        user_api.add_method("PUT", apigw.LambdaIntegration(lambda_stack.modify_user_lambda))
        user_api.add_method("DELETE", apigw.LambdaIntegration(lambda_stack.delete_user_lambda))

        # Define the API Gateway for image upload
        # image_api = api.root.add_resource("images")
        # image_api.add_method("POST", apigw.LambdaIntegration(post_image_lambda))

        # Create a deployment of the API
        api_deployment = apigw.Deployment(stack, "api-deployment", api=api)

        # Define the stage using the deployment
        api_stage = apigw.Stage(stack, f"{env}-stage",
                                deployment=api_deployment,
                                stage_name=env
                                )

        # Asocia el stage al recurso de API
        api.deployment_stage = api_stage

        # Outputs
        CfnOutput(stack, "HTTP API URL", value=api.url_for_path('/'))  # Cambia aquí a la ruta que desees
