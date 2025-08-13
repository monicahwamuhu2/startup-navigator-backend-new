# Kenya Startup Navigator - Backend API

**Live Application:** [https://kenya-startup-navigator-frontend-ruddy.vercel.app/](https://kenya-startup-navigator-frontend-ruddy.vercel.app/)


## Overview

The Kenya Startup Navigator Backend is a FastAPI-powered REST API that provides AI-driven insights and guidance for entrepreneurs navigating Kenya's startup ecosystem. Built with Groq's LLaMA 3 70B model, it offers specialized knowledge about funding opportunities, regulatory requirements, accelerators, and market dynamics specific to Kenya and East Africa.

## Features

- **AI-Powered Intelligence**: Kenya-specific startup ecosystem knowledge powered by Groq AI
- **Real-time Responses**: Sub-2-second response times with confidence scoring
- **Comprehensive Database**: Information on VCs, accelerators, regulatory requirements, and market data
- **RESTful API**: Clean endpoints with automatic documentation
- **CORS Enabled**: Ready for frontend integration
- **Production Ready**: Deployed with proper error handling and monitoring

## API Endpoints

- **Backend API**: https://startup-navigator-backend-new.onrender.com
- **API Documentation**: https://startup-navigator-backend-new.onrender.com/docs
- **Health Check**: https://startup-navigator-backend-new.onrender.com/health

## Technology Stack

- **Framework**: FastAPI 0.115.6
- **AI Model**: Groq LLaMA 3 70B
- **HTTP Client**: httpx
- **Validation**: Pydantic v2
- **Server**: Uvicorn
- **Deployment**: Render

## Prerequisites

- Python 3.8 or higher
- Groq API key (free tier available at https://console.groq.com/keys)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/kenya-startup-navigator-backend.git
cd kenya-startup-navigator-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Usage

### Basic Query

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I register my startup in Kenya?"}'
```

### Query with Context

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which VCs should I approach for fintech funding?",
    "context": "I have an MVP with 1000 users and $10K MRR"
  }'
```

## Deployment

### Render Deployment

The application is configured for deployment on Render:

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variable:
   - **Key**: `GROQ_API_KEY`
   - **Value**: Your Groq API key

### Alternative Deployment Options

#### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Railway

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment configuration
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore patterns
└── README.md          # Project documentation
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq AI service | Yes |
| `ENVIRONMENT` | Development/production environment | No |
| `DEBUG` | Enable debug mode | No |

## API Response Format

```json
{
  "answer": "Detailed AI response about Kenya startup ecosystem...",
  "confidence": 0.92,
  "processing_time": 2.3,
  "sources": ["Kenya Startup Ecosystem Database", "TLcom Capital"],
  "suggested_follow_ups": [
    "What documents do I need for investor meetings?",
    "How long does fundraising typically take?"
  ],
  "timestamp": "2025-01-21T12:00:00.000Z"
}
```

## Knowledge Base

The AI system has specialized knowledge about:

### Funding Landscape
- Major VCs: TLcom Capital, Novastar Ventures, GreenTec Capital
- Angel Networks: Nairobi Angel Network
- Government Programs: KIICO, Youth Enterprise Fund
- Development Finance: IFC, World Bank, AfDB

### Startup Ecosystem
- Accelerators: iHub, MEST Africa, Antler Kenya
- Co-working Spaces: NaiLab, GrowthHub Africa
- Universities: University of Nairobi C4DLab, Strathmore iLabAfrica

### Regulatory Environment
- Business Registration: eCitizen platform
- Tax Requirements: KRA (30% corporate tax, 16% VAT)
- Banking: CBK fintech sandbox
- Intellectual Property: KIPI

### Market Intelligence
- Population: 54M+ (65% under 35)
- Mobile Penetration: 95%
- Mobile Money: 45M+ users
- Internet Users: 28M+ (growing 8% annually)

## Testing

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Interactive Testing

Visit http://127.0.0.1:8000/docs for the interactive API documentation where you can test all endpoints directly in your browser.

## Error Handling

The API includes comprehensive error handling:

- **400**: Bad Request (invalid input)
- **429**: Rate limit exceeded
- **500**: Server error (AI service issues)

All errors return structured JSON responses with detailed error messages.

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 60 requests per minute per IP address
- Automatic retry logic for transient failures
- Exponential backoff for service unavailability

## Security

- Environment variables for sensitive data
- CORS protection for frontend integration
- Input validation using Pydantic models
- No sensitive information in source code

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the interactive API documentation at `/docs`
- Review error messages for debugging guidance
- Ensure your Groq API key is valid and has credits
- Verify environment variables are properly set
