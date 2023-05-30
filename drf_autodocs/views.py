from django.views.generic.base import TemplateView
from .parser import TreeAPIParser
from django.conf import settings


class TreeView(TemplateView):
    template_name = "drf_autodocs/index.html"

    def get_context_data(self, **kwargs):
        print("Getting the context")
        context = super().get_context_data(**kwargs)
        context["title"] = getattr(settings, "DOCS_TITLE", "DOCS")
        context["logo"] = getattr(settings, "DOCS_LOGO", "https://avatars.githubusercontent.com/u/24269907?s=200&v=4")
        context["sub_title"] = getattr(settings, "DOCS_SUB_TITLE", "REST API")
        context["endpoints_tree"] = TreeAPIParser().endpoints_tree.to_dict()
        # print(context["endpoints_tree"])
        return context
