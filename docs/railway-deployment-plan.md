# Deployment Plan for Railway

This guide outlines the end-to-end plan for deploying the Mutual Fund FAQ Assistant on **Railway.app**. 

Our backend API, vector database (`data/index/`), and frontend UI (`src/ui/`) will all be bundled and hosted inside a single robust Railway container. 

## 1. Prerequisites
- A GitHub account holding your Mutual Fund Analysis repository.
- A **Railway** account (sign up using GitHub at [railway.app](https://railway.app/)).
- Your **Groq API Key**.

---

## 2. Platform Setup & Deployment

Railway's native GitHub integration allows us to deploy the app in less than 5 minutes.

### Step 2.1: Initialize the Project
1. Log in to your Railway dashboard.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select `Keerttik/Mutual_Fund_Analysis`.
4. Click **Deploy Now**.
   
> [!NOTE]
> *Railway will immediately start building. However, the first build will fail because we haven't given it the Groq API Key yet. This is normal!*

### Step 2.2: Configure Environment Variables
1. Click on the new service block in your Railway project canvas.
2. Navigate to the **Variables** tab.
3. Click **New Variable** and add:
   - **Name:** `GROQ_API_KEY`
   - **Value:** `<your-groq-api-key>`
4. Adding the variable will automatically trigger a clean redeploy.

### Step 2.3: Verify Build & Settings
I have already pushed a `railway.json` file to your GitHub repository. Railway automatically detects this file to configure the build and start commands perfectly. 

You can confirm these settings in the **Settings** tab of the service:
- **Build Provider**: Nixpacks
- **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Step 2.4: Expose to the Internet
1. Still in the **Settings** tab, scroll down to the **Networking** section.
2. Click **Generate Domain**.
3. Railway will provide you with a public URL (e.g., `mutual-fund-app-production.up.railway.app`).
4. Click the URL to view your live, public-facing Mutual Fund chatbot!

---

## 3. Automation Lifecycle & Maintenance

One of the primary reasons we chose Railway is how it seamlessly integrates with our existing GitHub Actions automation.

### The CI/CD Flow
1. **10:00 IST Every Day**: The GitHub Action scraping job wakes up.
2. **Ingestion**: It fetches the freshest mutual fund metrics from Groww.
3. **Database Update**: The action updates the local ChromaDB files (`data/index/`).
4. **Push to Main**: The action automatically pushes the updated database directly to the `main` branch on GitHub.
5. **Zero-Downtime Redeploy**: Railway detects the new commit on `main`. It automatically clones the updated code (with the fresh vector data), runs a fast build, and performs a zero-downtime rollover. 

### Why this is resilient
- You do not need to host an expensive cloud vector database.
- You do not need to manage servers. 
- If the build fails for any reason, Railway retains the previous healthy deployment, ensuring your users never see a crashed app.

> [!TIP]
> If you ever want to change the frontend CSS or tweak the prompt, just push your changes to the `main` branch. Railway will deploy them instantly.
