"""
测试结果报告生成器
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, test_results: List[Dict], output_path: str = None) -> str:
        """生成HTML格式的测试报告"""
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = self.log_dir / f"test_report_{timestamp}.html"
        
        passed = sum(1 for r in test_results if r["passed"])
        failed = sum(1 for r in test_results if not r["passed"])
        total = len(test_results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>灵犀·晓伴测试报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .summary {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 20px;
            background-color: #f0f0f0;
            border-radius: 8px;
        }}
        .summary-item {{
            text-align: center;
        }}
        .summary-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .total {{ color: #666; }}
        .passed {{ color: #4CAF50; }}
        .failed {{ color: #f44336; }}
        .pass-rate {{
            color: #2196F3;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .status-pass {{
            background-color: #4CAF50;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .status-fail {{
            background-color: #f44336;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>灵犀·晓伴自动化测试报告</h1>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-value total">{total}</div>
                <div>总测试数</div>
            </div>
            <div class="summary-item">
                <div class="summary-value passed">{passed}</div>
                <div>通过</div>
            </div>
            <div class="summary-item">
                <div class="summary-value failed">{failed}</div>
                <div>失败</div>
            </div>
            <div class="summary-item">
                <div class="summary-value pass-rate">{pass_rate:.1f}%</div>
                <div>通过率</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>测试名称</th>
                    <th>状态</th>
                    <th>消息</th>
                    <th>时间</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in test_results:
            status_class = "status-pass" if result["passed"] else "status-fail"
            status_text = "PASS" if result["passed"] else "FAIL"
            
            html += f"""
                <tr>
                    <td>{result['name']}</td>
                    <td><span class="{status_class}">{status_text}</span></td>
                    <td>{result.get('message', '')}</td>
                    <td>{result.get('timestamp', '')}</td>
                </tr>
"""
        
        html += f"""
            </tbody>
        </table>
        
        <div class="timestamp">
            报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_path)
    
    def generate_json_report(self, test_results: List[Dict], output_path: str = None) -> str:
        """生成JSON格式的测试报告"""
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = self.log_dir / f"test_report_{timestamp}.json"
        
        passed = sum(1 for r in test_results if r["passed"])
        failed = sum(1 for r in test_results if not r["passed"])
        total = len(test_results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        report = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": round(pass_rate, 2)
            },
            "results": test_results,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return str(output_path)
    
    def generate_all_reports(self, test_results: List[Dict]):
        """生成所有格式的报告"""
        html_path = self.generate_html_report(test_results)
        json_path = self.generate_json_report(test_results)
        
        print(f"\n测试报告已生成:")
        print(f"  HTML报告: {html_path}")
        print(f"  JSON报告: {json_path}")
        
        return html_path, json_path
