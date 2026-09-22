import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Wrap action bar and section-eb inside section-eb
old_part = """      <!-- ==================== PRIMARY WORKFLOW ACTION BAR ==================== -->
      <div class="executive-card p-3 flex flex-wrap items-center justify-between gap-3 bg-white">"""

new_part = """      <!-- ==================== TAB 1: ENTERPRISE BANKING WORKSPACE (EB) ==================== -->
      <div id="section-eb" class="space-y-4">
      
      <!-- PRIMARY WORKFLOW ACTION BAR (EB) -->
      <div class="executive-card p-3 flex flex-wrap items-center justify-between gap-3 bg-white">"""

html = html.replace(old_part, new_part)

# Then remove id="section-eb" from the grid and replace with just the grid class, and close the div
old_grid = """      <!-- ==================== MAIN 3-COLUMN WORKSPACE (EB) ==================== -->
      <div id="section-eb" class="grid grid-cols-1 xl:grid-cols-12 gap-4 w-full">"""

new_grid = """      <!-- ==================== MAIN 3-COLUMN WORKSPACE (EB) ==================== -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-4 w-full">"""

html = html.replace(old_grid, new_grid)

# Close the section-eb div before section-rb
old_before_rb = """          </div>

        </div>
      </div>

      <!-- ==================== TAB 2: RETAIL BANKING WORKSPACE (RB) ==================== -->"""

new_before_rb = """          </div>

        </div>
      </div>
      </div> <!-- /section-eb -->

      <!-- ==================== TAB 2: RETAIL BANKING WORKSPACE (RB) ==================== -->"""

html = html.replace(old_before_rb, new_before_rb)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated section-eb wrapper successfully!")
