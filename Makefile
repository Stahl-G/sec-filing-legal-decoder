.PHONY: setup test smoke update release-check

setup:
	scripts/setup_dev.sh

test:
	pytest

smoke:
	scripts/run_smoke.sh

update:
	scripts/update_dev_env.sh

release-check:
	scripts/release_check.sh
