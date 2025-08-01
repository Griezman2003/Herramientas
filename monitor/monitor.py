import curses
import psutil
import platform
import datetime

def draw_box(stdscr, y, x, h, w, title=""):
    stdscr.attron(curses.color_pair(2))
    if y < curses.LINES and x + 2 < curses.COLS:
        stdscr.addstr(y, x + 2, f" {title} ")
    stdscr.attroff(curses.color_pair(2))
    for i in range(x + 1, x + w - 1):
        if y < curses.LINES:
            stdscr.addch(y, i, curses.ACS_HLINE)
        if y + h - 1 < curses.LINES:
            stdscr.addch(y + h - 1, i, curses.ACS_HLINE)
    for i in range(y + 1, y + h - 1):
        if x < curses.COLS:
            stdscr.addch(i, x, curses.ACS_VLINE)
        if x + w - 1 < curses.COLS:
            stdscr.addch(i, x + w - 1, curses.ACS_VLINE)
    stdscr.addch(y, x, curses.ACS_ULCORNER)
    stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
    stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
    stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)

def draw_cpu_graph(stdscr, y, x, h, w, history):
    max_bars = w - 2
    graph = history[-max_bars:]
    for i, val in enumerate(graph):
        bar_height = int((val / 100) * (h - 2))
        for j in range(h - 2):
            char = '█' if j >= (h - 2 - bar_height) else ' '
            stdscr.attron(curses.color_pair(3))
            stdscr.addch(y + 1 + j, x + 1 + i, char)
            stdscr.attroff(curses.color_pair(3))

def draw_bar(stdscr, y, x, width, percent, color_pair):
    filled = int(width * percent / 100)
    stdscr.attron(curses.color_pair(color_pair))
    stdscr.addstr(y, x, '█' * filled + '-' * (width - filled))
    stdscr.attroff(curses.color_pair(color_pair))

def draw_dashboard(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Box titles
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # CPU graph
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Warnings
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)    # High CPU

    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.nodelay(True)
    stdscr.timeout(1000)
    cpu_history = []

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        half_h = height // 2
        half_w = width // 2

        draw_box(stdscr, 0, 0, half_h, half_w, " Información General ")
        draw_box(stdscr, 0, half_w, half_h, width - half_w - 1, " Procesos ")
        draw_box(stdscr, half_h, 0, height - half_h - 1, half_w, " Disco y Red ")
        draw_box(stdscr, half_h, half_w, height - half_h - 1, width - half_w - 1, " Uso CPU (Gráfico) ")

        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        cpu_history.append(cpu)
        if len(cpu_history) > (width // 2 - 2):
            cpu_history.pop(0)

        color = 5 if cpu > 80 else 3
        stdscr.attron(curses.color_pair(color))
        stdscr.addstr(1, 2, f"CPU: {cpu}%")
        stdscr.attroff(curses.color_pair(color))
        draw_bar(stdscr, 2, 2, half_w - 4, cpu, color)

        stdscr.addstr(3, 2, f"Memoria: {mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")
        stdscr.addstr(4, 2, f"Disco: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
        stdscr.addstr(5, 2, f"Red: {net.bytes_sent // 1024} KB ↑ / {net.bytes_recv // 1024} KB ↓")

        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        stdscr.addstr(6, 2, f"Host: {platform.node()}")
        stdscr.addstr(7, 2, f"SO: {platform.system()} {platform.release()}")
        stdscr.addstr(8, 2, f"Uptime: {str(uptime).split('.')[0]}")

        proc_header_y = 1
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(proc_header_y, half_w + 2, f"{'PID':>6} {'Nombre':<25} {'CPU%':>6} {'Mem%':>6}")
        stdscr.attroff(curses.color_pair(2))
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append((p.info['pid'], p.info['name'], p.info['cpu_percent'], p.info['memory_percent']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        procs = sorted(procs, key=lambda x: x[2], reverse=True)
        max_procs = half_h - 3
        for i, (pid, name, cpu_p, mem_p) in enumerate(procs[:max_procs]):
            y_line = proc_header_y + 1 + i
            if y_line < half_h - 1:
                stdscr.addstr(y_line, half_w + 2, f"{pid:6} {name[:25]:25} {cpu_p:6.1f} {mem_p:6.1f}")

        stdscr.addstr(half_h + 1, 2, f"Disco Usado: {disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB")
        stdscr.addstr(half_h + 2, 2, f"Red Enviados: {net.bytes_sent // 1024} KB")
        stdscr.addstr(half_h + 3, 2, f"Red Recibidos: {net.bytes_recv // 1024} KB")

        draw_cpu_graph(stdscr, half_h, half_w, height - half_h - 2, width - half_w - 2, cpu_history)

        stdscr.addstr(height - 1, 2, "Presiona 'q' para salir | 'h' para ayuda")
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('h'):
            stdscr.addstr(height - 2, 2, "Ayuda: Monitoreo del sistema. Usa 'q' para salir. Actualiza cada segundo.")

def main():
    try:
        curses.wrapper(draw_dashboard)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
