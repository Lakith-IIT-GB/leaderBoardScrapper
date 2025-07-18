# HackerRank Leaderboard Auto Scraper with Google Sheets Integration

## Setup Instructions

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

### 2. Google Sheets Setup (Simple Explanation)

**Think of it like hiring a virtual assistant:**

🤖 **What you're doing**: You're creating a virtual assistant (robot) that can update your Google Sheet automatically when you're not around.

#### Real-World Example:
- You have a Google Sheet that you want to update automatically
- But you can't sit at your computer 24/7 to do it manually
- So you create a "robot assistant" that can do it for you
- This robot needs:
  1. **An account** (like you have a Gmail account)
  2. **A password** (to log in)
  3. **Permission** (to edit your specific Google Sheet)

---

#### Step 1: Create a Workspace for Your Robot
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project"
3. Name it "LeaderboardBot" (or anything you want)
4. Click "Create"

**What this does**: Creates a workspace where your robot will live.

#### Step 2: Give Your Robot Permission to Use Google Sheets
1. In the left menu: "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click "Enable"

**What this does**: Tells Google "My robot is allowed to work with Google Sheets."

#### Step 3: Create Your Robot Assistant (DETAILED STEPS)

**You're looking for the "Credentials" section. Here's exactly where to find it:**

1. **Look at the LEFT SIDEBAR** in Google Cloud Console
2. **Find "APIs & Services"** (it might be collapsed - click the hamburger menu ☰ if you don't see it)
3. **Click "APIs & Services"** - it will expand to show sub-options
4. **Click "Credentials"** (under APIs & Services)

**Screenshot guide:**
```
☰ Navigation Menu
├── IAM & Admin
├── APIs & Services  ← Click this
│   ├── Library
│   ├── Credentials  ← Then click this
│   ├── Dashboard
│   └── ...
├── Compute Engine
└── ...
```

5. **You'll see a page with buttons at the top**
6. **Click the blue "+ CREATE CREDENTIALS" button**
7. **Select "Service Account"** from the dropdown menu

**What you'll see:**
- A form asking for "Service account name"
- Enter: `LeaderboardBot`
- Service account ID will auto-fill
- Description: `Bot to update HackerRank leaderboard`

8. **Click "CREATE AND CONTINUE"**
9. **On the next screen (Grant access)**: Just click "CONTINUE" (skip this)
10. **On the final screen (Grant users access)**: Click "DONE"

**What this does**: Creates a robot account (like creating a Gmail account, but for robots).

#### Step 4: Get Your Robot's Login Information (DETAILED STEPS)

**After Step 3, you'll be back on the Credentials page:**

1. **Look for "Service Accounts" section** (scroll down if needed)
2. **You'll see your "LeaderboardBot" listed** with an email like:
   ```
   leaderboardbot@your-project-name.iam.gserviceaccount.com
   ```
3. **Click on the email/name** of your service account
4. **You'll see tabs at the top: DETAILS, PERMISSIONS, KEYS**
5. **Click the "KEYS" tab**
6. **Click "ADD KEY" button**
7. **Select "Create new key"**
8. **Select "JSON" format**
9. **Click "CREATE"**

**What happens next:**
- A file will automatically download to your Downloads folder
- The file name will be something like: `your-project-name-1234567890abcdef.json`
- **IMPORTANT**: Rename this file to `service_account.json`
- **IMPORTANT**: Move this file to your Python project folder:
  ```
  c:\Users\lakit\Desktop\leaderBoardScrapper\HackerRankLeaderboardGUI\
  ```

**What this does**: Downloads a file that contains your robot's username and password. This is like writing down your robot's login details so it can log in automatically.

#### Step 5: Create the Google Sheet You Want to Update
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "HackerRank Leaderboard"
4. Copy the ID from the URL (the long string in the middle)

**What this does**: Creates the actual spreadsheet that your robot will update.

#### Step 6: Give Your Robot Permission to Edit Your Sheet
1. In your Google Sheet, click "Share"
2. Open the `service_account.json` file with Notepad
3. Find the line that says "client_email" - it looks like:
   ```
   "client_email": "leaderboardbot@something.iam.gserviceaccount.com"
   ```
4. Copy that email address
5. Paste it in the "Share" box of your Google Sheet
6. Make sure it has "Editor" permission
7. Click "Send"

**What this does**: This is like giving your robot a key to your house. You're telling Google "This robot is allowed to edit my spreadsheet."

---

## 🎯 **The Final Result:**
- Your robot can now log into Google automatically
- Your robot has permission to edit your specific Google Sheet
- Your Python program will use the robot to update the sheet every 2 hours
- You never have to manually update the sheet again!

**It's like having a personal assistant that works 24/7 updating your spreadsheet for you.**

### 3. Configuration

#### A. Update uploader_config.json
```json
{
    "SPREADSHEET_ID": "YOUR_ACTUAL_SPREADSHEET_ID_HERE",
    "WORKSHEET_NAME": "Leaderboard",
    "UPLOAD_INTERVAL_HOURS": 2,
    "MAX_OFFLINE_HOURS": 6
}
```

### 4. Running the System

#### Option 1: Manual Run
```bash
# Run scraper once
python cli_scraper_no_dotenv.py

# Test Google Sheets upload
python google_sheets_uploader.py
```

#### Option 2: Automatic Mode
```bash
# Run the batch script for continuous operation
auto_scraper.bat
```

### 5. How It Works

1. **Scraper runs every 30 minutes**:
   - Fetches HackerRank leaderboard data
   - Generates Excel files in `Leaderboards/` folder

2. **Google Sheets upload attempts every 2 hours**:
   - Checks if internet is available
   - Uploads latest leaderboard to Google Sheets
   - If offline, queues the upload for later

3. **Offline handling**:
   - Stores failed uploads in `pending_uploads.json`
   - When internet returns, processes all pending uploads
   - Automatically cleans up old pending uploads (older than 6 hours)

### 6. Files Created

- `TotalHackerrankLeaderBoard.xlsx` - Main leaderboard file
- `coderally-6-0-training-weeks.xlsx` - Individual contest file
- `last_upload.json` - Tracks last upload time
- `pending_uploads.json` - Queued uploads when offline
- `uploader_config.json` - Configuration settings

### 7. Troubleshooting

#### Common Issues:
1. **"Service account file not found"**
   - Make sure `service_account.json` is in the correct directory
   - Check file permissions

2. **"Google Sheets ID not configured"**
   - Update `uploader_config.json` with your actual Spreadsheet ID

3. **"Permission denied"**
   - Make sure you shared the Google Sheet with the service account email

4. **"Import errors"**
   - Run: `pip install -r requirements.txt`

#### Test Commands:
```bash
# Test internet connection
python -c "import requests; print('Online' if requests.get('https://google.com').status_code == 200 else 'Offline')"

# Test Google Sheets connection
python google_sheets_uploader.py
```

### 8. Stopping the Auto Scraper

To stop the automatic scraper:
- Press `Ctrl+C` in the command window
- Or simply close the command window

### 9. Scheduling with Windows Task Scheduler (Alternative)

If you prefer using Windows Task Scheduler instead of the batch script:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" and repeat every 30 minutes
4. Set action to start your Python script

This setup ensures your leaderboard data is always up-to-date and automatically synced to Google Sheets!
