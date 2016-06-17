import re

from xblock.django.request import django_to_webob_request
import xblock.runtime

from django.templatetags.static import static

from . import field_data


class Runtime(xblock.runtime.Runtime):
    """
    TODO many unimplemented methods in here
    """

    def __init__(self, user_id):
        super(Runtime, self).__init__(
            IdReader(),
            services={
                'field-data': field_data.FieldData()
            }
        )
        self.user_id = user_id

    def resource_url(self, resource):
        return static("courseware/" + resource)

    def handle(self, block, handler_name, request, suffix=''):
        # Convert Django request to webob
        request = django_to_webob_request(request)
        return super(Runtime, self).handle(block, handler_name, request, suffix=suffix)
    # TODO implement missing methods
    # pylint: disable=too-many-arguments
    def handler_url(self, block, handler_name, suffix='', query='', thirdparty=False):
        raise NotImplementedError
    def local_resource_url(self, block, uri):
        raise NotImplementedError
    def query(self, block):
        raise NotImplementedError
    def publish(self, block, event_type, event_data):
        raise NotImplementedError

    def _wrap_ele(self, block, view, frag, extra_data=None):
        """
        Add javascript to the wrapped element

        We need to override this _wrap_ele method in order to load the
        javascript runtime. This code is heavily inspired by the workbench's
        _wrap_ele method.
        """
        wrapped = super(Runtime, self)._wrap_ele(block, view, frag, extra_data)
        wrapped.add_resource_url(
            self.resource_url('js/vendor/jquery-3.0.0.min.js'),
            'application/javascript',
            placement='head',
        )
        wrapped.add_javascript_url(self.resource_url("js/vendor/jquery.cookie.js"))

        if frag.js_init_fn:
            wrapped.add_javascript_url(self.resource_url("js/runtime/%s.js" % frag.js_init_version))

        return wrapped


class WebobRequest(object):

    def __init__(self, request):
        """
        Args:
            request: Flask request object
        """
        self.body = request.data
        self.method = request.method


class IdReader(xblock.runtime.IdReader):
    USAGE_ID_REGEXP = r'(?P<definition_id>.+)\/(?P<block_id>.+)'

    def get_definition_id(self, usage_id):
        match = re.match(self.USAGE_ID_REGEXP, usage_id)
        if match is None:
            raise ValueError
        return match.groupdict()['definition_id']

    def get_block_type(self, def_id):
        # TODO for now, the definition id is also the block_type
        return def_id

    # TODO implement missing methods
    def get_aside_type_from_usage(self, aside_id):
        raise NotImplementedError
    def get_aside_type_from_definition(self, aside_id):
        raise NotImplementedError
    def get_definition_id_from_aside(self, aside_id):
        raise NotImplementedError
    def get_usage_id_from_aside(self, aside_id):
        raise NotImplementedError

