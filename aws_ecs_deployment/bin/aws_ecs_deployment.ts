#!/usr/bin/env node
import "source-map-support/register";
import { FargateSpotStack } from "../lib/aws_ecs_deployment-stack";
import { App } from "aws-cdk-lib";

const app = new App();
new FargateSpotStack(app, "FargateSpotStack", {
  portNumber: 5042,
  containerImageURI: "public.ecr.aws/t8q6o3x2/tuamnuq-liar-detect-app:latest",
});
