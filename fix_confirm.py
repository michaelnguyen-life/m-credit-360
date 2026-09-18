# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''function confirmNewCustomerSession() {
      closeNewCustomerModal();
      
      // Clear Form Fields
      document.getElementById('eb-tax-id').value = '';
      document.getElementById('eb-company-name').value = '';'''

replacement = '''function confirmNewCustomerSession() {
      const modalTaxId = document.getElementById('modal-tax-id').value.trim();
      const modalCompanyName = document.getElementById('modal-company-name').value.trim();
      const modalPeriod = document.getElementById('modal-period').value;

      closeNewCustomerModal();
      
      // Clear Form Fields
      document.getElementById('eb-tax-id').value = modalTaxId;
      document.getElementById('eb-company-name').value = modalCompanyName;
      document.getElementById('eb-period').value = modalPeriod;'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
