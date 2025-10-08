# ERNI Gruppe Building Agents - Adaptation Documentation

## Overview

This document describes the adaptation of the OpenAI Customer Service Agents Demo for **ERNI Gruppe**, a leading Swiss timber construction company. The original airline customer service system has been transformed into a building project consultation and support system.

## Company Background

**ERNI Gruppe** is a Swiss construction company specializing in timber (wood) construction, based in Schongau, Luzern, Switzerland.

### Key Information:
- **Founded:** 1989
- **Employees:** 105 employees + 21 apprentices
- **Facility:** 14,000 m² production area
- **Certifications:** Minergie Partner, Holzbau Plus

### Services:
1. **Planung (Planning)** - Architecture and project planning
2. **Holzbau (Timber Construction)** - Wood construction and fabrication
3. **Spenglerei (Roofing/Sheet Metal)** - Roofing and waterproofing
4. **Ausbau (Interior Finishing)** - Interior work and carpentry
5. **Realisation** - General/Total contracting
6. **Agrar (Agricultural)** - Agricultural building construction

### Target Customers:
- Private homeowners
- Architects and engineers
- Agricultural businesses

## Architecture Changes

### Backend (Python)

#### 1. Context Model
**Original:** `AirlineAgentContext`
```python
class AirlineAgentContext(BaseModel):
    passenger_name: str | None = None
    confirmation_number: str | None = None
    seat_number: str | None = None
    flight_number: str | None = None
    account_number: str | None = None
```

**New:** `BuildingProjectContext`
```python
class BuildingProjectContext(BaseModel):
    customer_name: str | None = None
    customer_email: str | None = None
    customer_phone: str | None = None
    project_number: str | None = None
    project_type: str | None = None  # "Einfamilienhaus", "Mehrfamilienhaus", "Agrar"
    construction_type: str | None = None  # "Holzbau", "Systembau"
    area_sqm: float | None = None
    location: str | None = None
    budget_chf: float | None = None
    preferred_start_date: str | None = None
    consultation_booked: bool = False
    specialist_assigned: str | None = None
    inquiry_id: str | None = None
```

#### 2. Agents Mapping

| Original Agent | New Agent | Purpose |
|----------------|-----------|---------|
| Triage Agent | Triage Agent | Routes customer requests (adapted instructions) |
| FAQ Agent | FAQ Agent | Answers building/construction questions |
| Seat Booking Agent | **Cost Estimation Agent** | Provides preliminary project cost estimates |
| Flight Status Agent | **Project Status Agent** | Checks status of ongoing projects |
| Cancellation Agent | **Appointment Booking Agent** | Books consultations with specialists |
| *(new)* | **Project Information Agent** | Explains ERNI's services and processes |

#### 3. Tools (Functions)

**Removed:**
- `update_seat` - Seat booking
- `flight_status_tool` - Flight status lookup
- `display_seat_map` - Interactive seat map
- `cancel_flight` - Flight cancellation
- `baggage_tool` - Baggage information

**Added:**
- `faq_lookup_building` - Building/construction FAQ
- `estimate_project_cost` - Preliminary cost estimation
- `check_specialist_availability` - Check specialist calendars
- `book_consultation` - Book appointments
- `get_project_status` - Get project status updates

#### 4. Guardrails

**Updated:**
- **Relevance Guardrail:** Changed from airline topics to building/construction topics
- **Jailbreak Guardrail:** Unchanged (security)

### Frontend (TypeScript/React)

