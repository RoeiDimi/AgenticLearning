from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct

class McpServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function definition (code to be implemented later)
        mcp_lambda = _lambda.Function(
            self, "McpLambdaHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda/lambda_package.zip"),
            memory_size=512,
            timeout=Duration.seconds(30),
            environment={
                # Add environment variables if needed
            }
        )

        # API Gateway REST API (explicit resources and methods)
        api = apigateway.RestApi(
            self, "McpApiGateway",
            rest_api_name="McpApiGateway",
            description="API Gateway for MCP Lambda integration",
            deploy_options=apigateway.StageOptions(stage_name="prod")
        )

        # /mcp resource
        mcp_resource = api.root.add_resource("mcp")
        mcp_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(mcp_lambda),
            api_key_required=False
        )
