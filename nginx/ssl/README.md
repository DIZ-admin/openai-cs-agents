# SSL Certificates for ERNI Gruppe Building Agents

## Current Setup

This directory contains **self-signed SSL certificates** for local development and testing.

### Files

- `fullchain.pem` - SSL certificate (public key)
- `privkey.pem` - Private key

### Certificate Details

- **Type:** Self-signed X.509 certificate
- **Algorithm:** RSA 2048-bit
- **Validity:** 365 days
- **Subject:**
  - Country (C): CH
  - State (ST): Lucerne
  - Locality (L): Schongau
  - Organization (O): ERNI Gruppe
  - Organizational Unit (OU): IT
  - Common Name (CN): localhost

### Browser Warning

⚠️ **Expected Behavior:** Browsers will show a security warning when accessing `https://localhost` because the certificate is self-signed and not issued by a trusted Certificate Authority (CA).

**To bypass the warning:**
- **Chrome/Edge:** Click "Advanced" → "Proceed to localhost (unsafe)"
- **Firefox:** Click "Advanced" → "Accept the Risk and Continue"
- **Safari:** Click "Show Details" → "visit this website"

This is **normal and expected** for self-signed certificates in development.

---

## Production Deployment

For production deployment, you should use **Let's Encrypt** or another trusted CA.

### Option 1: Let's Encrypt (Recommended for Production)

Let's Encrypt provides **free, automated SSL certificates** that are trusted by all browsers.

#### Prerequisites

1. A registered domain name (e.g., `erni-agents.example.com`)
2. Domain DNS pointing to your server's public IP
3. Ports 80 and 443 open on your firewall

#### Setup with Certbot

1. **Install Certbot:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   
   # macOS
   brew install certbot
   ```

2. **Stop nginx temporarily:**
   ```bash
   docker-compose stop nginx
   ```

3. **Obtain certificate:**
   ```bash
   sudo certbot certonly --standalone \
     -d yourdomain.com \
     -d www.yourdomain.com \
     --email your-email@example.com \
     --agree-tos \
     --no-eff-email
   ```

4. **Copy certificates to nginx/ssl/:**
   ```bash
   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
   sudo chown $USER:$USER nginx/ssl/*.pem
   ```

5. **Restart nginx:**
   ```bash
   docker-compose up -d nginx
   ```

6. **Set up auto-renewal:**
   ```bash
   # Test renewal
   sudo certbot renew --dry-run
   
   # Add cron job for auto-renewal
   sudo crontab -e
   # Add this line:
   0 0 * * * certbot renew --quiet && docker-compose restart nginx
   ```

#### Certificate Renewal

Let's Encrypt certificates are valid for **90 days**. Certbot will automatically renew them when they have 30 days or less remaining.

---

### Option 2: Commercial SSL Certificate

If you prefer a commercial certificate (e.g., from DigiCert, Comodo, GlobalSign):

1. **Generate a Certificate Signing Request (CSR):**
   ```bash
   openssl req -new -newkey rsa:2048 -nodes \
     -keyout nginx/ssl/privkey.pem \
     -out nginx/ssl/csr.pem \
     -subj "/C=CH/ST=Lucerne/L=Schongau/O=ERNI Gruppe/CN=yourdomain.com"
   ```

2. **Submit CSR to your CA** and receive:
   - Certificate file (`certificate.crt`)
   - Intermediate certificate(s) (`intermediate.crt`)

3. **Create fullchain.pem:**
   ```bash
   cat certificate.crt intermediate.crt > nginx/ssl/fullchain.pem
   ```

4. **Restart nginx:**
   ```bash
   docker-compose restart nginx
   ```

---

## Regenerating Self-Signed Certificates

If you need to regenerate the self-signed certificates (e.g., they expired):

```bash
cd nginx/ssl

# Generate new certificate (valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem \
  -out fullchain.pem \
  -subj "/C=CH/ST=Lucerne/L=Schongau/O=ERNI Gruppe/OU=IT/CN=localhost"

# Restart nginx
cd ../..
docker-compose restart nginx
```

---

## Security Best Practices

### File Permissions

Ensure private key has restricted permissions:

```bash
chmod 600 nginx/ssl/privkey.pem
chmod 644 nginx/ssl/fullchain.pem
```

### Certificate Monitoring

Monitor certificate expiration:

```bash
# Check expiration date
openssl x509 -in nginx/ssl/fullchain.pem -noout -enddate

# Check certificate details
openssl x509 -in nginx/ssl/fullchain.pem -noout -text
```

### Nginx SSL Configuration

The nginx configuration (`nginx/nginx.conf`) includes:

- **TLS 1.2 and 1.3** only (no TLS 1.0/1.1)
- **Strong cipher suites** (ECDHE-ECDSA-AES128-GCM-SHA256, etc.)
- **HSTS** (HTTP Strict Transport Security)
- **Session caching** for performance

---

## Troubleshooting

### Certificate Not Found Error

```
nginx: [emerg] cannot load certificate "/etc/nginx/ssl/fullchain.pem"
```

**Solution:**
1. Check files exist: `ls -la nginx/ssl/`
2. Check docker-compose volume mount: `./nginx/ssl:/etc/nginx/ssl:ro`
3. Restart nginx: `docker-compose restart nginx`

### Browser Shows "NET::ERR_CERT_AUTHORITY_INVALID"

**For self-signed certificates:** This is expected. Click "Advanced" and proceed.

**For Let's Encrypt/commercial certificates:**
1. Check certificate chain: `openssl s_client -connect localhost:443 -showcerts`
2. Ensure `fullchain.pem` includes intermediate certificates
3. Check domain name matches certificate CN

### Certificate Expired

```bash
# Check expiration
openssl x509 -in nginx/ssl/fullchain.pem -noout -enddate

# Regenerate (self-signed) or renew (Let's Encrypt)
certbot renew  # For Let's Encrypt
# OR
# Regenerate self-signed (see above)
```

---

## Additional Resources

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Certbot Documentation](https://certbot.eff.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)

---

**Last Updated:** 2025-10-04  
**Certificate Type:** Self-signed (Development)  
**Expiration:** Check with `openssl x509 -in fullchain.pem -noout -enddate`

