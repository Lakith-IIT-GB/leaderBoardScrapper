# HackerRank Leaderboard Scraper - CLI Version

A command-line interface version of the HackerRank leaderboard scraper that allows you to generate and combine Excel sheets without using the GUI.

## Features

- **Option 1**: Generate Excel sheets from HackerRank contest IDs
- **Option 2**: Combine existing Excel sheets with student data
- Environment-based configuration
- Clean command-line interface
- Automatic Excel formatting

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses a `.env` file for configuration. You can modify the following settings:

```env
SEARCH_KEYWORD=hackerrank
USER_AGENT=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36
REQUEST_TIMEOUT=10
OFFSET_LIMIT=100
MAX_OFFSET=1000
```

## Usage

Run the CLI application:
```bash
python cli_scraper.py
```

### Menu Options

**Press 1**: Generate Excel Sheets from Contest IDs
- Enter comma-separated HackerRank contest IDs
- Generates individual Excel files for each contest
- Creates a combined `TotalHackerrankLeaderBoard.xlsx` file

**Press 2**: Combine Existing Excel Sheets
- Combine student data with HackerRank leaderboard
- Supports multiple student data formats:
  - File with 'Roll number' and 'Hackerrank' columns
  - File with just 'Hackerrank' usernames (auto-generates User_001, etc.)
  - File with usernames in first column

**Press 0**: Exit

## File Structure

```
Leaderboards/
├── contest1.xlsx
├── contest2.xlsx
├── TotalHackerrankLeaderBoard.xlsx
└── CombinedLeaderboard.xlsx
```

## Student Data Format

Your student Excel file should have one of these formats:

**Format 1** (Recommended):
| Roll number | Hackerrank |
|-------------|------------|
| 2021001     | username1  |
| 2021002     | username2  |

**Format 2** (Usernames only):
| Hackerrank |
|------------|
| username1  |
| username2  |

**Format 3** (Any column name):
| StudentName |
|-------------|
| username1   |
| username2   |

## Output

- All Excel files are saved in the `Leaderboards/` directory
- Files include proper formatting with colors and borders
- Automatic ranking based on scores
- Combined files show total scores across all contests

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Invalid file paths are validated
- Missing data is handled with appropriate warnings
- Progress tracking for long operations

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SEARCH_KEYWORD | Keyword for search operations | hackerrank |
| USER_AGENT | HTTP User-Agent string | Mozilla/5.0... |
| REQUEST_TIMEOUT | HTTP request timeout (seconds) | 10 |
| OFFSET_LIMIT | Records per API request | 100 |
| MAX_OFFSET | Maximum offset for pagination | 1000 |

## Troubleshooting

1. **Import Error**: Make sure you've installed all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **File Not Found**: Use absolute file paths when selecting files

3. **No Data Retrieved**: Check if contest IDs are correct and contests are public

4. **Excel Formatting Issues**: Ensure openpyxl is properly installed

## Files

- `cli_scraper.py` - Main CLI application
- `main.py` - Original GUI version (preserved)
- `.env` - Configuration file
- `requirements.txt` - Python dependencies
