"""Локальный HTTP-сервер для стенда (папка stand/).

Тесты поднимают сервер сами на свободном порту. Для ручной проверки стенда:
    python stand_server.py      → http://127.0.0.1:8000/login.html
"""
import contextlib
import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STAND_DIR = Path(__file__).parent / "stand"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # не засорять вывод pytest
        pass


def _make_server(port: int) -> ThreadingHTTPServer:
    handler = functools.partial(QuietHandler, directory=str(STAND_DIR))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


@contextlib.contextmanager
def run_stand():
    """Запускает стенд в фоновом потоке и возвращает базовый URL."""
    server = _make_server(0)  # 0 — ОС выберет свободный порт
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    srv = _make_server(8000)
    print("Стенд: http://127.0.0.1:8000/login.html (Ctrl+C — остановить)")
    with contextlib.suppress(KeyboardInterrupt):
        srv.serve_forever()
