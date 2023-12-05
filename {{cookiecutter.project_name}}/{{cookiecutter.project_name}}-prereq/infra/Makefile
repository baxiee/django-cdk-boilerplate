SHELL=/bin/bash -euo pipefail

CDK_CFG=--profile {{cookiecutter.project_name}} --require-approval never -c env=prod -c project_name={{cookiecutter.project_name}}
DJANGO_SECRET_KEY := $(shell python3 -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))')

.PHONY: venv-install create-django-secret bootstrap-prereq deploy-prereq destroy-prereq modify-rds remove-s3-ecr


venv-install:
	if [ ! -d "venv" ]; then python3 -m venv venv; fi
	venv/bin/pip3 install -r requirements.txt
	source venv/bin/activate


create-django-secret:
	aws secretsmanager create-secret --profile {{cookiecutter.project_name}} --name {{cookiecutter.project_name}}-prod-credentials --secret-string "{\"DJANGO_SECRET_KEY\":\"${DJANGO_SECRET_KEY}\"}"


bootstrap-prereq: venv-install
	cdk bootstrap -a "venv/bin/python3 app.py" ${CDK_CFG} -c stack_name=prereq


deploy-prereq: venv-install
	cdk deploy -a "venv/bin/python3 app.py" ${CDK_CFG} -c stack_name=prereq


destroy-prereq: venv-install
	cdk destroy -a "venv/bin/python3 app.py" ${CDK_CFG} -c stack_name=prereq


modify-rds:
	aws rds modify-db-instance --profile {{cookiecutter.project_name}} --no-deletion-protection --apply-immediately --db-instance-identifier {{cookiecutter.project_name}}-prod-prereq-rds-instance | jq -r ".DBInstance.DeletionProtection"

remove-s3-ecr:
	aws s3 rm --profile {{cookiecutter.project_name}} s3://{{cookiecutter.project_name}}-prod-prereq-bucket --recursive
	aws s3 rb --profile {{cookiecutter.project_name}} s3://{{cookiecutter.project_name}}-prod-prereq-bucket
	aws ecr delete-repository --profile {{cookiecutter.project_name}} --repository-name {{cookiecutter.project_name}}-prod-prereq-backend-repository --force

