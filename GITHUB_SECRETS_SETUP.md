# GitHub Secrets Configuration Guide
## ERNI Gruppe Building Agents

**Date:** October 5, 2025  
**Purpose:** Configure GitHub repository secrets for CI/CD pipeline

---

## 📋 Overview

This guide provides step-by-step instructions for configuring GitHub repository secrets required for the CI/CD pipeline, including test environment and production environment secrets.

---

## 🔐 Required Secrets

### Test Environment Secrets

These secrets are used for running tests in GitHub Actions CI/CD pipeline.

| Secret Name | Description | Format | Example |
|-------------|-------------|--------|---------|
| `OPENAI_API_KEY_TEST` | OpenAI API key for testing | `sk-proj-...` or `sk-...` | `sk-proj-abc123...` |
| `OPENAI_VECTOR_STORE_ID_TEST` | Vector Store ID for testing | `vs_xxxxx` | `vs_68e2b21188c4819184c3b5e23adce87e` |

### Production Environment Secrets

These secrets are used for production deployment and must meet strict security requirements.

| Secret Name | Description | Min Length | Requirements |
|-------------|-------------|------------|--------------|
| `SECRET_KEY_PROD` | Application secret key | 32 chars | Cryptographically random |
| `JWT_SECRET_KEY_PROD` | JWT signing secret key | 32 chars | Cryptographically random |
| `DB_PASSWORD_PROD` | PostgreSQL password | 32 chars | Strong password |
| `REDIS_PASSWORD_PROD` | Redis password | 32 chars | Strong password |

**Security Requirements:**
- All production secrets must be at least 32 characters long
- Secrets must not contain forbidden values: "changeme", "secret", "password", "test", "dev"
- Use cryptographically secure random generation
- Never reuse secrets across environments

---

## 🛠️ Step-by-Step Setup

### Step 1: Generate Secure Secrets

**Using Python (recommended):**
```bash
# Generate SECRET_KEY_PROD
python3 -c "import secrets; print('SECRET_KEY_PROD=' + secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY_PROD
python3 -c "import secrets; print('JWT_SECRET_KEY_PROD=' + secrets.token_urlsafe(32))"

# Generate DB_PASSWORD_PROD
python3 -c "import secrets; print('DB_PASSWORD_PROD=' + secrets.token_urlsafe(32))"

# Generate REDIS_PASSWORD_PROD
python3 -c "import secrets; print('REDIS_PASSWORD_PROD=' + secrets.token_urlsafe(32))"
```

**Using OpenSSL:**
```bash
# Generate SECRET_KEY_PROD
echo "SECRET_KEY_PROD=$(openssl rand -base64 32)"

# Generate JWT_SECRET_KEY_PROD
echo "JWT_SECRET_KEY_PROD=$(openssl rand -base64 32)"

# Generate DB_PASSWORD_PROD
echo "DB_PASSWORD_PROD=$(openssl rand -base64 32)"

# Generate REDIS_PASSWORD_PROD
echo "REDIS_PASSWORD_PROD=$(openssl rand -base64 32)"
```

**Example Output:**
```
SECRET_KEY_PROD=xK9mP2vL8nQ4wR7tY6uI3oP5aS1dF0gH2jK4lM6nB8vC
JWT_SECRET_KEY_PROD=zN3bV5cX8mK1wQ4rT7yU9iO2pA6sD0fG3hJ5kL7nM9vB
DB_PASSWORD_PROD=qW2eR4tY6uI8oP0aS1dF3gH5jK7lZ9xC2vB4nM6qW8eR
REDIS_PASSWORD_PROD=tY5uI7oP9aS1dF3gH5jK7lZ9xC2vB4nM6qW8eR0tY2uI
```

**⚠️ IMPORTANT:** Save these secrets securely! You will need them for GitHub configuration.

### Step 2: Access GitHub Repository Settings

1. Navigate to your GitHub repository: https://github.com/DIZ-admin/openai-cs-agents-demo
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. You should see the "Secrets" tab

### Step 3: Add Test Environment Secrets

#### OPENAI_API_KEY_TEST

1. Click **New repository secret**
2. Name: `OPENAI_API_KEY_TEST`
3. Secret: Paste your OpenAI API key (starts with `sk-proj-` or `sk-`)
4. Click **Add secret**

