from flask import Flask, render_template, request, jsonify
import os
import logging
from dotenv import load_dotenv

from utils.analyzer import (
    analyze_code,
    detect_language,
    extract_error_lines
)

from utils.groq_helper import (
    analyze_and_fix,
    analyze_chat
)

from utils.github_analyzer import (
    clone_repo,
    get_code_files,
    read_file_content
)

from database import (
    init_db,
    save_chat,
    save_analysis,
    get_chat_history
)

load_dotenv()

init_db()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "fallback-secret"
)

logging.basicConfig(level=logging.INFO)


# =========================
# HOME PAGE
# =========================

@app.route('/')
def index():

    return render_template('index.html')


# =========================
# CODE ANALYSIS
# =========================
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(silent=True) or {}

        code = data.get('code', '')

        if not code.strip():
            return jsonify({
                'error': 'No code provided'
            }), 400

        if len(code) > 10000:
            return jsonify({
                'error': 'Code too long'
            }), 400

        logging.info(f"Analyzing code of length {len(code)}")

        language = detect_language(code)

        try:
            issues_data = analyze_code(code)

            issues = issues_data[0]
            error_lines = issues_data[1]
            quality_score = issues_data[2]
            quality_metrics = issues_data[3]

        except Exception:
            issues = ["Static analysis failed."]
            error_lines = []
            quality_score = 0
            quality_metrics = {
                "maintainability": 0,
                "security": 0,
                "readability": 0,
                "performance": 0,
                "complexity": 0
            }

        ai_response = analyze_and_fix(
            code,
            issues,
            language
        ) or {}

        save_analysis(
            code,
            language,
            str(issues),
            ai_response.get(
                'fixed_code',
                code
            ),
            ai_response.get(
                'explanation',
                ''
            )
        )

        result = {
            'issues': issues,
            'error_lines': error_lines,
            'quality_score': quality_score,
            'quality_metrics': quality_metrics,
            'fixed_code': ai_response.get(
                'fixed_code',
                code
            ),
            'improvements': ai_response.get(
                'improvements',
                []
            ),
            'explanation': ai_response.get(
                'explanation',
                ''
            ),
            'language': language
        }

        return jsonify(result)

    except Exception as e:
        logging.exception(e)
        return jsonify({
            'error': str(e)
        }), 500

# =========================
# GITHUB REPOSITORY ANALYZER
# =========================

@app.route('/analyze-repo', methods=['POST'])
def analyze_repo():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        repo_url = data.get(
            'repo_url',
            ''
        )

        if not repo_url:

            return jsonify({
                'error': 'Repository URL required'
            }), 400

        logging.info(
            f"Analyzing repository: {repo_url}"
        )

        repo_path = clone_repo(repo_url)

        files = get_code_files(repo_path)

        results = []

        for file in files[:5]:

            code = read_file_content(file)

            if not code.strip():
                continue

            language = detect_language(code)

            try:

                issues_data = analyze_code(code)

                issues = (
                    issues_data[0]
                    if len(issues_data) > 1
                    else issues_data
                )

            except Exception:

                issues = [
                    'Static analysis failed.'
                ]

            ai_response = analyze_and_fix(
                code,
                issues,
                language
            )

            results.append({

                'file': file,

                'language': language,

                'issues': issues,

                'fixed_code': ai_response.get(
                    'fixed_code',
                    ''
                ),

                'explanation': ai_response.get(
                    'explanation',
                    ''
                )
            })

        return jsonify(results)

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            'error': str(e)
        }), 500


# =========================
# AI CHAT ASSISTANT
# =========================

@app.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        message = data.get(
            'message',
            ''
        )

        if not message.strip():

            return jsonify({
                'error': 'Message required'
            }), 400

        logging.info(
            f"AI Chat Message: {message}"
        )

        response = analyze_chat(
            message
        )

        # Save Chat History
        save_chat(
            message,
            response
        )

        return jsonify({
            'response': response
        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            'error': str(e)
        }), 500


# =========================
# CHAT HISTORY
# =========================

@app.route('/history')
def history():

    try:

        history_data = get_chat_history()

        result = []

        for item in history_data:

            result.append({

                "id": item["id"],

                "message": item["message"],

                "response": item["response"],

                "created_at": item["created_at"]
            })

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )