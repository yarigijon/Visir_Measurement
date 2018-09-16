'''
Copyright (C) 2018  Pablo Baizan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from bottle import BottleException, RouteError, tob, touni, update_wrapper, depr, makelist, DictProperty, cached_property,\
lazy_attribute, RouteReset, RouterUnknownModeError, RouteSyntaxError, RouteBuildError, _re_flatten, Router, Route, Bottle,\
BaseRequest, _hkey, _hval, HeaderProperty, BaseResponse, _local_property, LocalRequest, LocalResponse, HTTPResponse, HTTPError,\
PluginError, JSONPlugin, TemplatePlugin, _ImportRedirect, MultiDict, FormsDict, HeaderDict, WSGIHeaderDict, ConfigDict, AppStack,\
WSGIFileWrapper, _closeiter, ResourceManager, FileUpload, abort, redirect, _file_iter_range, static_file, debug, http_date,\
parse_date, parse_auth, parse_range_header, _hsplit, _parse_http_header, _parse_qsl, _lscmp, cookie_encode, cookie_decode,cookie_is_encoded,\
html_escape, html_quote, yieldroutes, path_shift, auth_basic, make_default_app_wrapper, route, get, post, put, delete, patch,\
error, mount, hook, install, uninstall, url, ServerAdapter, CGIServer, FlupFCGIServer, WSGIRefServer, CherryPyServer, CherootServer,\
WaitressServer, PasteServer, MeinheldServer, FapwsServer, TornadoServer, AppEngineServer, TwistedServer, DieselServer, GeventServer,\
GunicornServer, EventletServer, RocketServer, BjoernServer, AsyncioServerAdapter, AiohttpServer, AiohttpUVLoopServer, AutoServer,\
server_names, load, load_app, _debug, run, FileCheckerThread, TemplateError, BaseTemplate, MakoTemplate, CheetahTemplate, Jinja2Template,\
SimpleTemplate, StplSyntaxError, StplParser, template, mako_template, cheetah_template, jinja2_template, view, mako_view, cheetah_view,\
jinja2_view, TEMPLATE_PATH, TEMPLATES, DEBUG, NORUN, HTTP_CODES, HTTP_CODES, HTTP_CODES, HTTP_CODES, HTTP_CODES, HTTP_CODES, HTTP_CODES,\
_HTTP_STATUS_LINES, ERROR_PAGE_TEMPLATE, request, response, local, apps, app, default_app, ext