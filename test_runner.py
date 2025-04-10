from django.test.runner import DiscoverRunner
from django.core.management import call_command


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # This will call migrate again after DB creation
        db_cfg = super().setup_databases(**kwargs)
        print("Running migrate manually after test DB setup...")
        call_command("migrate", run_syncdb=True, verbosity=1)
        return db_cfg
