from django.contrib.auth.mixins import UserPassesTestMixin

class RoleRequiredMixin(UserPassesTestMixin):
    required_role = None

    def test_func(self):
        return self.request.user.groups.filter(name=self.required_role).exists()

    def handle_no_permission(self):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
