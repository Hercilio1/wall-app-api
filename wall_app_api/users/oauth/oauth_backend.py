import json
from oauth2_provider.oauth2_backends import OAuthLibCore

class JSONOAuthLibCore(OAuthLibCore):
    """
    Extends the default OAuthLibCore to parse correctly application/json requests
    Based on oauth-toolkit class JSONOAuthLibCore
    """

    def extract_body(self, request):
        """
        Extracts the JSON body from the Django request object
        :param request: The current django.http.HttpRequest object
        :return: provided POST parameters "urlencodable"
        """
        content_type = request.META.get('CONTENT_TYPE', '')

        if 'application/json' in content_type:
            try:
                body = json.loads(request.body.decode("utf-8")).items()
            except (AttributeError, ValueError):
                body = ""
        else:
            body = super().extract_body(request)

        return body
