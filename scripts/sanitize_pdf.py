#!/usr/bin/env python3.12
"""清除 PDF 文件元数据并随机生成新元数据"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

def random_name():
    surnames = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '高']
    given_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超', '秀兰', '霞', '平']
    return random.choice(surnames) + random.choice(given_names)

def random_title():
    words = ['报告', '文档', '方案', '总结', '计划', '分析', '研究', '手册', '指南', '说明']
    suffix = ['v1.0', 'v2.0', '最终版', '草稿', '正式版', '修订版']
    return random.choice(words) + str(random.randint(1, 999)) + ' ' + random.choice(suffix)

def random_date_years_back(max_years):
    """随机生成过去N年内的日期"""
    days_back = random.randint(1, max_years * 365)
    return (datetime.now() - timedelta(days=days_back)).strftime('D:%Y%m%d%H%M%S')

def random_date_months_back(max_months):
    """随机生成过去N月内的日期"""
    days_back = random.randint(1, max_months * 30)
    return (datetime.now() - timedelta(days=days_back)).strftime('D:%Y%m%d%H%M%S')

def sanitize_pdf(input_path, output_path):
    """清除 PDF 元数据并随机生成新数据"""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"错误: 文件不存在 {input_path}")
        return False

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("错误: 需要 pypdf 库")
        print("安装: pip install pypdf")
        return False

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # 添加新的元数据
        writer.add_metadata({
            '/Author': random_name(),
            '/Title': random_title(),
            '/Subject': random.choice(['商业报告', '技术文档', '市场分析', '项目总结', '']),
            '/Creator': random.choice(['Microsoft Word', 'WPS Office', 'Adobe Acrobat', 'Fiction Writer']),
            '/Producer': random.choice(['Microsoft Word', 'WPS Office', 'Adobe PDF Library']),
            '/CreationDate': random_date_years_back(3),
            '/ModDate': random_date_months_back(6),
        })

        with open(output_path, 'wb') as f:
            writer.write(f)

        print(f"✓ 已处理: {output_path}")
        print(f"  作者: {random_name()}")
        print(f"  标题: {random_title()}")
        return True

    except Exception as e:
        print(f"错误: 处理 PDF 失败 - {e}")
        return False

if __name__ == '__main__':
    # 默认输出目录
    DEFAULT_OUTPUT_DIR = Path.home() / '.openclaw' / 'workspace-daima' / 'skills' / 'docx-pdf-sanitizer' / 'output'
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("用法: python3 sanitize_pdf.py <输入文件.pdf> [输出目录或文件]")
        print(f"  若不指定输出路径，默认输出到: {DEFAULT_OUTPUT_DIR}")
        print("  输出文件名规则: [原文件名] output.pdf")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) == 3:
        output_arg = sys.argv[2]
        output_path = Path(output_arg)
        # 如果输出是目录，则在目录下生成 "原文件名 output.pdf"
        if output_path.is_dir():
            output_file = str(output_path / (Path(input_file).stem + ' output.pdf'))
        else:
            output_file = output_arg
    else:
        # 默认：输出到工作区默认目录
        output_file = str(DEFAULT_OUTPUT_DIR / (Path(input_file).stem + ' output.pdf'))

    success = sanitize_pdf(input_file, output_file)
    sys.exit(0 if success else 1)
