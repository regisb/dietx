#! /usr/bin/env python
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from .runtime import Runtime


def hello(request):
    return HttpResponse("Hello World!")

def block_handler(request, usage_id, handler_slug):
    """Handle calls made to xblock handler urls"""
    runtime = get_runtime(request)
    block = runtime.get_block(usage_id)

    # TODO catch NoSuchHandler
    # TODO we don't capture the suffix in the route...
    result = runtime.handle(block, handler_slug, request)
    return HttpResponse("pouac?")

@ensure_csrf_cookie
def course_student_view(request, usage_id):
    runtime = get_runtime(request)

    # TODO raise a 404 on ValueError
    # TODO raise a 404 on PluginMissingError (xblock class does not exist)
    block = runtime.get_block(usage_id)

    render_context = {}
    fragment = block.render("student_view", render_context)
    return render_to_response("student_view.html", context={
        'user_id': runtime.user_id,
        'body_html': fragment.body_html(),
        'head_html': fragment.head_html(),
        'foot_html': fragment.foot_html(),
        'js_init_fn': fragment.js_init_fn,
        'json_init_args': fragment.json_init_args,
    })

def get_runtime(request):
    user_id = get_user_id(request)
    return Runtime(user_id)

def get_user_id(req):
    # TODO
    return "1234"
