import logging
import json
import falcon

class JSONTranslator(object):

    def process_request(self, req, resp):
        self.logger = logging.getLogger("JSONTranslator Middleware")

        self.logger.info("Creating instance of JSONTranslator Middleware")

        if req.content_length in (None, 0):
            msg = ("In JSONTranslator middleware"
                   " req.content_length = {}").format(req.content_length)
            self.logger.debug(msg)
            return

        body = req.stream.read()

        if not body:
            self.logger.error("In JSONTranslator middleware: Empty request body. A valid JSON document is required.")

            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        else:
            self.logger.info("body : {}".format(body))

        try:
            req.context['data'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            self.logger.error("HTTP 753, Malformed JSON. Could not decode the request body. The JSON was incorrect or not encoded as UTF-8.")

            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
