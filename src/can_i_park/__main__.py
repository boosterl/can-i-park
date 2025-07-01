from asyncio import run
from can_i_park.cli import display_parking_data
from click import command, option, version_option


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
    run(display_parking_data(name, lez, verbose, chargers))


if __name__ == "__main__":
    main()
