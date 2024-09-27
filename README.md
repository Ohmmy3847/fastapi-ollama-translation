# FastAPI Ollama Translation

This repository contains a FastAPI application that uses Ollama to translate text from Chinese to Thai. The application is containerized using Docker for easy deployment and consistency across different environments.

## Prerequisites

- Git
- Docker
- At least 8GB of free RAM (16GB recommended) due to the memory requirements of the language model

## Quick Start Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/fastapi-ollama-translation.git
   cd fastapi-ollama-translation
   ```

2. **Build the Docker Image**

   ```bash
   docker build -t fastapi-ollama-app .
   ```

3. **Run the Docker Container**

   ```bash
   docker run -d -p 8000:8000 --name fastapi-translator fastapi-ollama-app
   ```

4. **Wait for Initialization**

   Check the logs to see when the application is ready:

   ```bash
   docker logs -f fastapi-translator
   ```

   Wait until you see a message indicating that the FastAPI application has started.

5. **Access the Application**

   - Web Interface: Open your web browser and go to `http://localhost:8000`
   - API: Send POST requests to `http://localhost:8000/translate/`

## Detailed Usage Guide

### Web Interface

1. Open `http://localhost:8000` in your web browser.
2. Enter Chinese text in the input field.
3. Click the "Translate" button.
4. View the Thai translation in the output field.

### API Usage

Send a POST request to `http://localhost:8000/translate/` with a JSON payload:

```json
{
  "text": "你好，世界"
}
```

Example using curl:

```bash
curl -X POST "http://localhost:8000/translate/" \
     -H "Content-Type: application/json" \
     -d '{"text":"你好，世界"}'
```

## Development

If you want to contribute or modify the application:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Make your changes to the code.

4. Run the application locally:

   ```bash
   uvicorn main:app --reload
   ```

   Note: This requires Ollama to be installed and running on your local machine.

5. Build and test the Docker image with your changes:

   ```bash
   docker build -t fastapi-ollama-app:dev .
   docker run -d -p 8000:8000 --name fastapi-translator-dev fastapi-ollama-app:dev
   ```

## Troubleshooting

- If the container fails to start, ensure you have allocated enough memory to Docker.
- If you can't access the web interface, check if the container is running:

  ```bash
  docker ps
  ```

- For any issues, check the container logs:

  ```bash
  docker logs fastapi-translator
  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[Specify your license here]

## Support

If you encounter any problems or have questions, please open an issue in this repository.