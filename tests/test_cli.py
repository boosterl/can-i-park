from click.testing import CliRunner
from can_i_park.__main__ import main

def test_cli_verbose_flag():
    runner = CliRunner()
    result = runner.invoke(main, ["-v"])
    assert result.exit_code == 0

def test_cli_parking_filter():
    runner = CliRunner()
    result = runner.invoke(main, ["-n", "NON_EXISTING_PARKING"])
    assert result.output == ""
    assert result.exit_code == 0

def test_cli_non_existing_argument():
    runner = CliRunner()
    result = runner.invoke(main, ["--no"])
    assert result.exit_code == 2
    
