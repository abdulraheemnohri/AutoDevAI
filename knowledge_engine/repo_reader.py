import os
import sqlite3
from backend.config import DATABASE_PATH

def read_repo_knowledge(repo_path):
    """Read README files and documentation from a repository to build knowledge."""
    print(f"📚 Reading repository knowledge from: {repo_path}")
    
    knowledge_items = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.lower() in ["readme.md", "readme.txt", "docs.md", "contributing.md"]:
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    knowledge_items.append({
                        "source": file_path,
                        "content": content,
                        "tags": "documentation"
                    })
                    
    # Store in database
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    for item in knowledge_items:
        c.execute("""
            INSERT INTO knowledge (source, content, tags)
            VALUES (?, ?, ?)
        """, (item["source"], item["content"], item["tags"]))
        
    conn.commit()
    conn.close()
    print(f"✅ Repository knowledge stored in database ({len(knowledge_items)} items).")
