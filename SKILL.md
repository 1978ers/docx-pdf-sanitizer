---
name: docx-pdf-sanitizer
description: 清除 DOCX 和 PDF 文件的元数据（作者、创建时间、修改时间等），并随机生成新的元数据。用于隐私保护、文档脱敏等场景。当用户提到去除文档元数据、清除文档属性、文档脱敏、随机生成文档作者/日期时触发。
---

# DOCX/PDF 元数据清除与随机化

## 功能

- 清除 DOCX/PDF 文件中的所有元数据
- 随机生成新的元数据（作者、标题、创建日期、修改日期等）
- 支持批量处理

## 使用方式

### 单文件处理

```bash
# 处理 DOCX（不指定输出路径时，自动输出到工作区 output 目录，文件名规则：原文件名 output.docx）
python3 /home/dell/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/scripts/sanitize_docx.py input.docx

# 指定输出目录
python3 /home/dell/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/scripts/sanitize_docx.py input.docx /path/to/output_dir/

# 指定完整输出路径
python3 /home/dell/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/scripts/sanitize_docx.py input.docx /path/to/custom_name.docx

# 处理 PDF
python3 /home/dell/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/scripts/sanitize_pdf.py input.pdf output.pdf
```

### 批量处理

```bash
python3 /home/dell/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/scripts/batch_sanitize.py /path/to/files/
```

## 输出位置

- **默认输出目录**: `~/.openclaw/workspace-daima/skills/docx-pdf-sanitizer/output/`
- **默认文件名规则**: `[原文件名] output.docx`
  - 例如: `报告.docx` → `报告 output.docx`

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `sanitize_docx.py` | 处理 DOCX 文件 |
| `sanitize_pdf.py` | 处理 PDF 文件 |
| `batch_sanitize.py` | 批量处理目录下所有 DOCX/PDF |

## DOCX 元数据清除逻辑

1. 解压 DOCX（本质是 ZIP）
2. 清空 `docProps/core.xml`（作者、标题、主题、关键词等）
3. 清空 `docProps/app.xml`（应用程序信息）
4. 随机生成新元数据并写入
5. 重新打包为 DOCX

## PDF 元数据清除逻辑

使用 `pypdf` 库：
1. 读取 PDF
2. 调用 `add_metadata({})` 覆盖空元数据
3. 随机生成新元数据
4. 保存

## 随机元数据生成规则

- **作者**: 随机中文姓名
- **标题**: 随机词汇组合
- **创建日期**: 随机过去3年内的日期
- **修改日期**: 随机过去1年内的日期
- **Producer/Creator**: 随机生成
