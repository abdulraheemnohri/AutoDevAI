from ai_engine.router import generate

def summarize_text(text):
    """Summarizes a given text concisely using an AI model."""
    if not text or len(text.strip()) == 0:
        return "No text provided to summarize."

    prompt = f"Please summarize the following text concisely, focusing on the most important points and any technical details:\n\n{text}"

    # Use the 'summarize' command to trigger the Researcher agent
    try:
        summary = generate(prompt, command="summarize")
        return summary
    except Exception as e:
        print(f"❌ Error during AI summarization: {e}")
        # Fallback to a very simple truncation if AI fails
        return f"(Fallback) {text[:200]}..."

def summarize_knowledge_item(item_id):
    """Fetches a knowledge item from the database and summarizes it."""
    import sqlite3
    from backend.config import DATABASE_PATH

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("SELECT content FROM knowledge WHERE id = ?", (item_id,))
        row = c.fetchone()
        conn.close()

        if row:
            return summarize_text(row[0])
        else:
            return "Knowledge item not found."
    except Exception as e:
        print(f"❌ Error fetching knowledge for summarization: {e}")
        return "Error summarizing knowledge."
