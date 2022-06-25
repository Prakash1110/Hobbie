from .forms import LoginFormAjax


def login_processor(request):
    return {'login_form': LoginFormAjax}
