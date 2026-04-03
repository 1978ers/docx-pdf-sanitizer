#!/usr/bin/env python3
"""清除 DOCX 文件元数据并随机生成新元数据"""

import sys
import zipfile
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

# 随机数据源
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '高']
GIVEN_NAMES = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超', '秀兰', '霞', '平']
TITLE_WORDS = ['报告', '文档', '方案', '总结', '计划', '分析', '研究', '手册', '指南', '说明', '记录', '档案', '资料', '数据', '信息']
TITLE_SUFFIX = ['v1.0', 'v2.0', '最终版', '草稿', '正式版', '2024', '2025', '修订版']

def random_name():
    return random.choice(SURNAMES) + random.choice(GIVEN_NAMES)

def random_title():
    return random.choice(TITLE_WORDS) + str(random.randint(1, 999)) + ' ' + random.choice(TITLE_SUFFIX)

def random_date_years_back(max_years):
    """随机生成过去N年内的日期"""
    days_back = random.randint(1, max_years * 365)
    return (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

def random_date_months_back(max_months):
    """随机生成过去N月内的日期"""
    days_back = random.randint(1, max_months * 30)
    return (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

def sanitize_docx(input_path, output_path):
    """清除 DOCX 元数据并随机生成新数据"""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        print(f"错误: 文件不存在 {input_path}")
        return False

    # 创建临时目录
    temp_dir = input_path.parent / f'.temp_{input_path.stem}'
    temp_dir.mkdir(exist_ok=True)

    try:
        # 解压 DOCX
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 定义 core.xml 命名空间
        namespaces = {
            'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'dcterms': 'http://purl.org/dc/terms/',
            'dcmitype': 'http://purl.org/dc/dcmitype/',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

        # 处理 core.xml
        core_xml_path = temp_dir / 'docProps' / 'core.xml'
        if core_xml_path.exists():
            tree = ET.parse(core_xml_path)
            root = tree.getroot()

            # 清除所有元数据
            for elem in list(root):
                root.remove(elem)

            # 添加随机元数据
            root.set('xmlns:cp', namespaces['cp'])
            root.set('xmlns:dc', namespaces['dc'])
            root.set('xmlns:dcterms', namespaces['dcterms'])
            root.set('xmlns:dcmitype', namespaces['dcmitype'])
            root.set('xmlns:xsi', namespaces['xsi'])

            # dc:creator
            creator = ET.SubElement(root, '{http://purl.org/dc/elements/1.1/}creator')
            creator.text = random_name()

            # dc:title
            title = ET.SubElement(root, '{http://purl.org/dc/elements/1.1/}title')
            title.text = random_title()

            # dcterms:created
            created = ET.SubElement(root, '{http://purl.org/dc/terms/}created')
            created.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'dcterms:W3CDTF')
            created.text = random_date_years_back(3)

            # dcterms:modified
            modified = ET.SubElement(root, '{http://purl.org/dc/terms/}modified')
            modified.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'dcterms:W3CDTF')
            modified.text = random_date_months_back(6)

            # cp:lastModifiedBy
            last_mod = ET.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy')
            last_mod.text = random_name()

            # cp:revision
            revision = ET.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}revision')
            revision.text = str(random.randint(1, 20))

            tree.write(core_xml_path, encoding='UTF-8', xml_declaration=True)

        # 处理 app.xml
        app_xml_path = temp_dir / 'docProps' / 'app.xml'
        if app_xml_path.exists():
            tree = ET.parse(app_xml_path)
            root = tree.getroot()

            root.set('xmlns', 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties')

            # 清除所有子元素
            for elem in list(root):
                root.remove(elem)

            # 添加随机数据
            props = {
                'Application': random.choice(['Microsoft Word', 'WPS Office', 'Google Docs']),
                'AppVersion': f'{random.randint(10,20)}.0.{random.randint(1000,9999)}',
                'Company': random.choice(['', '有限公司', '集团', '工作室']),
                'Manager': random_name(),
            }

            for key, value in props.items():
                elem = ET.SubElement(root, key)
                elem.text = value

            tree.write(app_xml_path, encoding='UTF-8', xml_declaration=True)

        # 重新打包为 DOCX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)

        print(f"✓ 已处理: {output_path}")
        print(f"  作者: {random_name()}")
        print(f"  标题: {random_title()}")
        return True

    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    # 默认输出目录
    DEFAULT_OUTPUT_DIR = Path.home() / '.openclaw' / 'workspace-daima' / 'skills' / 'docx-pdf-sanitizer' / 'output'
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("用法: python3 sanitize_docx.py <输入文件.docx> [输出目录或文件]")
        print(f"  若不指定输出路径，默认输出到: {DEFAULT_OUTPUT_DIR}")
        print("  输出文件名规则: [原文件名] output.docx")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) == 3:
        output_arg = sys.argv[2]
        output_path = Path(output_arg)
        # 如果输出是目录，则在目录下生成 "原文件名 output.docx"
        if output_path.is_dir():
            output_file = str(output_path / (Path(input_file).stem + ' output.docx'))
        else:
            output_file = output_arg
    else:
        # 默认：输出到工作区默认目录
        output_file = str(DEFAULT_OUTPUT_DIR / (Path(input_file).stem + ' output.docx'))

    success = sanitize_docx(input_file, output_file)
    sys.exit(0 if success else 1)
