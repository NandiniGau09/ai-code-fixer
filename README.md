                User Source Code
                       │
                       ▼
                Monaco Editor
                       │
                       ▼
                 Flask Backend
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      Static Analysis       AI Analysis
       Pylint / AST          Groq / Llama
             │                   │
             └─────────┬─────────┘
                       ▼
              Issues & Suggestions
                       │
                       ▼
             Corrected Code + Explanation

             # AI Code Fixer

An AI-powered web application that analyzes source code, identifies programming issues, explains errors, and generates improved code using AI-assisted analysis.

The application combines static code analysis with an AI coding assistant to help developers understand and fix coding problems.

##  Features

### AI Code Analysis
- Analyze source code using an interactive code editor.
- Identify programming errors and potential issues.
- Generate corrected/improved code using AI.
- Provide explanations for detected problems.
- Suggest improvements to the submitted code.

### Static Code Analysis
The application combines AI analysis with static code checking.

It supports checks such as:
- Code quality issues
- Coding style problems
- Long lines
- TODO/FIXME comments
- Potential hardcoded secrets
- Duplicate code patterns
- Python AST-based analysis
- Code complexity analysis
- Potentially unsafe constructs such as `eval()` and `exec()`

### Code Quality Analysis
The application provides code-quality information based on detected issues and complexity.

The analysis includes areas such as:
- Maintainability
- Readability
- Security
- Performance
- Complexity

### GitHub Repository Analyzer
Users can provide a GitHub repository URL for analysis.

The application:
1. Clones the repository.
2. Finds supported source files.
3. Reads the source code.
4. Performs static analysis.
5. Sends relevant information for AI analysis.
6. Generates explanations and suggested fixes.

### AI Coding Assistant
An integrated AI assistant helps users:
- Understand programming concepts
- Ask coding questions
- Debug problems
- Understand errors
- Get programming suggestions

### Analysis History
The application uses SQLite to store previous analysis and assistant-related information.

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite

### AI
- Groq API
- Llama 3.1 8B Instant

### Code Analysis
- Pylint
- Python AST
- Custom static-analysis logic

### Frontend
- HTML
- CSS
- JavaScript
- Monaco Editor

### GitHub Integration
- GitPython

### Configuration
- python-dotenv

## 📁 Project Structure

```text
ai-code-fixer/
│
├── app.py
├── database.py
├── requirements.txt
├── TODO.md
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
└── utils/
    ├── analyzer.py
    ├── github_analyzer.py
    └── groq_helper.py
