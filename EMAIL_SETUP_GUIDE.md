# Email Service Setup Guide

This guide will help you set up email functionality for your Todo application using Resend.

## Overview

The application uses **Resend** to send transactional emails for:
- Email verification (optional)
- Password reset requests

## Quick Start (Development)

**Without configuring Resend**, emails will be logged to the console where your frontend server is running. This is fine for development and testing.

To see email links during development:
1. Look at the terminal where you ran `npm run dev`
2. Email verification and password reset links will be printed to the console
3. Copy and paste the URL directly into your browser

## Production Setup with Resend

### Step 1: Create Resend Account

1. Go to https://resend.com/signup
2. Sign up for a free account
3. Verify your email address

**Free Tier Limits:**
- 100 emails per day
- 3,000 emails per month
- Perfect for small to medium applications

### Step 2: Get Your API Key

1. Log in to https://resend.com
2. Navigate to **API Keys** in the sidebar
3. Click **Create API Key**
4. Give it a name (e.g., "TodoMaster Production")
5. Select permissions: **Sending access**
6. Click **Create**
7. **Copy the API key immediately** (you won't see it again)

### Step 3: Configure Environment Variables

Add to your `frontend/.env.local`:

```bash
# Resend API Key
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Email "From" address
RESEND_FROM_EMAIL=onboarding@resend.dev
```

**For Development:**
- Use `onboarding@resend.dev` (Resend's test domain)
- Works immediately, no domain verification needed

**For Production:**
- Use your own domain (e.g., `noreply@yourdomain.com`)
- Requires domain verification (see Step 4)

### Step 4: Domain Verification (Production Only)

To send emails from your own domain:

1. Go to **Domains** in Resend dashboard
2. Click **Add Domain**
3. Enter your domain (e.g., `yourdomain.com`)
4. Add the DNS records shown to your domain provider:
   - SPF Record
   - DKIM Records (usually 3)
   - DMARC Record (optional but recommended)
5. Wait for DNS propagation (5 minutes to 48 hours)
6. Verify in Resend dashboard
7. Update `.env.local`:
   ```bash
   RESEND_FROM_EMAIL=noreply@yourdomain.com
   ```

### Step 5: Enable Email Verification (Optional)

To require users to verify their email before logging in:

1. Open `frontend/lib/auth/auth.ts`
2. Find the `emailAndPassword` configuration:
   ```typescript
   emailAndPassword: {
     enabled: true,
     requireEmailVerification: false, // Change this to true
     ...
   }
   ```
3. Change to:
   ```typescript
   requireEmailVerification: true,
   ```
4. Restart your frontend server

**Note:** Only enable this after confirming emails are sending successfully!

### Step 6: Test Email Sending

#### Test Password Reset:

1. Go to http://localhost:3000/forgot-password
2. Enter a registered email address
3. Click "Send Reset Link"
4. Check:
   - **Development (no API key):** Check console for the reset URL
   - **Production (with API key):** Check your email inbox

#### Test Email Verification:

1. Enable `requireEmailVerification: true` in `lib/auth/auth.ts`
2. Sign up with a new account
3. Check:
   - **Development:** Check console for verification URL
   - **Production:** Check email inbox
4. Click the verification link
5. You should be able to log in

## Troubleshooting

### Emails not sending (with Resend configured)

**Check 1: API Key**
- Verify `RESEND_API_KEY` is set in `.env.local`
- Check it starts with `re_`
- Ensure no extra spaces or quotes

**Check 2: From Email**
```bash
# Development - use Resend's test domain
RESEND_FROM_EMAIL=onboarding@resend.dev

# Production - verify domain first!
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

**Check 3: Check Console Logs**
- Look at frontend terminal output
- Resend errors will be logged
- Common error: "Domain not verified"

**Check 4: Resend Dashboard**
- Go to https://resend.com/emails
- Check for failed email attempts
- View error messages

### Email goes to spam

1. **Add DMARC record** to your domain DNS:
   ```
   _dmarc.yourdomain.com TXT "v=DMARC1; p=none"
   ```

2. **Improve email content:**
   - Use plain text version alongside HTML
   - Avoid spam trigger words
   - Include unsubscribe link (optional for transactional)

3. **Warm up your domain:**
   - Start with low volume
   - Gradually increase sending
   - Monitor spam rates in Resend dashboard

### Development mode issues

**Emails not logging to console:**
- Check if `RESEND_API_KEY` is NOT set in `.env.local`
- If set, remove it for development
- Restart frontend server

**Can't see console output:**
- Make sure you're looking at the **frontend** terminal (not backend)
- Look for lines with `=======` separators
- Scroll up if needed

## Email Templates

The application includes professionally designed email templates:

### Verification Email
- Branded header with gradient
- Clear "Verify Email Address" button
- Clickable link as fallback
- 24-hour expiration notice

### Password Reset Email
- Branded header with gradient
- Clear "Reset Password" button
- Clickable link as fallback
- 1-hour expiration notice

**Customization:**
Edit templates in `frontend/lib/email/client.ts`:
- `getVerificationEmailTemplate()`
- `getPasswordResetEmailTemplate()`

## Cost Estimation

### Resend Free Tier (Recommended for MVP)
- **100 emails/day** = plenty for small applications
- **3,000 emails/month** = ~100 users signing up per day
- **Cost:** $0

### Resend Paid Plans (If you grow)
- **$20/month:** 50,000 emails
- **$80/month:** 500,000 emails
- See https://resend.com/pricing

### Typical Usage
- New user signup: 1 verification email
- Password reset: 1 email per request
- 1,000 users signing up = ~1,000 emails

## Alternative Email Providers

If you prefer not to use Resend:

### SendGrid
- Similar pricing
- More mature platform
- Slightly more complex setup

### AWS SES
- Very cheap ($0.10 per 1,000 emails)
- Requires AWS account
- More complex setup

### Nodemailer + Gmail
- Free (for low volume)
- Easy to set up
- Not recommended for production
- Daily sending limits

To use alternatives, modify `frontend/lib/email/client.ts` to use their SDK instead of Resend.

## Security Best Practices

1. **Never commit API keys** to version control
   - Use `.env.local` (already in `.gitignore`)
   - Use environment variables in production

2. **Rotate API keys regularly**
   - Create new key in Resend dashboard
   - Update environment variables
   - Delete old key

3. **Use environment-specific keys**
   - Development: Use test domain
   - Staging: Use separate API key
   - Production: Use domain-verified email

4. **Monitor usage**
   - Check Resend dashboard regularly
   - Set up usage alerts
   - Watch for unusual patterns

## Support

- **Resend Documentation:** https://resend.com/docs
- **Resend API Reference:** https://resend.com/docs/api-reference
- **Resend Support:** support@resend.com
- **This Project:** Check console logs and Resend dashboard first

---

**Setup complete!** Your application now has professional email functionality. 🎉
