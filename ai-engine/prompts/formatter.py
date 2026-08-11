"""
Prompt export formatter converting output into Markdown, JSON, and plain TXT files.
"""
import json
from typing import Dict, Any

class PromptFormatter:
    @staticmethod
    def to_markdown(task_id: str, analysis: Dict[str, Any], prompts: Dict[str, str]) -> str:
        md = f"# 🎬 Video-to-Prompt Analysis Report (Task: `{task_id}`)\n\n"
        md += "## 👁️ Visual Feature Breakdown\n\n"
        md += f"- **Subject**: {analysis.get('subject')}\n"
        md += f"- **Action / Motion**: {analysis.get('action')}\n"
        md += f"- **Environment / Setting**: {analysis.get('environment')}\n"
        md += f"- **Lighting Style**: {analysis.get('lighting')}\n"
        md += f"- **Emotional Mood**: {analysis.get('mood')}\n\n"
        
        md += "## 🎨 Generated Target Prompts\n\n"
        for key, prompt in prompts.items():
            title = key.replace("_", " ").title()
            md += f"### {title}\n```text\n{prompt}\n```\n\n"
            
        return md

    @staticmethod
    def to_json(task_id: str, analysis: Dict[str, Any], prompts: Dict[str, str]) -> str:
        return json.dumps({
            "task_id": task_id,
            "analysis": analysis,
            "prompts": prompts
        }, indent=2)

    @staticmethod
    def to_txt(prompts: Dict[str, str]) -> str:
        txt = ""
        for key, prompt in prompts.items():
            txt += f"=== {key.upper()} PROMPT ===\n{prompt}\n\n"
        return txt
