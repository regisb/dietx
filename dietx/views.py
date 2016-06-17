#! /usr/bin/env python
from flask import Flask, request, render_template
import werkzeug.routing

from .runtime import Runtime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# TODO ugly routing
@app.route('/block/<path:usage_id>/<handler_slug>', methods=['GET', 'POST'])
@app.route('/block/<path:usage_id>/<handler_slug>/', methods=['GET', 'POST'])
def block_action_handler(usage_id, handler_slug):
    """Handle calls made to xblock handler urls"""
    runtime = get_runtime()
    block = runtime.get_block(usage_id)

    # TODO catch NoSuchHandler
    # TODO we don't capture the suffix in the route...
    result = runtime.handle(block, handler_slug, request)
    return "pouac?"

@app.route("/course/<path:usage_id>")
def block_student_view(usage_id):
    runtime = get_runtime()

    # TODO raise a 404 on ValueError
    # TODO raise a 404 on PluginMissingError (xblock class does not exist)
    block = runtime.get_block(usage_id)

    render_context = {}
    fragment = block.render("student_view", render_context)
    return render_template(
        "student_view.html",
        user_id=runtime.user_id,

        body_html=fragment.body_html(),
        head_html=fragment.head_html(),
        foot_html=fragment.foot_html(),

        js_init_fn=fragment.js_init_fn,
        json_init_args=fragment.json_init_args,
    )

def get_runtime():
    user_id = get_user_id(request)
    return Runtime(user_id)

def get_user_id(req):
    # TODO
    return "1234"

def run():
    app.run()
