import os
import json
import time
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsUploader:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SERVICE_ACCOUNT_FILE = 'service_account.json'  # You'll need to create this
        self.SPREADSHEET_ID = None  # Will be set from config
        self.WORKSHEET_NAME = 'Leaderboard'
        self.last_upload_file = 'last_upload.json'
        self.pending_uploads_file = 'pending_uploads.json'
        self.config_file = 'uploader_config.json'
        
        self.load_config()
        self.setup_google_sheets()
        
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            'SPREADSHEET_ID': '',  # User needs to set this
            'WORKSHEET_NAME': 'Leaderboard',
            'UPLOAD_INTERVAL_HOURS': 2,
            'MAX_OFFLINE_HOURS': 6
        }
        
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.SPREADSHEET_ID = config.get('SPREADSHEET_ID', '')
                    self.WORKSHEET_NAME = config.get('WORKSHEET_NAME', 'Leaderboard')
                    self.upload_interval = config.get('UPLOAD_INTERVAL_HOURS', 2)
                    self.max_offline_hours = config.get('MAX_OFFLINE_HOURS', 6)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.create_default_config(default_config)
        else:
            self.create_default_config(default_config)
    
    def create_default_config(self, config):
        """Create default configuration file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created default config file: {self.config_file}")
        print("Please edit the config file with your Google Sheets ID!")
        
    def setup_google_sheets(self):
        """Setup Google Sheets connection"""
        try:
            if not Path(self.SERVICE_ACCOUNT_FILE).exists():
                print(f"Service account file not found: {self.SERVICE_ACCOUNT_FILE}")
                print("Please create a service account JSON file from Google Cloud Console")
                return False
                
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.SERVICE_ACCOUNT_FILE, scope)
            
            self.gc = gspread.authorize(creds)
            return True
            
        except Exception as e:
            print(f"Error setting up Google Sheets: {e}")
            return False
    
    def check_internet_connection(self):
        """Check if internet connection is available"""
        try:
            response = requests.get('https://www.google.com', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_last_upload_time(self):
        """Get the last upload timestamp"""
        if Path(self.last_upload_file).exists():
            try:
                with open(self.last_upload_file, 'r') as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data['last_upload'])
            except:
                return None
        return None
    
    def update_last_upload_time(self):
        """Update the last upload timestamp"""
        data = {'last_upload': datetime.now().isoformat()}
        with open(self.last_upload_file, 'w') as f:
            json.dump(data, f)
    
    def should_upload(self):
        """Check if it's time to upload based on interval"""
        last_upload = self.get_last_upload_time()
        if last_upload is None:
            print("📤 First time upload - uploading immediately")
            return True
            
        time_since_last = datetime.now() - last_upload
        hours_passed = time_since_last.total_seconds() / 3600
        
        if time_since_last >= timedelta(hours=self.upload_interval):
            print(f"📤 {hours_passed:.1f} hours passed - time to upload")
            return True
        else:
            hours_remaining = self.upload_interval - hours_passed
            print(f"⏰ {hours_remaining:.1f} hours remaining until next upload")
            return False
    
    def add_to_pending_uploads(self, file_path):
        """Add file to pending uploads queue"""
        pending = []
        if Path(self.pending_uploads_file).exists():
            try:
                with open(self.pending_uploads_file, 'r') as f:
                    pending = json.load(f)
            except:
                pending = []
        
        # Add new file with timestamp
        pending.append({
            'file_path': str(file_path),
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent files (within max offline period)
        cutoff_time = datetime.now() - timedelta(hours=self.max_offline_hours)
        pending = [p for p in pending if datetime.fromisoformat(p['timestamp']) > cutoff_time]
        
        with open(self.pending_uploads_file, 'w') as f:
            json.dump(pending, f, indent=2)
    
    def get_pending_uploads(self):
        """Get list of pending uploads"""
        if Path(self.pending_uploads_file).exists():
            try:
                with open(self.pending_uploads_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def clear_pending_uploads(self):
        """Clear pending uploads after successful upload"""
        if Path(self.pending_uploads_file).exists():
            os.remove(self.pending_uploads_file)
    
    def excel_to_csv_data(self, excel_file_path):
        """Convert Excel file to CSV-like data format"""
        try:
            # Read Excel file
            df = pd.read_excel(excel_file_path)
            print(f"📊 Excel file loaded: {len(df)} rows, {len(df.columns)} columns")
            
            # Convert to simple CSV-like format
            # Get headers
            headers = df.columns.tolist()
            
            # Get data rows and convert everything to strings
            data_rows = []
            for index, row in df.iterrows():
                csv_row = []
                for value in row:
                    if pd.isna(value):
                        csv_row.append("")
                    elif isinstance(value, (int, float)):
                        csv_row.append(str(value))
                    else:
                        csv_row.append(str(value))
                data_rows.append(csv_row)
            
            print(f"📋 Converted to CSV format: {len(headers)} columns, {len(data_rows)} data rows")
            print(f"📊 Headers: {', '.join(headers)}")
            
            return headers, data_rows
            
        except Exception as e:
            print(f"❌ Error converting Excel to CSV format: {e}")
            return None, None

    def upload_csv_to_google_sheets(self, excel_file_path):
        """Upload Excel data as CSV format to Google Sheets"""
        try:
            if not self.SPREADSHEET_ID:
                print("Google Sheets ID not configured!")
                return False
                
            # Convert Excel to CSV format
            headers, data_rows = self.excel_to_csv_data(excel_file_path)
            if headers is None or data_rows is None:
                return False
            
            # Open the Google Sheet
            sheet = self.gc.open_by_key(self.SPREADSHEET_ID)
            
            # Try to get existing worksheet or create new one
            try:
                worksheet = sheet.worksheet(self.WORKSHEET_NAME)
                worksheet.clear()  # Clear existing data
                print(f"📋 Cleared existing worksheet: {self.WORKSHEET_NAME}")
            except gspread.WorksheetNotFound:
                worksheet = sheet.add_worksheet(title=self.WORKSHEET_NAME, rows=1000, cols=26)
                print(f"📋 Created new worksheet: {self.WORKSHEET_NAME}")
            
            # Upload in simple CSV style
            print("📤 Uploading data to Google Sheets...")
            
            # Row 1: Timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            worksheet.update(values=[[f"Last Updated: {timestamp}"]], range_name='A1')
            
            # Row 2: Headers
            worksheet.update(values=[headers], range_name='A2')
            
            # Row 3 onwards: Data
            if data_rows:
                # Upload all data at once
                start_row = 3
                end_row = start_row + len(data_rows) - 1
                range_name = f'A{start_row}:Z{end_row}'
                
                worksheet.update(values=data_rows, range_name=range_name)
            
            print(f"✅ Successfully uploaded {len(data_rows)} rows to Google Sheets")
            print(f"📊 Data range: A1:Z{len(data_rows)+2}")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading CSV to Google Sheets: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_uploads(self):
        """Process uploads - check if it's time and upload if online"""
        if not self.should_upload():
            print("⏰ Not time to upload yet")
            return
        
        # Check for the main leaderboard file
        main_file = Path('Leaderboards/TotalHackerrankLeaderBoard.xlsx')
        if not main_file.exists():
            print("📄 No leaderboard file found to upload")
            return
        
        # Check internet connection
        if not self.check_internet_connection():
            print("🌐 No internet connection - adding to pending uploads")
            self.add_to_pending_uploads(main_file)
            return
        
        # Upload main file
        if self.upload_csv_to_google_sheets(main_file):
            self.update_last_upload_time()
            
            # Process any pending uploads
            pending = self.get_pending_uploads()
            if pending:
                print(f"📤 Processing {len(pending)} pending uploads...")
                for item in pending:
                    file_path = Path(item['file_path'])
                    if file_path.exists():
                        self.upload_csv_to_google_sheets(file_path)
                
                # Clear pending uploads after successful processing
                self.clear_pending_uploads()
                print("✅ All pending uploads processed")
        else:
            # If upload failed, add to pending
            self.add_to_pending_uploads(main_file)

def main():
    """Main function to run the uploader"""
    uploader = GoogleSheetsUploader()
    
    print("🚀 Starting Google Sheets upload process...")
    print(f"📊 Spreadsheet ID: {uploader.SPREADSHEET_ID}")
    print(f"📋 Worksheet: {uploader.WORKSHEET_NAME}")
    print(f"⏱️ Upload interval: {uploader.upload_interval} hours")
    
    uploader.process_uploads()
    
    print("✅ Upload process completed")

if __name__ == "__main__":
    main()
