# PDF-DOCX Converter API

A FastAPI-based REST service that converts between PDF and DOCX formats.

## Installation

### Local Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. For Apryse (PDFTron) functionality:
   - Download PDFNetPython3 from [Apryse website](https://www.pdftron.com/documentation/python/get-started/)
   - Follow their installation instructions
   - Set the environment variable `PDFTRON_LICENSE_KEY` with your license key

### Docker Installation

You can also run the application using Docker:

1. Build the Docker image:
   ```
   docker build -t pdf-docx-converter .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 pdf-docx-converter
   ```

## Usage

### Starting the server

Run the following command to start the server locally:

```
python main.py
```

Or use uvicorn directly:

```
python -m uvicorn main:app --reload
```

The server will start at http://localhost:8000

### API Endpoints

- `GET /` - API info
- `POST /convert` - Convert between PDF and DOCX formats with direction parameter
- `POST /convert/apryse` - Convert PDF to DOCX using Apryse/PDFTron library (requires license)

### Converting Files

You can use curl to test the API:

```bash
# PDF to DOCX conversion (default)
curl -X POST -F "file=@/path/to/your/file.pdf" http://localhost:8000/convert --output output.docx

# DOCX to PDF conversion
curl -X POST -F "file=@/path/to/your/file.docx" -F "direction=docx_to_pdf" http://localhost:8000/convert --output output.pdf

# Using the Apryse/PDFTron converter (PDF to DOCX only)
curl -X POST -F "file=@/path/to/your/file.pdf" http://localhost:8000/convert/apryse --output output.docx
```

Or use the interactive Swagger UI by opening http://localhost:8000/docs in your browser.

## API Documentation

After starting the server, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc 