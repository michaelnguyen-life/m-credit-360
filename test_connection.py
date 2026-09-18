import os, urllib.request, json

def test_greennode():
    api_key = os.getenv('GREENNODE_API_KEY', '')
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if (not api_key or api_key == 'your_api_key_here') and os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('GREENNODE_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break

    if not api_key or api_key == 'your_api_key_here':
        print('[!] CHƯA CÓ API KEY!')
        print('-> Sếp hãy mở file .env và dán API Key vào dòng GREENNODE_API_KEY=...')
        return

    base_url = 'https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions'
    model = 'z-ai/glm-5.2-thirdparty'

    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'Bạn là AI Thẩm Định Tín Dụng M-Credit 360 của MSB.'},
            {'role': 'user', 'content': 'Chào bạn, hãy xác nhận bạn đã sẵn sàng giật giải nhất MSB AI Hackathon 2026.'}
        ],
        'temperature': 0.3,
        'max_tokens': 100
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    print(f'[*] Đang gửi request test tới GreenNode MaaS ({model})...')
    try:
        req = urllib.request.Request(base_url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode('utf-8'))
            print('[+] KẾT NỐI THÀNH CÔNG RỰC RỠ!')
            print('Phản hồi từ GreenNode LLM:', data['choices'][0]['message']['content'])
    except Exception as e:
        print(f'[-] Lỗi kết nối: {e}')

if __name__ == '__main__':
    test_greennode()
