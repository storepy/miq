from django.urls import reverse_lazy

class TestMixin:

# HTTP status codes

    def assertHttp201(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 201 - Created."""
        self.assertEqual(getattr(response, key), 201)

    def assertHttp400(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 400 - Bad request."""
        self.assertEqual(getattr(response, key), 400)

    def assertHttp404(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 404 - Not found."""
        self.assertEqual(getattr(response, key), 404)

    def assertHttp200(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 200 - Ok."""
        self.assertEqual(getattr(response, key), 200)

    def assertHttp302(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 302 - Found."""
        self.assertEqual(getattr(response, key), 302)

    def assertHttp401(self, response,*,key='status_code') -> None:      
        """Asserts that the response status code is 401 - Unauthorized."""
        self.assertEqual(getattr(response, key), 401)

    def assertHttp403(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 403 - Forbidden."""
        self.assertEqual(getattr(response, key), 403)

    def assertHttp405(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 405 - Method Not Allowed."""
        self.assertEqual(getattr(response, key), 405)

    def assertHttp500(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 500 - Internal Server Error."""
        self.assertEqual(getattr(response, key), 500)

    def assertHttp503(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 503 - Service Unavailable."""
        self.assertEqual(getattr(response, key), 503)

    def assertHttp204(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 204 - No Content."""
        self.assertEqual(getattr(response, key), 204)

    def assertHttp202(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 202 - Accepted."""
        self.assertEqual(getattr(response, key), 202)

    def assertHttp206(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 206 - Partial Content."""
        self.assertEqual(getattr(response, key), 206)

    def assertHttp301(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 301 - Moved Permanently."""
        self.assertEqual(getattr(response, key), 301)

    def assertHttp304(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 304 - Not Modified."""
        self.assertEqual(getattr(response, key), 304)

    def assertHttp307(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 307 - Temporary Redirect."""
        self.assertEqual(getattr(response, key), 307)

    def assertHttp308(self, response,*,key='status_code') -> None:
        """Asserts that the response status code is 308 - Permanent Redirect."""
        self.assertEqual(getattr(response, key), 308)

# MISC

    @property
    def reverse_lazy(self) -> None:
        """Reverse a URL for a given view with arguments and keyword arguments."""
        return reverse_lazy

    # def reverse_lazy(self, viewname, urlconf=None, args=None, kwargs=None, current_app=None) -> None:
    #     """Reverse a URL for a given view with arguments and keyword arguments."""
    #     return reverse_lazy(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)