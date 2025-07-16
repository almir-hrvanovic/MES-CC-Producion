# VBA Coding Standards and Conventions

## Language and Comments
- Use Serbian/Croatian language for variable names, comments, and user messages
- Keep English for VBA keywords and built-in functions
- Use descriptive variable names in local language (e.g., MASINA, NAZIV, REDOSLIJED)

## Variable Naming Conventions
- Use UPPERCASE for constants and important variables (ST, CET, OT, BT)
- Use descriptive names: ST (Start Time), CET (Calculated End Time), OT (Order Time)
- Use meaningful abbreviations: KPL (Komplet), POZ (Pozicija), NAZIV (Name)
- Date variables should have clear suffixes: stDate, btDate
- Time variables should have T suffix: STT, BTT

## Code Structure
- Always use `Option Explicit` at module level
- Disable screen updating for performance: `Application.ScreenUpdating = False`
- Use proper error handling and input validation
- Include progress bars for long-running operations
- Always restore application settings (ScreenUpdating, Calculation mode)

## Sheet References
- Use explicit sheet references: `Sheets("PRINT").Range("A1")`
- Common sheet names: PRINT, NOVO, QUERY, KALENDAR MASINA, PROMJENA, REDOSLIJED
- Use meaningful range names when possible

## Time and Date Handling
- Use proper time constants: ST1="00:00:00", ST2="07:00:00", ST3="15:00:00", ST4="23:00:00"
- Work shift zones: ZT1-ZT4 for break times
- Always separate date and time components when needed
- Use TimeSerial() for time calculations

## Performance Optimization
- Set `Application.Calculation = xlManual` during intensive operations
- Use `Application.DisplayStatusBar = False` during processing
- Always restore settings: `Application.Calculation = xlAutomatic`
- Copy and paste values instead of formulas when possible

## User Interface
- Provide clear Serbian/Croatian messages in MsgBox
- Use InputBox for user input with descriptive prompts
- Implement progress indicators for long operations
- Use color coding: rgbBlue, rgbRed for status indication

## Data Processing Patterns
- Use AutoFilter for data filtering
- Sort data using proper Sort objects
- Use VLOOKUP for calendar/schedule lookups
- Copy ranges efficiently with proper paste operations