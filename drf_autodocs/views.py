from django.views.generic.base import TemplateView
from .parser import TreeAPIParser


class TreeView(TemplateView):
    template_name = "drf_autodocs/index.html"

    def get_context_data(self, **kwargs):
        print("Getting the context")
        context = super().get_context_data(**kwargs)

        context["endpoints_tree"] = TreeAPIParser().endpoints_tree.to_dict()
        # print(context["endpoints_tree"])
        return context
