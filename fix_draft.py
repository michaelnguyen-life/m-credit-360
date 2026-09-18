# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''                if (draft.taxId) {
                    document.getElementById('eb-empty-state')?.classList.add('hidden');

            

                if (csContainer) {
                    csContainer.innerHTML = 
                    <div class="p-2.5 rounded-lg bg-orange-50 border border-orange-100 relative overflow-hidden group hover:shadow-md transition">
                      <div class="absolute right-0 top-0 bg-orange-200 text-[#FF5A00] text-[8px] px-1.5 py-0.5 rounded-bl-lg font-bold">HOT</div>
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">TAi tr Phi thu (Q?.039)</span>
                        <span class="text-[8px] px-1 rounded bg-orange-100 text-[#FF5A00] font-bold">P1</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Ti u dAng ti?n phi thu</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~  T</span>
                    </div>
                    <div class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-100 relative hover:shadow-md transition">
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">TAi tr SCF / LC</span>
                        <span class="text-[8px] px-1 rounded bg-emerald-100 text-[#027A48] font-bold">P2</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Thanh toAn chu-i cung cng</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~  T</span>
                    </div>
                    <div class="p-2.5 rounded-lg bg-blue-50 border border-blue-100 relative hover:shadow-md transition">
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">Bo lAnh Quc t</span>
                        <span class="text-[8px] px-1 rounded bg-blue-100 text-[#175CD3] font-bold">P3</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Giao d<ch xuyAn biAn gi>i</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~  T</span>
                    </div>;
                }
            } catch(e) { console.error("Cross-sell update failed:", e); }

                    document.getElementById('eb-results-container')?.classList.remove('hidden');
                }'''

replacement = '''                if (draft.taxId) {
                    document.getElementById('eb-empty-state')?.classList.add('hidden');
                    document.getElementById('eb-results-container')?.classList.remove('hidden');
                }'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    # Use regex if exact match fails due to line endings
    pattern = r"if \(draft\.taxId\)\s*\{\s*document\.getElementById\('eb-empty-state'\)\?\.classList\.add\('hidden'\);\s*if \(csContainer\)\s*\{.*?catch\(e\)\s*\{\s*console\.error\(\"Cross-sell update failed:\", e\);\s*\}\s*document\.getElementById\('eb-results-container'\)\?\.classList\.remove\('hidden'\);\s*\}"
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        codecs.open('templates/index.html', 'w', 'utf-8').write(content)
        print("SUCCESS REGEX")
    else:
        print("FAILED TO FIND CORRUPTED BLOCK")
