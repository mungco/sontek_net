from pyramid.response       import FileResponse
from pkg_resources          import resource_filename
from pyramid.view           import view_config
from pyramid.httpexceptions import HTTPMovedPermanently

from sontek.models          import Entry

import os
import json

here = os.path.dirname(__file__)

@view_config(
    route_name='index'
    , renderer='sontek:templates/index.mako'
)
def index(request):
    query = Entry.get_all_active(request)[:10]

    return {
        'entries': query
    }

@view_config(
    route_name='about'
    , renderer='sontek:templates/about.mako'
)
def about(request):
    return {}

@view_config(
    route_name='resume'
    , renderer='sontek:templates/resume.mako'
)
@view_config(
    route_name='resume.html'
    , renderer='sontek:templates/resume_empty.mako'
)
def resume(request):
    with open(os.path.join(here, '../static/resume.json')) as f:
        content = f.read()
        data = json.loads(content)
        dev = data['developer']
        contact = data['contact']
        preamble = data['preamble']
        catalog = data['catalog']
        experience = data['experiences']

    return dict(
        dev=dev
        , contact=contact
        , preamble=preamble
        , catalog=catalog
        , experience=experience
    )


@view_config(
    route_name='projects'
    , renderer='sontek:templates/projects.mako'
)
def projects(request):
    with open(os.path.join(here, '../static/projects.json')) as f:
        content = f.read()
        data = json.loads(content)

    return {
        'projects': data
    }

@view_config(
    route_name='bad_link_gevent'
)
def bad_link_gevent(request):
    return HTTPMovedPermanently(
        location = request.route_url(
            'hiero_entry_detail'
            , slug='pycon-sprints-part-1-the-realtime-web-with-gevent-socket-io-redis-and-django'
        )
    )

@view_config(
    route_name='old_detail'
)
def old_detail(request):
    slug = request.matchdict.get('slug')

    return HTTPMovedPermanently(
        location = request.route_url(
            'hiero_entry_detail'
            , slug=slug
        )
    )

def favicon_view(request):
    fname = resource_filename(__name__, '../static/favicon.ico')
    return FileResponse(fname, request=request)