#### 1. Branding
- **Color Scheme:** Changed from blue (#0066FF) to ERNI brown (#928472)
- **Company Name:** "Airline Co." → "ERNI Gruppe"
- **Headers:** "Customer View" → "ERNI Gruppe - Customer Chat"

#### 2. Components Modified

**chat.tsx:**
- Removed SeatMap component integration
- Updated color scheme to ERNI brown
- Simplified message handling (no special UI triggers)

**agent-panel.tsx:**
- Updated context interface for building projects
- Changed branding colors

**conversation-context.tsx:**
- Updated context fields to match `BuildingProjectContext`
- Fixed value rendering for boolean and numeric types

**agents-list.tsx:**
- Updated active agent highlighting color

**guardrails.tsx:**
- Updated relevance description

**runner-output.tsx:**
- Updated icon colors

#### 3. Removed Components
- `seat-map.tsx` - No longer needed for building projects

## Agent Instructions

All agents use bilingual instructions (German/English) to serve ERNI's Swiss customer base.

### Example: Cost Estimation Agent

```python
def cost_estimation_instructions(run_context, agent):
    return f"""
    You are a Cost Estimation Agent for ERNI Gruppe.
    
    Follow this procedure:
    1. Ask about project type (Einfamilienhaus, Mehrfamilienhaus, Agrar, Renovation)
    2. Ask for area in square meters (m²)
    3. Ask about construction type (Holzbau/timber or Systembau/system)
    4. Use estimate_project_cost tool
    5. Emphasize this is preliminary
    6. Offer consultation booking
    """
```

## Sample Dialogues

### Scenario 1: New Customer Inquiry
```
Customer: "Hello, I want to build a wooden house"
Triage: "Welcome to ERNI Gruppe! I'll help you with building information. 
         Do you have a project already or starting from scratch?"
Customer: "Starting from scratch"
→ Handoff to Project Information Agent
Project Info: "Great! We offer full service from planning to completion. 
               What type of house interests you?"
Customer: "Single-family house, about 150 m²"
→ Handoff to Cost Estimation Agent
Cost Est: "For a 150 m² single-family timber house, estimated cost is 
           CHF 450,000-600,000. Would you like to book a consultation?"
```

### Scenario 2: Project Status Check
```
Customer: "What's the status of project #2024-156?"
Triage: "I'll check your project status"
→ Handoff to Project Status Agent
Status: "Project #2024-156 (Single-family house, Muri):
         - Current stage: Production
         - Progress: 75%
         - Planned assembly: May 15-19, 2025
         - Project manager: Tobias Wili"
```

### Scenario 3: FAQ
```
Customer: "Why is wood better than other materials?"
→ FAQ Agent
FAQ: "🌲 Why Wood?
      ✓ Ecological and renewable
      ✓ Grows in Swiss forests
      ✓ Excellent thermal insulation
      ✓ Healthy indoor climate
      ✓ CO2-neutral
      ✓ Fast assembly
      ERNI is a certified Minergie partner."
```

## Testing

### Test Scenarios
1. ✅ General information request
2. ✅ Cost estimation for different project types
3. ✅ Consultation booking
4. ✅ Project status inquiry
5. ✅ FAQ about materials and processes
6. ✅ Guardrail testing (irrelevant queries)

### Running Tests
```bash
# Start backend
cd python-backend
source .venv/bin/activate
uvicorn api:app --reload --port 8000

# Start frontend
cd ui
npm run dev:next
```

## Future Enhancements

### Phase 1 (Completed)
- ✅ Basic agent system
- ✅ FAQ functionality
- ✅ Cost estimation
- ✅ Appointment booking

### Phase 2 (Recommended)
- [ ] Integration with ERNI's CRM/ERP system
- [ ] Real project status from database
- [ ] Calendar integration for appointments
- [ ] Email/SMS notifications
- [ ] Multi-language support (DE/EN/FR/IT)

### Phase 3 (Future)
- [ ] Document upload and analysis
- [ ] 3D visualization integration
- [ ] Mobile app
- [ ] Voice interface
- [ ] Analytics dashboard

## Technical Notes

### Dependencies
No new dependencies required. The adaptation uses the same tech stack:
- Python: FastAPI, OpenAI Agents SDK, Pydantic
- Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS

### Configuration
Environment variables remain the same:
```bash
OPENAI_API_KEY=your_key_here
```

### Deployment Considerations
- Backend: Deploy on cloud platform (AWS, Azure, GCP)
- Frontend: Deploy on Vercel or similar
- Database: Add PostgreSQL/MySQL for production
- Cache: Add Redis for session management

## Contact & Support

For questions about this adaptation:
- Original Demo: OpenAI Customer Service Agents Demo
- Adapted for: ERNI Gruppe (https://www.erni-gruppe.ch/)
- Adaptation Date: January 2025

## License

This adaptation maintains the original project's license terms.

