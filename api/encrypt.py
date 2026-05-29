import os, uuid, tempfile
from http.server import BaseHTTPRequestHandler
import pikepdf

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        import cgi, io

        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self._error(400, 'Invalid content type')
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        # multipart パース
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(length),
        }
        fs = cgi.FieldStorage(
            fp=io.BytesIO(body),
            environ=environ,
            keep_blank_values=True
        )

        # ファイル取得
        if 'file' not in fs:
            self._error(400, 'ファイルが選択されていません')
            return
        file_item = fs['file']
        filename = file_item.filename or 'upload.pdf'
        if not filename.lower().endswith('.pdf'):
            self._error(400, 'PDFファイルのみ対応しています')
            return

        # パスワード取得
        password = fs.getvalue('password', '').strip() if 'password' in fs else ''
        if not password:
            self._error(400, 'パスワードを入力してください')
            return
        if len(password) > 32:
            self._error(400, 'パスワードは32文字以内にしてください')
            return

        pdf_data = file_item.file.read()

        # Vercel は /tmp のみ書き込み可能
        with tempfile.TemporaryDirectory(dir='/tmp') as tmpdir:
            in_path = os.path.join(tmpdir, 'input.pdf')
            out_path = os.path.join(tmpdir, 'output.pdf')

            with open(in_path, 'wb') as f:
                f.write(pdf_data)

            try:
                with pikepdf.open(in_path) as pdf:
                    pdf.save(
                        out_path,
                        encryption=pikepdf.Encryption(
                            owner=password + '_owner_' + uuid.uuid4().hex[:8],
                            user=password,
                            R=6,
                            allow=pikepdf.Permissions(
                                accessibility=True,
                                extract=False,
                                modify_annotation=False,
                                modify_assembly=False,
                                modify_form=True,
                                modify_other=False,
                                print_lowres=False,
                                print_highres=True,
                            )
                        )
                    )
            except pikepdf.PasswordError:
                self._error(400, '入力PDFが既にパスワード保護されています')
                return
            except Exception as e:
                self._error(500, f'処理エラー: {str(e)}')
                return

            with open(out_path, 'rb') as f:
                result = f.read()

        base = os.path.splitext(filename)[0]
        download_name = f'{base}_protected.pdf'

        self.send_response(200)
        self.send_header('Content-Type', 'application/pdf')
        self.send_header('Content-Disposition', f'attachment; filename*=UTF-8\'\'{download_name}')
        self.send_header('Content-Length', str(len(result)))
        self.end_headers()
        self.wfile.write(result)

    def _error(self, code, message):
        import json
        body = json.dumps({'error': message}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
