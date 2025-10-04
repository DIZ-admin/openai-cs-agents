# ERNI Gruppe Knowledge Base

This directory contains the knowledge base for the FAQ Agent.

## Files

- `erni_knowledge_base.json` - Comprehensive knowledge base about ERNI Gruppe
- `erni_sitemap.json` - Complete website sitemap with all page URLs and descriptions

## Knowledge Base Structure

The knowledge base is organized into the following sections:

### 1. Company Information
- Basic company details (name, location, contact)
- Statistics (employees, apprentices, facility size)
- Opening hours

### 2. Divisions (6 total)
- Planung (Planning)
- Holzbau (Timber Construction)
- Spenglerei (Roofing & Sheet Metal)
- Ausbau (Interior Finishing)
- Realisation (General/Total Contracting)
- Agrar (Agricultural Buildings)

Each division includes:
- Name and description
- Services offered
- Leader name and phone number

### 3. Project Types
- Einfamilienhaus (Single-family houses)
- Mehrfamilienhaus (Multi-family houses)
- Agrar (Agricultural buildings)
- Renovation (Renovations & extensions)

### 4. Certifications
- Minergie-Fachpartner Gebäudehülle
- Holzbau Plus

### 5. Wood Advantages
Organized by category:
- Ökologie (Ecology)
- Ökonomie (Economy)
- Raumklima (Indoor Climate)
- Stabilität (Stability)
- Ästhetik (Aesthetics)
- Energieeffizienz (Energy Efficiency)

### 6. Building Process
4 phases:
- Planung (Planning)
- Produktion (Production)
- Montage (Assembly)
- Fertigstellung (Completion)

### 7. FAQ
20 frequently asked questions covering:
- Materials and certifications
- Timelines and costs
- Services and divisions
- Sustainability and warranties
- Contact and team information

### 8. Team
- Management (3 members)
- Extended Management (6 members)
- Administration (7 members)

### 9. Vision & Values
- Company vision
- 8 core values

## Sitemap Structure

The sitemap (`erni_sitemap.json`) contains a comprehensive map of the ERNI Gruppe website with:

### Page Information
Each page entry includes:
- **ID**: Unique identifier for the page
- **Title (DE/EN)**: Page title in German and English
- **URL**: Full URL to the page
- **Description (DE/EN)**: Brief description in both languages
- **Category**: Page category (main, company, services, information)
- **Tags**: Keywords for easy searching

### Categories
- **main**: Main navigation pages (home, contact, jobs)
- **company**: Company information pages (team, vision, news, etc.)
- **services**: Service division pages (Planung, Holzbau, Spenglerei, Ausbau, Realisation, Agrar)
- **information**: Informational pages (materials, certifications, etc.)

### Usage by FAQ Agent
The FAQ Agent uses the sitemap to:
1. Find relevant website pages based on customer questions
2. Provide direct links to specific pages in responses
3. Help customers navigate to detailed information
4. Support both German and English customers with bilingual links

### Example Pages Included
- All 6 service divisions with their subpages
- Team and contact pages
- Certification and partnership pages
- Project references
- Company information and values
- News and current projects

## Updating the Knowledge Base

### Step 1: Edit the JSON Files

Edit the appropriate JSON file(s) with new or updated information:

**For company information, FAQs, team, etc.:**
- Edit `erni_knowledge_base.json`

**For website structure, new pages, or URL changes:**
- Edit `erni_sitemap.json`
- Add new pages with all required fields (id, title_de, title_en, url, description_de, description_en, category, tags)
- Update existing page URLs if they change
- Add relevant tags to help FAQ Agent find pages

**Important:**
- Maintain the existing JSON structure
- Validate JSON syntax before uploading: `python -m json.tool <filename>.json`
- Use UTF-8 encoding
- Keep information accurate and up-to-date
- For sitemap: Ensure all URLs are correct and accessible

### Step 2: Upload to Vector Store

Run the upload script:

```bash
cd python-backend
.venv/bin/python upload_knowledge_base.py
```

The script will:
1. Upload the file to OpenAI
2. Add it to the Vector Store (ID: vs_68e14a087e3c8191b4b7483ba3cb8d2a)
3. Verify the upload
4. List all files in the vector store

### Step 3: Test the Changes

Run the FAQ Agent tests:

```bash
cd python-backend
.venv/bin/pytest tests/e2e/test_e2e_full_stack.py::TestFAQAgentVectorStore -v
```

Or test manually:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the address of ERNI Gruppe?"}'
```

### Step 4: Verify in Production

After deployment, verify that the FAQ Agent uses the updated knowledge base.

## Vector Store Details

- **Vector Store ID:** vs_68e14a087e3c8191b4b7483ba3cb8d2a

### Files in Vector Store

1. **erni_knowledge_base.json**
   - File ID: file-PXmza43TEH6UyX4pkkFdhD
   - File Size: 18,288 bytes
   - Last Updated: 2025-10-04
   - Content: Company information, FAQs, team, services, certifications

2. **erni_sitemap.json**
   - File ID: (Added by user)
   - Content: Complete website sitemap with all page URLs and descriptions
   - Last Updated: 2025-10-04
   - Purpose: Enable FAQ Agent to provide direct links to relevant website pages

## Best Practices

1. **Accuracy:** Always verify information from official sources
2. **Completeness:** Include all relevant details (names, phone numbers, addresses)
3. **Consistency:** Use consistent terminology and formatting
4. **Bilingual:** Provide information in both German and English where applicable
5. **Testing:** Always test after updates
6. **Versioning:** Keep track of changes and versions

## Troubleshooting

### Upload Fails

If the upload script fails:

1. Check OpenAI API key in `.env` file
2. Verify JSON syntax: `python -m json.tool erni_knowledge_base.json`
3. Check file size (should be < 512 MB)
4. Verify network connection

### FAQ Agent Not Using New Data

If the FAQ Agent doesn't use updated data:

1. Verify file was uploaded successfully
2. Check Vector Store ID in `main.py` matches
3. Restart the backend server
4. Clear any caches
5. Check agent logs for errors

### Tests Failing

If tests fail after update:

1. Review test assertions
2. Check if knowledge base structure changed
3. Verify expected keywords are in the new data
4. Update tests if necessary

## Contact

For questions or issues with the knowledge base:
- Check the main project documentation
- Review the ERNI_KNOWLEDGE_BASE_INTEGRATION_REPORT.md
- Contact the development team

## References

- OpenAI Agents SDK: https://github.com/openai/openai-agents-python
- ERNI Gruppe Website: https://www.erni-gruppe.ch/
- Vector Store Documentation: https://platform.openai.com/docs/assistants/tools/file-search

