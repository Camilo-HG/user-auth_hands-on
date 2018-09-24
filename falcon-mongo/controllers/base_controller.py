import json
import falcon
import logging
import sys
import jwt

from ..models.user_model import User


def Authorize(req, resp, resource, params):
    """
    Process the request in order to 
    verify user authentication
    """
    model = User

    jwt_algorithm = 'HS256'
    jwt_key = 'geoserver-secret'

    logger = logging.getLogger("Hook : Authorize")

    message = ('Initializing authentication validation')

    logger.info(message)

    #Raises: HTTPBadRequest when the header was not found in the request
    # neither in the req.params
    try:
        token = req.get_header('token', required=True)
    except:
        try:
            token = req.get_param('token', required=True)
        except:
            try:
                token = req.context['data']['token']
            except:
                message = 'No token provided.'

                # Log ERROR
                logger.error(message)
                raise falcon.HTTPError(falcon.HTTP_400,
                                           'Bad Request Error',
                                           'No token provided.')

    try:
        data = jwt.decode(token,
                          jwt_key,
                          algorithm=jwt_algorithm)
    except jwt.DecodeError as err:
        message = 'Token validation failed. Error: {}'.format(err)

        # Log ERROR
        logger.error(message)
        raise falcon.HTTPError(falcon.HTTP_500,
                               'Server Error',
                               'Error decoding authentication token')
    else:
        try:
            user = model.objects.get(id=data['id'])
        except Exception as err:
            message = 'Token validation failed. Error: {}'.format(str(err))

            # Log ERROR
            logger.error(message)
            raise falcon.HTTPError(falcon.HTTP_403,
                                   'Unauthorized')
        else:
            message = "Token valid"

            # Log INFO
            logger.info(message)

"""
Next methods are standard son can be used by different object models.
"""
@falcon.before(Authorize)
class BaseController:

    def get_error_message(self, error_status):
        return json.dumps(ERRORS_MSG[error_status])

    def get_allowed_methods(self, **kwargs):
        allowed_methods = []

        if hasattr(self, 'list') and not kwargs:
            allowed_methods.append('GET')

        if hasattr(self, 'retrieve') and kwargs:
            allowed_methods.append('GET')

        if hasattr(self, 'create') and not kwargs:
            allowed_methods.append('POST')

        if hasattr(self, 'update') and kwargs:
            allowed_methods.append('PUT')

        if hasattr(self, 'delete') and kwargs:
            allowed_methods.append('DELETE')

        return allowed_methods


    def on_get(self, request, response, **kwargs):
        # Log info entry
        self.logger.info(("Instance: {} , "
                          "method: {}, kwargs: {}").format(type(self).__name__,
                                                           request.method, kwargs))
        
        # If kwargs, call 'retrieve' method
        if kwargs:
            # Log INFO
            self.logger.info("Internal method required: 'retrieve'")

            if hasattr(self, 'retrieve'):
                # Log DEBUG
                self.logger.debug("on_get, calling self.retrieve")
                return self.retrieve(request, response, **kwargs)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'retrieve' method is not implemented").format(request.url,
                                                                          request.method,
                                                                          kwargs,
                                                                          type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not allowed
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllowed(self.get_allowed_methods(**kwargs))

        # If kwargs is empty, call 'list method
        elif not kwargs:
            # Log INFO
            self.logger.info("Internal method required: 'list'")

            if hasattr(self, 'list'):
                # Log DEBUG
                self.logger.debug("on_get, calling self.list")
                return self.list(request, response)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'list' method is not implemented").format(request.url,
                                                                      request.method,
                                                                      kwargs,
                                                                      type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not allowed
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllowed(self.get_allowed_methods(**kwargs))


    def on_post(self, request, response, **kwargs):
        # Log info entry
        self.logger.info(("Instance: {} , "
                          "method: {}, kwargs: {}").format(type(self).__name__,
                                                           request.method, kwargs))
        
        # If NOT kwargs, call 'create' method
        if not kwargs: 
            # Log INFO
            self.logger.info("Internal method required: 'create'")
            
            if hasattr(self, 'create'):
                # Log DEBUG
                self.logger.debug("on_post, calling self.create")
                return self.create(request, response)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'create' method is not implemented").format(request.url,
                                                                        request.method,
                                                                        kwargs,
                                                                        type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllowed(self.get_allowed_methods(**kwargs))

        # If kwargs is not empty
        else:
            message = ("URL: {} with HTTP method {} and kwargs {}\n"
                       "calls an instance of {} whose "
                       "'create' requires empty kwargs").format(request.url,
                                                                request.method,
                                                                kwargs,
                                                                type(self).__name__)
            # Log ERROR
            self.logger.error(message)

            # Method not allowed
            self.logger.error("HTTP Method not allowed")
            raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))


    def on_put(self, request, response, **kwargs):
        # Log info entry
        self.logger.info(("Instance: {} , "
                          "method: {}, kwargs: {}").format(type(self).__name__,
                                                           request.method, kwargs))
        
        # If kwargs, call 'update' method
        if kwargs:
            # Log INFO
            self.logger.info("Internal method required: 'update'")
    
            if hasattr(self, 'update'):
                # Log DEBUG
                self.logger.debug("on_put, calling self.update")
                return self.update(request, response, **kwargs)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'update' method is not implemented").format(request.url,
                                                                        request.method,
                                                                        kwargs,
                                                                        type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not implemented
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))

        # If kwargs is empty
        else:
            message = ("URL: {} with HTTP method {} and kwargs {}\n"
                       "calls an instance of {} whose "
                       "'update' requires non-empty kwargs").format(request.url,
                                                                    request.method,
                                                                    kwargs,
                                                                    type(self).__name__)
            # Log ERROR
            self.logger.error(message)

            # Method not allowed
            self.logger.error("HTTP Method not allowed")
            raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))


    def on_delete(self, request, response, **kwargs):
        # Log info entry
        self.logger.info(("Instance: {} , "
                          "method: {}, kwargs: {}").format(type(self).__name__,
                                                           request.method, kwargs))

        # If request.context['data'] != None, call 'delete_some' method
        # If 'data' in request.context, call 'delete_some'
        if 'data' in request.context:
            # Log INFO
            self.logger.info("Internal method required: 'delete_some'")

            if hasattr(self, 'delete_some'):
                # Log DEBUG
                self.logger.debug("on_delete, calling self.delete_some")
                return self.delete_some(request, response, **kwargs) 
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'delete_some' method is not implemented").format(request.url,
                                                                             request.method,
                                                                             kwargs,
                                                                             type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not implemented
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))

        # If kwargs, call 'delete_one' method
        elif kwargs:
            # Log INFO
            self.logger.info("Internal method required: 'delete_one'")
            
            if hasattr(self, 'delete_one'):
                # Log DEBUG
                self.logger.debug("on_delete, calling self.delete_one")
                return self.delete_one(request, response, **kwargs)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'delete_one' method is not implemented").format(request.url,
                                                                            request.method,
                                                                            kwargs,
                                                                            type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not implemented
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))

        # If NOT kwargs, call 'delete_all' method
        elif not kwargs:
            # Log INFO
            self.logger.info("Internal method required: 'delete_all'")
        
            if hasattr(self, 'delete_all'):
                # Log DEBUG
                self.logger.debug("on_delete, calling self.delete_all")
                return self.delete_all(request, response)
            else:
                message = ("URL: {} with HTTP method {} and kwargs {}\n"
                           "calls an instance of {} whose "
                           "'delete_all' method is not implemented").format(request.url,
                                                                            request.method,
                                                                            kwargs,
                                                                            type(self).__name__)
                # Log ERROR
                self.logger.error(message)

                # Method not implemented
                self.logger.error("HTTP Method not allowed")
                raise falcon.HTTPMethodNotAllodwed(self.get_allowed_methods(**kwargs))



