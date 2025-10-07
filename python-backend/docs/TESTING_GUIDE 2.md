# FAQ Agent Testing Guide - Link Functionality

**Quick testing guide for validating that FAQ Agent provides clickable URLs**

---

## ✅ What to Test

The FAQ Agent should now **ALWAYS** include clickable URLs in markdown format when answering questions about ERNI Gruppe services, contact, certifications, etc.

---

## 🧪 Test Cases

### Test 1: Roof Maintenance (Russian)

**Question:**
```
Где на сайте почитать о ремонте крыши?
```

**Expected Response Format:**
```
Информацию о ремонте и обслуживании крыш вы найдете здесь:

🔧 [Dachservice & Unterhalt](https://www.erni-gruppe.ch/spenglerei/dachservice-unterhalt) – Wartung, Reparaturen, Inspektionen
🏠 [Spenglerei - Übersicht](https://www.erni-gruppe.ch/spenglerei) – Все кровельные услуги

ERNI предлагает профессиональное обслуживание крыш, ремонт и регулярные инспекции.
```

**Validation:**
- ✅ Contains 1-3 clickable links
- ✅ Links in format `[Text](https://www.erni-gruppe.ch/...)`
- ✅ URLs are complete and correct
- ✅ User does NOT need to ask "дай ссылки"

---

### Test 2: Planning Services (German)

**Question:**
```
Welche Planungsdienstleistungen bietet ERNI an?
```

**Expected Response Format:**
```
ERNI Gruppe bietet umfassende Planungsdienstleistungen an:
- Entwurf & Vorprojekt
- Detaillierte Planungsarbeit
- Baubewilligung
- Bauleitung
- Minergie-Berechnungen

Mehr Informationen:
📋 [Planung - Übersicht](https://www.erni-gruppe.ch/planung)
📐 [Entwurf & Vorprojekt](https://www.erni-gruppe.ch/planung/entwurf-vorprojekt)
```

**Validation:**
- ✅ Contains planning service links
- ✅ Links are in German
- ✅ URLs point to correct pages

---

### Test 3: Contact Information (English)

**Question:**
```
How can I contact ERNI?
```

**Expected Response Format:**
```
You can contact ERNI Gruppe as follows:
📞 Phone: 041 570 70 70
📧 Email: kontakt@erni-gruppe.ch
📍 Address: Guggibadstrasse 8, 6288 Schongau

More information:
📞 [Contact Page](https://www.erni-gruppe.ch/kontakt)
📍 [Location & Directions](https://www.erni-gruppe.ch/erni-gruppe/standort-kontakt)
```

**Validation:**
- ✅ Contains contact page links
- ✅ Links are in English
- ✅ URLs are correct

---

### Test 4: Certifications (German)

**Question:**
```
Welche Zertifizierungen hat ERNI?
```

**Expected Response Format:**
```
ERNI Gruppe verfügt über folgende Zertifizierungen:
✓ Minergie-Fachpartner Gebäudehülle
✓ Holzbau Plus (als eines der ersten Holzbauunternehmen)

Diese Zertifizierungen garantieren höchste Qualität und Energieeffizienz.

Mehr erfahren:
🏆 [Mitgliedschaften & Partner](https://www.erni-gruppe.ch/erni-gruppe/mitgliedschaften-partner)
```

**Validation:**
- ✅ Contains certification page link
- ✅ URL is correct

---

### Test 5: Timber Construction (English)

**Question:**
```
Why should I choose wood for my house?
```

**Expected Response Format:**
```
🌲 Why Wood?

Wood is the ideal building material:
✓ Ecological and renewable
✓ Grows in Swiss forests
✓ Excellent thermal insulation
✓ Healthy indoor climate
✓ CO2-neutral
✓ Fast assembly (saves time)

ERNI is a certified Minergie partner.

Learn more:
🌲 [Wood as Building Material](https://www.erni-gruppe.ch/erni-gruppe/holz)
🏆 [Memberships & Partners](https://www.erni-gruppe.ch/erni-gruppe/mitgliedschaften-partner)
```

