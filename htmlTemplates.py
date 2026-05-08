import base64


def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Encode avatar images
bot_img = get_base64("ai.png")
user_img = get_base64("user.png")


# -------------------------------------------------------------------
#  Streamlit theme‑aware CSS with polished UI
# -------------------------------------------------------------------
css = """
<style>
    /* Global font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Title & subtitle */
    .title-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 10px;
    }
    .title-container h1 {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4f8cff;
        margin-top: -5px;
        margin-bottom: 1.5rem;
    }

    /* Chat message bubbles (dark backgrounds, white text) */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        width: 78px;
        height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Sidebar – theme‑aware */
    section[data-testid="stSidebar"] {
        background: var(--secondary-background-color);
        border-right: 1px solid var(--border-color-light, #e0e0e0);
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .css-1d391kg,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: var(--text-color);
    }

    /* File uploader – dotted border */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        border: 2px dotted #cbd5e1;
        border-radius: 12px;
        padding: 12px;
        background: var(--secondary-background-color);
    }

    /* Process button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(110, 142, 251, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(110, 142, 251, 0.5);
    }
    div.stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 6px rgba(110, 142, 251, 0.4);
    }

    /* "How it Works" card */
    .how-it-works {
        background: var(--primary-background-color);
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1.5rem;
        border: 1px solid var(--border-color-light, rgba(0,0,0,0.1));
    }
    .how-it-works h3 {
        margin-top: 0;
        font-weight: 600;
        color: var(--text-color);
    }
    .how-it-works ol {
        padding-left: 1.2rem;
        margin-bottom: 0;
    }
    .how-it-works li {
        margin-bottom: 0.6rem;
        color: var(--text-color);
        opacity: 0.85;
        line-height: 1.5;
    }
    .how-it-works li::marker {
        color: #a777e3;
        font-weight: bold;
    }

    /* Input field */
    [data-testid="stTextInput"] input {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 1rem;
    }

    /* Prompt label – larger, darkish but theme‑friendly */
    [data-testid="stTextInput"] label {
        font-size: 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
        opacity: 0.85;
        margin-bottom: 6px;
        letter-spacing: 0.3px;
    }
</style>
"""


# Chat message templates
bot_template = f'''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/png;base64,{bot_img}">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/png;base64,{user_img}">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''