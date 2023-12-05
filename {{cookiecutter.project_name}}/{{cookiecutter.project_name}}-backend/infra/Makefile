SHELL=/bin/bash -euo pipefail

CDK_CFG=--profile {{cookiecutter.project_name}} --require-approval never -c env=prod -c project_name={{cookiecutter.project_name}} -c assets-ecr-repository-name={{cookiecutter.project_name}}-prod-prereq-backend-repository

.PHONY: venv-install deploy-backend destroy-backend migrate


venv-install:
	if [ ! -d "venv" ]; then python3.10 -m venv venv; fi
	venv/bin/pip3.10 install -r requirements.txt
	source venv/bin/activate


deploy-backend: venv-install
	cp -r ../src/backend ./lambda
	cat ./lambda/requirements-aws.txt ../requirements.txt > ./lambda/requirements.txt
	-cdk deploy -a "venv/bin/python3 app_backend.py" ${CDK_CFG} -c stack_name="backend"
	rm -rf ./lambda/backend ./lambda/requirements.txt


destroy-backend: venv-install
	cdk destroy -a "venv/bin/python3 app_backend.py" ${CDK_CFG} -c stack_name="backend"


migrate:
	aws lambda invoke --profile {{cookiecutter.project_name}} --function-name {{cookiecutter.project_name}}-prod-backend-lambda --cli-binary-format raw-in-base64-out --payload '{"manage":"migrate"}' response.json
	cat response.json
	rm -rf response.json
