"""把一份 ETS 试卷的解析结果导出成 .docx 和 .txt。

用法:
    python 导出答案.py [试卷目录] [输出目录]

不传参数时自动从 %APPDATA%\\ETS 里挑最新的一份试卷。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
sys.path.insert(0, str(HERE / "vendor"))

from etsx import extractor, parser, scanner  # noqa: E402
from etsx.models import CATEGORY_TITLES  # noqa: E402


def default_root() -> Path:
    roaming = Path(os.environ.get("APPDATA", Path.home()))
    new = roaming / "ETS"
    if new.is_dir():
        return new
    old = roaming / "74656D705F74656D705F74656D705F74002"
    return old if old.is_dir() else roaming


def pick_paper(root: Path) -> Path:
    papers, _warnings = scanner.scan_root(root)
    if not papers:
        raise SystemExit(f"在 {root} 下没有找到试卷")
    papers.sort(key=lambda entry: entry.path, reverse=True)
    return Path(papers[0].path)


def is_paper_dir(path: Path) -> bool:
    return path.is_dir() and (
        (path / "content2.json").is_file()
        or any(p.is_dir() and p.name.startswith("content") for p in path.iterdir())
    )


def export_docx(paper, out: Path) -> None:
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.add_heading("E听说答案提取", level=0)
    meta = doc.add_paragraph()
    meta.add_run(f"试卷：{paper.name}    编号：{paper.stid or '-'}").font.size = Pt(9)

    for section in paper.sections:
        doc.add_heading(f"{CATEGORY_TITLES.get(section.category, section.title)}", level=1)
        for question in section.questions:
            head = doc.add_paragraph()
            head.add_run(f"第 {question.number} 题").bold = True
            if question.prompt:
                body = doc.add_paragraph(question.prompt)
                body.paragraph_format.space_after = Pt(4)
            if question.keywords:
                doc.add_paragraph(f"关键词：{question.keywords}")
            for index, answer in enumerate(question.answers, 1):
                label = "参考答案" if index == 1 else f"参考{index}"
                para = doc.add_paragraph()
                para.add_run(f"{label}：").bold = True
                para.add_run(answer.text)
                if answer.ai and answer.ai.strip() and answer.ai.strip() != answer.text.strip():
                    para.add_run(f"（AI 改写：{answer.ai.strip()}）")

    doc.save(out)


def main(argv: list[str]) -> int:
    arg1 = Path(argv[1]) if len(argv) > 1 else None
    if arg1 is not None and is_paper_dir(arg1):
        paper_dir = arg1
    elif arg1 is not None:
        paper_dir = pick_paper(arg1)
    else:
        paper_dir = pick_paper(default_root())

    out_dir = Path(argv[2]) if len(argv) > 2 else HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    paper = parser.parse_paper(paper_dir)
    text = extractor.render_text(paper)

    txt_path = out_dir / f"ETS答案_{paper.name}.txt"
    txt_path.write_text(text, encoding="utf-8")
    docx_path = out_dir / f"ETS答案_{paper.name}.docx"
    export_docx(paper, docx_path)

    print(f"试卷目录: {paper_dir}")
    for section in paper.sections:
        print(f"  {CATEGORY_TITLES.get(section.category, section.title)}: {len(section.questions)} 题")
    print(f"TXT : {txt_path} ({txt_path.stat().st_size} B)")
    print(f"DOCX: {docx_path} ({docx_path.stat().st_size} B)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
