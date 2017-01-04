# -*- coding: utf-8 -*-

"""Found at: https://gist.github.com/thedod/eafad9458190755ce943e7aa58355934 (27.05.16). 
Makes it possible to align items to the right side of the navar while still using a renderer """

from flask_nav import Nav
from dominate import tags
import flask_nav
from flask_nav.elements import View,  NavigationItem, Subgroup
import flask_bootstrap.nav


class ExtendedNavbar(NavigationItem):
    def __init__(self, title, root_class='navbar navbar-default', items=(), right_items=()):
        self.title = title
        self.root_class = root_class
        self.items = items
        self.right_items = right_items

    
class CustomBootstrapRenderer(flask_bootstrap.nav.BootstrapRenderer):

    def visit_ExtendedNavbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
        node_id = self.id or flask_bootstrap.nav.sha1(str(id(node)).encode()).hexdigest()

        root = tags.nav() if self.html5 else tags.div(role='navigation')
        root['class'] = node.root_class

        cont = root.add(tags.div(_class='container-fluid'))

        # collapse button
        header = cont.add(tags.div(_class='navbar-header'))
        btn = header.add(tags.button())
        btn['type'] = 'button'
        btn['class'] = 'navbar-toggle collapsed'
        btn['data-toggle'] = 'collapse'
        btn['data-target'] = '#' + node_id
        btn['aria-expanded'] = 'false'
        btn['aria-controls'] = 'navbar'

        btn.add(tags.span('Toggle navigation', _class='sr-only'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))

        # title may also have a 'get_url()' method, in which case we render
        # a brand-link
        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                header.add(tags.a(node.title.text, _class='navbar-brand',
                                  href=node.title.get_url()))
            else:
                header.add(tags.span(node.title, _class='navbar-brand'))

        bar = cont.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))
        bar_list = bar.add(tags.ul(_class='nav navbar-nav'))
        for item in node.items:
            bar_list.add(self.visit(item))

        if node.right_items:
            right_bar_list = bar.add(tags.ul(_class='nav navbar-nav navbar-right'))
            for item in node.right_items:
                right_bar_list.add(self.visit(item))

        return root
        
    def visit_Temp_Label(self, node):
            return tags.span(node.text, _class='navbar-brand', _id=node.id)


class Temp_Label(NavigationItem):
    """Label text.

    Not a ``<label>`` text, but a text label nonetheless. Precise
    representation is up to the renderer, but most likely something like
    ``<span>``, ``<div>`` or similar.
    """
    def __init__(self, text, id):
        self.text = text
        self.id = id


nav = Nav()


def dynamic_navbar():

    r_items = ()
    l_items = (
            View('Personal information', 'view_personal_information'),
            View('Education and work', 'view_education_work'),
            View('Skills', 'view_it_language'),
            View('Publications', 'view_publications'),
            View('References', 'view_references'),
            Subgroup('Other information',
                View('Further information', 'view_further_information'),
                View('Download CV', 'download_cv'),
                View('Imprint', 'view_imprint'),
            )
        )

    navbar = ExtendedNavbar(title='CV Jannik Schwab',
                            root_class='navbar navbar-inverse navbar-fixed-top',
                            items=l_items,
                            right_items=r_items, )
    return navbar


def init_app(app):
    nav.init_app(app)

    # For some reason, this didn't seem to do anything...
    app.extensions['nav_renderers']['bootstrap'] = (__name__, 'CustomBootstrapRenderer')
    # ... but this worked. Weird.
    app.extensions['nav_renderers'][None] = (__name__, 'CustomBootstrapRenderer')

    flask_nav.register_renderer(app, 'CustomBootstrapRenderer', CustomBootstrapRenderer)

    # register navbar to app
    nav.register_element('top', dynamic_navbar)
