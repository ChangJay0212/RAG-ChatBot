FROM python:3.10-slim

# Set the working directory
WORKDIR /workspace

# Copy necessary files from the root directory to the container
COPY ./chatta_app /workspace
COPY ./requirements.txt /workspace/requirements.txt

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Specify the command to run
CMD bash -c "python3 launcher.py"
