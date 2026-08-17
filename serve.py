#!/usr/bin/env python3
"""Local dev server that mimics Vercel's cleanUrls:true behavior,
so extensionless URLs like /neardeals or /articles/openota work
the same locally as they will in production."""
import http.server
import os
import socketserver

PORT = 8123


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        url_path = path.split("?")[0].split("#")[0]
        fs_path = super().translate_path(path)

        if url_path.endswith("/"):
            candidate = os.path.join(fs_path, "index.html")
            if os.path.exists(candidate):
                return candidate
            return fs_path

        if os.path.exists(fs_path):
            return fs_path

        html_candidate = fs_path + ".html"
        if os.path.exists(html_candidate):
            return html_candidate

        index_candidate = os.path.join(fs_path, "index.html")
        if os.path.isdir(fs_path) and os.path.exists(index_candidate):
            return index_candidate

        return fs_path


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving with clean URLs at http://localhost:{PORT}/")
        httpd.serve_forever()
