import os, subprocess, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
workspace_dir = os.path.abspath(r'd:\2026_FALL\DWP301c\Django Application Development with SQL and Databases')

def capture_screenshot(html_content, output_name, width=1280, height=800):
    # Insert base tag so styles and images load from local dev server
    base_tag = '<base href="http://127.0.0.1:8000/">'
    if '<head>' in html_content:
        html_content = html_content.replace('<head>', f'<head>\n{base_tag}')
    else:
        html_content = f'{base_tag}\n{html_content}'
    
    temp_html = os.path.join(workspace_dir, f'temp_{output_name}.html')
    out_png = os.path.join(workspace_dir, f'{output_name}.png')
    
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    cmd = [
        edge_path,
        '--headless=new',
        '--disable-gpu',
        f'--window-size={width},{height}',
        f'--screenshot={out_png}',
        f'file:///{temp_html}'
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Captured {output_name}.png: exists={os.path.exists(out_png)}, size={os.path.getsize(out_png)} bytes")

# 1. Capture 03-admin-site.png
c = Client()
c.login(username='admin', password='admin123')
admin_res = c.get('/admin/')
admin_html = admin_res.content.decode('utf-8')
capture_screenshot(admin_html, '03-admin-site', width=1280, height=850)

# 2. Capture 07-final.png
c_student = Client()
c_student.login(username='student', password='student123')
exam_res = c_student.get('/onlinecourse/course/1/submission/1/result/')
exam_html = exam_res.content.decode('utf-8')
capture_screenshot(exam_html, '07-final', width=1280, height=850)
