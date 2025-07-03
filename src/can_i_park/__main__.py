from asyncio import get_event_loop, run
from can_i_park.cli import display_parking_data
from can_i_park.exporter import run_metrics_loop
from click import command, option, version_option
from prometheus_client import start_http_server


@command()
@option("-c", "--chargers", envvar="CHARGERS", is_flag=True)
@option("-e", "--exporter", envvar="EXPORTER", is_flag=True)
@option("-i", "--interval", envvar="EXPORTER_INTERVAL", type=int)
@option("-p", "--port", envvar="EXPORTER_PORT", type=int)
@option("-n", "--name", envvar="NAME", multiple=True)
@option("-v", "--verbose", count=True)
@option("--lez/--no-lez", envvar="LEZ", default=True)
@version_option()
def main(chargers, exporter, interval, port, name, verbose, lez):
    if exporter:
        start_http_server(port if port else 9030)
        get_event_loop().run_until_complete(
            run_metrics_loop(interval if interval else 150)
        )
    else:
        run(display_parking_data(name, lez, verbose, chargers))


if __name__ == "__main__":
    main()
