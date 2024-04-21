import time
import click
from tqdm.auto import tqdm
import click
from AppKit import (
    NSWorkspace,
    NSApplication,
    NSApplicationActivateIgnoringOtherApps,
    NSApplicationPresentationFullScreen,
)


def list_running_applications(workspace):
    return workspace.runningApplications()


def find_target_application(workspace, app_name):
    for app in list_running_applications(workspace):
        if app.localizedName() == app_name:
            return app
    return None


def activate_application(target_app):
    target_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)


def is_focused(workspace, target_app):
    return workspace.frontmostApplication() == target_app


def tqdm_timer(duration, step_size=1):
    start_time = time.time()
    # progress_bar = tqdm(total=duration, unit="s", bar_format="{l_bar}")
    progress_bar = tqdm(total=duration)
    accumulated_time = 0
    while time.time() - start_time < duration:
        now = time.time()
        yield
        time_delta = now - start_time - accumulated_time
        if time_delta >= step_size:
            progress_bar.update(time_delta)
            accumulated_time += time_delta


def maintain_focus(workspace, target_app, duration, delay=0.1):
    for _ in tqdm_timer(duration):
        active_app = workspace.activeApplication()

        active_app_pid = active_app["NSApplicationProcessIdentifier"]
        target_app_pid = target_app.processIdentifier()

        if active_app_pid != target_app_pid:
            activate_application(target_app)
            time.sleep(0.1)  # Wait for the activation to take effect

        time.sleep(delay)  # Small delay to avoid excessive CPU usage


def focus_window(app_name, duration, delay):
    workspace = NSWorkspace.sharedWorkspace()

    app_name = app_name.strip()
    target_app = None

    if app_name == "":
        for app in list_running_applications(workspace):
            if is_focused(workspace, app):
                target_app = app
                app_name = app.localizedName()
                break
    else:
        target_app = find_target_application(workspace, app_name)
        if target_app is None:
            raise Exception(f"Application '{app_name}' not found.")

    print(f"Burning the boats in `{app_name}` for {duration/60.:.0f} minutes")
    maintain_focus(workspace, target_app, duration, delay)


def parse_duration(duration_str):
    total_seconds = 0
    time_parts = {"h": 3600, "m": 60, "s": 1}
    for unit, factor in time_parts.items():
        if unit in duration_str:
            num, duration_str = duration_str.split(unit)
            total_seconds += int(num) * factor
    return total_seconds


@click.command()
@click.option(
    "--duration",
    default="20m",
    help="Duration to keep the application in focus. Format: 1h2m, 20m, 30s etc.",
)
@click.option("--delay", default=0.1, help="Delay between checks for focus change.")
@click.argument("app_name", required=False)
def main(duration, app_name, delay):
    duration_seconds = parse_duration(duration)
    if not app_name:
        app_name = input(
            "Enter the name of the application to focus (or press enter for active window in 3 seconds): "
        )
        if app_name == "":
            time.sleep(3)
    focus_window(app_name or "", duration_seconds, delay)
