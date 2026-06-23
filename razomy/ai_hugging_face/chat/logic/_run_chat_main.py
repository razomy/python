import time
from typing import Iterable
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
import uuid
import subprocess

def check_appearance():
    """Checks DARK/LIGHT mode of macos."""
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    return bool(p.communicate()[0])

from ai_hugging_face.chat.predict import create_chat_model
from cache import global_cache_registry
from razomy.ai_hugging_face.chat.logic.predict import models, BackgroundStreamWorker, cache_predict_stream, \
    summarize_history
import json
import os

console = Console()
bindings = KeyBindings()

isDark = check_appearance()

@bindings.add('escape', 'enter')
def _(event):
    """Позволяет отправлять сообщение по нажатию Ctrl+Enter."""
    event.app.exit(result=event.app.current_buffer.text)


def render_md(text: str) -> Markdown:
    """Вспомогательная функция для единообразного рендеринга Markdown."""
    lite = dict(
        code_theme='vs',
        inline_code_theme='vs',
    )
    dark = dict(
        code_theme='monokai',
        inline_code_theme='monokai',
    )
    theme = dark if isDark else lite
    return Markdown(text, **theme, inline_code_lexer='python', justify="left")


def render_user_text(text: str):
    """
    Отрисовка ввода пользователя.
    Чтобы Markdown-разметка пользователя не 'сломала' интерфейс,
    мы выводим текст как обычный Text объект, либо в панели.
    """
    # Вариант 1: Просто как текст (игнорирует MD разметку)
    return Text(text, style="")


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


def get_active_context(messages):
    """
    Возвращает только часть истории, начиная с последнего саммари.
    Это позволяет модели не обрабатывать тысячи старых токенов.
    """
    last_summary_idx = -1
    for i, m in enumerate(messages):
        if m.get('is_summary'):
            last_summary_idx = i

            # Если саммари найдено, возвращаем всё от него и до конца.
    # Если нет - возвращаем всю историю.
    if last_summary_idx != -1:
        return messages[last_summary_idx:]
    return messages


def main():
    # --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ СОХРАНЕНИЯ ---
    def save_chat(chat_id, messages):
        filename = f"{chat_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)
        console.print(Panel(f"[bold green]Chat saved to {filename}[/bold green]", title="Save"))

    def load_chat(filename):
        if not os.path.exists(filename):
            return None
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def perform_compression(model_id, messages, fn):
        console.print(Panel("Auto-compressing...", title="System"))
        tail = messages[-3:]
        history_to_compress = messages[:-3]

        summary_text = summarize_history(None, model_id, history_to_compress, fn)

        new_messages = history_to_compress
        new_messages.append({
            "role": "system",
            "content": f"CONVERSATION SUMMARY: {summary_text}",
            "is_summary": True
        })
        new_messages.extend(tail)
        return new_messages

    """Точка входа и главный цикл чата."""
    session = PromptSession(erase_when_done=True)
    chat_id = str(generate_complex_id('chat'))
    model_id = '31_4'
    messages = []
    auto_save = False  # Флаг для автоматического сохранения

    def help():
        return Panel(
        "Нажимай \\[Enter] для новой строки.\n"
        "Нажимай \\[Opt+Enter] для ОТПРАВКИ.\n"
        "Нажимай \\[Cntr+C] to stop.\n"
        "write load <filename>': Load a chat\n"
        "write \"clear\" for a new chat.\n"
        "write \"raw\" to view chat as string.\n"
        "write \"save\" to enable AUTO-SAVE.\n"
        "write \"compress\" save chat.\n"
        "write \"help\" to see this message.\n"
        "write \"exit\" for an exit.",
        title=f"Welcome to the Chatbot({model_id})",
        border_style="green"
    )
    console.print(help())
    smart_stream = BackgroundStreamWorker(
        generator_func=cache_predict_stream
    )
    while True:
        console.rule("You:", align="left")
        try:
            user_input = session.prompt("", multiline=True, key_bindings=bindings).strip()
        except KeyboardInterrupt:
            continue

        if not user_input:
            continue

            # --- COMMAND HANDLING ---
        cmd = user_input.lower()

        if cmd in ['выход', 'exit']:
            console.print(Panel("[bold cyan]Бот: Пока! 👋[/bold cyan]", title="Goodbye"))
            if auto_save: save_chat(chat_id, messages)
            smart_stream.close()
            exit(0)

        if cmd == 'clear':
            console.print(Panel("[bold cyan]Бот: Clearing! 👋[/bold cyan]", title="Clearing"))
            global_cache_registry.delete(chat_id)
            chat_id = str(generate_complex_id('chat'))
            messages = []
            continue

        if cmd == 'help':
            console.print(help())
            continue

        if cmd == 'raw':
            # Format chat history as a single string
            chat_text = "\n".join([f"{m['role'].upper()}---\n{m['content']}" for m in messages])
            console.print(
                Panel(chat_text if chat_text else "Chat is empty", title="Raw Chat History", border_style="magenta"))
            continue

        if cmd.startswith('load '):
            filename = user_input[5:].strip()
            loaded_msgs = load_chat(filename)
            if loaded_msgs:
                messages = loaded_msgs
                chat_id = filename.replace('.json', '')
                # --- ОТРИСОВКА ВСЕГО ЧАТА ПОСЛЕ ЗАГРУЗКИ ---
                console.print(Panel("[bold yellow]--- Loaded Chat History ---[/bold yellow]"))
                for msg in messages:
                    if msg['role'] == 'user':
                        console.rule("You:", align="left")
                        console.print(render_user_text(msg['content']))
                    elif msg['role'] == 'model':
                        console.rule("Ai:", align="left")
                        console.print(render_md(msg['content']))
                    elif msg.get('is_summary'):
                        console.print(Panel(msg['content'], title="Summary", style="dim"))
                console.print(Panel("[bold yellow]--- End of History ---[/bold yellow]"))
                # -------------------------------------------
                console.print(Panel(f"[bold green]Chat loaded from {filename}[/bold green]", title="Load"))
            else:
                console.print("[red]File not found![/red]")
            continue

        if cmd == 'save':
            auto_save = not auto_save
            console.print(Panel(f"Auto-save: {'ENABLED' if auto_save else 'DISABLED'}", title="Save Mode"))
            if auto_save: save_chat(chat_id, messages)
            continue

            # --- ЛОГИКА ОБЩЕНИЯ ---
        messages.append({'role': 'user', 'content': user_input})
        # Используем render_user_text вместо render_md, чтобы избежать нежелательного форматирования
        console.print(render_user_text(user_input))

        active_messages = get_active_context(messages)

        # АВТО-КОМПРЕСС: Если сообщений больше 20, сжимаем
        if len(active_messages) > 30 or cmd == 'compress':
            messages = perform_compression(models[model_id], messages, smart_stream)
            chat_id = str(generate_complex_id('chat'))
            active_messages = get_active_context(messages)
            if cmd == 'compress':
                continue

        try:
            console.rule("Ai:", align="left")
            stream_iterator = smart_stream(chat_id, models[model_id], active_messages)
            full_response = stream_ai_response(console, stream_iterator)
            messages.append({'role': 'model', 'content': full_response})
        except Exception as e:
            console.print(Panel(f"Error: {e}", border_style="red"))

        if auto_save:
            save_chat(chat_id, messages)


if __name__ == '__main__':
    main()
