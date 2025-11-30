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
    new sst.aws.StaticSite("DisagreeAndCommitSite", {
      domain: "disagreeandcommit.chat",
      build: {
        command: "npm run build",
        output: "dist",
      },
    });
  },
});
