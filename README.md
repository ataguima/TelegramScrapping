# Telegram Scraper Fork

This repository is a fork of the original Telegram Scraper project. I have updated and improved the code to modernize it and enhance its robustness and readability. This README explains the situation and lists all the changes made.

## Overview

The original code was designed to scrape members from Telegram groups and add them to another group. My fork introduces several updates, including:

- **Modernization of the asynchronous workflow**
- **Enhanced error handling**
- **Code refactoring for better readability and maintainability**
- **Improved logging and messaging**
- **Better file handling and data validation**

## Changes List

### 1. Imports and Initial Setup
- **Asyncio Integration:**  
  - *Old:* Used `time.sleep()` for delays.  
  - *New:* Replaced with `await asyncio.sleep()` to prevent blocking the event loop.
- **Error Imports:**  
  - *Old:* Imported a limited set of Telegram error classes.  
  - *New:* Added `UserIdInvalidError` to handle cases of invalid user IDs.
- **Colorama Initialization:**  
  - *Old:* Used `init()` without parameters.  
  - *New:* Uses `init(autoreset=True)` to automatically reset terminal colors.

### 2. Logo Function
- **Type Annotations:**  
  - *Old:* No explicit return type was defined.  
  - *New:* Function signature now includes `-> None`.
- **Enhanced String Iteration:**  
  - *Old:* Used basic conditions for setting colors.  
  - *New:* Utilizes a variable for total lines and clearer conditions for applying different colors using f‑strings.

### 3. File Title Definition (`define_title_file`)
- **String Manipulation:**  
  - *Old:* Removed trailing underscores by comparing the last character.  
  - *New:* Uses `endswith("_")` for improved clarity.
- **Conditional Title Construction:**  
  - *Old:* Used concatenation with the username for non-own group scenarios.  
  - *New:* Uses f‑strings to build the filename.

### 4. Join Group Function
- **Exception Handling Improvements:**  
  - *Old:* Had a single try/except block for each group.  
  - *New:* Uses nested try/except blocks to better handle cases where the user is already a member or cannot join, with more informative logging messages.

### 5. Scrapping Members Functions
- **Path Handling:**  
  - *Old:* Constructed file paths using `Path(path_csv / title_file)`.  
  - *New:* Uses `Path(path_csv) / title_file` for clarity.
- **User Status Verification:**  
  - *Old:* Compared user status with `str(UserStatusRecently())`.  
  - *New:* Uses `isinstance(user.status, UserStatusRecently)` for a more robust type-check.

### 6. CSV Writing and Reading
- **CSV File Writing:**  
  - *Old:* Opened CSV files without specifying `newline=""`, which can cause extra blank lines on some systems.  
  - *New:* Now opens files with `newline=""` to ensure proper formatting.
- **Data Extraction:**  
  - *Old:* Checked user attributes with if/else blocks.  
  - *New:* Uses the `.get()` method and inline conditional expressions for cleaner code.
- **Blacklist Handling:**  
  - *Old:* Compared a boolean flag using `== False`.  
  - *New:* Uses a more Pythonic `if not title_file:` check and f‑strings for filename construction.

### 7. Random Username Selection
- **Eliminated Recursion:**  
  - *Old:* Used recursion to avoid returning the same username.  
  - *New:* Filters the list and randomly selects from the available options, avoiding recursion and potential performance issues.
- **Added Documentation:**  
  - *New:* Includes a docstring describing the function's purpose.

### 8. Message Sending Function
- **Message Construction:**  
  - *Old:* Constructed messages by appending to a list in a loop.  
  - *New:* Uses a generator expression with `" ".join()` for a more concise implementation.
- **Type Annotations:**  
  - *New:* Function now explicitly states its return type (`-> None`).

### 9. Adding Members to a Group
- **Asynchronous Improvements:**  
  - *Old:* Used `time.sleep()` to wait between adding members, blocking the entire process.  
  - *New:* Utilizes `await asyncio.sleep()` for non-blocking delays.
- **Input Channel Conversion:**  
  - *New:* Converts the target group to an `InputChannel` for improved compatibility.
- **User Data Validation:**  
  - *New:* Checks if `id` and `access_hash` exist before attempting to add a user, skipping invalid entries.
- **Blacklist Aggregation:**  
  - *New:* Combines multiple blacklist sources into a set for efficient lookups.
- **Error Handling and Logging:**  
  - *Old:* Had less granular logging and error handling.  
  - *New:* Provides detailed error messages (including handling for `UserIdInvalidError`) and uses f‑strings to display progress and wait times.

## How to Use

1. **Clone or Fork This Repository:**  
   If you need your own copy, fork it on GitHub.
2. **Create a Virtual Environment:**  
   Set up a Python virtual environment and install the required dependencies.
3. **Configuration:**  
   Ensure that your configuration file (`myconfig.py`) is correctly set with variables like `path_csv`, `link_channel_to_add_members`, etc.
4. **Run the Script:**  
   Execute the script using an asynchronous event loop (e.g., `asyncio.run(main())`) where `main()` initializes your Telegram client and calls `add_members_to_group`.

## Contributing

If you have suggestions or further improvements, feel free to open an issue or submit a pull request.

## License

This project remains under the same license as the original repository. Please refer to the original license for details regarding distribution and use.