**Where to get OpenAI API key:**
- Go to https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy the key immediately (you won't be able to see it again)
- Paste into GitHub secret

#### OPENAI_VECTOR_STORE_ID_TEST

1. Click **New repository secret**
2. Name: `OPENAI_VECTOR_STORE_ID_TEST`
3. Secret: Paste your Vector Store ID (format: `vs_xxxxx`)
4. Click **Add secret**

**Where to get Vector Store ID:**
- Use the existing Vector Store ID from your `.env` file
- Or create a new one using `python-backend/create_vector_store.py`
- Format: `vs_68e2b21188c4819184c3b5e23adce87e`

### Step 4: Add Production Environment Secrets

#### SECRET_KEY_PROD

1. Click **New repository secret**
2. Name: `SECRET_KEY_PROD`
3. Secret: Paste the generated secret from Step 1
4. Click **Add secret**

#### JWT_SECRET_KEY_PROD

1. Click **New repository secret**
2. Name: `JWT_SECRET_KEY_PROD`
3. Secret: Paste the generated secret from Step 1
4. Click **Add secret**

#### DB_PASSWORD_PROD

1. Click **New repository secret**
2. Name: `DB_PASSWORD_PROD`
3. Secret: Paste the generated password from Step 1
4. Click **Add secret**

#### REDIS_PASSWORD_PROD

1. Click **New repository secret**
2. Name: `REDIS_PASSWORD_PROD`
3. Secret: Paste the generated password from Step 1
4. Click **Add secret**

### Step 5: Verify Secrets

After adding all secrets, you should see 6 secrets in the list:

- ✅ `OPENAI_API_KEY_TEST`
- ✅ `OPENAI_VECTOR_STORE_ID_TEST`
- ✅ `SECRET_KEY_PROD`
- ✅ `JWT_SECRET_KEY_PROD`
- ✅ `DB_PASSWORD_PROD`
- ✅ `REDIS_PASSWORD_PROD`

**Note:** GitHub will show `***` for secret values. You cannot view them after creation.

---

## ✅ Validation

### Automatic Validation

The CI/CD pipeline includes a `security-load-tests` job that validates all secrets:

1. **Length Check:** All `*_PROD` secrets must be ≥ 32 characters
2. **Forbidden Values:** Secrets must not contain "changeme", "secret", "password", "test", "dev"
3. **Format Check:** OpenAI API key must start with `sk-` or `sk-proj-`
4. **Vector Store ID:** Must start with `vs_`

**Validation Script:** `scripts/preflight_check.py`

### Manual Validation

**Test locally (optional):**
```bash
# Set environment variables
export SECRET_KEY_PROD="your-generated-secret"
export JWT_SECRET_KEY_PROD="your-generated-jwt-secret"
export DB_PASSWORD_PROD="your-generated-db-password"
export REDIS_PASSWORD_PROD="your-generated-redis-password"
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_VECTOR_STORE_ID="your-vector-store-id"
export ENVIRONMENT="production"

# Run validation
cd python-backend
python -c "from security_validator import ProductionSecurityValidator; ProductionSecurityValidator.validate()"
```

**Expected output:**
```
🔒 Validating production security configuration...
✅ Production security validation passed
```

---

## 🚀 Testing the CI/CD Pipeline

### Trigger the Pipeline

**Option 1: Push to staging branch**
```bash
git add .
git commit -m "test: verify GitHub secrets configuration"
git push origin staging
```

**Option 2: Manual workflow dispatch**
1. Go to **Actions** tab in GitHub
2. Select **CI/CD Pipeline** workflow
3. Click **Run workflow**
4. Select branch: `staging`
5. Click **Run workflow**

### Monitor the Pipeline

1. Go to **Actions** tab
2. Click on the running workflow
3. Monitor the `security-load-tests` job
4. Check for any errors in the logs

**Expected result:**
- ✅ All jobs pass (green checkmarks)
- ✅ `security-load-tests` job completes successfully
- ✅ No secret validation errors

---

## 🔒 Security Best Practices

### Secret Management

1. **Never commit secrets to Git**
   - Always use `.env` files (in `.gitignore`)
   - Use GitHub Secrets for CI/CD
   - Use environment variables in production

2. **Rotate secrets regularly**
   - Production secrets: Every 90 days
   - Test secrets: Every 180 days
   - After any security incident: Immediately

3. **Use different secrets for each environment**
   - Development: Local `.env` file
   - Test: GitHub Secrets (`*_TEST`)
   - Production: GitHub Secrets (`*_PROD`)

4. **Limit access to secrets**
   - Only repository admins can view/edit secrets
   - Use GitHub Teams for access control
   - Audit secret access regularly

### Secret Rotation Procedure

**When to rotate:**
- Every 90 days (scheduled)
- After team member departure
- After security incident
- If secret is suspected to be compromised

**How to rotate:**
1. Generate new secrets using Step 1
2. Update GitHub Secrets (Steps 3-4)
3. Update production environment variables
4. Restart services with new secrets
5. Verify services are working
6. Document rotation in security log

---

## 📞 Support

**If you encounter issues:**

1. **Secret validation fails:**
   - Check secret length (must be ≥ 32 characters)
   - Check for forbidden values
   - Regenerate secrets if needed

2. **CI/CD pipeline fails:**
   - Check GitHub Actions logs
   - Verify all 6 secrets are configured
   - Check secret names match exactly (case-sensitive)

3. **OpenAI API errors:**
   - Verify API key is valid
   - Check API key has sufficient credits
   - Verify Vector Store ID exists

**Contact:**
- GitHub Issues: https://github.com/DIZ-admin/openai-cs-agents-demo/issues
- Email: devops@erni-gruppe.ch

---

## 📝 Checklist

Before proceeding to production deployment:

- [ ] All 6 GitHub secrets configured
- [ ] Secrets meet minimum length requirements (32 chars)
- [ ] Secrets are cryptographically random
- [ ] OpenAI API key is valid and has credits
- [ ] Vector Store ID exists and is accessible
- [ ] CI/CD pipeline passes all jobs
- [ ] `security-load-tests` job completes successfully
- [ ] Secrets documented in secure password manager
- [ ] Secret rotation schedule documented
- [ ] Team members trained on secret management

---

**Document Version:** 1.0.0  
**Last Updated:** October 5, 2025  
**Next Review:** January 5, 2026

