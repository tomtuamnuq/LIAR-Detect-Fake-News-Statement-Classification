import { Stack, StackProps, CfnOutput } from "aws-cdk-lib";
import { Vpc, SecurityGroup, Peer, Port } from "aws-cdk-lib/aws-ec2";
import {
  Cluster,
  FargateTaskDefinition,
  ContainerImage,
  LogDriver,
  FargateService,
} from "aws-cdk-lib/aws-ecs";
import { Construct } from "constructs";

interface FargateDeploymentProps extends StackProps {
  portNumber: number;
  containerImageURI: string;
}

export class FargateSpotStack extends Stack {
  constructor(scope: Construct, id: string, props: FargateDeploymentProps) {
    super(scope, id, props);

    // Create a VPC for ECS
    const vpc = new Vpc(this, "FargateVpc", {
      maxAzs: 1,
      natGateways: 0,
    });

    // Create an ECS Cluster in the VPC
    const cluster = new Cluster(this, "FargateCluster", {
      vpc,
    });

    // Define the ECS Task Definition
    const taskDefinition = new FargateTaskDefinition(this, "TaskDef", {
      cpu: 256,
      memoryLimitMiB: 512,
    });

    // Add container to the task definition
    const container = taskDefinition.addContainer("AppContainer", {
      image: ContainerImage.fromRegistry(props.containerImageURI),
      logging: LogDriver.awsLogs({ streamPrefix: "FargateAppLogs" }),
    });

    // Map the container's port to the task
    container.addPortMappings({
      containerPort: props.portNumber,
    });

    // Create a security group allowing inbound traffic
    const securityGroup = new SecurityGroup(this, "FargateSG", {
      vpc,
      description: "Allow inbound traffic to the container application",
    });

    securityGroup.addIngressRule(
      Peer.anyIpv4(),
      Port.tcp(props.portNumber),
      "Allow inbound traffic"
    );

    // Create a Fargate Service with Spot Instances
    const service = new FargateService(this, "FargateService", {
      cluster,
      taskDefinition,
      desiredCount: 1,
      capacityProviderStrategies: [
        {
          capacityProvider: "FARGATE_SPOT",
          weight: 1,
        },
      ],
      assignPublicIp: true, // Enable public IP
      securityGroups: [securityGroup],
    });

    // Output the public IP for the task
    new CfnOutput(this, "ServiceTaskPublicIP", {
      value: `Check ECS console to find the public IP of the running task.`,
    });
  }
}
