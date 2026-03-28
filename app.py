import gradio as gr
from gtts import gTTS
from groq import Groq
import os
import tempfile
from pydub import AudioSegment

# 1. API Setup
GROQ_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_KEY)

# 2. System Prompt (fallback only)
system_prompt = """
You are Thrisha Karkera in a job interview. Speak in first person always.
RULES:
- Answer ONLY what was asked in 2-3 sentences maximum.
- NEVER introduce yourself unless directly asked.
- NEVER mention your name, university, or CGPA unless directly asked.
- NEVER say things like "I am here for the interview" or "please go ahead".
- NEVER ask "what would you like to know".
- If the input is unclear or just one word, say: "Sorry, I did not catch that. Could you please repeat the question?"
- Be direct, confident and specific.
"""

# 3. Scripted Answers — only introduce yourself mentions Thrisha and BCA
SCRIPTED_ANSWERS = {
    # ONLY THESE 2 mention Thrisha + BCA
    "tell me about yourself":  "I am Thrisha Karkera, a final-year BCA student at St Aloysius University with an 8.19 CGPA. I specialize in Python and AI development and have built hands-on projects like a Hand Gesture Controlled Mouse. I am looking to bring that practical experience to a real AI engineering team.",
    "introduce yourself":      "I am Thrisha Karkera, a final-year BCA student specializing in Python and Generative AI. I have built real projects including a Hand Gesture Mouse and this AI voice agent you are talking to right now.",

    # ALL BELOW — no name, no university, no CGPA
    "life story":        "I am an aspiring Generative AI Engineer currently completing my BCA at St Aloysius University. My technical journey is defined by a rapid transition from core programming to building AI-native workflows. By combining my academic excellence (8.19 CGPA) with hands-on projects like an OpenCV-based Gesture Control system, I am now focused on mastering autonomous agent architectures and large language model integration.",
    "superpower":        "My superpower is practical problem-solving .I do not just study concepts, I build things. I proved this by independently creating a Hand Gesture Controlled Mouse using Python and OpenCV completely from scratch.",
    "growth areas":      "I want to grow in three areas — autonomous AI agent design, production-level web deployment, and advanced NLP workflows. These are gaps I have identified and I am already closing them through personal projects.",
    "misconception":     "People assume I need constant direction because I am still a student. In reality I am extremely self-directed — most of what I know I taught myself completely outside the classroom.",
    "push boundaries":   "I push my limits by refusing to choose between academic excellence and self-taught technical skills. That constant tension between the two is exactly what keeps me growing every day.",
    "why should we hire": "Because I do not just learn AI — I build with it. I have already shipped a gesture-controlled interface and this voice AI agent you are speaking to right now. I take full ownership and deliver results.",
    "weakness":          "I sometimes over-polish a project before sharing it. I am actively working on shipping faster and gathering feedback earlier instead of waiting until everything feels perfect.",
    "experience":        "I have built a Hand Gesture Controlled Mouse using Python and OpenCV, a manufacturing seller interface, and this voice-enabled AI interview agent. Each project pushed me into completely new territory.",
    "skills":            "My core skills are Python, Gradio, OpenCV, and working with LLMs through APIs like Groq. I also hold certifications in Data Science, NLP, and Computer Vision.",
    "goal":              "My goal is to become a full-stack AI engineer who can design, build, and deploy autonomous agents end to end. This role at 100x is exactly that opportunity.",
    "salary":            "I am open to discussing compensation based on the role. My priority right now is finding the right team where I can grow fast and make a real impact.",
    "where do you see":  "In five years I see myself leading the architecture of AI agent systems, not just contributing to them. I want to design the overall system and mentor engineers coming up behind me.",
}

