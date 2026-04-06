import os
import sqlite3
from backend.config import DATABASE_PATH

def read_repo_knowledge(repo_path):
    """Recursively scan for Markdown and documentation files to build repository knowledge."""
    print(f"📚 Reading repository knowledge from: {repo_path}")
    
    knowledge_items = []
    
    # Supported documentation file extensions
    doc_extensions = [".md", ".txt", ".rst", ".doc"]
    # Common documentation file names (case-insensitive)
    doc_filenames = ["readme", "contributing", "license", "docs", "changelog", "security"]

    for root, _, files in os.walk(repo_path):
        for file in files:
            file_name_lower = file.lower()
            file_ext = os.path.splitext(file_name_lower)[1]

            # Check if file is a markdown file or a recognized doc file
            is_doc = any(name in file_name_lower for name in doc_filenames) or file_ext in [".md", ".rst"]

            if is_doc and file_ext in doc_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        # Simple tag extraction (e.g., from directory name)
                        tag = os.path.basename(root) if root != repo_path else "root"
                        knowledge_items.append({
                            "source": file_path,
                            "content": content,
                            "tags": f"documentation,{tag}"
                        })
                except Exception as e:
                    print(f"⚠️ Error reading doc file {file_path}: {e}")
                    
    # Store in database
    if knowledge_items:
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()

            for item in knowledge_items:
                # Use REPLACE or check existence to avoid duplicates
                c.execute("""
                    INSERT OR REPLACE INTO knowledge (source, content, tags)
                    VALUES (?, ?, ?)
                """, (item["source"], item["content"], item["tags"]))

            conn.commit()
            conn.close()
            print(f"✅ Repository knowledge stored in database ({len(knowledge_items)} items).")
        except Exception as e:
            print(f"❌ Error storing knowledge in database: {e}")
    else:
        print("ℹ️ No documentation files found to index.")
