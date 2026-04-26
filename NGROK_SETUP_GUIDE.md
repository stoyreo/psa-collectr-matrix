# ngrok Setup Guide — PSA × Collectr Tracer

## Problem

The `START_EVERYTHING.bat` script failed with:
```
ERROR: ngrok failed to connect within 30 seconds
```

This indicates one of the following issues:

1. **ngrok.exe is not installed** ← Most likely
2. ngrok authentication token is missing or expired
3. Reserved domain is not configured on your ngrok account
4. Network connectivity issue

---

## Solution: Install ngrok

### Option 1: Direct Download (Recommended)

1. **Download ngrok** from [ngrok.com/download](https://ngrok.com/download)
   - Select: Windows → 64-bit
   - File: `ngrok-v3-stable-windows-amd64.zip` (or latest version)

2. **Extract ngrok.exe** to your project folder:
   ```
   C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer\
   ```

3. **Verify installation**:
   ```cmd
   ngrok --version
   ```
   Should output: `ngrok version 3.x.x` (or higher)

---

### Option 2: Package Manager

Choose one of these if you have the package manager installed:

**Chocolatey** (if installed):
```cmd
choco install ngrok
```

**Scoop**:
```cmd
scoop install ngrok
```

**Windows Package Manager** (built-in on Windows 11):
```cmd
winget install ngrok
```

---

## Setup ngrok Authentication (Optional but Recommended)

For the **reserved domain** feature (`automated-crummiest-puritan.ngrok-free.dev`) to work, you need:

### Step 1: Create ngrok Account
1. Visit [ngrok.com](https://ngrok.com)
2. Sign up for free account
3. Email verification required

### Step 2: Get Auth Token
1. Log in to [dashboard.ngrok.com](https://dashboard.ngrok.com)
2. Go to **Your Authtoken** section
3. Copy your token (looks like: `2gVkr...xyz123`)

### Step 3: Configure ngrok Locally
```cmd
ngrok config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with your actual token from Step 2.

### Step 4: Verify Reserved Domain
1. Go to [dashboard.ngrok.com/cloud/reserved-domains](https://dashboard.ngrok.com/cloud/reserved-domains)
2. Verify that `automated-crummiest-puritan.ngrok-free.dev` is listed
3. If not reserved, you can reserve it here (free tier may have limited availability)

---

## Testing ngrok Installation

Run the diagnostic tool to verify everything is set up correctly:

```cmd
DIAGNOSE_NGROK.bat
```

This will check:
- ✓ ngrok binary availability
- ✓ ngrok version
- ✓ Authentication token
- ✓ Flask backend connectivity
- ✓ Tunnel creation

---

## Running the Application

### With ngrok (Full Setup)
After installing ngrok and auth token, run:
```cmd
START_EVERYTHING.bat
```

This will:
1. ✓ Start Flask backend
2. ✓ Start ngrok tunnel with reserved domain
3. ✓ Open Vercel dashboard
4. ✓ Show live/snapshot status in footer

### Without ngrok (Snapshot Only)
If you don't want to set up ngrok, use snapshot mode:
```cmd
START_SNAPSHOT_ONLY.bat
```

This will:
1. ✓ Start Flask backend (local development only)
2. ✓ Use cached portfolio snapshot
3. ✓ Open Vercel dashboard
4. ✗ No remote tunnel access

---

## Troubleshooting

### "ERROR: ngrok.exe not found"
- **Solution**: Download ngrok.exe and extract to project folder (Option 1 above)

### "ERROR: ngrok failed to connect within 30 seconds"
After installing ngrok, if you still get this:
- Verify Flask is running first: Check for Flask window in taskbar
- Check your internet connection
- Check ngrok status: [status.ngrok.com](https://status.ngrok.com)
- Review logs: `%USERPROFILE%\.ngrok2\ngrok.log`

### "ERROR: Reserved domain not found"
- Your account may not have reserved this domain
- Free tier has limited reserved domains
- Go to [dashboard.ngrok.com/cloud/reserved-domains](https://dashboard.ngrok.com/cloud/reserved-domains) to reserve it
- Or use a different domain that's available to your account

### Flask shows "NGROK_DOMAIN: unknown"
- ngrok is not connected with auth token
- Run: `ngrok config add-authtoken YOUR_TOKEN`
- Restart Flask after adding token

---

## Port Forwarding Alternative (Advanced)

If you cannot use ngrok, you can set up manual port forwarding:

1. **Router Configuration**:
   - Forward external port 443 to localhost:5000
   - Requires public IP address
   - More complex than ngrok

2. **Update Environment Variables**:
   - Edit `.env` file
   - Set `NEXT_PUBLIC_API_BASE=https://your-public-ip:443`
   - Update Flask CORS settings

This is **not recommended** compared to ngrok's simplicity and security.

---

## Next Steps

1. **Install ngrok** using Option 1 or Option 2 above
2. **Run diagnostic**: `DIAGNOSE_NGROK.bat`
3. **Start the app**: `START_EVERYTHING.bat`
4. **Check dashboard**: [psa-collectr-matrix.vercel.app](https://psa-collectr-matrix.vercel.app)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Computer (Bangkok)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────┐         ┌────────────────┐                │
│  │  Flask Backend │◄────────│  ngrok Tunnel  │                │
│  │ localhost:5000 │  (local) │   (Vercel ←)  │                │
│  └────────────────┘         └────────────────┘                │
│       ▲                              ▲                          │
│       │                              │                          │
│       └──────────────────┬───────────┘                         │
│                          │                                      │
│               Portfolio_Master.xlsx                            │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           │ (HTTPS tunnel)
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     Vercel (Global CDN)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────┐                            │
│  │  Next.js Frontend              │                            │
│  │  psa-collectr-matrix.vercel.app│                            │
│  └────────────────────────────────┘                            │
│       │                                                         │
│       ├─► Try live API via ngrok tunnel                       │
│       └─► Fallback to snapshot.json if offline               │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Support

- **ngrok Issues**: [ngrok docs](https://ngrok.com/docs)
- **ngrok Status**: [status.ngrok.com](https://status.ngrok.com)
- **Diagnostic Tool**: Run `DIAGNOSE_NGROK.bat` for detailed error messages

