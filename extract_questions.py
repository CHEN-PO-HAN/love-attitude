from pathlib import Path
import json
import re

DOC_PATH = Path("ch01/愛情態度量表.docx")

def main():
    data = DOC_PATH.read_bytes()
    text = data.decode("utf-16le", errors="ignore")
    text = re.sub(r"[\r\x00]", "", text)
    pattern = re.compile(r"1  2  3  4  5\s*(\d+)(.*?)(?=1  2  3  4  5|$)", re.S)
    items = pattern.findall(text)
    print(f"Found {len(items)} items")
    cleaned = {}
    for num, body in items:
        body = re.sub(r"SHAPE .*?FORMAT", "", body, flags=re.IGNORECASE | re.DOTALL)
        body = " ".join(body.split())
        body = body.lstrip(". ")
        if "。" in body:
            body = body.split("。", 1)[0] + "。"
        cleaned[int(num)] = body

    cleaned[33] = "我享受和他/她及一些不同的情人玩愛情遊戲。"

    questions = [cleaned.get(index, "") for index in range(1, 37)]
    Path("questions.json").write_text(
        json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    snippet_lines = []
    for idx, text in enumerate(questions, 1):
        snippet_lines.append('<div class="question">')
        snippet_lines.append(f"  <p>第 {idx} 題：{text}</p>")
        snippet_lines.append('  <div class="options">')
        for value in range(1, 6):
            required = " required" if value == 1 else ""
            snippet_lines.append(
                f'    <label><input type="radio" name="q{idx}" value="{value}"{required}> {value}</label>'
            )
        snippet_lines.append('  </div>')
        snippet_lines.append('</div>')
    Path("questions.html.snippet").write_text("\n".join(snippet_lines), encoding="utf-8")
    print(json.dumps(questions, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
