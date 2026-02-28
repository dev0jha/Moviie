import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from recommender.content_based import recommend, load_movies

console = Console()

ACCENT = "bright_magenta"
DIM = "dim white"
TITLE_GRADIENT = ["bright_magenta", "bright_cyan", "bright_magenta"]

LOGO = r"""
  ███╗   ███╗ ██████╗ ██╗   ██╗██╗██╗███████╗
  ████╗ ████║██╔═══██╗██║   ██║██║██║██╔════╝
  ██╔████╔██║██║   ██║██║   ██║██║██║█████╗  
  ██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██║██║██╔══╝  
  ██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██║██║███████╗
  ╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝╚══════╝"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    logo_text = Text(LOGO, style=f"bold {ACCENT}")
    subtitle = Text(
        "  Your Personal Movie Recommendation Engine",
        style=f"italic {DIM}",
    )
    banner = Text.assemble(logo_text, "\n", subtitle)
    console.print(
        Panel(
            banner,
            border_style=ACCENT,
            box=box.DOUBLE_EDGE,
            padding=(1, 4),
        )
    )
    console.print()


def show_menu():
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=False,
    )
    table.add_column(style=f"bold {ACCENT}", width=4, justify="right")
    table.add_column(style="white")
    table.add_row("1.", "🔍  Search & Get Recommendations")
    table.add_row("2.", "🎲  Random Movie Pick")
    table.add_row("3.", "📊  Browse Top Movies")
    table.add_row("4.", "❌  Exit")
    console.print(
        Panel(
            table,
            title=f"[bold {ACCENT}]  MENU  [/]",
            border_style="bright_black",
            box=box.ROUNDED,
            padding=(1, 3),
        )
    )
    console.print()


def animate_searching():
    with Progress(
        SpinnerColumn("dots", style=ACCENT),
        TextColumn("[bold white]Analyzing movie database..."),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("search", total=None)
        time.sleep(1.2)


def display_recommendations(movie_title, results):
    table = Table(
        title=f"[bold white]Recommendations for [bold {ACCENT}]'{movie_title}'[/]",
        box=box.SIMPLE_HEAVY,
        border_style="bright_black",
        title_style=f"bold {ACCENT}",
        padding=(0, 2),
        expand=False,
    )
    table.add_column("#", style=f"bold {ACCENT}", width=4, justify="right")
    table.add_column("Movie Title", style="white", min_width=30)

    for i, title in enumerate(results, 1):
        table.add_row(str(i), f"🎬  {title}")

    console.print()
    console.print(
        Panel(
            table,
            border_style=ACCENT,
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()


def handle_search():
    console.print()
    movie = Prompt.ask(f"  [{ACCENT}]🎯  Enter a movie title[/]")
    movie = movie.strip()

    if not movie:
        console.print(f"  [bold red]✖  No movie name provided.[/]\n")
        return

    animate_searching()

    results = recommend(movie)

    if not results:
        console.print(
            Panel(
                f"[bold red]✖[/]  No match found for [bold]'{movie}'[/]\n"
                f"  [dim]Tip: Check spelling or try another title[/]",
                border_style="red",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        console.print()
    else:
        display_recommendations(movie, results)


def handle_random():
    console.print()
    with Progress(
        SpinnerColumn("dots", style=ACCENT),
        TextColumn("[bold white]Picking a random gem..."),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("random", total=None)
        movies = load_movies()
        time.sleep(0.8)

    pick = movies.sample(1).iloc[0]
    title = pick["title"]
    overview = pick["overview"]
    if not overview or overview.strip() == "":
        overview = "No overview available."

    console.print(
        Panel(
            f"[bold {ACCENT}]🎲  {title}[/]\n\n"
            f"[white]{overview}[/]",
            title=f"[bold {ACCENT}]  RANDOM PICK  [/]",
            border_style=ACCENT,
            box=box.DOUBLE_EDGE,
            padding=(1, 3),
            width=70,
        )
    )
    console.print()

    get_recs = Prompt.ask(
        f"  [{DIM}]Get recommendations for this movie? (y/n)[/]",
        default="n",
    )
    if get_recs.lower() == "y":
        animate_searching()
        results = recommend(title)
        if results:
            display_recommendations(title, results)
        else:
            console.print(f"  [dim]No recommendations found for this title.[/]\n")


def handle_browse():
    console.print()
    with Progress(
        SpinnerColumn("dots", style=ACCENT),
        TextColumn("[bold white]Loading movie catalog..."),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("browse", total=None)
        movies = load_movies()
        time.sleep(0.6)

    top = movies.head(20)

    table = Table(
        title=f"[bold {ACCENT}]Top 20 Movies in Database[/]",
        box=box.SIMPLE_HEAVY,
        border_style="bright_black",
        padding=(0, 2),
        expand=False,
    )
    table.add_column("#", style=f"bold {ACCENT}", width=4, justify="right")
    table.add_column("Title", style="white", min_width=35)
    table.add_column("Overview", style=DIM, max_width=40, no_wrap=True)

    for i, (_, row) in enumerate(top.iterrows(), 1):
        overview = row["overview"]
        if len(overview) > 37:
            overview = overview[:37] + "..."
        table.add_row(str(i), row["title"], overview)

    console.print(
        Panel(
            table,
            border_style=ACCENT,
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()


def run():
    clear_screen()
    show_banner()

    while True:
        show_menu()
        choice = Prompt.ask(
            f"  [{ACCENT}]▸  Choose an option[/]",
            choices=["1", "2", "3", "4"],
            show_choices=False,
        )

        if choice == "1":
            handle_search()
        elif choice == "2":
            handle_random()
        elif choice == "3":
            handle_browse()
        elif choice == "4":
            console.print()
            console.print(
                Panel(
                    f"[bold {ACCENT}]Thanks for using MOVIIE![/]\n"
                    f"[{DIM}]See you next time 🍿[/]",
                    border_style=ACCENT,
                    box=box.DOUBLE_EDGE,
                    padding=(1, 3),
                )
            )
            console.print()
            sys.exit(0)
