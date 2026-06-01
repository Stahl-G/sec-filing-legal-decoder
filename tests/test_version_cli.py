from sec_filing_legal_decoder import __version__
from sec_filing_legal_decoder.cli import main


def test_cli_version_outputs_package_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    output = capsys.readouterr().out.strip()
    assert output == f"sec-filing-legal-decoder {__version__}"
