from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import textstat
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# -----------------------------------------------------------
# SET YOUR GROQ API KEY HERE (one key works for both models)
# -----------------------------------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
# -----------------------------------------------------------

# Model 1: Qwen3 32B (reasoning model by Alibaba, active on Groq March 2026)
DEEPSEEK_MODEL = "qwen/qwen3-32b"

# Model 2: LLaMA 3.3 70B (fast general model)
LLAMA_MODEL = "llama-3.3-70b-versatile"

# Configure Groq client (shared by both models)
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("[OK] Groq client configured (DeepSeek R1 + LLaMA 3.3)")
except Exception as e:
    groq_client = None
    print(f"[WARNING] Groq config failed: {e}")


# -----------------------------------------------------------
# Text Analysis Helper
# -----------------------------------------------------------
def analyze_text_metrics(text, query):
    word_count        = textstat.lexicon_count(text, removepunct=True)
    sentence_count    = textstat.sentence_count(text)
    avg_sentence_len  = (word_count / sentence_count) if sentence_count > 0 else 0
    readability_score = textstat.flesch_kincaid_grade(text)
    main_keyword      = query.split()[0].lower() if query else ''
    keyword_occ       = text.lower().count(main_keyword)
    keyword_density   = (keyword_occ / word_count * 100) if word_count > 0 else 0
    return {
        'word_count':          word_count,
        'avg_sentence_length': avg_sentence_len,
        'readability_score':   readability_score,
        'keyword_density':     keyword_density,
    }


# -----------------------------------------------------------
# Generic Groq Handler (used for both models)
# -----------------------------------------------------------
def get_groq_model_response(query, model_name, display_name):
    start = time.time()
    try:
        if groq_client is None:
            raise Exception("Groq client not initialized. Check GROQ_API_KEY.")

        response = groq_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": query}],
            max_tokens=500
        )
        text          = response.choices[0].message.content
        input_tokens  = response.usage.prompt_tokens     if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        metrics       = analyze_text_metrics(text, query)

        return {
            'response':      text,
            'time':          time.time() - start,
            'input_tokens':  input_tokens,
            'output_tokens': output_tokens,
            'cost':          0,
            **metrics
        }

    except Exception as e:
        print(f"[{display_name} Error] {e}")
        return {
            'response':            f"{display_name} Error: {e}",
            'time':                time.time() - start,
            'input_tokens':        0,
            'output_tokens':       0,
            'cost':                0,
            'word_count':          0,
            'avg_sentence_length': 0,
            'readability_score':   0,
            'keyword_density':     0,
        }


def get_deepseek_response(query):
    return get_groq_model_response(query, DEEPSEEK_MODEL, "Qwen3 32B")

def get_llama_response(query):
    return get_groq_model_response(query, LLAMA_MODEL, "LLaMA 3.3")


# -----------------------------------------------------------
# Flask Routes
# -----------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/compare_responses', methods=['POST'])
def compare_responses():
    user_query = request.json.get('query', '').strip()
    if not user_query:
        return jsonify({'error': 'No query provided.'}), 400

    deepseek_data = get_deepseek_response(user_query)
    llama_data    = get_llama_response(user_query)

    summary_data = [
        {
            'Model':               'Qwen3 32B',
            'avg_response_time':   deepseek_data['time'],
            'total_input_tokens':  deepseek_data['input_tokens'],
            'total_output_tokens': deepseek_data['output_tokens'],
            'total_approx_cost':   deepseek_data['cost'],
            'word_count':          deepseek_data.get('word_count', 0),
            'avg_sentence_length': deepseek_data.get('avg_sentence_length', 0),
            'readability_score':   deepseek_data.get('readability_score', 0),
            'keyword_density':     deepseek_data.get('keyword_density', 0),
        },
        {
            'Model':               'LLaMA 3.3 70B',
            'avg_response_time':   llama_data['time'],
            'total_input_tokens':  llama_data['input_tokens'],
            'total_output_tokens': llama_data['output_tokens'],
            'total_approx_cost':   llama_data['cost'],
            'word_count':          llama_data.get('word_count', 0),
            'avg_sentence_length': llama_data.get('avg_sentence_length', 0),
            'readability_score':   llama_data.get('readability_score', 0),
            'keyword_density':     llama_data.get('keyword_density', 0),
        },
    ]

    d_time, l_time = deepseek_data['time'], llama_data['time']
    if   d_time < l_time:
        stmt = "For this query, DeepSeek R1 was faster."
    elif l_time < d_time:
        stmt = "For this query, LLaMA 3.3 70B was faster."
    else:
        stmt = "Both models performed at the same speed for this query."

    # ── Graph ──
    static_dir = os.path.join(app.root_path, 'static')
    os.makedirs(static_dir, exist_ok=True)

    df       = pd.DataFrame(summary_data)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax1.set_facecolor('#16213e')

    models    = df['Model']
    avg_times = df['avg_response_time']
    bar_width = 0.5
    x         = range(len(models))

    bars = ax1.bar(x, avg_times, width=bar_width,
                   color=['#7B2D8C', '#00d4aa'], label='Response Time (s)', alpha=0.9)
    ax1.set_xlabel('Model', fontsize=12, color='#e0e0e0')
    ax1.set_ylabel('Response Time (s)', color='#c084fc', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#c084fc')
    ax1.tick_params(axis='x', labelcolor='#e0e0e0')
    ax1.set_title(f'Performance: "{user_query[:40]}..."',
                  fontsize=14, weight='bold', color='white', pad=15)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.2f}s',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 6), textcoords="offset points",
                     ha='center', va='bottom', color='white', fontsize=11, fontweight='bold')

    plt.xticks(list(x), models, fontsize=12, color='white')
    for spine in ax1.spines.values():
        spine.set_color('#444')

    ax1.legend(loc='upper right', fontsize=10,
               facecolor='#1a1a2e', labelcolor='white', edgecolor='#444')
    plt.grid(axis='y', linestyle='--', alpha=0.3, color='#888')
    fig.tight_layout()

    ts         = datetime.now().strftime("%Y%m%d_%H%M%S")
    graph_file = f"comparison_{ts}.png"
    plt.savefig(os.path.join(static_dir, graph_file), facecolor=fig.get_facecolor())
    plt.close(fig)

    return jsonify({
        'gemini_response':        deepseek_data['response'],  # key kept same so frontend works
        'groq_response':          llama_data['response'],
        'summary':                summary_data,
        'graph_url':              f'/static/{graph_file}',
        'better_model_statement': stmt,
    })


# -----------------------------------------------------------
if __name__ == '__main__':
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)
    app.run(debug=True)