# 4. Smart Matcher
def find_scripted_answer(user_text):
    user_lower = user_text.lower().strip()
    print(f"DEBUG - Matching against: '{user_lower}'")

    # Life story
    if any(p in user_lower for p in [
        "life story", "what should we know", "know about your life",
        "in a few sentences", "tell us your story", "your story",
        "few sentences", "about your life"
    ]):
        print("DEBUG - Matched: life story")
        return SCRIPTED_ANSWERS["life story"]

    # Superpower
    if any(p in user_lower for p in [
        "superpower", "super power", "number 1", "#1", "number one",
        "what's your", "whats your", "your superpower", "your super power",
        "greatest strength", "biggest strength", "top strength", "best quality",
        "what do you bring", "special ability", "stand out", "unique skill",
        "super", "power", "strength", "strong", "best at", "good at"
    ]):
        print("DEBUG - Matched: superpower")
        return SCRIPTED_ANSWERS["superpower"]

    # Growth areas
    if any(p in user_lower for p in [
        "top 3", "three areas", "3 areas", "areas you'd like to grow",
        "areas you would like", "grow in", "growth areas", "areas of growth",
        "want to grow", "like to grow", "areas to improve", "areas to develop",
        "grow", "growth", "improve", "development", "get better", "learning goals"
    ]):
        print("DEBUG - Matched: growth areas")
        return SCRIPTED_ANSWERS["growth areas"]

    # Misconception
    if any(p in user_lower for p in [
        "misconception", "coworkers have about you", "colleagues think",
        "people think about you", "others think", "misunderstand you",
        "wrong about you", "assume about you", "think about you",
        "coworker", "colleague", "people think", "assume"
    ]):
        print("DEBUG - Matched: misconception")
        return SCRIPTED_ANSWERS["misconception"]

    # Push boundaries
    if any(p in user_lower for p in [
        "push your boundaries", "push your limits", "boundaries and limits",
        "how do you push", "push yourself", "challenge yourself",
        "overcome limits", "go beyond", "extra mile", "comfort zone",
        "push", "boundary", "boundaries", "limits", "limit", "overcome"
    ]):
        print("DEBUG - Matched: push boundaries")
        return SCRIPTED_ANSWERS["push boundaries"]

    # Tell me about yourself
    if any(p in user_lower for p in [
        "tell me about yourself", "tell me about you",
        "about yourself", "describe yourself", "your self", "about you"
    ]):
        print("DEBUG - Matched: tell me about yourself")
        return SCRIPTED_ANSWERS["tell me about yourself"]

    # Introduce yourself
    if any(p in user_lower for p in [
        "introduce yourself", "introduction", "who are you"
    ]):
        print("DEBUG - Matched: introduce yourself")
        return SCRIPTED_ANSWERS["introduce yourself"]

    # Why hire
    if any(p in user_lower for p in [
        "why should we hire", "why hire you", "why you",
        "choose you", "pick you", "why 100x", "why this role"
    ]):
        print("DEBUG - Matched: why should we hire")
        return SCRIPTED_ANSWERS["why should we hire"]

    # Weakness
    if any(p in user_lower for p in [
        "weakness", "weak point", "struggle", "not good at",
        "fail", "challenge for you", "difficult for you"
    ]):
        print("DEBUG - Matched: weakness")
        return SCRIPTED_ANSWERS["weakness"]

    # Experience
    if any(p in user_lower for p in [
        "experience", "project", "built", "worked on",
        "created", "developed", "made"
    ]):
        print("DEBUG - Matched: experience")
        return SCRIPTED_ANSWERS["experience"]

    # Skills
    if any(p in user_lower for p in [
        "skill", "technology", "tech stack", "tools",
        "languages", "frameworks", "python", "technical"
    ]):
        print("DEBUG - Matched: skills")
        return SCRIPTED_ANSWERS["skills"]

    # Goal
    if any(p in user_lower for p in [
        "goal", "ambition", "dream", "aspire",
        "future plan", "career", "want to achieve"
    ]):
        print("DEBUG - Matched: goal")
        return SCRIPTED_ANSWERS["goal"]

    # Salary
    if any(p in user_lower for p in [
        "salary", "pay", "compensation", "money", "package", "ctc"
    ]):
        print("DEBUG - Matched: salary")
        return SCRIPTED_ANSWERS["salary"]

    # Future
    if any(p in user_lower for p in [
        "five years", "5 years", "see yourself", "long term", "vision"
    ]):
        print("DEBUG - Matched: where do you see")
        return SCRIPTED_ANSWERS["where do you see"]

    print("DEBUG - No match found, using LLaMA fallback")
    return None

# 5. Audio Conversion
def convert_to_wav(audio_filepath):
    audio = AudioSegment.from_file(audio_filepath)
    audio = audio.set_frame_rate(16000).set_channels(1)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

# 6. Core Logic
def process_interview(audio_filepath, history):
    if not audio_filepath:
        return None, "⚠️ Please record a question first.", history

    try:
        # Step 1: Transcribe with Groq Whisper
        converted_path = convert_to_wav(audio_filepath)
        with open(converted_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                response_format="text"
            )
        user_text = transcription.strip()
        print(f"DEBUG - Transcribed question: '{user_text}'")

        if not user_text:
            return None, "❌ Couldn't hear clearly. Please try again.", history

        # Step 2: Try scripted answer first
        bot_answer = find_scripted_answer(user_text)

        # Step 3: LLaMA fallback for unscripted questions
        if not bot_answer:
            print("DEBUG - Using LLaMA fallback")
            messages = [{"role": "system", "content": system_prompt}]
            for h in history:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
            messages.append({"role": "user", "content": user_text})

            chat_response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=120
            )
            bot_answer = chat_response.choices[0].message.content

        print(f"DEBUG - Final answer: '{bot_answer}'")

        # Step 4: Update history
        history.append((user_text, bot_answer))

        # Step 5: Text to Speech
        tts = gTTS(text=bot_answer, lang='en')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        return temp_file.name, f"**🎤 You:** {user_text}\n\n**🤖 Thrisha:** {bot_answer}", history

    except Exception as e:
        print(f"DEBUG - Error: {str(e)}")
        return None, f"❌ Error: {str(e)}", history

# 7. Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Thrisha Karkera — AI Interview Agent")
    gr.Markdown("Click 'Record', ask your question, then click 'Submit'.")

    history_state = gr.State([])

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Speak to Thrisha"
            )
            submit_btn = gr.Button("Submit Question", variant="primary")
            clear_btn = gr.Button("Clear")

        with gr.Column():
            audio_output = gr.Audio(label="🔊 Response Audio", autoplay=True)
            text_output = gr.Markdown()

    submit_btn.click(
        fn=process_interview,
        inputs=[audio_input, history_state],
        outputs=[audio_output, text_output, history_state]
    )

    clear_btn.click(
        lambda: (None, None, "", []),
        None,
        [audio_input, audio_output, text_output, history_state]
    )

demo.launch()
