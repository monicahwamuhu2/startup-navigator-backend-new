from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import time
from datetime import datetime
from typing import Optional, List

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug: Print to see if key is loaded
print(f"GROQ_API_KEY loaded: {'Yes' if os.getenv('GROQ_API_KEY') else 'No'}")
print(f"Key starts with: {os.getenv('GROQ_API_KEY', 'NOT_FOUND')[:10]}...")

# Initialize FastAPI app
app = FastAPI(
    title="Kenya Startup Navigator API",
    description="AI-powered guidance for Kenya's startup ecosystem",
    version="1.0.0"
)

# CORS middleware - Allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kenya-startup-navigator-frontend-ruddy.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    startup_profile: Optional[dict] = None
    context: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    processing_time: float
    sources: List[str]
    suggested_follow_ups: List[str]
    timestamp: str

# Health checks
@app.get("/")
async def root():
    return {
        "message": "🚀 Kenya Startup Navigator API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/api/v1/query"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Kenya Startup Navigator API"
    }

# Main query endpoint
@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    start_time = time.time()
    
    try:
        # Get API key from environment
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="GROQ_API_KEY environment variable not set"
            )
        
        # Enhanced system prompt for Kenya startup ecosystem
        system_prompt = """You are KenyaStartup AI, an expert advisor on Kenya's startup ecosystem with deep knowledge of:

🏦 FUNDING LANDSCAPE:
- Major VCs: TLcom Capital (Series A/B, $5-15M), Novastar Ventures (fintech, $2-10M), GreenTec Capital (impact, $1-5M), 4DX Ventures (early stage, $250K-2M)
- Angel Networks: Nairobi Angel Network, Lagos Angel Network (active in Kenya)
- Government: KIICO, Youth Enterprise Fund, Women Enterprise Fund
- Development Finance: IFC, World Bank, AfDB, FMO, DEG

🚀 STARTUP ECOSYSTEM:
- Accelerators: iHub (tech hub), MEST Africa (12-month), Antler Kenya (pre-seed), Founder Institute, Strathmore iLabAfrica
- Co-working: iHub (Ngong Road), NaiLab (Kilimani), GrowthHub Africa, The Foundry
- Universities: University of Nairobi C4DLab, Strathmore Business School

📋 REGULATORY:
- Business Registration: eCitizen platform, KRA PIN, business permits
- Banking: CBK sandbox for fintech
- Technology: Communications Authority of Kenya
- Tax: KRA - 30% corporate tax, 16% VAT

🎯 MARKET CONTEXT:
- Population: 54M+, 65% under 35
- Mobile: 95%+ penetration, 45M+ mobile money users
- Internet: 28M+ users, growing 8% annually

Provide specific, actionable advice with:
1. Concrete next steps with timelines
2. Specific contact information when relevant
3. Realistic costs and requirements
4. Kenyan regulatory context
5. Clear structure with headers and bullet points"""

        # Prepare Groq API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Build context-aware prompt
        user_prompt = request.question
        if request.context:
            user_prompt += f"\n\nAdditional context: {request.context}"
        
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        # Make API call to Groq
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 401:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid Groq API key. Please check your GROQ_API_KEY."
                )
            elif response.status_code == 429:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again in a moment."
                )
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Groq API error: {response.status_code} - {response.text}"
                )
            
            data = response.json()
            
            # Extract response content
            if "choices" in data and data["choices"]:
                content = data["choices"][0]["message"]["content"]
            else:
                content = "I apologize, but I couldn't generate a response. Please try again."
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Generate follow-up questions
            follow_ups = generate_follow_ups(request.question)
            
            # Calculate confidence based on response quality
            confidence = calculate_confidence(content, request.question)
            
            # Generate sources
            sources = generate_sources(content)
            
            return QueryResponse(
                answer=content,
                confidence=confidence,
                processing_time=round(processing_time, 2),
                sources=sources,
                suggested_follow_ups=follow_ups,
                timestamp=datetime.now().isoformat()
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing query: {str(e)}"
        )

def generate_follow_ups(question: str) -> List[str]:
    """Generate relevant follow-up questions based on the query"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["funding", "invest", "money", "capital", "raise"]):
        return [
            "What documents do I need to prepare for investor meetings?",
            "How long does the fundraising process typically take in Kenya?",
            "What valuation should I expect at my current stage?"
        ]
    elif any(word in question_lower for word in ["legal", "register", "compliance", "law"]):
        return [
            "What are the ongoing compliance requirements after incorporation?",
            "How much should I budget for legal and regulatory costs?",
            "Which law firms in Kenya specialize in startups?"
        ]
    elif any(word in question_lower for word in ["accelerator", "incubator", "program"]):
        return [
            "What are the application requirements for top accelerators?",
            "When are the next application deadlines?",
            "How do I prepare for accelerator interviews?"
        ]
    elif any(word in question_lower for word in ["market", "customer", "competition"]):
        return [
            "How do I conduct effective market research in Kenya?",
            "What are the key customer acquisition channels here?",
            "How should I price my product for the Kenyan market?"
        ]
    else:
        return [
            "How do I get started in Kenya's startup ecosystem?",
            "What funding options are available for early-stage startups?",
            "Which accelerators should I consider applying to in Nairobi?"
        ]

def calculate_confidence(content: str, question: str) -> float:
    """Calculate confidence score based on response quality"""
    if not content:
        return 0.0
    
    score = 0.0
    
    # Length factor
    length_score = min(len(content) / 1000, 1.0) * 0.3
    score += length_score
    
    # Kenya-specific content
    kenya_terms = [
        'kenya', 'kenyan', 'nairobi', 'mombasa', 'kra', 'cbk', 'ihub',
        'tlcom', 'novastar', 'mest', 'antler', 'shilling', 'east africa',
        'kiico', 'ecitizen'
    ]
    kenya_mentions = sum(1 for term in kenya_terms if term.lower() in content.lower())
    kenya_score = min(kenya_mentions / 5, 1.0) * 0.4
    score += kenya_score
    
    # Structure indicators
    structure_indicators = ["##", "**", "###", "- ", "1.", "2.", "3."]
    structure_count = sum(1 for indicator in structure_indicators if indicator in content)
    structure_score = min(structure_count / 5, 1.0) * 0.2
    score += structure_score
    
    # Specificity (numbers, contacts, etc.)
    if any(char.isdigit() for char in content):
        score += 0.1
    
    return min(score, 1.0)

def generate_sources(content: str) -> List[str]:
    """Generate relevant sources based on content"""
    sources = ["Kenya Startup Ecosystem Database"]
    
    # Check for mentions of specific organizations
    if "tlcom" in content.lower():
        sources.append("TLcom Capital")
    if "novastar" in content.lower():
        sources.append("Novastar Ventures")
    if "ihub" in content.lower():
        sources.append("iHub Nairobi")
    if "mest" in content.lower():
        sources.append("MEST Africa")
    if any(term in content.lower() for term in ["cbk", "central bank"]):
        sources.append("Central Bank of Kenya")
    if "kra" in content.lower():
        sources.append("Kenya Revenue Authority")
    
    # Add AI source
    sources.append("Groq AI Analysis")
    
    return sources[:4]  # Limit to 4 sources

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)