class Object2Dict:
    def object2dict(self, obj):
        dictionary = {}
        for key in obj.to_mongo().keys():
            if '_id' in key:
                key = key.lstrip('_')
                dictionary[key] = str(obj[key])
            else:
                dictionary[key] = obj[key]
        return dictionary



class CreateGeneral(Object2Dict):
    def create(self, request, response):
        # Log DEBUG
        self.logger.debug(("On 'create' method - "
                           "Instance: {}").format(type(self).__name__))
        
        data = request.context['data']

        if 'token' in data:
            data.pop('token')

        # data received
        if len(data.keys()) != 0:

            # Log INFO
            self.logger.info("Method was called with data: {}".format(data))
            try:
                obj = self.model(**data)
            except:
                message = "{}".format(sys.exc_info())
                # Log ERROR
                self.logger.error(message)
                raise falcon.HTTPError(falcon.HTTP_417,
                                       'Expectation failed',
                                       message)
            else:
                try:
                    obj.save()
                except:
                    message = "{}".format(sys.exc_info())

                    # Log ERROR
                    self.logger.error(message)
                    raise falcon.HTTPError(falcon.HTTP_500,
                                           'Database Error',
                                           'Unable to create object in database\n'
                                           + message)
                else:
                    # SUCCEED. Object CREATED
                    object_dict = self.object2dict(obj)

                    # Log INFO
                    self.logger.info("Object {} CREATED".format(object_dict))
                    # Response
                    response.status = falcon.HTTP_201
                    response.body = json.dumps(object_dict, ensure_ascii=False)

        # NO data received
        else:
            message = "NO data received, data : {}".format(data)
            
            # Log ERROR
            self.logger.error(message)
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Bad request',
                                   message)





