# Serverless Framework AWS Python with slack bolt


### Deployment

In order to deploy, you need to run the following command:

```
$ serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying aws-python-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-project-dev (112s)

functions:
  hello: aws-python-project-dev-hello (1.5 kB)
```

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
serverless invoke --function hello
```

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function hello
```

### Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Setup
```
service: myService
plugins:
  - serverless-python-requirements
```


Preload function environment variables into Serverless. Use this plugin if you have variables stored in a .env file that you want loaded into your functions.

Install
```
npm i -D serverless-dotenv-plugin
```

Setup
```
service: myService
plugins:
  - serverless-dotenv-plugin
```

Set env variables in .env
```
OPENAI_API_KEY=''
SLACK_BOT_TOKEN=''
SLACK_SIGNING_SECRET=''
```
