# AI Code Fixer - Error Line Highlighting Steps

## Phase 1: Backend Updates
- [x] 1. Update utils/analyzer.py: Add extract_error_lines() function, modify analyze_code() to return (issues, error_lines)
- [x] 2. Update app.py: Import new func, unpack issues/error_lines, add 'error_lines' to API response

## Phase 2: Frontend Monaco + Highlighting
- [x] 3. Update templates/index.html: Add Monaco CDN, replace textarea with #editor div, init editor in JS
- [x] 4. Update JS: Use editor.getValue(), add highlightErrors() func using deltaDecorations, call in displayResults
- [x] 5. Update static/style.css: Add .error-highlight styles

## Phase 3: Testing
- [ ] 6. Test backend: Run app.py, POST /analyze → verify \"error_lines\" in response (e.g. [2,5])
- [ ] 7. Test frontend: Open index.html → check Monaco loads, highlights red lines on errors
- [ ] 8. Complete task

