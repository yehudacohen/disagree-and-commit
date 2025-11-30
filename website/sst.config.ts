/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "disagree-and-commit",
      removal: input?.stage === "production" ? "retain" : "remove",
      protect: ["production"].includes(input?.stage),
      home: "aws",
    };
  },
  async run() {
    const githubRepo = "yehudacohen/disagree-and-commit";

    // OIDC provider for GitHub Actions
    const oidcProvider = new aws.iam.OpenIdConnectProvider("GitHubOIDC", {
      url: "https://token.actions.githubusercontent.com",
      clientIdLists: ["sts.amazonaws.com"],
      thumbprintLists: ["ffffffffffffffffffffffffffffffffffffffff"],
    });

    // IAM role for GitHub Actions to assume
    const deployRole = new aws.iam.Role("GitHubActionsDeployRole", {
      assumeRolePolicy: oidcProvider.arn.apply((arn) =>
        JSON.stringify({
          Version: "2012-10-17",
          Statement: [
            {
              Effect: "Allow",
              Principal: { Federated: arn },
              Action: "sts:AssumeRoleWithWebIdentity",
              Condition: {
                StringEquals: {
                  "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                },
                StringLike: {
                  "token.actions.githubusercontent.com:sub": `repo:${githubRepo}:*`,
                },
              },
            },
          ],
        })
      ),
    });

    // Attach AdministratorAccess for SST deployments
    new aws.iam.RolePolicyAttachment("GitHubActionsDeployPolicy", {
      role: deployRole.name,
      policyArn: "arn:aws:iam::aws:policy/AdministratorAccess",
    });

    new sst.aws.StaticSite("DisagreeAndCommitSite", {
      build: {
        command: "npm run build",
        output: "dist",
      },
    });

    return {
      GitHubActionsRoleArn: deployRole.arn,
    };
  },
});
