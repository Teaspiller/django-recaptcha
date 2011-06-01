from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from recaptcha.client import captcha

class ReCaptcha(forms.widgets.Widget):
    """
    Keyword Arguments:
    
        use_ssl: If True, then forces the widget to use SSL. If False, then falls back on 
                    settings.RECAPTCHA_USE_SSL
    """
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def __init__(self, *args, **kwargs):
        self.use_ssl = kwargs.pop('use_ssl', False)
        super(ReCaptcha, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        use_ssl = self.use_ssl or False
        if 'RECAPTCHA_USE_SSL' in settings.__members__:
            use_ssl = use_ssl or settings.RECAPTCHA_USE_SSL
        
        return mark_safe(u'%s' %
                         captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY,
                                             use_ssl=use_ssl))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None),
            data.get(self.recaptcha_response_name, None)]
