FROM python:3.11-slim

WORKDIR /app

# install deps first so this layer is cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# create mount points for the shared frontend data volumes
RUN mkdir -p /app/frontend/data /app/frontend/faq /app/frontend/policyandguidelines

# copy the rest of the project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
