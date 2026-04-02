from fastapi import FastAPI
import gradio as gr

app = FastAPI()

# 🔹 Required endpoint for OpenEnv
@app.post("/reset")
def reset():
    return {"status": "ok"}

# 🔹 Reply generator
def generate_reply(email_text):
    if "meeting" in email_text.lower():
        return "Sure, I will attend the meeting."
    elif "offer" in email_text.lower():
        return "No thanks, I am not interested."
    else:
        return "Thanks for your email. I will get back to you soon."

# 🔹 Main logic
def process_email(email):
    email_lower = email.lower()

    if "urgent" in email_lower:
        category = "🔥 Urgent"
    elif "meeting" in email_lower:
        category = "⭐ Important"
    elif "offer" in email_lower or "win" in email_lower:
        category = "🚨 Spam"
    else:
        category = "📩 Normal"

    reply = generate_reply(email)
    confidence = "High" if category != "📩 Normal" else "Medium"

    return category + f" ({confidence})", reply

# 🔹 Gradio UI
demo = gr.Interface(
    fn=process_email,
    inputs=gr.Textbox(lines=5, placeholder="Paste your email here..."),
    outputs=[
        gr.Textbox(label="📌 Category"),
        gr.Textbox(label="💬 Suggested Reply")
    ],
    title="🚀 Smart Email AI Assistant",
    description="AI-powered system that classifies emails and generates smart replies to improve productivity."
)

# 🔹 Mount Gradio inside FastAPI
app = gr.mount_gradio_app(app, demo, path="/ui")

# 🔹 Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
