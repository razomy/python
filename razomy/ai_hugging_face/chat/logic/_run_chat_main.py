import time
from typing import Iterable
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
import uuid

from cache import global_cache_registry
from razomy.ai_hugging_face.chat.logic.predict import cache_predict_stream, models

console = Console()
bindings = KeyBindings()

@bindings.add('escape', 'enter')
def _(event):
    """Позволяет отправлять сообщение по нажатию Ctrl+Enter."""
    event.app.exit(result=event.app.current_buffer.text)


def render_md(text: str) -> Markdown:
    """Вспомогательная функция для единообразного рендеринга Markdown."""
    return Markdown(text, code_theme='vs', inline_code_theme='vs', inline_code_lexer='python', justify="left")


def generate_complex_id(prefix="item"):
    timestamp = int(time.time())
    # Берем первые 8 символов от полноценного UUID4
    unique_part = str(uuid.uuid4())[:8]

    return f"{prefix}_{timestamp}_{unique_part}"

def stream_ai_response(console: Console, stream_iterator: Iterable[dict]) -> str:
    """
    Управляет потоковым ответом и отрисовывает его блоками,
    чтобы длинный текст и код не ломали терминал.
    """
    full_response = ""
    buffer = ""
    max_live_height = max(5, console.height - 10)
    is_break = False
    try:
        with Live(render_md(""), console=console, refresh_per_second=15, transient=True) as live:
            for chunk in stream_iterator:
                content = chunk.get('content', '')
                if not content:
                    continue

                full_response += content
                buffer += content

                # --- ЛОГИКА РАЗБИЕНИЯ НА БЛОКИ ---
                lines = buffer.split('\n')
                blocks_to_commit = []
                temp_block = []
                in_code = False

                for line in lines:
                    temp_block.append(line)  # Добавляем строку в любом случае

                    if line.startswith('```'):
                        in_code = not in_code
                        if not in_code:  # Блок кода только что закрылся
                            blocks_to_commit.append("\n".join(temp_block))
                            temp_block.clear()
                    elif not in_code and not line.strip():  # Пустая строка (конец абзаца)
                        if any(l.strip() for l in temp_block):
                            blocks_to_commit.append("\n".join(temp_block))
                        temp_block.clear()

                # Всё, что не завершено, возвращаем в буфер
                buffer = "\n".join(temp_block)

                # 1. Печатаем ГОТОВЫЕ блоки НАВСЕГДА (strip('\n') бережет отступы списков)
                for block in blocks_to_commit:
                    if block.strip():
                        console.print(render_md(block.strip('\n')))

                # 2. Отрисовываем НЕЗАВЕРШЕННЫЙ кусок в Live
                display_lines = buffer.split('\n')
                is_in_code = buffer.count('```') % 2 != 0

                # Ограничиваем высоту Live виджета
                if len(display_lines) > max_live_height:
                    if is_in_code:
                        header = display_lines[0] if display_lines[0].startswith('```') else '```'
                        display_text = f"{header}\n...\n" + "\n".join(display_lines[-max_live_height:])
                    else:
                        display_text = "...\n" + "\n".join(display_lines[-max_live_height:])
                else:
                    display_text = buffer

                # Временно закрываем тег кода
                if is_in_code:
                    display_text += "\n```"

                live.update(render_md(display_text))
    except KeyboardInterrupt:
        is_break = True
        # This triggers the exact millisecond you press Ctrl+C
    # --- КОНЕЦ ГЕНЕРАЦИИ (Хвост) ---
    if buffer.strip():
        if buffer.count('```') % 2 != 0:
            buffer += "\n```"
        console.print(render_md(buffer.strip('\n')))
    if is_break:
        console.print(Panel("[bold cyan]Break! Loop stopped gracefully. 👋[/bold cyan]", title="Break"))
    return full_response


def main():
    """Точка входа и главный цикл чата."""
    session = PromptSession(erase_when_done=True)
    chat_id = str(generate_complex_id('chat'))
    messages = []

    console.print(Panel(
        "Нажимай \\[Enter] для новой строки.\n"
        "Нажимай \\[Opt+Enter] для ОТПРАВКИ.\n"
        "Нажимай \\[Cntr+C] to stop.\n"
        "write \"clear\" for a new chat.\n"
        "write \"raw\" to view chat as string.\n"
        "write \"save\" to save chat to file.\n"
        "write \"exit\" for an exit.",
        title="Welcome to the Chatbot",
        border_style="green"
    ))

    while True:
        console.rule("You:", align="left")
        user_input = session.prompt("", multiline=True, key_bindings=bindings).strip()

        if not user_input:
            continue

            # --- COMMAND HANDLING ---
        cmd = user_input.lower()

        if cmd in ['выход', 'exit']:
            console.print(Panel("[bold cyan]Бот: Пока! 👋[/bold cyan]", title="Goodbye"))
            break

        if cmd == 'clear':
            console.print(Panel("[bold cyan]Бот: Clearing! 👋[/bold cyan]", title="Clearing"))
            global_cache_registry.delete(chat_id)
            chat_id = str(generate_complex_id('chat'))
            messages = []
            continue

        if cmd == 'raw':
            # Format chat history as a single string
            chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
            console.print(
                Panel(chat_text if chat_text else "Chat is empty", title="Raw Chat History", border_style="magenta"))
            continue

        if cmd == 'save':
            # Format chat history and save to file with random name
            chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
            filename = f"{chat_id}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(chat_text)
            console.print(Panel(f"[bold green]Chat saved to {filename}[/bold green]", title="File Saved"))
            continue
            # --- END COMMAND HANDLING ---

        messages.append({'role': 'user', 'content': user_input})

        console.print(render_md(user_input))
        console.rule("Ai:", align="left")

        try:
            stream_iterator = cache_predict_stream(chat_id, models['31_4'], messages)
            full_response = stream_ai_response(console, stream_iterator)
            messages.append({'role': 'model', 'content': full_response})
        except Exception as e:
            console.print(
                Panel(f"[bold red]Ошибка при получении ответа:[/bold red] {e}", title="Error", border_style="red"))
if __name__ == '__main__':
    main()
