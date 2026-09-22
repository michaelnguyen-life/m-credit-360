import io
import re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clear hardcoded files in eb-docs-list
docs_list_start = html.find('<div id="eb-docs-list" class="space-y-2 text-xs">')
docs_list_end = html.find('</div>', html.find('Ho_so_TSBD.docx', docs_list_start)) + 6
# Actually let's just use regex to replace everything inside eb-docs-list up to the </button>
docs_list_empty = '<div id="eb-docs-list" class="space-y-2 text-xs">\n              <!-- Files will be injected here -->\n            </div>'
# wait, better to just string slice
target1 = html[docs_list_start:docs_list_end]
if 'Ho_so_TSBD.docx' in target1:
    html = html.replace(target1, docs_list_empty)

# 2. Add Box 2: M-CREDIT AI Insight below Box 1
box1_end = html.find('</p>\n          </div>', docs_list_start) + 19
box2_html = '''
          <!-- Box 2: M-CREDIT AI Insight -->
          <div id="ai-insight-box" class="executive-card p-3.5 space-y-2.5 hidden">
            <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
              <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                <i data-lucide="sparkles" class="w-4 h-4 text-[#FF5A00]"></i>
                <span>M-CREDIT AI Insight</span>
              </span>
              <span class="text-[9px] px-1.5 py-0.5 rounded bg-orange-100 text-[#FF5A00] font-bold">Mới</span>
            </div>

            <div id="ai-insight-content" class="space-y-3 pt-1">
              <!-- AI insights will be injected here -->
            </div>

            <!-- Copilot Action Buttons -->
            <div class="grid grid-cols-2 gap-1.5 pt-2 border-t border-[#E6EAF0]">
              <button onclick="triggerAICopilot('Giải thích chi tiết các chỉ số tài chính yếu kém')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Giải thích
              </button>
              <button onclick="triggerAICopilot('Chạy kịch bản Stress Test dòng tiền nếu doanh thu giảm 15%')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Stress Test
              </button>
              <button onclick="exportDocxMemo()" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Soạn tờ trình
              </button>
              <button onclick="triggerAICopilot('Phân tích sâu rủi ro đòn bẩy và kiểm soát dòng tiền Rule 5D')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Phân tích sâu
              </button>
            </div>
          </div>
'''
if 'id="ai-insight-box"' not in html:
    html = html[:box1_end] + box2_html + html[box1_end:]

# 3. Update JS to populate Box 1 and Box 2
# Add to confirmNewCustomerSession:
clear_js = "document.getElementById('eb-docs-list').innerHTML = '<div class=\"p-3 text-center text-slate-400 text-[10px] border border-dashed rounded-lg\">Chưa có tài liệu nào</div>'; document.getElementById('ai-insight-box').classList.add('hidden');"
html = html.replace("document.getElementById('eb-ca').value = '0';", "document.getElementById('eb-ca').value = '0';\n      " + clear_js)

# Add to runEBAssessment:
insight_js = '''
        // Render AI Insight (SWOT)
        const swot = data.swot_analysis;
        if (swot) {
            const insightBox = document.getElementById('ai-insight-box');
            const insightContent = document.getElementById('ai-insight-content');
            insightBox.classList.remove('hidden');
            
            let swotHtml = '';
            if (swot.strengths && swot.strengths.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-green-700">Điểm mạnh (Strengths):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.strengths.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.weaknesses && swot.weaknesses.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-red-600">Điểm yếu (Weaknesses):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.weaknesses.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.opportunities && swot.opportunities.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-blue-600">Cơ hội (Opportunities):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.opportunities.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.threats && swot.threats.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-orange-600">Rủi ro (Threats):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.threats.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            
            insightContent.innerHTML = swotHtml;
            lucide.createIcons();
        }
'''
# inject into runEBAssessment just after setting cross-sell totalDeal
target_js = "document.getElementById('eb-cross-total').textContent = `Quy mô: ${(totalDeal / 1000000000).toFixed(1)} Tỷ`;"
if 'Render AI Insight (SWOT)' not in html:
    html = html.replace(target_js, target_js + '\n' + insight_js)


with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