**Validation:**
- ✅ Contains relevant links about wood and certifications
- ✅ Links are in English

---

## ❌ What Should NOT Happen

### Wrong Response Examples

**❌ WRONG - No URLs:**
```
Информацию о ремонте крыш вы найдете на следующих страницах:
- Dachservice & Unterhalt
- Spenglerei - Übersicht
```

**❌ WRONG - Vague reference:**
```
Sie finden mehr Informationen auf unserer Planungsseite.
```

**❌ WRONG - User has to ask for links:**
```
User: "Где почитать о ремонте крыши?"
Agent: "На странице Dachservice & Unterhalt"
User: "Дай ссылки"
Agent: "Вот ссылки: [Dachservice](...)"
```

---

## ✅ Validation Checklist

For each test, verify:

- [ ] Response includes 1-3 clickable links
- [ ] Links are in markdown format: `[Text](URL)`
- [ ] URLs start with `https://www.erni-gruppe.ch/`
- [ ] URLs are correct and accessible
- [ ] Link descriptions match customer's language
- [ ] User does NOT need to ask "give me links" separately
- [ ] Links are relevant to the question
- [ ] No more than 3 links per response

---

## 🚀 How to Test

### Option 1: Web Interface

1. Open http://localhost:3000 in browser
2. Start a new conversation
3. Ask one of the test questions above
4. Verify response includes clickable URLs
5. Click the URLs to verify they work

### Option 2: API Testing

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Где на сайте почитать о ремонте крыши?",
    "conversation_id": "test-123"
  }' | jq -r '.response'
```

### Option 3: Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Где на сайте почитать о ремонте крыши?",
        "conversation_id": "test-123"
    }
)

print(response.json()["response"])
```

---

## 📊 Success Criteria

**Test is PASSED if:**
- ✅ All 5 test cases return responses with clickable URLs
- ✅ URLs are in correct markdown format
- ✅ URLs are accurate and accessible
- ✅ No need to ask "give me links" separately

**Test is FAILED if:**
- ❌ Any response lacks URLs
- ❌ URLs are not in markdown format
- ❌ URLs are incorrect or broken
- ❌ User has to ask for links explicitly

---

## 🔧 Troubleshooting

### Issue: Agent doesn't provide URLs

**Possible causes:**
1. Server not reloaded with new instructions
2. Agent not using file_search tool
3. Sitemap not in Vector Store

**Solutions:**
1. Restart backend server
2. Check server logs for file_search calls
3. Verify sitemap uploaded to Vector Store

### Issue: URLs are incorrect

**Possible causes:**
1. Sitemap data is incorrect
2. Agent retrieving wrong pages

**Solutions:**
1. Validate sitemap URLs manually
2. Check sitemap tags match question keywords

### Issue: Too many or too few links

**Possible causes:**
1. Agent not following "1-3 links" guideline

**Solutions:**
1. Review agent instructions
2. Adjust max_num_results in FileSearchTool

---

## 📝 Test Results Template

```
Test Date: ___________
Tester: ___________

Test 1 (Roof Maintenance): [ ] PASS [ ] FAIL
Notes: _________________________________

Test 2 (Planning Services): [ ] PASS [ ] FAIL
Notes: _________________________________

Test 3 (Contact Info): [ ] PASS [ ] FAIL
Notes: _________________________________

Test 4 (Certifications): [ ] PASS [ ] FAIL
Notes: _________________________________

Test 5 (Timber Construction): [ ] PASS [ ] FAIL
Notes: _________________________________

Overall Result: [ ] PASS [ ] FAIL
Comments: _________________________________
```

---

## 🎯 Next Steps After Testing

### If Tests Pass:
1. ✅ Mark as production-ready
2. ✅ Deploy to production
3. ✅ Monitor user feedback
4. ✅ Track link click-through rates

### If Tests Fail:
1. ❌ Document specific failures
2. ❌ Review FAQ Agent instructions
3. ❌ Adjust instructions as needed
4. ❌ Re-test until passing

---

**Ready to test!** 🚀

Open http://localhost:3000 and start asking questions!