class ListGeneral(Object2Dict):
    def get_queryset(self, request):
        """
        'query' corresponds to an URL query parameter
        
        Up-to-date 13-Apr-2018:
        
        If url: /projects/{project_id}/sites  then
            request.context['query'] = project_id

        If url: /sites/{site_id}/layers  then
            request.context['query'] = site_id
        """
        if not ('query' in request.context):
            # Log DEBUG
            self.logger.debug("No 'query' in request.context")
            return self.model.objects.all()
        else:
            # Log DEBUG
            self.logger.debug("'query' in request.context")
            return self.model.objects(**request.context['query'])

    def list(self, request, response):
        # Log DEBUG
        self.logger.debug(("On 'list' method - "
                           "Instance: {}").format(type(self).__name__))
        try:
            object_dict_array = list(map(self.object2dict, self.get_queryset(request)))
        except:
            message = "{}".format(sys.exc_info())

            # Log ERROR
            self.logger.error(message)
            raise falcon.HTTPError(falcon.HTTP_500,
                                   'Database Error',
                                   'Unable to list objects of database')
        else:
            response.body = json.dumps(object_dict_array, ensure_ascii=False)
            response.status = falcon.HTTP_200


class RetrieveGeneral(Object2Dict):
    def retrieve(self, request, response, **kwargs):
        # Log DEBUG
        self.logger.debug(("On 'retrieve' method - "
                           "Instance: {}").format(type(self).__name__))
        try:
            #obj = self.model.objects.get(id=kwargs['id'])
            for key in kwargs.keys():
                if 'id' in key:
                    obj = self.model.objects.get(id=kwargs[key])
        except:
            message = "{}".format(sys.exc_info())

            # Log ERROR
            self.logger.error(message)
            raise falcon.HTTPError(falcon.HTTP_404,
                                   'Object Not Found',
                                   'Unable to find object in database')
        else:
            object_dict = self.object2dict(obj)
            response.body = json.dumps(object_dict, ensure_ascii=False)
            response.status = falcon.HTTP_200


class UpdateGeneral(Object2Dict):
    def update(self, request, response, **kwargs):
        # Log DEBUG
        self.logger.debug(("On 'update' method - "
                           "Instance: {}").format(type(self).__name__))

        data = request.context['data']

        if 'token' in data:
            data.pop('token')

        if len(data.keys()) != 0:
            try:
                for key in kwargs.keys():
                    if 'id' in key:
                        obj = self.model.objects.get(id=kwargs[key])
            except:
                raise falcon.HTTPError(falcon.HTTP_404,
                                        'Query Error',
                                        'Object not found')
            else:
                for key in data.keys():
                    obj[key] = data[key]
                try:
                    obj.save()
                except:
                    self.logger.error("{}".format(sys.exc_info()))
                    raise falcon.HTTPError(falcon.HTTP_500,
                                           'Database Error',
                                           'Unable to update database')
                else:
                    response.status = falcon.HTTP_200
                    object_dict = self.object2dict(obj)
                    response.body = json.dumps(object_dict, ensure_ascii=False)
                    self.logger.info("Object {} UPDATE".format(object_dict))

        else:
            raise falcon.HTTPError(falcon.HTTP_400)


class DeleteGeneral:
    def delete_some(self, request, response):
        self.logger.info("On self.delete_some - self : {}".format(self))
        
        try:
            data = request.context['data']
        except:
            # No data
            msg = ("No 'data' in request.context"
                    "request received : {}").format(vars(request))

            self.logger.error(msg)

            raise falcon.HTTPError(falcon.HTTP_400,
                                        'Bad Request',
                                        msg)

        else:
            ids = data['ids']

            count = len(ids)

            for _id in ids:
                try:
                    obj = self.model.objects.get(id=_id)
                except:
                    count -= 1

                    msg = 'Object with id = {} was not found'.format(_id)
                    self.logger.error(msg)
                else:
                    obj.delete()
            
            message = '{} objects were deleted'.format(count)
            response.body = message
            response.status = falcon.HTTP_200


    def delete_all(self, request, response):
        self.logger.info("On self.delete_all - self : {}".format(self))
        if not ('query' in request.context):
           objs = self.model.objects.all()
           count = self.model.objects.count()
           objs.delete()
        else:
            try:
                objs = self.model.objects(**request.context['query'])
                count = self.model.objects(**request.context['query']).count()
                objs.delete()
            except:
                raise falcon.HTTPError(falcon.HTTP_404)
        if count == 1:
           message = '{} object was deleted'.format(count)
        else:
           message = '{} objects were deleted'.format(count)
        response.body = message
        response.status = falcon.HTTP_200


    def delete_one(self, request, response, **kwargs):
        self.logger.info("On self.delete_one - self : {}".format(self))
        try:
           for key in kwargs.keys():
              if 'id' in key:
                  obj = self.model.objects.get(id=kwargs[key])
        except:
           self.logger.error("Query Error, Object not found")
           raise falcon.HTTPError(falcon.HTTP_404,
                                  'Query Error',
                                  'Object not found')
        else:
            obj.delete()
            message = '1 object was deleted'
            response.body = message
            response.status = falcon.HTTP_200
