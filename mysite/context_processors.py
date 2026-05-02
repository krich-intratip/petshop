from django.conf import settings

from mysite.site_meta import get_site_last_updated_display, get_site_version


def site_settings(_request):
    return {
        'LINE_ORDER_URL': getattr(
            settings,
            'LINE_ORDER_URL',
            'https://line.me/R/ti/p/@Dr.peakmaker',
        ),
        'SITE_VERSION': get_site_version(),
        'SITE_LAST_UPDATED_DISPLAY': get_site_last_updated_display(),
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Peakmaker Cat Shop'),
    }
