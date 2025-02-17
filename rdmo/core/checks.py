from django.conf import settings
from django.core.checks import Error, register


@register()
def check_account_terms_of_use_date_setting(app_configs, **kwargs):
    errors = []

    if settings.ACCOUNT_TERMS_OF_USE:
        if 'rdmo.accounts.middleware.TermsAndConditionsRedirectMiddleware' not in settings.MIDDLEWARE:
            errors.append(
                Error(
                    "When ACCOUNT_TERMS_OF_USE is enabled, "
                    "The TermsAndConditionsRedirectMiddleware is missing from the middlewares.",
                    hint="add rdmo.accounts.middleware.TermsAndConditionsRedirectMiddleware to MIDDLEWARE",
                    id="core.E001",
                )
            )

        if settings.ACCOUNT_TERMS_OF_USE_DATE is not None:
            # Ensure that ACCOUNT_TERMS_OF_USE_DATE is a valid date string
            from .utils import parse_date_from_string
            try:
                parse_date_from_string(settings.ACCOUNT_TERMS_OF_USE_DATE)
            except ValueError as exc:
                errors.append(
                    Error(
                        f"ACCOUNT_TERMS_OF_USE_DATE = {settings.ACCOUNT_TERMS_OF_USE_DATE} is not a valid date string.",
                        hint=f"{exc}",
                        id="core.E002",
                    )
                )

    return errors
