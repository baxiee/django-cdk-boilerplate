FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY backend ${LAMBDA_TASK_ROOT}
COPY lambda.py ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

CMD [ "lambda.handler" ]
