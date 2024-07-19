# Start with the AWS Lambda Python 3.12 image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt .

# Install Python packages
RUN pip install -r requirements.txt

# Copy the 'src' directory itself, not just its contents
COPY src ${LAMBDA_TASK_ROOT}/src

# Set the entry point for the AWS Lambda function
CMD ["src/main.handler"]