from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda
    # ------------------- SNS & SQS -----------------------------
    # Duration,
    # aws_iam as iam,
    # aws_sqs as sqs,
    # aws_sns as sns,
    # aws_sns_subscriptions as subs,
    # ----------------------------------------------------------
)


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ------------------- SNS & SQS -----------------------------
        # queue = sqs.Queue(
        #     self, "CdkWorkshopQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "CdkWorkshopTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
        # ----------------------------------------------------------

        my_lambda = _lambda.Function(
                    self, 'hello_handler',
                    runtime=_lambda.Runtime.PYTHON_3_11,
                    code=_lambda.Code.from_asset('lambda'),
                    handler='hello.handler')

