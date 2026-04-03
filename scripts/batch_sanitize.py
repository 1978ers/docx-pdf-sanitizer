#!/usr/bin/env python3
"""批量处理目录下所有 DOCX 和 PDF 文件"""

import sys
import os
import shutil
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def get_output_path(input_path, suffix='_sanitized'):
    """生成输出文件路径"""
    p = Path(input_path)
    return p.parent / f'{p.stem}{suffix}{p.suffix}'

def process_file(input_path):
    """根据文件类型处理"""
    p = Path(input_path)
    output_path = get_output_path(input_path)

    if p.suffix.lower() == '.docx':
        from sanitize_docx import sanitize_docx
        return sanitize_docx(input_path, output_path)
    elif p.suffix.lower() == '.pdf':
        from sanitize_pdf import sanitize_pdf
        return sanitize_pdf(input_path, output_path)
    else:
        print(f"跳过 (不支持的格式): {input_path}")
        return False

def batch_sanitize(directory):
    """批量处理目录下的所有 DOCX 和 PDF 文件"""
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        print(f"错误: 目录不存在 {directory}")
        return

    # 收集所有文件
    files = []
    for ext in ['*.docx', '*.pdf']:
        files.extend(dir_path.glob(ext))
        files.extend(dir_path.glob(ext.upper()))

    if not files:
        print(f"在 {directory} 中未找到 DOCX 或 PDF 文件")
        return

    print(f"找到 {len(files)} 个文件待处理\n")

    success_count = 0
    fail_count = 0

    for file_path in sorted(files):
        print(f"处理: {file_path.name}")
        if process_file(file_path):
            success_count += 1
        else:
            fail_count += 1
        print()

    print(f"完成! 成功: {success_count}, 失败: {fail_count}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 batch_sanitize.py <目录路径>")
        sys.exit(1)

    batch_sanitize(sys.argv[1])
