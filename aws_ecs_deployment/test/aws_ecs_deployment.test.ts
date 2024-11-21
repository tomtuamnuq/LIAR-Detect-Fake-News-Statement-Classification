import { Template } from "aws-cdk-lib/assertions";
import { FargateSpotStack } from "../lib/aws_ecs_deployment-stack";
import { App } from "aws-cdk-lib";

let app: App;
let stack: FargateSpotStack;
let template: Template;

beforeAll(() => {
  // Initialize the CDK app and stack once for all tests
  app = new App();
  stack = new FargateSpotStack(app, "MyTestStack", {
    portNumber: 5042,
    containerImageURI: "public.ecr.aws/t8q6o3x2/tuamnuq-liar-detect-app:latest",
  });
  template = Template.fromStack(stack); // Extract the template for assertions
});

test("ECS Cluster Created", () => {
  // Check that an ECS Cluster resource is created
  template.resourceCountIs("AWS::ECS::Cluster", 1);
});

test("Fargate Service with Public IP and Spot Capacity Created", () => {
  // Check that a Fargate Service is created with Spot capacity provider
  template.hasResourceProperties("AWS::ECS::Service", {
    CapacityProviderStrategy: [
      {
        CapacityProvider: "FARGATE_SPOT",
        Weight: 1,
      },
    ],
    NetworkConfiguration: {
      AwsvpcConfiguration: {
        AssignPublicIp: "ENABLED",
      },
    },
    DesiredCount: 1,
  });
});

test("Security Group Allows Ingress on Specified Port", () => {
  // Check that the Security Group allows ingress on the specified port
  template.hasResourceProperties("AWS::EC2::SecurityGroup", {
    SecurityGroupIngress: [
      {
        IpProtocol: "tcp",
        FromPort: 5042,
        ToPort: 5042,
        CidrIp: "0.0.0.0/0",
      },
    ],
  });
});
